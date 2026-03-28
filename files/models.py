import uuid
from django.db import models
from django.conf import settings

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    original_name = models.CharField(max_length=255)
    stored_name = models.CharField(max_length=255)

    size = models.IntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)
    last_download = models.DateTimeField(null=True, blank=True)

    comment = models.TextField(blank=True)

    path = models.CharField(max_length=500)

    public_link = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.original_name