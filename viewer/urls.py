from django.urls import path
from viewer import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', views.upload_and_view, name='upload_and_view'),
    path('', views.list_files, name='list_files'),
    path('view/<int:file_id>/', views.view_file, name='view_file'),
]

# This serves media files in development mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)