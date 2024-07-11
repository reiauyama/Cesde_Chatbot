import requests
from bs4 import BeautifulSoup
from .models import ScrapedData


def scrape_website():
    url = "https://www.cesde.edu.co/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')   #Obtener el html de la pagina 

    menu = soup.find('nav', id='desktop-navigation')     #Bucamos dentro del html, la barra de navegacion con ese id
    ul_principal = menu.find('ul', class_='cesde-menu') #Dentro de menu, buscamos los ul con esa clase
    menu_items = ul_principal.find_all('li', recursive=False)   #Dentro de ese ul buscamos todos los li hijos (no mas abajo) y los añadimos a un arreglo con find_all

    
    for item in menu_items:     #Buscamos dentro del arreglo sus etiquetas a
        link = item.find('a')
        
        text = link.get_text(strip=True)    #agarramos su texto  
        # Comprobar si L ya existe en la base de datos
        if not ScrapedData.objects.filter(title=text).exists():
            ScrapedData.objects.create(title=text)
            print(f"New entry added - Title: {text}")
        else:
            print(f"Entry already exists - Title: {text}")

    
    





    premenu = soup.find('nav', id='preheader-navigation')
    ul_premenu = premenu.find('ul', class_='cesde-preheader-menu')
    premenu_items = ul_premenu.find_all('li', recursive=False)

    for item in premenu_items:
        link = item.find('a')
        text = link.get_text(strip=True) #agarramos su texto y lo imprimimos
        # Comprobar si la URL ya existe en la base de datos
        if not ScrapedData.objects.filter(title=text).exists():
            ScrapedData.objects.create(title=text)
            print(f"New entry added - Title: {text}")
        else:
            print(f"Entry already exists - Title: {text}")

    print("Scraping completed")
        


    
    
        
scrape_website()
        # Guardar los datos en la base de datos
        
        #ScrapedData.objects.create(...): Crea una nueva instancia del modelo 
        #ScrapedData.objects.create(title=title, url=url)
