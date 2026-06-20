import random
import time


while True:
    co2_wert = random.gauss(1000, 150)
    if co2_wert < 800:
        print(f"CO2: {co2_wert:.0f} ppm - Luftqualität: Sehr gut")
    elif co2_wert < 1000:
        print(f"CO2: {co2_wert:.0f} ppm - Luftqualität: Gut")
    elif co2_wert < 1400:
        print(f"CO2: {co2_wert:.0f} ppm - Luftqualität: Mittel – lüften empfohlen")
    else:
        print(f"CO2: {co2_wert:.0f} ppm - Luftqualität: Schlecht – bitte sofort lüften!")
    time.sleep(1)
