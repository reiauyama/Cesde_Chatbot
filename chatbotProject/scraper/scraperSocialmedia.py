import requests
from bs4 import BeautifulSoup
from .models import Menu, SubMenu
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def scrapersocial_networks():
    url = "https://www.cesde.edu.co/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Buscar el contenedor de Redes Sociales
    social_container = soup.find('div', {'area-label': 'network'})
    if not social_container:
        logger.warning("No se encontró el contenedor de redes sociales")
        return

    social_heading = social_container.find('h2', text="Redes sociales")
    if not social_heading:
        logger.warning("No se encontró el título 'Redes sociales'")
        return

    # Crear o actualizar la entrada del menú principal para Redes Sociales
    menu_entry, created = Menu.objects.update_or_create(
        title="Redes sociales",
        defaults={'link': '', 'active': True}
    )

    # Encontrar y procesar los enlaces de redes sociales
    social_links = social_container.find_all('a', class_='social-element')
    for link in social_links:
        title = link.get('title', '').replace('ir a ', '')
        url = link.get('href', '')

        # Asegurarse de que tanto el título como el enlace estén presentes
        if title and url:
            logger.info(f"Encontrada red social: {title} - {url}")
            # Crear o actualizar la entrada del submenú para cada red social
            SubMenu.objects.update_or_create(
                menu=menu_entry,
                title=title,
                defaults={'link': url, 'active': True}
            )
        else:
            logger.warning(f"Faltan datos para red social: title={title}, url={url}")