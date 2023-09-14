from io import BytesIO
from pathlib import Path

from django.urls import reverse
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.conf import settings
from viewer.utils import _SlideCache, _Directory, _SlideFile  # Import your classes


# Cache setup
config_map = {
    'DEEPZOOM_TILE_SIZE': 'tile_size',
    'DEEPZOOM_OVERLAP': 'overlap',
    'DEEPZOOM_LIMIT_BOUNDS': 'limit_bounds',
}
opts = {v: getattr(settings, k) for k, v in config_map.items()}
cache = _SlideCache(
    settings.SLIDE_CACHE_SIZE,
    settings.SLIDE_TILE_CACHE_MB,
    opts,
    settings.DEEPZOOM_COLOR_MODE,
)

def get_slide(path):
    slide_dir = Path(settings.SLIDE_DIR)
    slide_path = (slide_dir / path).resolve()

    if not slide_path.exists():
        raise Http404("Slide does not exist.")

    try:
        slide = cache.get(str(slide_path))
        slide.filename = slide_path.name
        return slide
    except Exception as e:
        raise Http404(str(e))

def index(request):
    root_dir = _Directory(settings.SLIDE_DIR)
    return render(request, 'files.html', {'root_dir': root_dir})

def slide(request, path):
    slide_obj = get_slide(path)
    # Assuming you have a URL pattern named 'dzi' for the next view
    slide_url = reverse('dzi', args=[path])
    root_dir = _Directory(settings.SLIDE_DIR)
    context = {
        'slide_url': slide_url,
        'slide_filename': slide_obj.filename,
        'slide_mpp': slide_obj.mpp,
        'root_dir': root_dir
    }
    return render(request, 'view.html', context)


def dzi(request, path):
    slide_obj = get_slide(path)
    format_ = settings.DEEPZOOM_FORMAT
    dzi_content = slide_obj.get_dzi(format_)
    return HttpResponse(dzi_content, content_type='application/xml')

def tile(request, path, level, col, row, format_):
    slide_obj = get_slide(path)
    format_ = format_.lower()
    if format_ not in ['jpeg', 'png']:
        # Not supported by Deep Zoom
        raise Http404("Format not supported.")
    try:
        tile_obj = slide_obj.get_tile(level, (col, row))
    except ValueError:
        # Invalid level or coordinates
        raise Http404("Invalid level or coordinates.")
    slide_obj.transform(tile_obj)

    buf = BytesIO()
    tile_obj.save(
        buf,
        format_,
        quality=settings.DEEPZOOM_TILE_QUALITY,
        icc_profile=tile_obj.info.get('icc_profile')
    )

    response = HttpResponse(content=ContentFile(buf.getvalue()), content_type=f'image/{format_}')
    return response