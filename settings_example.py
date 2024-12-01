#Settings example

import os

# Vul hier je bestandsnaam in 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Adres van je database bestand
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'database.db')

# adres van de csv bestanden
CSV_FILES = {
    'users': os.path.join(BASE_DIR, 'data', 'users.csv'),
    'products': os.path.join(BASE_DIR, 'data', 'products.csv'),
    'sales': os.path.join(BASE_DIR, 'data', 'sales.csv'),
}

#Debug modus (True als je nog aan het ontwikkelen bent, False qls je wil produceren.)
DEBUG = True


DATABASE = {
    'ENGINE': 'sqlite3',
    'NAME': 'database_used_for_project.db'
}

