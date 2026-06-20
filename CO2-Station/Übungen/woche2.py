import random
import time
import csv
import datetime
import os


def bewerte_co2(wert):
    if wert < 800:
        return "Sehr gut"
    elif wert < 1000:
        return "Gut"
    elif wert < 1400:
        return "Mittel – lüften empfohlen"
    else:
        return "Schlecht – bitte sofort lüften!"
def generiere_messung():
    co2 = random.gauss(1000, 150)
    bewertung = bewerte_co2(co2)
    return co2, bewertung
PFAD = r"C:\Users\Admin\Desktop\Projekt\Projekt\CO2-Station\Übungen\messungen.csv"

def speichere_messung(co2, bewertung):
    zeitstempel = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(PFAD, "a", newline="", encoding="utf-8") as datei:
        writer = csv.writer(datei)
        writer.writerow([zeitstempel, round(co2), bewertung])

def erstelle_csv_wenn_noetig():
    if not os.path.exists(PFAD):
        with open(PFAD, "w", newline="", encoding="utf-8") as datei:
            writer = csv.writer(datei)
            writer.writerow(["Zeitstempel", "CO2 (ppm)", "Bewertung"])

erstelle_csv_wenn_noetig()
           
while True:
    co2_wert, bewertung = generiere_messung()
    print(f"CO2: {co2_wert:.0f} ppm – {bewertung}")
    speichere_messung(co2_wert, bewertung)
    time.sleep(1)