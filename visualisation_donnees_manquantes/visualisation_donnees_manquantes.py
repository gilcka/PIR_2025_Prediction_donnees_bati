import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt


shp_file = "BDTOPO_3-5_TOUSTHEMES_SHP_LAMB93_D075_2025-06-15/BDTOPO/1_DONNEES_LIVRAISON_2025-06-00363/BDT_3-5_SHP_LAMB93_D075_ED2025-06-15/BATI/BATIMENT.shp"
BD_Paris = gpd.read_file(shp_file)
natures_bat = ['Agricole', 'Annexe', 'Commercial et services', 'Indifférencié', 'Industriel', 'Religieux', 'Résidentiel', 'Sportif']
param_interet = ["NB_LOGTS", "NB_ETAGES", "MAT_MURS", "MAT_TOITS", "HAUTEUR"]

# Extraction des bâtiments par catégorie
nb_bat_par_categorie = []
nb_bat_ok_par_categorie = []
nb_bat_ok_par_categorie_norm = []
for nat in natures_bat:
    bat_nat = BD_Paris.query(f"USAGE1 == '{nat}'")
    nb_tot = len(bat_nat)
    if nat == 'Résidentiel': # cas particulier des bâtiments résidentiels : valeur 0 équivaut à NULL
        bat_complet = bat_nat[(bat_nat["NB_LOGTS"].notnull()) & (bat_nat["NB_LOGTS"] != 0) & (bat_nat["NB_ETAGES"].notnull()) & (bat_nat["NB_ETAGES"] != 0) & (bat_nat["MAT_MURS"].notnull()) & (bat_nat["MAT_TOITS"].notnull()) & (bat_nat["HAUTEUR"].notnull()) & (bat_nat["HAUTEUR"] != 0)]
    else:
        bat_complet = bat_nat[(bat_nat["NB_LOGTS"].notnull()) & (bat_nat["NB_ETAGES"].notnull()) & (bat_nat["MAT_MURS"].notnull()) & (bat_nat["MAT_TOITS"].notnull()) & (bat_nat["HAUTEUR"].notnull())]
    nb_complet = len(bat_complet)
    nb_bat_par_categorie.append(nb_tot)
    nb_bat_ok_par_categorie.append(nb_complet)
    nb_bat_ok_par_categorie_norm.append(nb_complet / nb_tot * 100) # pourcentage
    
# Focus sur les bâtiments résidentiels
bat_resi = BD_Paris.query("USAGE1 == 'Résidentiel'")
nb_resi_ok = []
resi_ok_norm = []
for param in param_interet:
    if param == "NB_LOGTS" or param == "NB_ETAGES" or param == "HAUTEUR": # valeur 0 équivaut à NULL
        resi_null = bat_resi[(bat_resi[f'{param}'].isnull()) | (bat_resi[f'{param}'] == 0)] # bâtiments où le paramètre est manquant
    else:
        resi_null = bat_resi[(bat_resi[f'{param}'].isnull())]
    nb_resi_ok.append(nb_bat_par_categorie[6] - len(resi_null)) # nb bâtiments avec paramètre renseigné
    resi_ok_norm.append((nb_bat_par_categorie[6] -len(resi_null)) / nb_bat_par_categorie[6] * 100) # pourcentage de bâtiments avec paramètre renseigné
    

# Nombre d'attributs manquants pour chaque bâtiment résidentiel
bat_resi_array = np.array(bat_resi)
nb_i_manquants = [0 for i in range(6)] # contient le nombre de bâtiments avec i données manquantes (i = indice)
for bat in bat_resi_array:
    nb_donnees_manquantes = 0
    if bat[16] == None or not bat[16] > 0: # NB_LOGTS
        nb_donnees_manquantes += 1
    if bat[17] == None or not bat[17] > 0: # NB_ETAGES
        nb_donnees_manquantes += 1
    if bat[18] == None: # MAT_MURS
        nb_donnees_manquantes += 1
    if bat[19] == None: # MAT_TOITS
        nb_donnees_manquantes += 1
    if bat[20] == None or not bat[20] > 0: # HAUTEUR
        nb_donnees_manquantes += 1
    nb_i_manquants[nb_donnees_manquantes] += 1
    
i_manquants_norm = [] # contient la même information sous forme de pourcentage
for val in nb_i_manquants:
    i_manquants_norm.append(val / nb_bat_par_categorie[6] * 100)

    
# Affichages graphiques
plt.figure()
plt.barh(natures_bat, nb_bat_ok_par_categorie)
plt.title("Fréquence de bâtiments bien renseignés par catégorie")
plt.plot()

plt.figure()
plt.barh(natures_bat, nb_bat_ok_par_categorie_norm)
plt.title("Pourcentage de bâtiments bien renseignés par catégorie")
plt.plot()

plt.figure()
plt.bar(param_interet, nb_resi_ok)
plt.title("Fréquence d'apparition de données bien renseignées (Résidentiel)")

plt.figure()
plt.bar(param_interet, resi_ok_norm)
plt.title("Pourcentage d'apparition de données bien renseignées (Résidentiel)")
plt.plot()

plt.figure()
plt.bar(range(6), nb_i_manquants)
plt.title("Nombre de données manquantes sur les bâtiments résidentiels (fréquence)")
plt.xlabel("Nombre de critères manquants")
plt.ylabel("Nombre de bâtiments")
plt.plot()

plt.figure()
plt.bar(range(6), i_manquants_norm)
plt.title("Nombre de données manquantes sur les bâtiments résidentiels (pourcentage)")
plt.xlabel("Nombre de critères manquants")
plt.ylabel("% de bâtiments")
plt.plot()