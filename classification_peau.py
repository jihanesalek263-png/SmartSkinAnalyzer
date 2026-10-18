"""
SmartSkinAnalyzer - Classification du type de peau (version 3 capteurs)
------------------------------------------------------------------------
Entrées :
    distance_cm : distance visage <-> capteur (Sharp IR)
    temperature : température de la peau en °C (MLX90614)
    humidite    : humidité en % (DHT22)

classifier_peau(temperature, humidite) garde la même signature qu'avant,
donc generer_dataset.py et tester_classification.py continuent de marcher.

NB : les seuils ci-dessous ont été retrouvés à partir de dataset_peau.csv
(100 % de correspondance). Si ton ancien classification_peau.py avait
d'autres seuils, remets-les dans classifier_peau().
"""

# Zone de distance où la mesure infrarouge est fiable :
# trop loin, le MLX90614 voit aussi le décor derrière le visage
# (température sous-estimée) ; le Sharp GP2Y0A21 ne lit pas sous ~10 cm.
DISTANCE_MIN_CM = 10.0
DISTANCE_MAX_CM = 30.0


def classifier_peau(temperature: float, humidite: float) -> str:
    """Retourne : 'seche', 'normale', 'mixte' ou 'grasse'."""
    if humidite < 30:
        return "seche"
    if temperature > 34:
        return "grasse" if humidite > 60 else "mixte"
    if temperature < 31 and humidite <= 60:
        return "mixte"
    return "normale"


def distance_valide(distance_cm) -> bool:
    return distance_cm is not None and DISTANCE_MIN_CM <= distance_cm <= DISTANCE_MAX_CM


def classifier_mesure(distance_cm, temperature, humidite):
    """Version complète avec les 3 capteurs.
    Retourne (type_peau, message). type_peau vaut None si la mesure est invalide."""
    if temperature is None or humidite is None:
        return None, "Capteur illisible (valeur manquante)"
    if distance_cm is None:
        return None, "Aucun visage détecté devant le capteur de distance"
    if distance_cm < DISTANCE_MIN_CM:
        return None, f"Trop près ({distance_cm:.0f} cm) : recule un peu"
    if distance_cm > DISTANCE_MAX_CM:
        return None, f"Trop loin ({distance_cm:.0f} cm) : approche-toi"
    return classifier_peau(temperature, humidite), "OK"
