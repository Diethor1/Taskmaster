import os
import csv
import sqlite3
import random 
import datetime as dt
import pandas as pd
import time
from dateutil.relativedelta import relativedelta
import openpyxl # 3.1.5

#Dit is een takenverdelerdie willekeurig taken verdeeld genaamd Random Taskmaster. Zie bijgevoegd document voor meer informatie
# Verbinding maken met de database

# Basisfolder waar dit script zich bevindt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pad naar 'data_files' waar de .csv files zijn
CSV_DIR = os.path.join(BASE_DIR, 'data_files')

# Pad waar de databank is
DB_PATH = os.path.join(BASE_DIR, 'ratama.db')

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()


# Tabellen maken 
try:
	c.execute('''CREATE TABLE IF NOT EXISTS team
			 (WN_id INTEGER PRIMARY KEY, Voornaam TEXT, Achternaam TEXT, Positie TEXT, Start_Werk DATE, Werk_Email TEXT)''')
	c.execute('''CREATE TABLE IF NOT EXISTS taken
			 (Taak_id INTEGER PRIMARY KEY, Datum DATE, Open_door TEXT, Afdeling TEXT, Omschrijving TEXT, Status DATE, Urgentie_grd INTEGER)''')
	c.execute('''CREATE TABLE IF NOT EXISTS urgentie
			 (Graad INTEGER PRIMARY KEY, Urgentie TEXT, Tijdlimiet TEXT)''')
	c.execute('''CREATE TABLE IF NOT EXISTS lid_taak
				(WN_id INTEGER , Taak_id INTEGER, Startdatum DATE, Urgentie_grd INTEGER, Status TEXT, Einddatum DATE)''')
except OSError as e:
	print(e)

# De veranderingen implementeren
conn.commit()

# We openen het cvs-bestand teamleden.csv en lezen de gegevens in
teamleden_csv_path = os.path.join(CSV_DIR, 'teamleden.csv')
with open(teamleden_csv_path, 'r') as tl_file:
	reader = csv.reader(tl_file)
	# We slaan de header over, want die die bevat de kolomnamen
	next(reader)
	for row in reader:
		# We voegen de data in onze tabel toe
		c.execute(f''' INSERT OR IGNORE INTO team (WN_id, Voornaam, Achternaam, Positie, Start_werk, Werk_Email)
			VALUES (?, ?, ?, ?, ?, ?) ''', row)



# We openen het cvs-bestand taken.csv en lezen de gegevens in
taken_csv_path = os.path.join(CSV_DIR, 'taken.csv')
with open(taken_csv_path, 'r') as taak_file:
	reader = csv.reader(taak_file)
	next(reader)
	for row in reader:
		# We voegen de data in onze tabel toe
		c.execute(f''' INSERT OR IGNORE INTO taken (Taak_id, Datum, Open_door, Afdeling, Omschrijving, Status, Urgentie_grd)
			VALUES (? ,? ,? ,? ,? ,? ,?) ''', row)

# We openen het cvs-bestand urgentie.csv en lezen de gegevens in
urgentie_csv_path = os.path.join(CSV_DIR, 'urgentie.csv')
with open(urgentie_csv_path , 'r') as urg_file:
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

