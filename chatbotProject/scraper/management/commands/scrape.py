from django.core.management.base import BaseCommand
from scraper.scraperAll import scrape_all


class Command(BaseCommand):
    help = 'Scrapes the website and saves the data to the database'
    
    def handle(self, *args, **kwargs):
        full_scraping = self.ask_for_full_scraping()
        
        scrape_all(full_scraping)
        
        self.stdout.write(self.style.SUCCESS('Successfully scraped the website'))
    
    def ask_for_full_scraping(self):
        while True:
            response = input('Realizar scrap completo (Esto eliminará las entradas inactivas o que ya no se encuentren, si no se hace scrap completo se mantendrán estos datos) (Y/N): ')
            if response.lower() in ['y', 'n']:
                return response.lower() == 'y'
            else:
                print("Por favor ingresa 'Y' o 'N'.")
