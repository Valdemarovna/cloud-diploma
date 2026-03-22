from django.db import models
from django.contrib.auth.models import AbstractUser
import os
import re
from django.core.exceptions import ValidationError

def validate_username(value):
    if not re.match(r'^[A-Za-z][A-Za-z0-9]{3,19}$', value):
        raise ValidationError(
            "Логин: 4-20 символов, латиница и цифры, первый символ — буква"
        )

def user_storage_path(instance, filename):
    return os.path.join(instance.username, filename)


class User(AbstractUser):
    # убираем стандартные поля
    first_name = None
    last_name = None
    username = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_username]
    )   
    # наши поля
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    storage_path = models.CharField(
        max_length=255,
        blank=True
    )

    def save(self, *args, **kwargs):
        # автоматически задаём путь к хранилищу
        if not self.storage_path:
            self.storage_path = f"user_{self.username}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    