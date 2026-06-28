# Python-Lernplan – CO₂-Messstation
Stand: Juni 2026 · Ole Meißner · Universität Stuttgart, Maschinenbau

---

## Woche 1 – Setup & Python-Grundlagen
*Ziel: Grundlegende Programmierkonzepte anwenden und einfache Programme erstellen.*

### Setup (einmalig)
- VS Code installieren: https://code.visualstudio.com
- Python 3 installieren: https://www.python.org/downloads
- In VS Code: Extension „Python" (von Microsoft) installieren

### Konzepte
1. **Variablen & Datentypen**
2. **print()** – Ausgabe auf dem Bildschirm
3. **Rechnen** – `+`, `-`, `*`, `/`, Klammern
4. **if / elif / else** – Bedingte Ausführung
5. **while-Schleife** – Iteration für kontinuierliche Messung

### Meilenstein ✅ Abgeschlossen
Programm zur Bewertung eines simulierten CO₂-Werts mit kategorisierter Ausgabe.

---

## Woche 2 – Funktionen, Dateien & Timestamps
*Ziel: Messdaten strukturiert speichern.*

### Konzepte
1. **Funktionen** – `def messe_co2():` – Modularisierung von Code
2. **Listen & Schleifen** – Verwaltung von Messwerten
3. **Datum und Uhrzeit** – `import datetime` – Zeitstempel für Messungen
4. **CSV-Dateien schreiben** – `import csv` – Tabellarische Datenspeicherung
5. **f-Strings** – `f"CO₂: {wert} ppm"` – Dynamische Zeichenketten

### Meilenstein ✅ Abgeschlossen
Programm zur sekündlichen Generierung simulierter CO₂-Werte mit Zeitstempel-Speicherung in CSV.

---

## Woche 3 – Raspberry Pi & SSH
*Ziel: Remote-Entwicklung auf dem Raspberry Pi.*

### Setup RasPi (einmalig)
1. SD-Karte mit Raspberry Pi OS flashen (Raspberry Pi Imager)
2. SSH und WLAN im Imager vorkonfigurieren
3. Pi booten, SSH-Verbindung herstellen: `ssh ole@raspberrypi.local`
4. VS Code Remote SSH Extension verbinden

### Konzepte
1. **Terminal-Grundlagen** – `ls`, `cd`, `mkdir`, `python3 datei.py`
2. **pip** – Paketmanager für Python-Bibliotheken
3. **SSH** – Verschlüsselte Remote-Verbindung

### Meilenstein ✅ Abgeschlossen (24.06.2026)
VS Code Remote SSH verbunden mit Pi (`raspberrypi.local`), Python-Skripte werden direkt auf dem Pi ausgeführt.

---

## Woche 4 – Sensorintegration (SCD41)
*Ziel: Echte CO₂-Messdaten erfassen.*

### Hardware (I2C, 4 Kabel)
| SCD-41 Pin | RasPi GPIO Pin |
|------------|----------------|
| VIN        | Pin 1 (3.3V)   |
| GND        | Pin 6 (GND)    |
| SDA        | Pin 3 (SDA)    |
| SCL        | Pin 5 (SCL)    |

### Software
```bash
sudo raspi-config  # Interface Options → I2C → Enable
pip install adafruit-circuitpython-scd4x
```

### Konzepte
1. **Bibliotheken importieren** – `import board`, `import adafruit_scd4x`
2. **Objekte & Methoden** – `sensor.CO2`, `sensor.temperature`, `sensor.relative_humidity`
3. **try / except** – Fehlerbehandlung bei Sensor-Kommunikationsfehler

### Meilenstein ✅ Abgeschlossen (24.06.2026)
`logger.py` läuft auf dem Pi, liest echte CO₂-Werte vom SCD41 und schreibt diese mit Zeitstempel in CSV.

---

## Woche 5 – Webdashboard & Live-Visualisierung
*Ziel: Messdaten in Echtzeit im Browser darstellen.*

### Umgesetzt
- Flask-Dashboard (`dashboard.py`) mit Live-Anzeige: CO₂-Wert, Ampelindikator, Bewertung, Temperatur, Luftfeuchtigkeit
- `logger.py` erfasst und speichert CO₂, Bewertung, Temperatur und Luftfeuchtigkeit in CSV
- AJAX-basierter Auto-Refresh alle 10 Sekunden über `/daten`-Endpoint (JSON)

### Konzepte
1. **Flask** – Python-Webframework, Routing via `@app.route()`
2. **JSON / jsonify** – Datenaustauschformat zwischen Server und Browser
3. **AJAX / fetch()** – Asynchrone HTTP-Anfragen ohne Seitenneuladen
4. **DOM-Manipulation** – `document.getElementById()`, `.textContent`, `.style`
5. **setInterval()** – Periodische Funktionsausführung im Browser
6. **async / await** – Asynchrone Programmierung in JavaScript

### Meilenstein ✅ Abgeschlossen (27.06.2026)
Dashboard läuft auf dem Pi, zeigt CO₂-Wert mit Ampel und Bewertung sowie Temperatur und Luftfeuchtigkeit, aktualisiert sich alle 10 Sekunden per AJAX.

---

## Woche 6 – Autostart & Dauerbetrieb (systemd)
*Ziel: Pi läuft vollständig autonom – kein manuelles Starten nötig.*

### Umgesetzt
- Zwei systemd-Service-Dateien erstellt: `co2-logger.service` und `co2-dashboard.service`
- Logger startet nach `local-fs.target`, Dashboard nach Logger (`After=` + `Wants=`)
- Beide Dienste mit `systemctl enable` aktiviert → starten automatisch beim Booten
- Getestet: Pi neugestartet, beide Dienste liefen sofort – auch ohne vorhandene CSV

### Konzepte
1. **systemd** – Dienst-Manager unter Linux, startet alle Hintergrunddienste beim Booten
2. **Service-Datei** – Textdatei mit drei Abschnitten: `[Unit]`, `[Service]`, `[Install]`
3. **`After=` / `Wants=`** – Abhängigkeiten zwischen Diensten definieren
4. **`ExecStart=`** – absoluter Pfad zu Python + Skript (systemd kennt keine `PATH`-Variable)
5. **`systemctl enable/start/stop/status`** – Dienste verwalten

### Meilenstein ✅ Abgeschlossen (28.06.2026)
Pi startet vollständig autonom: Logger und Dashboard laufen nach dem Booten ohne manuellen Eingriff. Phase 1 abgeschlossen.

---

## Ressourcen

- Python-Dokumentation: https://docs.python.org/3/tutorial/
- Adafruit SCD-41 Guide: https://learn.adafruit.com/adafruit-scd-40-and-scd-41
- Raspberry Pi GPIO Pinout: https://pinout.xyz
- SSH in VS Code: https://code.visualstudio.com/docs/remote/ssh
- Flask-Dokumentation: https://flask.palletsprojects.com/

---

## CO₂-Referenzwerte

| Konzentration | Bewertung |
|---------------|-----------|
| < 800 ppm | Sehr gut – Außenluftqualität |
| 800–1000 ppm | Gut |
| 1000–1400 ppm | Mittel – Lüftung empfohlen |
| 1400–2000 ppm | Schlecht – Lüftung erforderlich |
| > 2000 ppm | Sehr schlecht – gesundheitlich relevant |

Außenluft: typischerweise ~420 ppm (Stand 2024). In unzureichend belüfteten Räumen wurden Werte über 3000 ppm gemessen.
