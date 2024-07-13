import requests
from bs4 import BeautifulSoup
from .models import  SubMenu, SubSubMenu, sub3menu

def scrape_medellin():
    url = "https://www.cesde.edu.co/sedes/medellin/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    programasAcordeon = soup.find('div', class_='programas__accordeon')
    programas = programasAcordeon.find_all('article', class_='programas__accordeon__item')

    submenu_entry = SubMenu.objects.filter(title='Medellín').first()
    if not submenu_entry:
        print("No se encontró el SubMenu con el título 'Medellín'")
        return

    for programasItem in programas:
        extract = programasItem.find('h3')
        subsub_title = extract.get_text(strip=True)

        subsubmenu_entry, created = SubSubMenu.objects.update_or_create(
            submenu=submenu_entry,
            title=subsub_title,
            defaults={'link': ' ', 'active': True}
        )

        contentExtract = programasItem.find('div', class_='text__content')
        content = contentExtract.get_text(strip=True)
        escuela = programasItem.find('h4').get_text(strip=True)
        link = programasItem.find('a')['href']

        sub3menu.objects.update_or_create(
            subsubmenu=subsubmenu_entry,
            escuela=escuela,
            defaults={'content': content, 'link': link}
        )
def scrape_bello():
    url = "https://www.cesde.edu.co/sedes/bello/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    programasAcordeon = soup.find('div', class_='programas__accordeon')
    programas = programasAcordeon.find_all('article', class_='programas__accordeon__item')

    submenu_entry = SubMenu.objects.filter(title='Bello').first()
    if not submenu_entry:
        print("No se encontró el SubMenu con el título 'Bello'")
        return

    for programasItem in programas:
        extract = programasItem.find('h3')
        subsub_title = extract.get_text(strip=True)

        subsubmenu_entry, created = SubSubMenu.objects.update_or_create(
            submenu=submenu_entry,
            title=subsub_title,
            defaults={'link': ' ', 'active': True}
        )

        contentExtract = programasItem.find('div', class_='text__content')
        content = contentExtract.get_text(strip=True)
        escuela = programasItem.find('h4').get_text(strip=True)
        link = programasItem.find('a')['href']

        sub3menu.objects.update_or_create(
            subsubmenu=subsubmenu_entry,
            escuela=escuela,
            defaults={'content': content, 'link': link}
        )
def scrape_rionegro():
    url = "https://www.cesde.edu.co/sedes/rionegro/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    programasAcordeon = soup.find('div', class_='programas__accordeon')
    programas = programasAcordeon.find_all('article', class_='programas__accordeon__item')

    submenu_entry = SubMenu.objects.filter(title='Rionegro').first()
    if not submenu_entry:
        print("No se encontró el SubMenu con el título 'Bello'")
        return

    for programasItem in programas:
        extract = programasItem.find('h3')
        subsub_title = extract.get_text(strip=True)

        subsubmenu_entry, created = SubSubMenu.objects.update_or_create(
            submenu=submenu_entry,
            title=subsub_title,
            defaults={'link': ' ', 'active': True}
        )

        contentExtract = programasItem.find('div', class_='text__content')
        content = contentExtract.get_text(strip=True)
        escuela = programasItem.find('h4').get_text(strip=True)
        link = programasItem.find('a')['href']

        sub3menu.objects.update_or_create(
            subsubmenu=subsubmenu_entry,
            escuela=escuela,
            defaults={'content': content, 'link': link}
        )
def scrape_pintada():
    url = "https://www.cesde.edu.co/sedes/pintada/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    programasAcordeon = soup.find('div', class_='programas__accordeon')
    programas = programasAcordeon.find_all('article', class_='programas__accordeon__item')

    submenu_entry = SubMenu.objects.filter(title='La Pintada').first()
    if not submenu_entry:
        print("No se encontró el SubMenu con el título 'Pintada'")
        return

    for programasItem in programas:
        extract = programasItem.find('h3')
        subsub_title = extract.get_text(strip=True)

        subsubmenu_entry, created = SubSubMenu.objects.update_or_create(
            submenu=submenu_entry,
            title=subsub_title,
            defaults={'link': ' ', 'active': True}
        )

        contentExtract = programasItem.find('div', class_='text__content')
        content = contentExtract.get_text(strip=True)
        escuela = programasItem.find('h4').get_text(strip=True)
        link = programasItem.find('a')['href']

        sub3menu.objects.update_or_create(
            subsubmenu=subsubmenu_entry,
            escuela=escuela,
            defaults={'content': content, 'link': link}
        )
def scrape_apartado():
    url = "https://www.cesde.edu.co/sedes/apartado/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    programasAcordeon = soup.find('div', class_='programas__accordeon')
    programas = programasAcordeon.find_all('article', class_='programas__accordeon__item')

    submenu_entry = SubMenu.objects.filter(title='Apartadó').first()
    if not submenu_entry:
        print("No se encontró el SubMenu con el título 'Apartadó'")
        return

    for programasItem in programas:
        extract = programasItem.find('h3')
        subsub_title = extract.get_text(strip=True)

        subsubmenu_entry, created = SubSubMenu.objects.update_or_create(
            submenu=submenu_entry,
            title=subsub_title,
            defaults={'link': ' ', 'active': True}
        )

        contentExtract = programasItem.find('div', class_='text__content')
        content = contentExtract.get_text(strip=True)
        escuela = programasItem.find('h4').get_text(strip=True)
        link = programasItem.find('a')['href']

        sub3menu.objects.update_or_create(
            subsubmenu=subsubmenu_entry,
            escuela=escuela,
            defaults={'content': content, 'link': link}
        )
def scrape_bogota():
    url = "https://www.cesde.edu.co/sedes/bogota/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    programasAcordeon = soup.find('div', class_='programas__accordeon')
    programas = programasAcordeon.find_all('article', class_='programas__accordeon__item')

    submenu_entry = SubMenu.objects.filter(title='Bogotá').first()
    if not submenu_entry:
        print("No se encontró el SubMenu con el título 'Bogotá'")
        return

    for programasItem in programas:
        extract = programasItem.find('h3')
        subsub_title = extract.get_text(strip=True)

        subsubmenu_entry, created = SubSubMenu.objects.update_or_create(
            submenu=submenu_entry,
            title=subsub_title,
            defaults={'link': ' ', 'active': True}
        )

        contentExtract = programasItem.find('div', class_='text__content')
        content = contentExtract.get_text(strip=True)
        escuela = programasItem.find('h4').get_text(strip=True)
        link = programasItem.find('a')['href']

        sub3menu.objects.update_or_create(
            subsubmenu=subsubmenu_entry,
            escuela=escuela,
            defaults={'content': content, 'link': link}
        )