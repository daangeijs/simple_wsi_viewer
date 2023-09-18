from django.core.management.base import BaseCommand
from pathlib import Path

from openslide import OpenSlide

from viewer.models import Image


class Command(BaseCommand):
    help = 'Index images in the directory'

    def add_arguments(self, parser):
        parser.add_argument('dir', type=str, help='Directory containing the images')

    def handle(self, *args, **kwargs):
        dir_path = Path(kwargs['dir'])
        for path in dir_path.glob('*'):  # recursively search through directories
            if OpenSlide.detect_format(path):
                Image.objects.get_or_create(name=path.name, path=str(path))
        self.stdout.write(self.style.SUCCESS('Successfully indexed images'))
