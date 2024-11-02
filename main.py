from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Fonction pour scraper le calendrier et les jours fériés
def get_calendar_and_holidays(year):
    url = f"https://www.calendrier-365.fr/calendrier-{year}.html"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Extraire le calendrier par mois
    calendrier = {}
    for month_section in soup.find_all("div", class_="jaarkalender"):
        month_name = month_section.find("caption", class_="calendar-title").text.strip()
        calendrier[month_name] = []
        for row in month_section.find("tbody").find_all("tr"):
            week_data = [cell.text.strip() if cell.text.strip() else ' ' for cell in row.find_all("td")]
            calendrier[month_name].append(week_data)

    # Extraire les jours fériés
    jours_feries = []
    for table in ["legenda_left", "legenda_right"]:
        for row in soup.find("table", {"id": table}).find_all("tr"):
            date = row.find("div", class_="legenda_day").text.strip()
            event = row.find("div", class_="fl").text.strip()
            jours_feries.append({"date": date, "event": event})

    return {
        "calendrier": calendrier,
        "jours_feries": jours_feries
    }

# Formater les résultats JSON selon le modèle demandé
def format_result(data):
    # En-tête des jours de la semaine
    week_header = "n°\t Lu\tMa\tMe\tJe\tVe\tSa\tDi"

    # Formater le calendrier
    calendrier_formatted = "Calendrier par mois:\n"
    for month, weeks in data["calendrier"].items():
        calendrier_formatted += f"\n{month}:\n{week_header}\n"
        for week in weeks:
            calendrier_formatted += "\t " + "\t".join(week) + "\n"
    
    # Formater les jours fériés
    jours_feries_formatted = "\nJours fériés 2025 :\n"
    for jour in data["jours_feries"]:
        jours_feries_formatted += f"{jour['date']} - {jour['event']}\n"

    return calendrier_formatted + jours_feries_formatted

# Route GET pour rechercher le calendrier d'une année
@app.route('/recherche', methods=['GET'])
def recherche_calendrier():
    year = request.args.get("calendrier")
    
    # Vérification de l'année spécifiée
    if not year or not year.isdigit():
        return jsonify({"error": "Veuillez spécifier une année valide (par exemple, ?calendrier=2025)"}), 400
    
    try:
        data = get_calendar_and_holidays(year)
        formatted_result = format_result(data)
        return jsonify({"result": formatted_result})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Erreur lors de la récupération du calendrier"}), 500

# Lancement de l'application Flask sur host=0.0.0.0 et port=5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
