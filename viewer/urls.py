from django.urls import path
from viewer import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('<path:path>/', views.slide, name='slide'),
    path('<path:path>.dzi', views.dzi, name='dzi'),
    path('<path:path>_files/<int:level>/<int:col>_<int:row>.<format_>', views.tile, name='tile'),
]

# This serves media files in development mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)