from django.core.management.base import BaseCommand
from scraper.scraper import scrape_website
from scraper.scraperSocialmedia import scrapersocial_networks
from scraper.scraperWho import scrape_who_we_are
from scraper.scraperProgramasSedes import scrape_medellin, scrape_bello, scrape_rionegro, scrape_pintada

class Command(BaseCommand):
    help = 'Scrapes the website and saves the data to the database'

    def handle(self, *args, **kwargs):
        scrape_website()
        scrapersocial_networks()
        scrape_who_we_are()
        scrape_medellin()
        scrape_bello()
        scrape_rionegro()
        scrape_pintada()
        self.stdout.write(self.style.SUCCESS('Successfully scraped the website'))
