# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import geopandas as gpd
import matplotlib.pyplot as plt

shp_file = "BDTOPO_3-5_TOUSTHEMES_SHP_LAMB93_D075_2025-06-15/BDTOPO/1_DONNEES_LIVRAISON_2025-06-00363/BDT_3-5_SHP_LAMB93_D075_ED2025-06-15/BATI/BATIMENT.shp"
BD_Paris = gpd.read_file(shp_file)

query = "USAGE1 == 'Résidentiel'"
bat_resi = BD_Paris.query(query)

nb_bat_resi = len(bat_resi)

param_interet = ["NB_LOGTS", "NB_ETAGES", "MAT_MURS", "MAT_TOITS", "HAUTEUR"]
nb_param_null = []
param_null_norm = []

for param in param_interet :
    nb_null = bat_resi[bat_resi[f'{param}'].isnull()]
    nb_param_null.append(len(nb_null))
    param_null_norm.append(len(nb_null)/nb_bat_resi)

plt.figure()
plt.bar(param_interet, nb_param_null)
plt.title("Fréquence d'apparition de données manquantes")

plt.figure()
plt.bar(param_interet, param_null_norm)
plt.title("Pourcentage d'apparition de données manquantes")
plt.plot()