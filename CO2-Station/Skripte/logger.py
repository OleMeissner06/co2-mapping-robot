import board
import adafruit_scd4x
import time
import csv
import datetime
import os

i2c = board.I2C()
sensor = adafruit_scd4x.SCD4X(i2c)
sensor.start_periodic_measurement()
time.sleep(5)

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
    co2 = sensor.CO2
    bewertung = bewerte_co2(co2)
    temperatur = sensor.temperature
    feuchte = sensor.relative_humidity

    return co2, bewertung, temperatur, feuchte

BASE_DIR = os.path.dirname(__file__)
PFAD = os.path.join(BASE_DIR, "messungen.csv")

def speichere_messung(co2, bewertung, temperatur, feuchte):
    zeitstempel = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(PFAD, "a", newline="", encoding="utf-8") as datei:
        writer = csv.writer(datei)
        writer.writerow([zeitstempel, round(co2), bewertung, round(temperatur), round(feuchte)])

def erstelle_csv_wenn_noetig():
    if not os.path.exists(PFAD):
        with open(PFAD, "w", newline="", encoding="utf-8") as datei:
            writer = csv.writer(datei)
            writer.writerow(["Zeitstempel", "CO2 (ppm)", "Bewertung", "Temperatur (°C)", "Luftfeuchtigkeit (%)"])

erstelle_csv_wenn_noetig()
           
while True:
    co2_wert, bewertung, temperatur, feuchte = generiere_messung()
    print(f"CO2: {co2_wert:.0f} ppm – {bewertung}")
    speichere_messung(co2_wert, bewertung, temperatur, feuchte)
    time.sleep(1)