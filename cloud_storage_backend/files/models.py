import uuid
from django.db import models
from django.conf import settings

def upload_to(instance, filename):
    return f"{instance.owner.storage_path}/{uuid.uuid4()}"

class File(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    original_name = models.CharField(max_length=255)
    file = models.FileField(upload_to=upload_to)

    size = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_download = models.DateTimeField(null=True, blank=True)

    comment = models.TextField(blank=True)

    public_token = models.UUIDField(default=uuid.uuid4, unique=True)