import csv
import os
from flask import Flask, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
CSV_PFAD = os.path.join(BASE_DIR, "messungen.csv")

def lade_messungen():
    if not os.path.exists(CSV_PFAD):
        return []
    with open(CSV_PFAD, encoding="utf-8") as datei:
        zeilen = list(csv.reader(datei))
    return zeilen[1:]

def farbe(bewertung):
    if "Sehr gut" in bewertung:
        return "#2ecc71"
    elif "Gut" in bewertung:
        return "#27ae60"
    elif "Mittel" in bewertung:
        return "#f39c12"
    else:
        return "#e74c3c"

@app.route("/")
def startseite():
    messungen = lade_messungen()

    if not messungen:
        return "<p>Keine Daten vorhanden.</p>"

    letzte = messungen[-1]
    aktueller_co2 = letzte[1]
    aktuelle_bewertung = letzte[2]
    ampelfarbe = farbe(aktuelle_bewertung)

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>CO₂-Station</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #f5f5f5; color: #222; padding: 40px; }}
        h1 {{ font-size: 1.4rem; font-weight: 600; color: #333; margin-bottom: 30px; letter-spacing: 0.5px; }}
        .aktuell {{ background: white; border-radius: 6px; padding: 24px 30px;
                    display: flex; align-items: center; gap: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .ampel {{ width: 16px; height: 16px; border-radius: 50%; background: {ampelfarbe}; flex-shrink: 0; }}
        .co2-wert {{ font-size: 2.4rem; font-weight: 700; color: #111; }}
        .co2-einheit {{ font-size: 1rem; color: #888; margin-left: 6px; }}
        .bewertung {{ font-size: 0.95rem; color: #555; }}
    </style>
</head>
<body>
    <h1>CO₂-Station</h1>

    <div class="aktuell">
        <div class="ampel" id="ampel"></div>
        <div>
            <span class="co2-wert" id="co2-wert">{aktueller_co2}</span>
            <span class="co2-einheit">ppm CO₂</span>
            <div class="bewertung" id="bewertung">{aktuelle_bewertung}</div>
            <span id="temperatur">{letzte[3]}</span>
            <span> °C · </span>
            <span id="feuchte">{letzte[4]}</span>
            <span> % Luftfeuchtigkeit</span>
        </div>
    </div>

    <script>
        function farbe(bewertung) {{
            if (bewertung.includes("Sehr gut")) return "#2ecc71";
            if (bewertung.includes("Gut"))      return "#27ae60";
            if (bewertung.includes("Mittel"))   return "#f39c12";
            return "#e74c3c";
        }}
        async function fetchDaten() {{
            const antwort = await fetch('/daten');
            const d = await antwort.json();
            document.getElementById('co2-wert').textContent = d.co2;
            document.getElementById('bewertung').textContent = d.bewertung;
            document.getElementById('ampel').style.background = farbe(d.bewertung);
            document.getElementById('temperatur').textContent = d.temperatur;
            document.getElementById('feuchte').textContent = d.feuchte
        }}
        setInterval(fetchDaten, 10000);
    </script>
</body>
</html>"""

    return html

@app.route("/daten")
def daten():
    messungen = lade_messungen()
    letzte = messungen[-1]
    return jsonify({
        "co2": letzte[1],
        "bewertung": letzte[2],
        "temperatur": letzte[3],
        "feuchte": letzte[4]
    })

if __name__ == "__main__":
    app.run(debug=True)
