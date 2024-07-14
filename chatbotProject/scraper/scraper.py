import requests
from bs4 import BeautifulSoup
from .models import Menu, SubMenu, SubSubMenu, sub3menu
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

                subsubmenu_ul = subitem.find('ul')
                if subsubmenu_ul:
                    subsubmenu_items = subsubmenu_ul.find_all('li', recursive=False)
                    for subsubitem in subsubmenu_items:
                        subsub_link = subsubitem.find('a')
                        subsub_title = subsub_link.get_text(strip=True) if subsub_link else None
                        subsub_href = subsub_link['href'] if subsub_link and 'href' in subsub_link.attrs else None

                        SubSubMenu.objects.update_or_create(
                            submenu=submenu_entry,
                            title=subsub_title,
                            defaults={'link': subsub_href, 'active': True}
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
    SubSubMenu.objects.all().update(active=False)

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
    SubSubMenu.objects.filter(active=False).delete()

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

    # Crear un diccionario para rastrear las entradas procesadas
    processed_subsubmenus = {}
    processed_sub3menus = {}

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

        # Agregar al diccionario de procesados
        processed_subsubmenus[subsubmenu_entry.id] = subsubmenu_entry

        content_extract = programa_item.find('div', class_='text__content')
        content = content_extract.get_text(strip=True) if content_extract else 'Sin contenido'
        escuela_extract = programa_item.find('h4')
        escuela = escuela_extract.get_text(strip=True) if escuela_extract else 'Sin escuela'
        link = programa_item.find('a')['href'] if programa_item.find('a') else ''
        logger.info(f"Procesando Sub3Menu: {escuela} - {content} - {link}")

        # Actualizar o crear sub3menu_entry
        sub3menu_entry, created = update_or_create_entry(
            sub3menu,
            {'subsubmenu': subsubmenu_entry, 'escuela': escuela},
            {'content': content, 'link': link, 'active': True}
        )
        if not sub3menu_entry:
            continue
        logger.info(f"{'Creado' if created else 'Actualizado'} Sub3Menu: {escuela} - {content} - {link}")

        # Agregar al diccionario de procesados
        processed_sub3menus[sub3menu_entry.id] = sub3menu_entry

    # Desactivar las entradas no procesadas
    SubSubMenu.objects.filter(submenu=submenu_entry).exclude(id__in=processed_subsubmenus.keys()).update(active=False)
    sub3menu.objects.filter(subsubmenu__submenu=submenu_entry).exclude(id__in=processed_sub3menus.keys()).update(active=False)

    # Eliminar las entradas no activas
    SubSubMenu.objects.filter(submenu=submenu_entry, active=False).delete()
    sub3menu.objects.filter(subsubmenu__submenu=submenu_entry, active=False).delete()
def scrape_sedes():
    def scrape_medellin():
        scrape_location("https://www.cesde.edu.co/sedes/medellin/", "Medellín")
    scrape_medellin()

    def scrape_bello():
        scrape_location("https://www.cesde.edu.co/sedes/bello/", "Bello")
    scrape_bello()

    def scrape_rionegro():
        scrape_location("https://www.cesde.edu.co/sedes/rionegro/", "Rionegro")
    scrape_rionegro()

    def scrape_pintada():
        scrape_location("https://www.cesde.edu.co/sedes/pintada/", "La Pintada")
    scrape_pintada()

    def scrape_apartado():
        scrape_location("https://www.cesde.edu.co/sedes/apartado/", "Apartadó")
    scrape_apartado()

    def scrape_bogota():
        scrape_location("https://www.cesde.edu.co/sedes/bogota/", "Bogotá")
    scrape_bogota()
