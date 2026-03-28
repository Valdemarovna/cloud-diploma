from django.shortcuts import render
import os
import uuid
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import File
from django.http import FileResponse
from django.utils import timezone

@api_view(['GET'])
def list_files(request):
    if not request.user.is_authenticated:
        return Response(status=401)

    user_id = request.GET.get('user_id')

    if request.user.is_superuser and user_id:
        files = File.objects.filter(owner_id=user_id)
    else:
        files = File.objects.filter(owner=request.user)

    data = [{
        'id': f.id,
        'name': f.original_name,
        'size': f.size,
        'upload_date': f.upload_date,
        'comment': f.comment
    } for f in files]

    return Response(data)

@api_view(['POST'])
def upload_file(request):
    if not request.user.is_authenticated:
        return Response(status=401)

    file = request.FILES.get('file')

    if not file:
        return Response({'error': 'No file'}, status=400)

    user_folder = os.path.join(settings.FILE_STORAGE_ROOT, request.user.storage_path)
    os.makedirs(user_folder, exist_ok=True)

    unique_name = str(uuid.uuid4())
    path = os.path.join(user_folder, unique_name)

    with open(path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)

    db_file = File.objects.create(
        owner=request.user,
        original_name=file.name,
        stored_name=unique_name,
        size=file.size,
        path=path
    )

    return Response({'id': db_file.id})

@api_view(['DELETE'])
def delete_file(request, file_id):
    if not request.user.is_authenticated:
        return Response(status=401)

    try:
        file = File.objects.get(id=file_id)
    except File.DoesNotExist:
        return Response(status=404)

    if file.owner != request.user and not request.user.is_superuser:
        return Response(status=403)

    if os.path.exists(file.path):
        os.remove(file.path)

    file.delete()

    return Response({'message': 'Deleted'})

@api_view(['PATCH'])
def rename_file(request, file_id):
    if not request.user.is_authenticated:
        return Response(status=401)

    new_name = request.data.get('name')

    try:
        file = File.objects.get(id=file_id)
    except File.DoesNotExist:
        return Response(status=404)

    if file.owner != request.user:
        return Response(status=403)

    file.original_name = new_name
    file.save()

    return Response({'message': 'Renamed'})

@api_view(['PATCH'])
def update_comment(request, file_id):
    if not request.user.is_authenticated:
        return Response(status=401)

    comment = request.data.get('comment')

    file = File.objects.get(id=file_id)

    if file.owner != request.user:
        return Response(status=403)

    file.comment = comment
    file.save()

    return Response({'message': 'Updated'})

@api_view(['GET'])
def download_file(request, file_id):
    if not request.user.is_authenticated:
        return Response(status=401)

    try:
        file = File.objects.get(id=file_id)
    except File.DoesNotExist:
        return Response(status=404)

    if file.owner != request.user and not request.user.is_superuser:
        return Response(status=403)

    file.last_download = timezone.now()
    file.save()

    response = FileResponse(open(file.path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file.original_name}"'

    return response

@api_view(['POST'])
def generate_link(request, file_id):
    if not request.user.is_authenticated:
        return Response(status=401)

    file = File.objects.get(id=file_id)

    if file.owner != request.user:
        return Response(status=403)

    return Response({
        'link': f"/api/files/public/{file.public_link}"
    })

@api_view(['GET'])
def public_download(request, link_id):
    try:
        file = File.objects.get(public_link=link_id)
    except File.DoesNotExist:
        return Response(status=404)

    response = FileResponse(open(file.path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file.original_name}"'

    return response