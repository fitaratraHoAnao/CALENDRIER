import requests
from bs4 import BeautifulSoup

# URL de la page du calendrier
url = "https://www.calendrier-365.fr/calendrier-2025.html"

# Récupérer le contenu de la page
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# Extraire les informations du menu et de l'en-tête
menu_text = soup.find("div", class_="navbar").text.strip()
date_info = soup.find("div", class_="bs-docs-section").text.strip()
header_text = soup.find("div", class_="main_info").text.strip()

# Extraction des mois et des jours fériés
calendrier = {}
for month_section in soup.find_all("div", class_="jaarkalender"):
    month_name = month_section.find("caption", class_="calendar-title").text.strip()
    calendrier[month_name] = []
    for row in month_section.find("tbody").find_all("tr"):
        week_data = [cell.text.strip() for cell in row.find_all("td") if cell.text.strip()]
        calendrier[month_name].append(week_data)

# Extraction des jours fériés
jours_feries = []
for table in ["legenda_left", "legenda_right"]:
    for row in soup.find("table", {"id": table}).find_all("tr"):
        date = row.find("div", class_="legenda_day").text.strip()
        event = row.find("div", class_="fl").text.strip()
        jours_feries.append({"date": date, "event": event})

# Affichage des informations extraites
print("Menu :", menu_text)
print("Date et semaine actuelle :", date_info)
print("En-tête du site :", header_text)

print("\nCalendrier par mois :")
for month, weeks in calendrier.items():
    print(f"\n{month}:")
    for week in weeks:
        print("\t", " | ".join(week))

print("\nJours fériés 2025 :")
for jour in jours_feries:
    print(f"{jour['date']} - {jour['event']}")
