from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Clear the cache'
    def handle(self, *args, **kwargs):
        cache.clear()
        self.stdout.write(self.style.SUCCESS('Cache cleared!'))
