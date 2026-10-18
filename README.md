# SmartSkinAnalyzer

Analyse du type de peau (sèche, normale, mixte, grasse) avec un Arduino Uno
et 3 capteurs : humidité, température de la peau et distance.

## Matériel

- Arduino Uno + câble USB (câble de données)
- Breadboard et fils
- DHT22 (humidité) + résistance 10 kΩ
- MLX90614 (température de la peau, broches soudées de préférence)
- Capteur de distance infrarouge (3 fils : rouge, noir, jaune)

## Fichiers

| Fichier | Rôle |
|---|---|
| `smartskin_uno/smartskin_uno.ino` | code de l'Arduino |
| `classification_peau.py` | classification du type de peau |
| `lire_capteurs.py` | lit l'Arduino et affiche le résultat |

## Branchements

| Capteur | Fil / broche | Broche de l'Uno |
|---|---|---|
| DHT22 | patte 1 (VCC) | 5V |
| DHT22 | patte 2 (DATA) | 2 |
| DHT22 | patte 3 | rien |
| DHT22 | patte 4 (GND) | GND |
| MLX90614 | VIN | 3.3V |
| MLX90614 | GND | GND |
| MLX90614 | SDA | A4 |
| MLX90614 | SCL | A5 |
| Distance | rouge | 5V |
| Distance | noir | GND |
| Distance | jaune | A0 |

La résistance 10 kΩ se place entre la patte 1 et la patte 2 du DHT22.
Attention : le MLX90614 se branche sur le 3.3V, jamais sur le 5V.

## Installation

1. Installer **Arduino IDE 2.x** (arduino.cc/en/software).
2. Dans Arduino IDE, installer les bibliothèques (Outils → Gérer les bibliothèques) :
   - DHT sensor library (Adafruit)
   - Adafruit Unified Sensor
   - Adafruit MLX90614 Library
3. Installer Python, puis dans un terminal : `py -m pip install pyserial`

## Utilisation

1. Ouvrir `smartskin_uno/smartskin_uno.ino` dans Arduino IDE.
2. Choisir **Outils → Carte → Arduino Uno** et le bon **Port**.
3. Cliquer sur **Téléverser**, puis vérifier dans le Moniteur série (115200 baud).
4. **Fermer le Moniteur série et Arduino IDE** (sinon le port est occupé).
5. Lancer le programme : `py lire_capteurs.py COM5`
   (remplacer COM5 par le port de ton Arduino).
6. Placer le visage entre 10 et 30 cm du capteur de distance :
   le type de peau s'affiche.

Test sans matériel : `py lire_capteurs.py --simuler`

## Remarques

- Si `temp_peau` affiche `null`, vérifier le contact du MLX90614.
- Les mesures sont enregistrées dans `mesures_reelles.csv`
  et la dernière dans `derniere_mesure.json` (ignorés par Git).
