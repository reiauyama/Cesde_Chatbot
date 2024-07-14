from django.core.management.base import BaseCommand
from scraper.scraper import scrape_website

from scraper.scraperProgramasSedes import scrape_sedes

class Command(BaseCommand):
    help = 'Scrapes the website and saves the data to the database'

    def handle(self, *args, **kwargs):
        scrape_website()
        
        scrape_sedes()
        self.stdout.write(self.style.SUCCESS('Successfully scraped the website'))
