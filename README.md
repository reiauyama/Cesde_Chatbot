# **EJECUCION GENERAL (set-up)**
- Si consideramos que estas ubicado en la carpeta raiz del proyecto <chatbotProject> se debe levantar en entorno **virtualenv venv** para crear el entorno virtual (importante en el directorio raiz del proyecto) y para su ejecucion con el siguiente comando **'.\venv\Scripts\activate'** , de cualquier forma, solo es requerida la ejecucion del script llamado 'activate' en la siguiente ubicacion chatbotProject>venv>Scripts>activate
- Una vez activo el entorno virtual es nesesario instalar sus dependencias, ejecute **pip install -r requirements.txt** esto es de un archivo que recolecta todas las librerias/dependencias usadas y en que version
- Levantar el servidor de base de datos local (XAMPP)  [Apache y MySQL]
- Realizar migraciones, 'python manage.py makemigrations' -> 'python manage.py migrate'
- Ejecutar el web scraping 'python manage.py scrape'
# **SCRAPING**
Info: hay una aplicacion dentro del proyecto llamada 'scraper', esta aplicacion tiene dentro scripts como 'scraper.py', 'scraperProgramasSedes.py' etc. tambien en esta aplicacion se encuentra la carpeta 'management'
carpeta en la cual hay un script que se encarga de recopilar las funciones donde se hace el scraping para ejecutar todas los scrapings con solo un comando
## Ejecutar scraping
- La linea **'python manage.py scrape** ejecuta el scraping completo con las funciones recopiladas en 'management/scrape.py'
# **CHATBOT**
Info: La parte que se encarga de el modelo que respondera las preguntas de los usuarios, esta en su propia actividad 'nltk_app' mas especificamente, la parte principal esta en 'views.py'
## Ejecutar scraping
- En la version en la que se redacta esto, el comando de ejecucion del chatbot es **python nltk_app/console_chatbot.py**

# NOTA:
- Si se siguen estos pasos de ejecucion no deberia de dar problemas
### Lista de comandos
- .\venv\Scripts\activate
- python manage.py makemigrations
- python manage.py migrate
- python manage.py scrape
- python nltk_app/console_chatbot.py
