import os
import sys
import django

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# ///////////// Preparar los datos ////////////////////////

from scraper.models import Menu, SubMenu, SubSubMenu, sub3menu

menus = Menu.objects.all()
submenus = SubMenu.objects.all()
subsubmenus = SubSubMenu.objects.all()
sub3menus = sub3menu.objects.all()

# /////////////// pre -  Procesado de datos /////////////

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess(text):
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]
    stop_words = set(stopwords.words('spanish'))
    tokens = [word for word in tokens if not word in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

menu_titles = [preprocess(menu.title) for menu in menus]
submenu_titles = [preprocess(submenu.title) for submenu in submenus]
subsubmenu_titles = [preprocess(subsubmenu.title) for subsubmenu in subsubmenus]
sub3menu_titles = [preprocess(sub3menu.escuela) for sub3menu in sub3menus]
# ///Depuracion interna
print("Ejemplos de menú preprocesado:", menu_titles[:5])
print("Ejemplos de submenú preprocesado:", submenu_titles[:5])
print("Ejemplos de sub-submenú preprocesado:", subsubmenu_titles[:5])
print("Ejemplos de sub3menu preprocesado:", sub3menu_titles[:5])

# /////////////////// Entrenamiento del modelo //////////////////////////////

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Combina todos los títulos y crea etiquetas
texts = menu_titles + submenu_titles + subsubmenu_titles + sub3menu_titles
labels = ['menu'] * len(menu_titles) + ['submenu'] * len(submenu_titles) + ['subsubmenu'] * len(subsubmenu_titles) + ['sub3menu'] * len(sub3menu_titles)

# Une los tokens en una sola cadena
texts = [' '.join(tokens) for tokens in texts]

# Entrena el modelo
model = Pipeline([('vectorizer', CountVectorizer()), ('classifier', LogisticRegression())])
model.fit(texts, labels)


# /////////////////////////// Implementacion del modelo y prueba //////////////////////////////
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def classify_query(query):
    query = preprocess(query)
    query = ' '.join(query)
    return model.predict([query])[0]

# Ejemplo de uso
query = "Quiero información sobre eCesde"
category = classify_query(query + "\n")
print(f"La consulta pertenece a la categoría: {category}")

X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# /////////////////// Manejo de errores de sintaxis del usuario /////////////////

from fuzzywuzzy import process

def correct_spelling(query, choices):
    corrected_query = []
    for word in query.split():
        corrected_word, _ = process.extractOne(word, choices)
        corrected_query.append(corrected_word)
    return ' '.join(corrected_query)

choices = set(word for text in texts for word in text.split())
query = "Quiero informacion sobre eCesde"
query = correct_spelling(query, choices)
category = classify_query(query)
print(f"La consulta pertenece a la categoría: {category}")
