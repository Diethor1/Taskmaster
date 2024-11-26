"""Dit is mijn Random Taskmaster. HHij zal jou helpen bij het verdelen van taken. Hij is fair, hij is rechtvaardig, hij is de Taskmaster."""

#Vooreerst impoteren we enkele modules
import csv
import sqlite3
from sqlite3 import Error
import random 
import datetime as dt
import pandas as pd
import time

# Verbinding maken met de database
conn = sqlite3.connect('ratama.db')
c = conn.cursor()

# Tabellen maken 
try:
	c.execute('''CREATE TABLE IF NOT EXISTS team
			 (WN_id INTEGER PRIMARY KEY, Voornaam TEXT, Achternaam TEXT, Positie TEXT, Start_Werk DATE, Werk_Email TEXT)''')
	c.execute('''CREATE TABLE IF NOT EXISTS taken
			 (Taak_id INTEGER PRIMARY KEY, Datum DATE, Open_door TEXT, Afdeling TEXT, Omschrijving TEXT, Status DATE, Urgentie_grd TEXT)''')
	c.execute('''CREATE TABLE IF NOT EXISTS urgentie
			 (Graad INTEGER PRIMARY KEY, Urgentie TEXT, Tijdlimiet TEXT)''')
	c.execute('''CREATE TABLE IF NOT EXISTS lid_taak
			  (Emp_id INTEGER , Taak_id INTEGER, Startdatum DATE, Urgentie_grd TEXT, Status TEXT, Einddatum DATE)''')
except Error as e:
	print(e)

# De veranderingen implementeren
conn.commit()

# We openen het cvs-bestand teamleden.csv en lezen de gegevens in
with open('teamleden.csv', 'r') as tl_file:
	reader = csv.reader(tl_file)
	# We slaan de header over, want die die bevat de kolomnamen
	next(reader)
	for row in reader:
		# We voegen de data in onze tabel toe
		c.execute(f''' INSERT OR IGNORE INTO team (WN_id, Voornaam, Achternaam, Positie, Start_werk, Werk_Email)
			VALUES (?, ?, ?, ?, ?, ?) ''', row)

# We openen het cvs-bestand taken.csv en lezen de gegevens in
with open('taken.csv', 'r') as taak_file:
	reader = csv.reader(taak_file)
	next(reader)
	for row in reader:
		# We voegen de data in onze tabel toe
		c.execute(f''' INSERT OR IGNORE INTO taken (Taak_id, Datum, Open_door, Afdeling, Omschrijving, Status, Urgentie_grd)
			VALUES (? ,? ,? ,? ,? ,? ,?) ''', row)

# We openen het cvs-bestand urgentie.csv en lezen de gegevens in
with open('urgentie.csv', 'r') as urg_file:
	reader = csv.reader(urg_file)
	next(reader)
	for row in reader:
		# We voegen de data in onze tabel toe
		c.execute(f''' INSERT OR IGNORE INTO urgentie (Graad, Urgentie, Tijdlimiet)
			VALUES (? ,? ,?) ''', row)

# En de nieuwe veranderingen implementeren
conn.commit()

# Query om alle tabellen op te sommen
c.execute("SELECT name FROM sqlite_master WHERE type='table'")

# Neem en print alle tabellen
tables = c.fetchall()
for table in tables:
	print(table[0])

# We sluiten de verbinding
conn.close()