from django.core.management.base import BaseCommand
from scraper.models import ScrapedData

class Command(BaseCommand):
    help = 'Deletes all scraped data from the database'

    def handle(self, *args, **kwargs):
        count, _ = ScrapedData.objects.all( ).delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} entries from the database'))
