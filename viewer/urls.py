from django.urls import path
from viewer import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', views.upload_and_view, name='upload_and_view'),
    path('view/<int:tif_id>/', views.view_dzi, name='view_dzi'),
]

# This serves media files in development mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)