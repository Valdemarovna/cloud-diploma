from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import File
import os
import uuid
from django.conf import settings
from django.http import FileResponse
from django.utils.timezone import now

def has_access(user, file):
    return user.is_superuser or file.owner == user

class FileListView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Не авторизован"}, status=401)

        files = File.objects.filter(owner=request.user)

        data = []
        for f in files:
            data.append({
                "id": f.id,
                "name": f.original_name,
                "size": f.size,
                "upload_date": f.upload_date,
                "last_download": f.last_download,
                "comment": f.comment,
            })

        return Response(data)

class UploadFileView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Не авторизован"}, status=401)

        file = request.FILES.get('file')
        comment = request.data.get('comment', '')

        if not file:
            return Response({"error": "Файл не передан"}, status=400)

        # генерируем уникальное имя
        unique_name = str(uuid.uuid4())

        user_folder = os.path.join(
            settings.FILE_STORAGE_ROOT,
            request.user.storage_path
        )

        os.makedirs(user_folder, exist_ok=True)

        file_path = os.path.join(user_folder, unique_name)

        # сохраняем файл
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # сохраняем в БД
        db_file = File.objects.create(
            owner=request.user,
            original_name=file.name,
            size=file.size,
            comment=comment,
            path=file_path
        )

        return Response({"message": "Файл загружен"})
    
class DeleteFileView(APIView):
    def delete(self, request, file_id):
        try:
            file = File.objects.get(id=file_id)
        except File.DoesNotExist:
            return Response({"error": "Файл не найден"}, status=404)

        if not has_access(request.user, file):
            return Response({"error": "Нет доступа"}, status=403)

        if os.path.exists(file.path):
            os.remove(file.path)

        file.delete()

        return Response({"message": "Файл удалён"})
    
class RenameFileView(APIView):
    def patch(self, request, file_id):
        new_name = request.data.get("name")

        file = File.objects.get(id=file_id)

        if not has_access(request.user, file):
            return Response({"error": "Нет доступа"}, status=403)

        file.original_name = new_name
        file.save()

        return Response({"message": "Имя обновлено"})
    
class UpdateCommentView(APIView):
    def patch(self, request, file_id):
        comment = request.data.get("comment", "")

        file = File.objects.get(id=file_id)

        if not has_access(request.user, file):
            return Response({"error": "Нет доступа"}, status=403)

        file.comment = comment
        file.save()

        return Response({"message": "Комментарий обновлён"})
    
class DownloadFileView(APIView):
    def get(self, request, file_id):
        file = File.objects.get(id=file_id)

        if not has_access(request.user, file):
            return Response({"error": "Нет доступа"}, status=403)

        file.last_download = now()
        file.save()

        response = FileResponse(open(file.path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{file.original_name}"'

        return response
    
class PublicLinkView(APIView):
    def get(self, request, file_id):
        file = File.objects.get(id=file_id)

        if not has_access(request.user, file):
            return Response({"error": "Нет доступа"}, status=403)

        return Response({
            "link": f"/api/files/public/{file.public_token}/"
        })
    
class PublicLinkView(APIView):
    def get(self, request, file_id):
        file = File.objects.get(id=file_id)

        if not has_access(request.user, file):
            return Response({"error": "Нет доступа"}, status=403)

        return Response({
            "link": f"/api/files/public/{file.public_token}/"
        })
    
class PublicDownloadView(APIView):
    def get(self, request, token):
        try:
            file = File.objects.get(public_token=token)
        except File.DoesNotExist:
            return Response({"error": "Файл не найден"}, status=404)

        response = FileResponse(open(file.path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{file.original_name}"'

        return response