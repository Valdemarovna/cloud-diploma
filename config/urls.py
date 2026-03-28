"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as user_views
from files import views as file_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users
    path('api/register', user_views.register),
    path('api/login', user_views.login_view),
    path('api/logout', user_views.logout_view),
    path('api/users', user_views.users_list),
    path('api/users/<int:user_id>', user_views.delete_user),

    # Files
    path('api/files', file_views.list_files),
    path('api/files/upload', file_views.upload_file),
    path('api/files/<uuid:file_id>', file_views.delete_file),
    path('api/files/<uuid:file_id>/rename', file_views.rename_file),
    path('api/files/<uuid:file_id>/comment', file_views.update_comment),
    path('api/files/<uuid:file_id>/download', file_views.download_file),
    path('api/files/<uuid:file_id>/link', file_views.generate_link),
    path('api/files/public/<uuid:link_id>', file_views.public_download),
]