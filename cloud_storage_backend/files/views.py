from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import File
from django.http import FileResponse
from django.urls import reverse
from users.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
import logging
from rest_framework.pagination import PageNumberPagination
from django.db.models.functions import Coalesce

logger = logging.getLogger(__name__)

def is_admin(user):
    return user.is_authenticated and (user.is_admin or user.is_superuser)

def has_access(user, file):
    return file.owner == user or is_admin(user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    if 'file' not in request.FILES:
        logger.warning(f"User {request.user} tried upload without file")
        return Response({"error": "No file provided"}, status=400)
    file_obj = request.FILES['file']

    file = File.objects.create(
        owner=request.user,
        original_name=file_obj.name,
        file=file_obj,
        size=file_obj.size
    )

    logger.info(f"User {request.user} uploaded file {file_obj.name}")
    return Response({"id": file.id})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_files(request):
    user = request.user

    queryset = File.objects.all()

    if not user.is_admin:
        queryset = queryset.filter(owner=user)
    else:
        user_id = request.GET.get("user_id")
        if user_id:
            queryset = queryset.filter(owner_id=user_id)
        else:
            logger.error(f"User {request.user} not found")
            return Response({"error": "User not found"}, status=404)

    ordering = request.GET.get("ordering")
    if ordering:
        queryset = queryset.order_by(ordering)

    paginator = PageNumberPagination()
    paginator.page_size = 10

    page = paginator.paginate_queryset(queryset, request)

    data = []
    for f in page:
        data.append({
            "id": f.id,
            "name": f.original_name,
            "size": f.size,
            "owner": f.owner.username,
            "comment": f.comment,
            "uploaded_at": f.uploaded_at,
            "last_download": f.last_download,
        })

    return paginator.get_paginated_response(data)

@api_view(['DELETE'])
def delete_file(request, file_id):
    try:
        file = File.objects.get(id=file_id)

        if not has_access(request.user, file):
            logger.error(f"User {request.user} has not access to delete file {file.original_name}")
            return Response({"error": "Forbidden"}, status=403)

        file.delete()
        logger.info(f"User {request.user} deleted file {file.original_name}")
        return Response({"message": "Deleted"})

    except File.DoesNotExist:
        logger.error(f"File {file.original_name} not found")
        return Response({"error": "File not found"}, status=404)

@api_view(['PATCH'])
def rename_file(request, file_id):
    try:
        file = File.objects.get(id=file_id)

        if not has_access(request.user, file):
            logger.error(f"User {request.user} has not access to rename file {file.original_name}")
            return Response({"error": "Forbidden"}, status=403)

        file.original_name = request.data.get('name', file.original_name)
        file.save()

        logger.info(f"User {request.user} renamed file {file.original_name}")
        return Response({"message": "Renamed"})

    except File.DoesNotExist:
        logger.error(f"File {file.original_name} not found")
        return Response({"error": "File not found"}, status=404)

@api_view(['PATCH'])
def update_comment(request, file_id):
    try:
        file = File.objects.get(id=file_id)

        if not has_access(request.user, file):
            logger.error(f"User {request.user} has not access to update comment for file {file.original_name}")
            return Response({"error": "Forbidden"}, status=403)

        file.comment = request.data.get('comment', '')
        file.save()

        logger.info(f"User {request.user} update comment for file {file.original_name}")
        return Response({"message": "Updated"})

    except File.DoesNotExist:
        logger.error(f"File {file.original_name} not found")
        return Response({"error": "File not found"}, status=404)

@api_view(['GET'])
def download_file(request, file_id):
    try:
        file = File.objects.get(id=file_id)

        if not has_access(request.user, file):
            logger.error(f"User {request.user} has not access to download file {file.original_name}")
            return Response({"error": "Forbidden"}, status=403)

        return FileResponse(
            file.file.open(),
            as_attachment=True,
            filename=file.original_name
        )

    except File.DoesNotExist:
        logger.error(f"File {file.original_name} not found")
        return Response({"error": "File not found"}, status=404)

@api_view(['GET'])
def get_public_link(request, file_id):
    try:
        file = File.objects.get(id=file_id)

        if not has_access(request.user, file):
            logger.error(f"User {request.user} has not access to share file {file.original_name}")
            return Response({"error": "Forbidden"}, status=403)

        link = request.build_absolute_uri(f"/public/{file.public_token}")
        logger.info(f"User {request.user} got link for file {file.original_name}")
        return Response({"link": link})

    except File.DoesNotExist:
        logger.error(f"File {file.original_name} not found")
        return Response({"error": "File not found"}, status=404)

def public_download(request, token):
    file = File.objects.get(public_token=token)
    logger.info(f"file {file.original_name} was downloaded by public method")
    return FileResponse(file.file.open(), as_attachment=True, filename=file.original_name)