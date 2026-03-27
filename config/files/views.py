from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import File

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    file_obj = request.FILES['file']

    file = File.objects.create(
        owner=request.user,
        original_name=file_obj.name,
        file=file_obj,
        size=file_obj.size,
        comment=request.data.get('comment', '')
    )

    return Response({'id': str(file.id)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_files(request):
    files = File.objects.filter(owner=request.user)

    data = [
        {
            "id": str(f.id),
            "name": f.original_name,
            "size": f.size,
            "uploaded": f.uploaded_at
        }
        for f in files
    ]

    return Response(data)