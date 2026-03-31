from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import File
from django.http import FileResponse
from django.urls import reverse
from users.models import User


def is_admin(user):
    return user.is_authenticated and (user.is_admin or user.is_superuser)

def has_access(user, file):
    return file.owner == user or is_admin(user)

@api_view(['POST'])
def upload_file(request):
    file_obj = request.FILES['file']

    file = File.objects.create(
        owner=request.user,
        original_name=file_obj.name,
        file=file_obj,
        size=file_obj.size
    )

    return Response({"id": file.id})

@api_view(['GET'])
def list_files(request):
    user_id = request.GET.get('user_id')

    # Обычный пользователь
    if not is_admin(request.user):
        files = File.objects.filter(owner=request.user)

    # Админ
    else:
        if user_id:
            try:
                target_user = User.objects.get(id=user_id)
                files = File.objects.filter(owner=target_user)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
        else:
            # если не передан user_id — вернуть ВСЕ файлы
            files = File.objects.all()

    return Response([
        {
            "id": f.id,
            "name": f.original_name,
            "size": f.size,
            "owner": f.owner.username,
            "comment": f.comment
        } for f in files
    ])

@api_view(['DELETE'])
def delete_file(request, file_id):
    try:
        file = File.objects.get(id=file_id)

        if not has_access(request.user, file):
            return Response({"error": "Forbidden"}, status=403)

        file.delete()
        return Response({"message": "Deleted"})

    except File.DoesNotExist:
        return Response({"error": "File not found"}, status=404)

@api_view(['PATCH'])
def rename_file(request, file_id):
    try:
        file = File.objects.get(id=file_id)

        if not has_access(request.user, file):
            return Response({"error": "Forbidden"}, status=403)

        file.original_name = request.data.get('name', file.original_name)
        file.save()

        return Response({"message": "Renamed"})

    except File.DoesNotExist:
        return Response({"error": "File not found"}, status=404)

@api_view(['PATCH'])
def update_comment(request, file_id):
    try:
        file = File.objects.get(id=file_id)

        if not has_access(request.user, file):
            return Response({"error": "Forbidden"}, status=403)

        file.comment = request.data.get('comment', '')
        file.save()

        return Response({"message": "Updated"})

    except File.DoesNotExist:
        return Response({"error": "File not found"}, status=404)

@api_view(['GET'])
def download_file(request, file_id):
    try:
        file = File.objects.get(id=file_id)

        if not has_access(request.user, file):
            return Response({"error": "Forbidden"}, status=403)

        return FileResponse(
            file.file.open(),
            as_attachment=True,
            filename=file.original_name
        )

    except File.DoesNotExist:
        return Response({"error": "File not found"}, status=404)

@api_view(['GET'])
def get_public_link(request, file_id):
    try:
        file = File.objects.get(id=file_id)

        if not has_access(request.user, file):
            return Response({"error": "Forbidden"}, status=403)

        link = request.build_absolute_uri(f"/public/{file.public_token}")
        return Response({"link": link})

    except File.DoesNotExist:
        return Response({"error": "File not found"}, status=404)

def public_download(request, token):
    file = File.objects.get(public_token=token)
    return FileResponse(file.file.open(), as_attachment=True, filename=file.original_name)