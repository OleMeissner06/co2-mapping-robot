# CO2-Messstation Dashboard
# Startet einen lokalen Webserver. Aufruf im Browser: http://127.0.0.1:5000


import csv
import os
from flask import Flask

app = Flask(__name__)

# Absoluter Pfad zur CSV-Datei mit den Messdaten
BASE_DIR = os.path.dirname(__file__)
CSV_PFAD = os.path.join(BASE_DIR, "messungen.csv")


# DATENZUGRIFF
# Liest alle Messungen aus der CSV und gibt sie als Liste zurück.
# Zeile 0 (Kopfzeile) wird übersprungen.

def lade_messungen():
    if not os.path.exists(CSV_PFAD):
        return []
    with open(CSV_PFAD, encoding="utf-8") as datei:
        zeilen = list(csv.reader(datei))
    return zeilen[1:]


# HILFSFUNKTION
# Gibt einen Farbcode (Hex) zurück abhängig von der Bewertung.
# Wird für die Ampel und die Tabellenfärbung verwendet.

def farbe(bewertung):
    if "Sehr gut" in bewertung:
        return "#2ecc71"   # grün
    elif "Gut" in bewertung:
        return "#27ae60"   # dunkelgrün
    elif "Mittel" in bewertung:
        return "#f39c12"   # orange
    else:
        return "#e74c3c"   # rot


# ROUTE
# Flask-Konzept: @app.route("/") bedeutet: wenn jemand die
# Startseite aufruft, führe die Funktion darunter aus und
# schicke das Ergebnis (HTML) zurück an den Browser.

@app.route("/")
def startseite():
    messungen = lade_messungen()

    if not messungen:
        return "<p>Keine Daten vorhanden.</p>"

    # Letzten Eintrag für die Anzeige oben verwenden
    letzte = messungen[-1]
    aktueller_co2 = letzte[1]
    aktuelle_bewertung = letzte[2]
    ampelfarbe = farbe(aktuelle_bewertung)

    # Für das Diagramm: letzte 60 Messungen
    # Labels = Uhrzeiten (Zeichen 11-19 des Timestamps, z.B. "19:07:03")
    # Werte = CO2-Zahlen

    chart_daten = messungen[-60:]
    labels = [z[0][11:19] for z in chart_daten]
    werte = [z[1] for z in chart_daten]

    # Chart.js erwartet die Daten als JavaScript-Array mit doppelten Anführungszeichen

    labels_js = str(labels).replace("'", '"')
    werte_js = str(werte).replace("'", '"')

    # Tabelle: letzte 20 Einträge, neueste zuerst (reversed)

    tabelle_zeilen = ""
    for z in reversed(messungen[-20:]):
        f = farbe(z[2])
        tabelle_zeilen += f"""
        <tr>
            <td>{z[0]}</td>
            <td>{z[1]}</td>
            <td style="color:{f}; font-weight:600">{z[2]}</td>
        </tr>"""

    # HTML-SEITE
    # Python gibt einen langen HTML-String zurück den der Browser
    # rendert. Besteht aus drei Teilen:
    #   1. <style>  – Aussehen (CSS)
    #   2. <body>   – Inhalt (aktueller Wert, Diagramm, Tabelle)
    #   3. <script> – Diagramm-Logik (Chart.js, läuft im Browser)

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>CO₂-Messstation</title>

    <!-- Chart.js wird direkt aus dem Internet geladen (kein Install nötig) -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        /* Basis-Reset und Schrift */
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #f5f5f5; color: #222; padding: 40px; }}
        h1 {{ font-size: 1.4rem; font-weight: 600; color: #333; margin-bottom: 30px; letter-spacing: 0.5px; }}

        /* Aktueller Wert – Zeile mit Ampelpunkt, großer Zahl, Bewertungstext */
        .aktuell {{ background: white; border-radius: 6px; padding: 24px 30px; margin-bottom: 24px;
                    display: flex; align-items: center; gap: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .ampel {{ width: 16px; height: 16px; border-radius: 50%; background: {ampelfarbe}; flex-shrink: 0; }}
        .co2-wert {{ font-size: 2.4rem; font-weight: 700; color: #111; }}
        .co2-einheit {{ font-size: 1rem; color: #888; margin-left: 6px; }}
        .bewertung {{ font-size: 0.95rem; color: #555; }}

        /* Karten-Container für Diagramm und Tabelle */
        .karte {{ background: white; border-radius: 6px; padding: 24px 30px; margin-bottom: 24px;
                  box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .karte h2 {{ font-size: 0.85rem; font-weight: 600; color: #888; text-transform: uppercase;
                     letter-spacing: 1px; margin-bottom: 16px; }}
        canvas {{ max-height: 220px; }}

        /* Tabelle */
        table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
        th {{ text-align: left; padding: 8px 12px; color: #888; font-weight: 600;
              font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px;
              border-bottom: 1px solid #eee; }}
        td {{ padding: 9px 12px; border-bottom: 1px solid #f0f0f0; color: #333; }}
        tr:last-child td {{ border-bottom: none; }}
    </style>
</head>
<body>
    <h1>CO₂-Messstation</h1>

    <!-- Aktueller Wert mit Ampel -->
    <div class="aktuell">
        <div class="ampel"></div>
        <div>
            <span class="co2-wert">{aktueller_co2}</span>
            <span class="co2-einheit">ppm CO₂</span>
            <div class="bewertung">{aktuelle_bewertung}</div>
        </div>
    </div>

    <!-- Verlaufsdiagramm -->
    <div class="karte">
        <h2>Verlauf (letzte 60 Messungen)</h2>
        <canvas id="chart"></canvas>
    </div>

    <!-- Datentabelle -->
    <div class="karte">
        <h2>Letzte Messungen</h2>
        <table>
            <tr><th>Zeitstempel</th><th>CO₂ (ppm)</th><th>Bewertung</th></tr>
            {tabelle_zeilen}
        </table>
    </div>

    <!-- Chart.js Diagramm: läuft komplett im Browser -->
    <script>
        new Chart(document.getElementById('chart'), {{
            type: 'line',
            data: {{
                labels: {labels_js},      // Uhrzeiten auf der X-Achse
                datasets: [{{
                    label: 'CO₂ (ppm)',
                    data: {werte_js},     // CO2-Werte auf der Y-Achse
                    borderColor: '#555',
                    borderWidth: 1.5,
                    pointRadius: 0,       // keine Punkte an jedem Messwert
                    tension: 0.3,         // leicht gerundete Kurve
                    fill: false
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ ticks: {{ maxTicksLimit: 8, color: '#aaa' }}, grid: {{ color: '#f0f0f0' }} }},
                    y: {{ ticks: {{ color: '#aaa' }}, grid: {{ color: '#f0f0f0' }},
                          suggestedMin: 400, suggestedMax: 2000 }}
                }}
            }}
        }});
    </script>
</body>
</html>"""

    return html


# EINSTIEGSPUNKT
# Wird nur ausgeführt wenn du diese Datei direkt startest.
# debug=True: bei Code-Änderungen startet der Server automatisch neu.

if __name__ == "__main__":
    app.run(debug=True)