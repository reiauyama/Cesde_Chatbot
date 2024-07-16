import requests
from bs4 import BeautifulSoup
from .models import Menu, SubMenu, SubSubMenu
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def update_or_create_entry(model, **kwargs):
    return model.objects.update_or_create(**kwargs)

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def scrape_navigation(menu_id, ul_class):
    url = "https://www.cesde.edu.co/"
    soup = get_soup(url)

    menu = soup.find('nav', id=menu_id)
    ul_principal = menu.find('ul', class_=ul_class)
    menu_items = ul_principal.find_all('li', recursive=False)

    for item in menu_items:
        link = item.find('a')
        title = link.get_text(strip=True) if link else None
        href = link['href'] if link and 'href' in link.attrs else None

        menu_entry, _ = update_or_create_entry(Menu, title=title, defaults={'link': href, 'active': True})

        submenu_ul = item.find('ul')
        if submenu_ul:
            for subitem in submenu_ul.find_all('li', recursive=False):
                sublink = subitem.find('a')
                subtitle = sublink.get_text(strip=True) if sublink else None
                subhref = sublink['href'] if sublink and 'href' in sublink.attrs else None

                update_or_create_entry(SubMenu, menu=menu_entry, title=subtitle, defaults={'link': subhref, 'active': True})

def scrape_social_networks(soup):
    social_container = soup.find('div', {'area-label': 'network'})
    if not social_container:
        logger.warning("No se encontró el contenedor de redes sociales")
        return

    social_heading = social_container.find('h2', text="Redes sociales")
    if not social_heading:
        logger.warning("No se encontró el título 'Redes sociales'")
        return

    menu_entry, _ = update_or_create_entry(Menu, title="Redes sociales", defaults={'link': '', 'active': True})

    for link in social_container.find_all('a', class_='social-element'):
        title = link.get('title', '').replace('ir a ', '')
        url = link.get('href', '')

        if title and url:
            logger.info(f"Encontrada red social: {title} - {url}")
            update_or_create_entry(SubMenu, menu=menu_entry, title=title, defaults={'link': url, 'active': True})
        else:
            logger.warning(f"Faltan datos para red social: title={title}, url={url}")

def scrape_who_we_are():
    url = "https://www.cesde.edu.co/nosotros/"
    soup = get_soup(url)

    main_container = soup.find('div', {'data-id': '78d319a'})
    if not main_container:
        logger.warning("No se encontró el contenedor principal de '¿Quiénes somos?'")
        return

    heading = main_container.find('h1', class_='elementor-heading-title')
    text_container = main_container.find('div', class_='elementor-widget-text-editor')

    if not heading or not text_container:
        logger.warning("No se encontró el título o contenido de '¿Quiénes somos?'")
        return

    title = heading.get_text(strip=True)
    content = text_container.get_text(strip=True)

    submenu_entry = SubMenu.objects.filter(title='¿Quiénes somos?').first()
    if not submenu_entry:
        logger.warning("No se encontró el SubMenu '¿Quiénes somos?'")
        return

    update_or_create_entry(SubSubMenu, submenu=submenu_entry, title=title, defaults={'link': url, 'content': content, 'active': True})

def scrape_academic_schedule():
    url = "https://www.cesde.edu.co/aspirantes/"
    soup = get_soup(url)

    schedule_container = soup.find('div', class_='elementor-accordion-item')
    if not schedule_container:
        logger.warning("No se encontró el contenedor del cronograma académico")
        return

    accordion_item = schedule_container.find('a', class_='elementor-accordion-title')
    if not accordion_item:
        logger.warning("No se encontró el elemento de acordeón del cronograma académico")
        return

    title = accordion_item.get_text(strip=True)
    content = str(accordion_item.find('div', class_='elementor-tab-content'))

    menu_entry = Menu.objects.filter(title='Aspirantes').first()
    if menu_entry:
        logger.info("Menu 'Aspirantes' encontrado")
    else:
        logger.warning("No se encontró el Menu 'Aspirantes'")
        return

    update_or_create_entry(SubMenu, menu=menu_entry, title=title, defaults={'link': url, 'active': True})

def scrape_website():
    Menu.objects.all().update(active=False)
    SubMenu.objects.all().update(active=False)
    

    url = "https://www.cesde.edu.co/"
    soup = get_soup(url)

    scrape_navigation('preheader-navigation', 'cesde-preheader-menu')
    scrape_navigation('desktop-navigation', 'cesde-menu')
    scrape_social_networks(soup)
    scrape_who_we_are()
    scrape_academic_schedule()

    Menu.objects.filter(active=False).delete()
    SubMenu.objects.filter(active=False).delete()
    