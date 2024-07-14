import requests
from bs4 import BeautifulSoup
from .models import Menu, SubMenu
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def update_or_create_menu_entry(title, link, model, **kwargs):
    if link is not None:
        model.objects.update_or_create(
            title=title,
            defaults={**kwargs, 'link': link, 'active': True}
        )

def scrape_navigation(menu_id, ul_class):
    url = "https://www.cesde.edu.co/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    menu = soup.find('nav', id=menu_id)
    ul_principal = menu.find('ul', class_=ul_class)
    menu_items = ul_principal.find_all('li', recursive=False)

    for item in menu_items:
        link = item.find('a')
        title = link.get_text(strip=True) if link else None
        href = link['href'] if link and 'href' in link.attrs else None

        menu_entry, created = Menu.objects.update_or_create(
            title=title,
            defaults={'link': href, 'active': True}
        )

        submenu_ul = item.find('ul')
        if submenu_ul:
            submenu_items = submenu_ul.find_all('li', recursive=False)
            for subitem in submenu_items:
                sublink = subitem.find('a')
                subtitle = sublink.get_text(strip=True) if sublink else None
                subhref = sublink['href'] if sublink and 'href' in sublink.attrs else None

                submenu_entry, created = SubMenu.objects.update_or_create(
                    menu=menu_entry,
                    title=subtitle,
                    defaults={'link': subhref, 'active': True}
                )

                

def scrape_social_networks(soup):
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

def scrape_website():
    # Desactivar todas las entradas existentes antes de actualizar
    Menu.objects.all().update(active=False)
    SubMenu.objects.all().update(active=False)
    

    url = "https://www.cesde.edu.co/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Scraping para ambos menús
    scrape_navigation('preheader-navigation', 'cesde-preheader-menu')
    scrape_navigation('desktop-navigation', 'cesde-menu')

    # Scraping para redes sociales
    scrape_social_networks(soup)

    # Eliminar las entradas que no se actualizaron (que ya no están activas)
    Menu.objects.filter(active=False).delete()
    SubMenu.objects.filter(active=False).delete()


