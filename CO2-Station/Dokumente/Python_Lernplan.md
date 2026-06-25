# Python-Lernplan – CO₂-Messstation



## Woche 1 – Setup & Python-Grundlagen
*Ziel: Einfache Programme schreiben und Verständnis der Grundbausteine.*

### Setup (einmalig, ca. 30 Min.)
- **VS Code** installieren: https://code.visualstudio.com
- **Python 3** installieren: https://www.python.org/downloads
- In VS Code: Extension „Python" (von Microsoft) installieren
- Ersten Test: eine Datei `hallo.py` anlegen, `print("Hallo Welt")` schreiben, ausführen

### Konzepte dieser Woche
1. **Variablen & Datentypen** 
2. **print()** – Ausgabe auf dem Bildschirm
3. **Rechnen** – `+`, `-`, `*`, `/`, Klammern
4. **if / elif / else** – Entscheidungen
5. **while-Schleife** – Endlosschleife für kontinuierliche Messung

### Meilenstein ✅ Abgeschlossen
Ein Programm, das eine simulierte CO₂-Zahl einliest, bewertet (gut/mittel/schlecht)
und eine farblich passende Meldung ausgibt.

---

## Woche 2 – Funktionen, Dateien & Timestamps
*Ziel: Messdaten strukturiert speichern.*

### Konzepte
1. **Funktionen** – `def messe_co2():` – Code in wiederverwendbare Blöcke packen
2. **Listen & Schleifen** – Messwerte verwalten
3. **Datum und Uhrzeit** – `import datetime` – Timestamps für jede Messung
4. **CSV-Dateien schreiben** – `import csv` – Daten tabellarisch speichern
5. **f-Strings** – `f"CO₂: {wert} ppm"` – Texte dynamisch zusammenbauen

### Meilenstein ✅ Abgeschlossen
Ein Programm, das jede Sekunde einen simulierten CO₂-Wert generiert,
mit Timestamp in eine CSV-Datei schreibt, und nach 60 Sekunden stoppt.

---

## Woche 3 – Raspberry Pi & SSH einrichten *(Hardware ausstehend)*
*Ziel: Arbeit remote auf dem RasPi.*

### Setup RasPi (einmalig, ca. 2 Stunden)
1. Pi an Monitor + Maus + Tastatur anschließen, booten
2. WLAN einrichten über Pi OS Desktop
3. SSH aktivieren: `sudo raspi-config` → Interface Options → SSH → Enable
4. IP-Adresse des Pi herausfinden: `hostname -I`
5. Monitor aus, nur noch SSH

### VS Code Remote SSH einrichten
- Extension „Remote - SSH" in VS Code installieren
- Verbindung: `ssh ole@<IP-Adresse>`
- Passwort: Standard ist `raspberry` → ändern mit `passwd`

### Konzepte
1. **Terminal-Grundlagen** – `ls`, `cd`, `mkdir`, `python3 datei.py`
2. **pip** – Paketmanager für Python-Bibliotheken
3. **Virtuelle Umgebung** – `python3 -m venv venv` 

### Meilenstein ✅ Abgeschlossen (24.06.2026)
VS Code auf dem Laptop, Verbindung via SSH mit dem Pi,
und Ausführung des CSV-Programm aus Woche 2 direkt auf dem Pi.

---

## Woche 4 – Echter CO₂-Wert
*Ziel: Der SCD-41 liefert echte Messdaten.*

### Hardware anschließen (I2C, 4 Kabel)
| SCD-41 Pin | RasPi GPIO Pin |
|------------|----------------|
| VIN        | Pin 1 (3.3V)   |
| GND        | Pin 6 (GND)    |
| SDA        | Pin 3 (SDA)    |
| SCL        | Pin 5 (SCL)    |

### Software einrichten
```bash
# I2C aktivieren
sudo raspi-config → Interface Options → I2C → Enable

# Bibliotheken installieren
pip install adafruit-circuitpython-scd4x
```

### Konzepte
1. **Bibliotheken importieren** – `import board`, `import adafruit_scd4x`
2. **Objekte & Methoden** – `sensor.CO2`, `sensor.temperature`, `sensor.relative_humidity`
3. **try / except** – Fehlerbehandlung falls Sensor nicht antwortet

### Meilenstein ✅ Abgeschlossen (24.06.2026)
logger.py läuft auf dem Pi, liest echte CO₂-Werte (892 ppm) vom SCD41 und schreibt in CSV.

---

## Woche 5 – Visualisierung & Dashboard 🔄 In Arbeit
*Ziel: Daten werden live dargestellt.*

### Umgesetzt (auf dem Laptop, vor RasPi-Einrichtung)
- Flask-Dashboard (`dashboard.py`) ist fertig und läuft lokal
- Zeigt aktuellen CO₂-Wert mit Ampel, Verlaufsdiagramm (letzte 60 Messungen), Tabelle (letzte 20)
- Liest aus `messungen.csv`

### Umgesetzt auf dem Pi (24.06.2026)
- Dashboard läuft auf dem Pi (logger.py + dashboard.py)
- Zeigt echte Sensor-Daten live im Browser

### Noch offen
- Dashboard auf dem Pi laufen lassen
- Messung und Dashboard parallel als Hintergrundprozesse
- Auto-Refresh aktivieren

### Meilenstein ⬜ Vollständig abgeschlossen wenn:
Live Dashboard über den Browser von den Messdaten.

---

## Ressourcen (alle kostenlos)

- **Python lernen:** https://docs.python.org/3/tutorial/ (offizielle Doku, sehr gut)
- **Adafruit SCD-41 Guide:** https://learn.adafruit.com/adafruit-scd-40-and-scd-41
- **RasPi GPIO Pinout:** https://pinout.xyz
- **SSH in VS Code:** https://code.visualstudio.com/docs/remote/ssh

---

## CO₂-Referenzwerte (zum Einordnen der späteren Daten)

| Bereich | Bewertung |
|---------|-----------|
| < 800 ppm | Sehr gut – frische Außenluft |
| 800–1000 ppm | Gut |
| 1000–1400 ppm | Mittel – Lüften empfohlen |
| 1400–2000 ppm | Schlecht – dringend lüften |
| > 2000 ppm | Sehr schlecht – gesundheitlich relevant |

*Außenluft hat typischerweise ~420 ppm (2024). In schlecht gelüfteten Altbauwohnungen
wurden Werte über 3000 ppm gemessen.*

---

*Dieser Plan ist ein lebendiges Dokument - Anpassungen folgen nach Fortschritt*
