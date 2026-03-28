"""
URL configuration for cloud_storage_backend project.

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
from django.urls import path
from users import views as u
from files import views as f

urlpatterns = [
    path('register/', u.register),
    path('login/', u.login_view),
    path('logout/', u.logout_view),

    path('users/', u.users_list),
    path('users/<int:user_id>/', u.delete_user),
    path('users/<int:user_id>/make_admin/', u.make_admin),
    path('users/<int:user_id>/remove_admin/', u.remove_admin),

    path('files/', f.list_files),
    path('upload/', f.upload_file),
    path('files/<int:file_id>/', f.delete_file),
    path('files/<int:file_id>/rename/', f.rename_file),
    path('files/<int:file_id>/comment/', f.update_comment),
    path('files/<int:file_id>/delete/', f.delete_file),

    path('files/<int:file_id>/link/', f.get_public_link),
    path('download/<int:file_id>/', f.download_file),
    path('public/<uuid:token>/', f.public_download, name='public_download'),
]