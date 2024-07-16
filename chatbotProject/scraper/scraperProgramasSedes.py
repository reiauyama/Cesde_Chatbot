import requests
from bs4 import BeautifulSoup
from .models import SubMenu, SubSubMenu, sub3menu
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def update_or_create_entry(model, filter_kwargs, update_kwargs):
    try:
        entry, created = model.objects.update_or_create(
            **filter_kwargs,
            defaults=update_kwargs
        )
        return entry, created
    except Exception as e:
        logger.error(f"Error al actualizar o crear entrada en {model.__name__}: {e}")
        return None, False

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

    update_or_create_entry(SubSubMenu, {'submenu': submenu_entry, 'title': title}, {'link': url, 'content': content, 'active': True})

def scrape_location(url, location_title):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    programas_acordeon = soup.find('div', class_='programas__accordeon')
    if not programas_acordeon:
        logger.warning(f"No se encontró el acordeón de programas en la URL: {url}")
        return

    programas = programas_acordeon.find_all('article', class_='programas__accordeon__item')

    submenu_entry = SubMenu.objects.filter(title=location_title).first()
    if not submenu_entry:
        logger.warning(f"No se encontró el SubMenu con el título '{location_title}'")
        return

    # Desactivar las entradas existentes específicas de este SubMenu antes de actualizar
    subsubmenus_to_update = SubSubMenu.objects.filter(submenu=submenu_entry)
    sub3menus_to_update = sub3menu.objects.filter(subsubmenu__submenu=submenu_entry)

    subsubmenus_to_update.update(active=False)
    sub3menus_to_update.update(active=False)

    for programa_item in programas:
        extract = programa_item.find('h3')
        subsub_title = extract.get_text(strip=True) if extract else 'Sin título'
        logger.info(f"Procesando SubSubMenu: {subsub_title}")

        # Actualizar o crear subsubmenu_entry
        subsubmenu_entry, created = update_or_create_entry(
            SubSubMenu,
            {'submenu': submenu_entry, 'title': subsub_title},
            {'link': ' ', 'active': True}
        )
        if not subsubmenu_entry:
            continue
        logger.info(f"{'Creado' if created else 'Actualizado'} SubSubMenu: {subsub_title}")

        content_extract = programa_item.find('div', class_='text__content')
        content = content_extract.get_text(strip=True) if content_extract else 'Sin contenido'
        escuela_extract = programa_item.find('h4')
        title = escuela_extract.get_text(strip=True) if escuela_extract else 'Sin título'
        link = programa_item.find('a')['href'] if programa_item.find('a') else ''
        logger.info(f"Procesando Sub3Menu: {title} - {content} - {link}")

        # Actualizar o crear sub3menu_entry
        sub3menu_entry, created = update_or_create_entry(
            sub3menu,
            {'subsubmenu': subsubmenu_entry, 'title': title},
            {'content': content, 'link': link, 'active': True}
        )
        if not sub3menu_entry:
            continue
        logger.info(f"{'Creado' if created else 'Actualizado'} Sub3Menu: {title} - {content} - {link}")

    # Eliminar las entradas específicas de este SubMenu que no se actualizaron (que ya no están activas)
    subsubmenus_to_update.filter(active=False).delete()
    sub3menus_to_update.filter(active=False).delete()

def scrape_aspirantes():
    url = "https://www.cesde.edu.co/aspirantes/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table_content = soup.find('div', id='elementor-tab-content-1181')
    if not table_content:
        logger.warning(f"No se encontró la tabla de contenido en la URL: {url}")
        return

    # Encontrar la entrada de 'Cronograma académico' en SubMenu
    cronograma_academico_entry = SubMenu.objects.filter(title='Cronograma académico').first()
    if not cronograma_academico_entry:
        logger.warning("No se encontró la entrada de 'Cronograma académico' en SubMenu")
        return

    rows = table_content.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) != 2:
            continue
        date = cells[0].get_text(strip=True)
        event = cells[1].get_text(strip=True)

        logger.info(f"Procesando evento: {date} - {event}")

        # Actualizar o crear subsubmenu_entry para eventos de aspirantes
        subsubmenu_entry, created = update_or_create_entry(
            SubSubMenu,
            {'submenu': cronograma_academico_entry, 'title': date},
            {'link': '', 'active': True, 'content': event}
        )

def scrape_sedes():
    scrape_location("https://www.cesde.edu.co/sedes/medellin/", "Medellín")
    scrape_location("https://www.cesde.edu.co/sedes/bello/", "Bello")
    scrape_location("https://www.cesde.edu.co/sedes/rionegro/", "Rionegro")
    scrape_location("https://www.cesde.edu.co/sedes/pintada/", "La Pintada")
    scrape_location("https://www.cesde.edu.co/sedes/apartado/", "Apartadó")
    scrape_location("https://www.cesde.edu.co/sedes/bogota/", "Bogotá")

def scrape_all():
    scrape_sedes()
    scrape_aspirantes()
    scrape_who_we_are()  


