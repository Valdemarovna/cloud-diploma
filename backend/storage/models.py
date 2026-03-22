import uuid
from django.db import models
from django.conf import settings


class File(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='files'
    )

    original_name = models.CharField(max_length=255)
    size = models.BigIntegerField()

    upload_date = models.DateTimeField(auto_now_add=True)
    last_download = models.DateTimeField(null=True, blank=True)

    comment = models.TextField(blank=True)

    path = models.CharField(max_length=500)

    public_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    def __str__(self):
        return self.original_name
        