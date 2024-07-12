import requests
from bs4 import BeautifulSoup
from .models import Menu, SubMenu, SubSubMenu



def scrape_who_we_are():
    url = "https://www.cesde.edu.co/nosotros/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Buscar el contenedor principal
    main_container = soup.find('div', {'data-id': '78d319a'})
  

    # Extraer el contenido del título y el texto
    heading = main_container.find('h1', class_='elementor-heading-title')
    text_container = main_container.find('div', class_='elementor-widget-text-editor')
    
    

    title = heading.get_text(strip=True)
    content = text_container.get_text(strip=True)

    # Buscar el submenú correspondiente a "¿Quiénes somos?"
    submenu_entry = SubMenu.objects.filter(title='¿Quiénes somos?').first()
    

    # Crear o actualizar la entrada del sub-submenú con el contenido
    SubSubMenu.objects.update_or_create(
        submenu=submenu_entry,
        title=title,
        defaults={'link': url, 'content': content, 'active': True}
    )

    