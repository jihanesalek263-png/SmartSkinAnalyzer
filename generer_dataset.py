"""
SmartSkinAnalyzer - Génération d'un dataset synthétique
---------------------------------------------------------
Sert à tester ton code de classification (classification_peau.py)
avant d'avoir de vraies données capteur.

Génère un fichier CSV avec des lignes :
    temperature, humidite, type_peau

Le type_peau est calculé automatiquement à partir des mêmes règles
que ton classifieur (donc ce dataset "colle" parfaitement à ta logique).
Une fois que tu auras de vraies mesures, remplace ce fichier par tes
données réelles et compare les résultats.
"""

import csv
import random

from classification_peau import classifier_peau


def generer_dataset(nb_lignes: int = 200, nom_fichier: str = "dataset_peau.csv"):
    """Génère un CSV de nb_lignes mesures température/humidité + label."""

    with open(nom_fichier, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["temperature", "humidite", "type_peau"])

        for _ in range(nb_lignes):
            # Températures réalistes de peau : 28°C à 37°C
            temperature = round(random.uniform(28.0, 37.0), 1)
            # Humidité de peau réaliste : 10% à 80%
            humidite = round(random.uniform(10.0, 80.0), 1)

            type_peau = classifier_peau(temperature, humidite)

            writer.writerow([temperature, humidite, type_peau])

    print(f"Dataset généré : {nom_fichier} ({nb_lignes} lignes)")


def afficher_repartition(nom_fichier: str = "dataset_peau.csv"):
    """Affiche combien de lignes appartiennent à chaque type de peau,
    utile pour vérifier que ton dataset est équilibré."""

    compteur = {}
    with open(nom_fichier, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for ligne in reader:
            t = ligne["type_peau"]
            compteur[t] = compteur.get(t, 0) + 1

    print("Répartition des types de peau dans le dataset :")
    for type_peau, nb in compteur.items():
        print(f"  {type_peau} : {nb}")


if __name__ == "__main__":
    generer_dataset(nb_lignes=200)
    afficher_repartition()
