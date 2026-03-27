from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    storage_path = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.storage_path:
            self.storage_path = f"user_{self.username}"
        super().save(*args, **kwargs)
