import os
import sys
import json
import django

# Configuración del entorno de Django
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from scraper.models import Menu, SubMenu, SubSubMenu, sub3menu

def generate_intents_json():
    intents = {"intents": []}
    
    # Recorrer cada entrada de la tabla Menu
    for menu in Menu.objects.all():
        menu_entry = {
            "tag": f"menu_{menu.id}",
            "patterns": [menu.title],
            "responses": [],
            "context_set": ""
        }
        
        # Obtener los submenús relacionados
        submenus = SubMenu.objects.filter(menu=menu)
        for submenu in submenus:
            submenu_entry = f"{submenu.title} (ID: {submenu.id})"
            menu_entry["responses"].append(submenu_entry)
            
            # Obtener los subsubmenús relacionados
            subsubmenus = SubSubMenu.objects.filter(submenu=submenu)
            for subsubmenu in subsubmenus:
                subsubmenu_entry = f"{subsubmenu.title} (ID: {subsubmenu.id})"
                menu_entry["responses"].append(subsubmenu_entry)
                
                # Obtener los sub3menús relacionados
                sub3menus = sub3menu.objects.filter(subsubmenu=subsubmenu)
                for sub3menu_item in sub3menus:
                    sub3menu_entry = f"{sub3menu_item.content} (ID: {sub3menu_item.id})"
                    menu_entry["responses"].append(sub3menu_entry)
        
        intents["intents"].append(menu_entry)
    
    # Guardar el JSON a un archivo, asegurándose de que los caracteres Unicode se decodifiquen
    with open('intents.json', 'w', encoding='utf-8') as json_file:
        json.dump(intents, json_file, ensure_ascii=False, indent=4)

generate_intents_json()