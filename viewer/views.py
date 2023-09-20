import io
from io import BytesIO
from pathlib import Path

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.conf import settings
from openslide import open_slide

from viewer.utils import SlideCache, get_thumbnail

from django.views.decorators.cache import cache_page
from viewer.models import Image, IndexingStatus
from viewer.tasks import index_images
from django.http import FileResponse

# Cache setup
config_map = {
    'DEEPZOOM_TILE_SIZE': 'tile_size',
    'DEEPZOOM_OVERLAP': 'overlap',
    'DEEPZOOM_LIMIT_BOUNDS': 'limit_bounds',
}
opts = {v: getattr(settings, k) for k, v in config_map.items()}
cache = SlideCache(
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
        properties = open_slide(slide_path).properties
        return slide, properties
    except Exception as e:
        raise Http404(str(e))

def list_view(request):
    # get all the slides from models
    files = Image.objects.all()
    return render(request, 'list_view.html', {'files': files, 'MEDIA_URL': settings.MEDIA_URL,
                                            'finished_indexing': IndexingStatus.objects.get(id=1).finished})

def tile_view(request):
    # get all the slides from models
    files = Image.objects.all()
    return render(request, 'tile_view.html', {'files': files, 'MEDIA_URL': settings.MEDIA_URL,
                                            'finished_indexing': IndexingStatus.objects.get(id=1).finished})

def trigger_indexing(request):
    task = index_images.delay()
    return JsonResponse({"task_id": str(task.id)})


def check_indexing_status(request):
    try:
        status = IndexingStatus.objects.get(id=1).finished
    except ObjectDoesNotExist:
        status = False

    if status:
        # Optionally clear the cache of the main page here, if necessary
        # cache.clear()
        pass

    return JsonResponse({"finished": status})


@cache_page(60)
def slide(request, path):
    slide_obj, properties = get_slide(path)
    # Assuming you have a URL pattern named 'dzi' for the next view
    slide_url = reverse('dzi', args=[path])
    # get the requested image object
    current_image = Image.objects.get(path=path)
    current_name = current_image.name
    prev_image = Image.objects.filter(name__lt=current_name).order_by('-name').first() or current_image
    next_image = Image.objects.filter(name__gt=current_name).order_by('name').first() or current_image

    context = {
        'slide_url': slide_url,
        'slide_filename': slide_obj.filename,
        'slide_mpp': slide_obj.mpp,
        'available_files': Image.objects.all(),
        'previous_slide': prev_image.path,
        'next_slide': next_image.path,
        'properties': properties,
    }
    return render(request, 'view.html', context)


def dzi(request, path):
    slide_obj, _ = get_slide(path)
    format_ = settings.DEEPZOOM_FORMAT
    dzi_content = slide_obj.get_dzi(format_)
    return HttpResponse(dzi_content, content_type='application/xml')


def tile(request, path, level, col, row, format_):
    slide_obj, _ = get_slide(path)
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


def generate_thumbnail(request, image_path):
    # Gnerate the thumbnail on-the-fly
    # Create an in-memory binary stream
    thumbnail = get_thumbnail(image_path)
    thumb_io = io.BytesIO()

    # Save the PIL Image to the binary stream in PNG format
    thumbnail.save(thumb_io, format="PNG")

    # Move the cursor of the binary stream back to the start
    thumb_io.seek(0)

    # Return the binary stream as a response
    return FileResponse(thumb_io, content_type="image/png")
