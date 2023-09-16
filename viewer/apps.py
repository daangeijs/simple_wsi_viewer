from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ViewerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'viewer'

    def ready(self):
        # Connect our signal handler
        post_migrate.connect(run_indexing, sender=self)


def run_indexing(sender, **kwargs):
    # Import the task here to avoid circular imports
    from viewer.tasks import index_images
    from viewer.models import IndexingStatus
    index_images.delay()