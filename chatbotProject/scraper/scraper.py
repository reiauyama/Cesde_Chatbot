import requests
from bs4 import BeautifulSoup
from .models import Menu, SubMenu, SubSubMenu

def scrape_website():
    
    url = "https://www.cesde.edu.co/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    menu = soup.find('nav', id='desktop-navigation')
    ul_principal = menu.find('ul', class_='cesde-menu')
    menu_items = ul_principal.find_all('li', recursive=False)

    # Desactivar todas las entradas existentes antes de actualizar
    Menu.objects.all().update(active=False)
    SubMenu.objects.all().update(active=False)
    SubSubMenu.objects.all().update(active=False)

    for item in menu_items:
        link = item.find('a')
        title = link.get_text(strip=True)

        # Crear o actualizar la entrada del menú principal
        menu_entry, created = Menu.objects.update_or_create(
            title=title,
            defaults={'link': link['href'], 'active': True}
        )

        # Encontrar y procesar los submenús
        submenu_ul = item.find('ul')
        if submenu_ul:
            submenu_items = submenu_ul.find_all('li', recursive=False)
            for subitem in submenu_items:
                sublink = subitem.find('a')
                subtitle = sublink.get_text(strip=True)

                # Crear o actualizar la entrada del submenú
                submenu_entry, created = SubMenu.objects.update_or_create(
                    menu=menu_entry,
                    title=subtitle,
                    defaults={'link': sublink['href'], 'active': True}
                )

                # Encontrar y procesar los sub-submenús
                subsubmenu_ul = subitem.find('ul')
                if subsubmenu_ul:
                    subsubmenu_items = subsubmenu_ul.find_all('li', recursive=False)
                    for subsubitem in subsubmenu_items:
                        subsub_link = subsubitem.find('a')
                        subsub_title = subsub_link.get_text(strip=True)

                        # Crear o actualizar la entrada del sub-submenú
                        SubSubMenu.objects.update_or_create(
                            submenu=submenu_entry,
                            title=subsub_title,
                            defaults={'link': subsub_link['href'], 'active': True}
                        )

    # Eliminar las entradas que no se actualizaron (que ya no están activas)
    Menu.objects.filter(active=False).delete()
    SubMenu.objects.filter(active=False).delete()
    SubSubMenu
