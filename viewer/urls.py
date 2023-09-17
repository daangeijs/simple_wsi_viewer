from django.urls import path
from viewer import views
from django.conf import settings
from django.conf.urls.static import static

from viewer.views import generate_thumbnail

# pages urls
urlpatterns = [
    path('', views.list_view, name='list_view'),
    path('catalog/list', views.list_view, name='list_view'),
    path('catalog/tile', views.tile_view, name='tile_view'),
    path('trigger_indexing/', views.trigger_indexing, name='trigger_indexing'),
    path('check_indexing_status/', views.check_indexing_status, name='check_indexing_status'),
    path('generate_thumbnail/<path>/', generate_thumbnail, name='thumbnail')

]

# slide viewer endpoints
urlpatterns += [
    path('<path:path>/', views.slide, name='slide'),
    path('<path:path>.dzi', views.dzi, name='dzi'),
    path('<path:path>_files/<int:level>/<int:col>_<int:row>.<format_>', views.tile, name='tile'),
]

# This serves media files in development mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
