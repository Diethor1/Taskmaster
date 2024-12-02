# TaskMaster

#TaskMaster is a task allocation tool designed to randomly assign tasks to team members, ensuring an even distribution and consideration of urgency levels. This project utilizes a SQLite database for storing task and team data and provides functionality for monitoring task progress.

---

## Features

- **Database Management**: Automatically creates tables if they do not exist.
- **Data Import**: Reads team member, task, and urgency data from CSV files and populates the database.
- **Random Task Assignment**: Assigns tasks to team members randomly.
- **Urgency-Based Deadlines**: Calculates deadlines based on task urgency levels.
- **Task Status Monitoring**: Prompts users about task progress and provides feedback.
- **Customizable**: Modify the database and logic as per project needs.

---

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Diethor1/Taskmaster.git
   cd Taskmaster
2. Install Dependencies: Ensure Python 3.x is installed along with the required libraries:
```bash
pip install -r requirements.txt
```

## Prepare Input Files: 

The following CSV files with example data are in the project directory:

teamleden.csv: Contains team member data.
taken.csv: Contains task data.
urgentie.csv: Contains urgency level data.

## Settings.py
The settingsfile contains instructions on how to add your own data to start appointing tasks randomly.

## Run the Program: Execute the script:

```bash
python Taskmaster.py
```
##Usage Taskaster

CSV File Format
```bash
teamleden.csv:

WN_id	Voornaam	Achternaam	Positie	Start_Werk	Werk_Email
1	John	Doe	Developer	2022-01-01	john.doe@company.com

taken.csv:

Taak_id	Datum	Open_door	Afdeling	Omschrijving	Status	Urgentie_grd
1	2024-01-01	Manager	IT	Update software	Open	2

urgentie.csv:

Graad	Urgentie	Tijdlimiet
1	High	Same day
```
## Interacting with the Program

When prompted, answer questions about task progress to log updates.
View task assignments and deadlines directly from the terminal.
After task assignment, you can download the task list.

## Project Structure

- ratama.db: SQLite database for storing team, task, and urgency data.
- teamleden.csv: CSV file containing team member information.
- taken.csv: CSV file containing task information.
- urgentie.csv: CSV file defining urgency levels and time limits.
- Taskmaster.py: Python script for managing and assigning tasks.
  
## How It Works

a. Database Initialization:

  Creates four tables: team, taken, urgentie, and lid_taak.
  
b. Data Import:

  Imports data from teamleden.csv, taken.csv, and urgentie.csv.
  
c. Task Assignment:

Randomly selects a task and assigns it to a team member.
Calculates a deadline based on urgency level.

d. Task Progress Monitoring:

Interacts with the user to log task progress and completion status.

c. Database Update:

Saves task assignments to the lid_taak table with deadlines and statuses.

## Example Output

```bash
De taak 'Update software' met ID 1 werd toegewezen aan John Doe met Werknemernummer 1. Het urgentieniveau is 2.
De taak met nummer '1' en Werknemernummer 1 werden in Taak_lid toegevoegd.
De taak werd aangenomen op 2024-11-18.
De deadline is op 2024-11-19.
Ben je al begonnen met de taak? ja/nee
```
##Output

After the tasks have been assigned you get asked if you want to save the file as an xls. If yes, you are asked to give it a name before saving.

## License

This project is licensed under the MIT License.


