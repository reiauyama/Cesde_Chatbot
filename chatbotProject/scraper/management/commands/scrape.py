from django.core.management.base import BaseCommand
from scraper.scraper import scrape_website
from scraper.scraperWho import scrape_who_we_are
from scraper.scraperProgramasSedes import scrape_sedes

class Command(BaseCommand):
    help = 'Scrapes the website and saves the data to the database'

    def handle(self, *args, **kwargs):
        scrape_website()
        scrape_who_we_are()
        scrape_sedes()
        self.stdout.write(self.style.SUCCESS('Successfully scraped the website'))
