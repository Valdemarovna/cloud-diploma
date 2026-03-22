from django.urls import path
from .views import *

urlpatterns = [
    path('', FileListView.as_view()),
    path('upload/', UploadFileView.as_view()),
    path('<int:file_id>/', DeleteFileView.as_view()),
    path('<int:file_id>/rename/', RenameFileView.as_view()),
    path('<int:file_id>/comment/', UpdateCommentView.as_view()),
    path('<int:file_id>/download/', DownloadFileView.as_view()),
    path('<int:file_id>/link/', PublicLinkView.as_view()),
    path('public/<uuid:token>/', PublicDownloadView.as_view()),
]