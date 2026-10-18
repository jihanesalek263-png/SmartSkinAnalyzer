"""
SmartSkinAnalyzer - Lecture des 3 capteurs depuis l'ESP32 + classification
---------------------------------------------------------------------------
Installation (une seule fois) :   py -m pip install pyserial

Utilisation :
    py lire_capteurs.py COM3          # vraie lecture (remplace COM3 par ton port)
    py lire_capteurs.py --simuler     # sans matériel, pour tester le code

Chaque mesure valide est ajoutée à mesures_reelles.csv
et la dernière mesure est écrite dans derniere_mesure.json (pour le dashboard).
"""

import csv
import json
import os
import random
import sys
import time
from datetime import datetime

from classification_peau import classifier_mesure

FICHIER_CSV = "mesures_reelles.csv"
FICHIER_JSON = "derniere_mesure.json"


def lignes_simulees():
    """Fait semblant d'être l'ESP32 (utile pour tester sans branchement)."""
    while True:
        yield json.dumps({
            "distance_cm": round(random.uniform(5, 40), 1),
            "temp_peau": round(random.uniform(28, 37), 1),
            "temp_air": round(random.uniform(20, 26), 1),
            "humidite": round(random.uniform(10, 80), 1),
        })
        time.sleep(1)


def lignes_serie(port):
    import serial  # pyserial
    with serial.Serial(port, 115200, timeout=3) as ser:
        print(f"Connecté à {port}. Ctrl+C pour arrêter.\n")
        while True:
            brut = ser.readline().decode("utf-8", errors="ignore").strip()
            if brut:
                yield brut


def enregistrer_csv(ligne):
    nouveau = not os.path.exists(FICHIER_CSV)
    with open(FICHIER_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if nouveau:
            w.writerow(["date", "distance_cm", "temperature", "humidite", "type_peau"])
        w.writerow(ligne)


def main():
    if len(sys.argv) < 2:
        print("Usage : py lire_capteurs.py COM3   (ou --simuler)")
        return
    source = lignes_simulees() if sys.argv[1] == "--simuler" else lignes_serie(sys.argv[1])

    for brut in source:
        if not brut.startswith("{"):
            continue  # messages de démarrage de l'ESP32, on ignore
        try:
            m = json.loads(brut)
        except json.JSONDecodeError:
            continue
        if "erreur" in m:
            print("ESP32 :", m["erreur"])
            continue

        distance = m.get("distance_cm")
        temp = m.get("temp_peau")
        hum = m.get("humidite")
        type_peau, message = classifier_mesure(distance, temp, hum)

        if type_peau is None:
            print(f"[mesure ignorée] {message}")
            continue

        print(f"d={distance} cm | peau={temp} °C | hum={hum} % -> {type_peau}")
        date = datetime.now().isoformat(timespec="seconds")
        enregistrer_csv([date, distance, temp, hum, type_peau])
        with open(FICHIER_JSON, "w", encoding="utf-8") as f:
            json.dump({**m, "date": date, "type_peau": type_peau}, f, ensure_ascii=False)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nArrêt.")
