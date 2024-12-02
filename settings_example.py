#Settings example

import os

# This is the path to your file. It is important, that they are in the same folder as your script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# THe path to your database, here,'data' is the subfolder and 'database.db' the name of your database
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'database.db')

# Path to the csv files. Again, 'Data' is the subdirectory and 'users.csv' etc are examples of csv fileneames
CSV_FILES = {
    'users': os.path.join(BASE_DIR, 'data', 'users.csv'),
    'products': os.path.join(BASE_DIR, 'data', 'products.csv'),
    'sales': os.path.join(BASE_DIR, 'data', 'sales.csv'),
}

#Debug modus (True, try if you are still developing, False if you want to produce.)
DEBUG = True

#Small dictionary with information about your database
DATABASE = {
    'ENGINE': 'sqlite3',
    'NAME': 'database_used_for_project.db'
}
# If there is an API Key you can add it here
API_KEY = "my api key"

# Sepcify Host information
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

