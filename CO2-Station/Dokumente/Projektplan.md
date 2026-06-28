# Projektplan – Autonomer CO₂-Kartierungsroboter
Stand: Juni 2026 · Ole Meißner · Universität Stuttgart, Maschinenbau

---

## Projektvision

Entwicklung eines autonomen Roboters, der Räume systematisch abfährt und eine räumlich aufgelöste CO₂-Karte (Heatmap) erstellt. Das System erkennt Luftqualitätsprobleme selbstständig und ist erweiterbar auf weitere Schadstoffe (Feinstaub PM2.5, VOC). Langfristiges Ziel: autonomes Verhalten in unbekannten Umgebungen mit selbst erstelltem Messplan.

---

## Hardware

| Komponente | Modell | Zweck | Status |
|---|---|---|---|
| Hauptrechner | Raspberry Pi 5 Starterkit 4GB (inkl. 64GB SD, Gehäuse, Netzteil, Pi OS) | Steuerung, Datenspeicherung, Dashboard | ✅ In Betrieb |
| CO₂-Sensor | Pimoroni SCD41 Breakout PIM587 (CO₂, Temp., Luftfeuchtigkeit) | Hauptsensor Phase 1+2 | ✅ In Betrieb |
| Verbindungskabel | 40pin Jumper/Dupont Female-Female 0,50m | GPIO-Verbindung Sensor ↔ Pi | ✅ In Betrieb |
| Stromversorgung mobil | Powerbank USB-C, min. 20W PD | Phase 2 – mobiler Betrieb | ⬜ Offen |
| Antrieb | DC-Motoren + Motortreiber (Modell TBD) | Phase 2 | ⬜ Offen |
| Hinderniserkennung | Ultraschallsensoren HC-SR04 (×3–4) | Phase 2 | ⬜ Offen |
| Erweiterung Sensorik | Sensirion SPS30 (PM2.5) + SGP40 (VOC) | Phase 3 | ⬜ Offen |

Hardware-Entscheidungen für Phase 2 und 3 sind vorläufig und werden vor Baubeginn finalisiert.

**Sensor-Bibliothek:** Der Pimoroni SCD41 (PIM587) verwendet denselben Sensirion SCD41-Chip wie die Adafruit-Variante. Die Bibliothek `adafruit-circuitpython-scd4x` ist vollständig kompatibel. I2C-Adresse: `0x62`. Anschluss über Female-Female Jumper-Kabel direkt an GPIO-Pins (kein STEMMA QT erforderlich).

---

## Phasen & Meilensteine

### Phase 1 – Stationäre CO₂-Messstation
Ziel: Lauffähiges Messsystem mit Datenspeicherung und Live-Dashboard.

| Meilenstein | Beschreibung | Status |
|---|---|---|
| M1.1 | Python-Grundlagen: Variablen, Schleifen, Bedingungen | ✅ Abgeschlossen |
| M1.2 | Funktionen, CSV-Speicherung, Timestamps | ✅ Abgeschlossen |
| M1.3 | RasPi einrichten, SSH + VS Code Remote | ✅ Abgeschlossen (24.06.2026) |
| M1.4 | SCD-41 anschließen, erste echte Messung | ✅ Abgeschlossen (24.06.2026) |
| M1.5 | Live-Dashboard im Browser (Flask) | ✅ Abgeschlossen (26.06.2026) |
| M1.6 | Dauerbetrieb einrichten (Autostart beim Booten) | ✅ Abgeschlossen (28.06.2026) |

Ergebnis Phase 1: RasPi läuft 24/7, misst CO₂/Temp/Luftfeuchtigkeit, speichert alle Daten mit Timestamp, zeigt Live-Dashboard im Browser. Logger und Dashboard starten automatisch beim Booten via systemd.

---

### Phase 2 – Mobiler Messroboter
Ziel: Fahrender Roboter mit Hinderniserkennung, der Sensor aus Phase 1 trägt.

| Meilenstein | Beschreibung | Status |
|---|---|---|
| M2.1 | Chassis-Konzept: Skizzen, Maße, Materialwahl | ⬜ Offen |
| M2.2 | Konstruktion & Fertigung des Chassis | ⬜ Offen |
| M2.3 | Motorsteuerung: Vorwärts, Rückwärts, Kurven | ⬜ Offen |
| M2.4 | Hinderniserkennung mit Ultraschall | ⬜ Offen |
| M2.5 | Autonome Navigation: vordefinierte Route (Stufe 1) | ⬜ Offen |
| M2.6 | Integration SCD-41 auf Rover, erste Messfahrt | ⬜ Offen |
| M2.7 | Positionserfassung + Verknüpfung mit Messdaten | ⬜ Offen |

Ergebnis Phase 2: Rover fährt einen Raum nach vorgegebener Route ab und erstellt eine erste CO₂-Heatmap mit räumlicher Auflösung.

---

### Phase 3 – Autonome Kartierung & erweiterte Sensorik
Ziel: Selbstständige Navigation in bekannter Wohnung, kombinierte Heatmaps, Anomalieerkennung.

| Meilenstein | Beschreibung | Status |
|---|---|---|
| M3.1 | SLAM-Grundlagen: Raumkarte aus Sensordaten aufbauen | ⬜ Offen |
| M3.2 | Navigation in bekannter Wohnung (mehrere Räume) | ⬜ Offen |
| M3.3 | Erweiterung Sensorik: PM2.5 + VOC | ⬜ Offen |
| M3.4 | Kombinierte Heatmaps (CO₂ + Feinstaub + VOC) | ⬜ Offen |
| M3.5 | Anomalieerkennung: automatische Alarmierung bei Ausschlägen | ⬜ Offen |
| M3.6 | Autonomes Verhalten in unbekannten Umgebungen (SLAM Stufe 3) | ⬜ Offen |

Ergebnis Phase 3: Vollautonomes System, das unbekannte Räume kartiert, einen Messplan erstellt und Luftqualitätsprobleme selbstständig identifiziert.

---

## Softwarearchitektur

Der Code ist modular aufgebaut – Sensor-Logger und Dashboard sind strikt getrennt:

```
CO2-Station/
├── Skripte/
│   ├── dashboard.py       # Flask Web-Dashboard
│   └── logger.py          # Sensor-Logger (SCD41 → CSV)
└── Dokumente/
    ├── Projektplan.md
    ├── Python_Lernplan.md
    ├── Kostenübersicht.md
    └── Elektronik_Cheatsheet.html

/etc/systemd/system/          # auf dem Raspberry Pi (nicht im Repo)
├── co2-logger.service        # Autostart logger.py beim Booten
└── co2-dashboard.service     # Autostart dashboard.py (nach Logger)
```

Sensor-Code und Dashboard sind strikt getrennt – das ermöglicht den nahtlosen Übergang von Phase 1 zu Phase 2 ohne Umschreiben.

---

## Zeitplan

| Phase | Geschätzte Dauer |
|---|---|
| Phase 1 | 4–6 Wochen |
| Phase 2 | 2–4 Monate (inkl. Konstruktion) |
| Phase 3 | offen |

---

## Backlog

- Webserver im Heimnetzwerk erreichbar machen (alle Geräte können Dashboard öffnen)
- Datenbank statt CSV (SQLite) für bessere Abfragemöglichkeiten
- Mehrere stationäre Sensoren in der Wohnung verteilen
- Exportfunktion für wissenschaftliche Auswertung