#We creeren een eerste klasse randomizer
class Randomizer:
		vandaag = dt.date.today()
		morgen = dt.date.today() + dt.timedelta(days=1)
		binnen_week_ = dt.date.today() + dt.timedelta(weeks=1)
		binnen_maand = dt.date.today() + relativedelta(months=1)

		def __init__(self, db_name):
			# We schrijven een constructor die een verbinding maakt met de databank
			self.conn = sqlite3.connect('ratama.db')
			self.cursor = self.conn.cursor()

		def get_execution_time(self):
			# Capture current datetime when function is called
			 uitvoertijd = (dt.date.today())
			 return uitvoertijd
		
		def get_random_taak(self):
			# We halen een willekeurige taak uit de tabel taken
			self.cursor.execute("SELECT * FROM taken")
			taken =  self.cursor.fetchall()
			if not taken:
				return None
			return random.choice(taken)

		def get_random_teamlid(self):
			# We halen een willekeurig lid uit de tabel teamleden
			self.cursor.execute("SELECT * FROM team")
			teamleden = self.cursor.fetchall()
			if not teamleden:
				return None
			return random.choice(teamleden)	

		def koppel_taak_aan_teamlid(self):
			# De taak wordt aan het teamlid toegewezen
			taak = self.get_random_taak()
			teamlid = self.get_random_teamlid()

			if taak and teamlid:
				Taak_id, Datum, Open_door, Afdeling, Omschrijving, Status, Urgentie_grd = taak
				WN_id, Voornaam, Achternaam, Positie, Start_werk, Werk_Email = teamlid
				print(f"De taak '{Omschrijving}' met ID {Taak_id} werd toegewezen aan {Voornaam} {Achternaam} met Werknemernummer {WN_id}. Het urgentieniveau is {Urgentie_grd}.")
				return(WN_id, Taak_id, Urgentie_grd, Status)
			else:
				print("De taak kon niet toegewezen worden. Controleer de databank op taken en teamleden.")
				return None

		def schrijf_naar_lid_taak(self):
			# We voegen de toegewezen taak met teamlid toe aan de tabel lid_taak
			toegewezen_taak = self.koppel_taak_aan_teamlid()
			if toegewezen_taak:
					WN_id, Taak_id, Urgentie_grd, Status = toegewezen_taak
					startdatum = self.get_execution_time()
					if Urgentie_grd == 1:
						Einddatum = self.vandaag
					elif Urgentie_grd == 2:
						Einddatum = self.morgen
					elif Urgentie_grd == 3:
						Einddatum = self.binnen_week_
					else:
						Einddatum = self.binnen_maand
	
					try:
						self.cursor.execute('''INSERT OR IGNORE INTO lid_taak 
																	 (WN_id, Taak_id, Startdatum, Urgentie_grd, Status, Einddatum)
																	 VALUES (?, ?, ?, ?, ?, ?)''',
																(WN_id, Taak_id, startdatum, Urgentie_grd, Status, Einddatum))
						print(f"De taak met nummer '{Taak_id}' en Werknemernummer {WN_id} werden in lid_taak toegevoegd.\n"
									f"De taak werd aangenomen op {startdatum}. De deadline is op {Einddatum}.")
						self.conn.commit()  # Vergeet niet de wijzigingen op te slaan
					except sqlite3.Error as e:
						print("Er is jammer genoeg iets misgegaan:", e)
			else:
				print("Geen taak of teamlid beschikbaar om toe te wijzen.")



		def geef_taak_aan_teamlid(self):
			self.schrijf_naar_lid_taak()
			vraag1 = input(f"Ben je al begonnen met de taak? ja/nee\n")
			if vraag1.lower() == "ja":
				vraag2 = input("en heb je nog veel werk?\n")
				if vraag2.lower() == "ja":
					print("Goed, dan weet je wat je te doen staat, denk aan de deadline!")
				elif vraag2.lower() == "nee":
					vraag3 =input("Betekent dit dat je bijna klaar bent?\n")
					if vraag3.lower() == "ja":
						print("Fantastisch, doe zo voort!")
					elif vraag3.lower() == "nee":
						print("Gelieve de taak af te werken. Denk aan de deadline!")
					else: print("De input is jammer genoeg fout")
				else: print("Deze input wordt niet aanvaard.")
			elif vraag1.lower() == "nee":
				print("Denk aan de deadline! Stel jouw taak aub niet langer uit.")
			else:
				print("Deze input is jammer genoeg niet correct.")

		def exporteer_lid_taak_naar_excel(self, bestandsnaam='lid_taak.xlsx'):
			try:
				# Haal alle gegevens op uit de tabel lid_taak 
				query = "SELECT * FROM lid_taak"
				df = pd.read_sql_query(query, self.conn)
				# Schrijf de gegevens naar een Excel-bestand
				df.to_excel(bestandsnaam, index=False, engine='openpyxl')
				print(f"De tabel 'lid_taak' is succesvol opgeslagen als'{bestandsnaam}'.")
			except Exception as e:
				print(f"Er is iets misgegaan bij het exporteren: {e}")
						



		def sluiten(self):
			#we sluiten de verbinding met de databank
			self.conn.close()

#We vragen of we de takenlijst lid_taak misschien willen opslaan.
def vraag_om_takenlijst_op_te_slaan(randomizer):
	while True:
		vraag_xls = input("Wenst u de takenlijst op te slaan? ja/nee\n").strip().lower()
		if vraag_xls == 'ja':
			bestandsnaam = input("Voer de naam van het Excel-bestand in (bijv. lid_taak.xlsx): ").strip()
			if not bestandsnaam.endswith('.xlsx'):
					bestandsnaam += '.xlsx'
			randomizer.exporteer_lid_taak_naar_excel(bestandsnaam)
			break
		elif vraag_xls == 'nee':
			print("Hopelijk heb je alles opgeschreven? Veel succes!")
			break
		else:
			print("Je antwoord is ongeldig, probeer het opnieuw.")

if __name__ == '__main__':
	try:
		Random_TaskMaster = Randomizer('Ratama.db')	
		#Taken toewijzen
		for _ in range(4):
			Random_TaskMaster.geef_taak_aan_teamlid()
		#We vragen de gebruiker of hij/zij lid_taak wenst op te slaan
		vraag_om_takenlijst_op_te_slaan(Random_TaskMaster)
	except Exception as e:
		print(f"Er is een fout opgetreden: {e}")
	finally:
		Random_TaskMaster.sluiten()


			


