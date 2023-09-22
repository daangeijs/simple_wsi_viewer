from celery import shared_task
from pathlib import Path

from openslide import OpenSlide

from viewer.models import Image, IndexingStatus
from viewer.utils import save_thumbnail


def set_status(status):
    status_obj, _ = IndexingStatus.objects.get_or_create(id=1)
    status_obj.finished = status
    status_obj.save()


@shared_task
def index_images():
    set_status(False)
    # Check for existing images in DB
    for image in Image.objects.all():
        if not Path(image.path).exists():
            image.delete()
            # delete thumbnail if exists
            if image.thumbnail:
                Path(image.thumbnail).unlink()
        elif not image.thumbnail:
            # Async task to generate and save the thumbnail
            generate_thumbnail_for_image.delay(image.id)

    # Glob the /data dir and add new items
    image_paths = Path("/slides").glob("*A15.tif")
    for image_path in image_paths:
        if OpenSlide.detect_format(image_path):
            image_obj, created = Image.objects.get_or_create(name=image_path.name, path=str(image_path))

            if created:
                # Async task to generate and save the thumbnail
                generate_thumbnail_for_image.delay(image_obj.id)

    set_status(True)
    return "Indexing completed"


@shared_task
def generate_thumbnail_for_image(image_id):
    image = Image.objects.get(pk=image_id)
    thumbnail_path = save_thumbnail(Path(image.path))
    image.thumbnail = str(thumbnail_path)
    image.save()
