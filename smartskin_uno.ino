/*
  SmartSkinAnalyzer - Firmware ARDUINO UNO
  -----------------------------------------
  3 capteurs :
    - MLX90614 (température infrarouge de la peau, sans contact) -> I2C (A4 / A5)
    - DHT22    (humidité + température de l'air)                 -> broche D2
    - Sharp IR (distance visage <-> capteur)                     -> broche A0

  Envoie une ligne JSON toutes les 2 secondes sur le port série (115200 bauds).
  Exemple :
  {"distance_cm":18.3,"temp_peau":33.4,"temp_air":24.1,"humidite":46.2}
  (une valeur illisible est envoyée en null)

  BRANCHEMENTS (Arduino UNO) :
    MLX90614 : VIN -> 5V | GND -> GND | SDA -> A4 | SCL -> A5
    DHT22    : pin 1 (VCC) -> 5V | pin 2 (DATA) -> D2 | pin 4 (GND) -> GND
               + résistance 10 kΩ entre VCC et DATA (si ton DHT22 a 4 pattes nues)
    Sharp IR : rouge -> 5V | noir -> GND | jaune -> A0

  Fonctionne avec le même lire_capteurs.py que pour l'ESP32.
*/

#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include "DHT.h"

#define PIN_DHT    2
#define PIN_SHARP  A0
#define DHTTYPE    DHT22

DHT dht(PIN_DHT, DHTTYPE);
Adafruit_MLX90614 mlx = Adafruit_MLX90614();
bool mlxOk = false;

// Distance en cm avec un Sharp GP2Y0A21 (portée 10-80 cm).
// Si ton capteur est un autre modèle, la formule change : on la règle au test.
float lireDistanceCm() {
  long somme = 0;
  for (int i = 0; i < 10; i++) {            // moyenne de 10 mesures (réduit le bruit)
    somme += analogRead(PIN_SHARP);
    delay(5);
  }
  float volts = (somme / 10.0) * 5.0 / 1023.0;
  if (volts < 0.4) return NAN;               // rien devant le capteur / trop loin
  return 29.988 * pow(volts, -1.173);
}

void afficherValeur(const char* nom, float v, bool dernier = false) {
  Serial.print("\""); Serial.print(nom); Serial.print("\":");
  if (isnan(v)) Serial.print("null");
  else Serial.print(v, 1);
  if (!dernier) Serial.print(",");
}

void setup() {
  Serial.begin(115200);
  delay(500);
  dht.begin();
  mlxOk = mlx.begin();
  if (!mlxOk) {
    Serial.println("{\"erreur\":\"MLX90614 non detecte (verifie SDA/SCL/alim)\"}");
  }
}

void loop() {
  float distance = lireDistanceCm();
  float tempPeau = mlxOk ? mlx.readObjectTempC() : NAN;
  float tempAir  = dht.readTemperature();
  float humidite = dht.readHumidity();

  Serial.print("{");
  afficherValeur("distance_cm", distance);
  afficherValeur("temp_peau", tempPeau);
  afficherValeur("temp_air", tempAir);
  afficherValeur("humidite", humidite, true);
  Serial.println("}");

  delay(2000);   // le DHT22 ne peut pas être lu plus vite que toutes les 2 s
}
