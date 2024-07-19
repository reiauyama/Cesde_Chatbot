import requests
from bs4 import BeautifulSoup
from .models import Menu, SubMenu, SubSubMenu, sub3menu
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

 
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

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def scrape_navigation(menu_id, ul_class, full_scraping):
    url = "https://www.cesde.edu.co/"
    soup = get_soup(url)

    menu = soup.find('nav', id=menu_id)
    ul_principal = menu.find('ul', class_=ul_class)
    menu_items = ul_principal.find_all('li', recursive=False)

    for item in menu_items:
        link = item.find('a')
        title = link.get_text(strip=True) if link else None
        href = link['href'] if link and 'href' in link.attrs else None

        menu_entry, _ = update_or_create_entry(Menu, {'title': title}, {'link': href, 'active': True})

        submenu_ul = item.find('ul')
        if submenu_ul:
            for subitem in submenu_ul.find_all('li', recursive=False):
                sublink = subitem.find('a')
                subtitle = sublink.get_text(strip=True) if sublink else None
                subhref = sublink['href'] if sublink and 'href' in sublink.attrs else None

                update_or_create_entry(SubMenu, {'menu': menu_entry, 'title': subtitle}, {'link': subhref, 'active': True})

def scrape_social_networks(soup):
    social_container = soup.find('div', {'area-label': 'network'})
    if not social_container:
        logger.warning("No se encontró el contenedor de redes sociales")
        return

    social_heading = social_container.find('h2', class_="elementor-heading-title elementor-size-default")
    title = social_heading.get_text(strip=True)
    if not social_heading:
        logger.warning("No se encontró el título 'Redes sociales'")
        return

    menu_entry, _ = update_or_create_entry(Menu, {'title': title}, {'link': '', 'active': True})

    for link in social_container.find_all('a', class_='social-element'):
        title = link.get('title', '').replace('ir a ', '')
        url = link.get('href', '')

        if title and url:
            logger.info(f"Encontrada red social: {title} - {url}")
            update_or_create_entry(SubMenu, {'menu': menu_entry, 'title': title}, {'link': url, 'active': True})
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

    update_or_create_entry(SubSubMenu, {'submenu': submenu_entry, 'title': title}, {'link': url, 'content': content, 'active': True})

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

    update_or_create_entry(SubMenu, {'menu': menu_entry, 'title': title}, {'link': url, 'active': True})

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

    subsubmenus_to_update = SubSubMenu.objects.filter(submenu=submenu_entry)
    sub3menus_to_update = sub3menu.objects.filter(subsubmenu__submenu=submenu_entry)

    subsubmenus_to_update.update(active=False)
    sub3menus_to_update.update(active=False)

    for programa_item in programas:
        extract = programa_item.find('h3')
        subsub_title = extract.get_text(strip=True) if extract else 'Sin título'
        logger.info(f"Procesando SubSubMenu: {subsub_title}")

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

        sub3menu_entry, created = update_or_create_entry(
            sub3menu,
            {'subsubmenu': subsubmenu_entry, 'title': title},
            {'content': content, 'link': link, 'active': True}
        )
        if not sub3menu_entry:
            continue
        logger.info(f"{'Creado' if created else 'Actualizado'} Sub3Menu: {title} - {content} - {link}")

    subsubmenus_to_update.filter(active=False).delete()
    sub3menus_to_update.filter(active=False).delete()

def estudiantesLinks():
    url = "https://www.cesde.edu.co/estudiantes/"
    soup = get_soup(url)

    service_items = soup.find_all('div', class_='service-item')

        # Crear una lista para almacenar los datos extraídos

    for item in service_items:
        link_tag = item.find('a')
        if link_tag:
            link = link_tag['href']
            title = link_tag.find_next('h3').get_text(strip=True)
            menu_entry = Menu.objects.filter(title='Estudiantes').first()
            update_or_create_entry(SubMenu, {'menu': menu_entry, 'title': title}, {'link': url, 'active': True})
 
    # Guardar los datos en la base de datos usando Django ORM
    try:
        menu_entry = Menu.objects.get(title="Estudiantes")
    except Menu.DoesNotExist:
        print("No se encontró la entrada de menú 'Estudiantes'")

def reglamentos():
    url = "https://www.cesde.edu.co/estudiantes/"
    soup = get_soup(url)

    reglamentos_items = soup.find('div', class_='elementor-column elementor-col-100 elementor-top-column elementor-element elementor-element-a00777a')
    reglamentos_title= reglamentos_items.find('h2', class_='"elementor-heading-title elementor-size-default')
    print(reglamentos_title)
    title =reglamentos_title.get_text(strip=True)
    menu_entry = Menu.objects.filter(title='Estudiantes').first()
    update_or_create_entry(SubMenu, {'menu': menu_entry, 'title': title}, {'link': url, 'active': True})
    
        
def scrape_sedes():
    scrape_location("https://www.cesde.edu.co/sedes/medellin/", "Medellín")
    scrape_location("https://www.cesde.edu.co/sedes/bello/", "Bello")
    scrape_location("https://www.cesde.edu.co/sedes/rionegro/", "Rionegro")
    scrape_location("https://www.cesde.edu.co/sedes/pintada/", "La Pintada")
    scrape_location("https://www.cesde.edu.co/sedes/apartado/", "Apartadó")
    scrape_location("https://www.cesde.edu.co/sedes/bogota/", "Bogotá")

def scrape_all(full_scraping):
    if full_scraping:
        Menu.objects.all().update(active=False)
        SubMenu.objects.all().update(active=False)
        SubSubMenu.objects.all().update(active=False)
        sub3menu.objects.all().update(active=False)
    
    url = "https://www.cesde.edu.co/"
    soup = get_soup(url)

    #scrape_navigation('preheader-navigation', 'cesde-preheader-menu', full_scraping)
    #scrape_navigation('desktop-navigation', 'cesde-menu', full_scraping)
    #scrape_social_networks(soup)
    #scrape_who_we_are()
    #scrape_academic_schedule()
    #scrape_sedes()
    #estudiantesLinks()
    reglamentos()

    if full_scraping:
        Menu.objects.filter(active=False).delete()
        SubMenu.objects.filter(active=False).delete()
        SubSubMenu.objects.filter(active=False).delete()
        sub3menu.objects.filter(active=False).delete()
