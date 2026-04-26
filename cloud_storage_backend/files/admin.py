from django.contrib import admin
from .models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("id", "original_name", "owner", "size", "uploaded_at")
    search_fields = ("original_name",)
    list_filter = ("owner",)