from django.core.management.base import BaseCommand
from scraper.scraper import scrape_website

class Command(BaseCommand):
    help = 'Scrapes the website and saves the data to the database'

    def handle(self, *args, **kwargs):
        scrape_website()
        self.stdout.write(self.style.SUCCESS('Successfully scraped the website'))
