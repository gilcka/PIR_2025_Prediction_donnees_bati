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
    bat_complet = bat_nat[(bat_nat["NB_LOGTS"].notnull()) & (bat_nat["NB_ETAGES"].notnull()) & (bat_nat["MAT_MURS"].notnull()) & (bat_nat["MAT_TOITS"].notnull()) & (bat_nat["HAUTEUR"].notnull())]
    nb_complet = len(bat_complet)
    nb_bat_par_categorie.append(nb_tot)
    nb_bat_ok_par_categorie.append(nb_complet)
    nb_bat_ok_par_categorie_norm.append(nb_complet / nb_tot)
    
# Focus sur les bâtiments résidentiels
bat_resi = BD_Paris.query("USAGE1 == 'Résidentiel'")
nb_param_null = []
param_null_norm = []
for param in param_interet:
    nb_null = bat_resi[bat_resi[f'{param}'].isnull()]
    nb_param_null.append(len(nb_null))
    param_null_norm.append(len(nb_null)/nb_bat_ok_par_categorie[6])
    
      
# Affichages graphiques
plt.figure()
plt.bar(param_interet, nb_param_null_1)
plt.title("Fréquence d'apparition de données manquantes")

plt.figure()
plt.bar(param_interet, param_null_norm_1)
plt.title("Pourcentage d'apparition de données manquantes")
plt.plot()

plt.figure()
plt.barh(natures_bat, nb_bat_ok_par_categorie)
plt.title("Fréquence de bâtiments bien renseignés par catégorie")
plt.plot()

plt.figure()
plt.barh(natures_bat, nb_bat_ok_par_categorie_norm)
plt.title("Pourcentage de bâtiments bien renseignés par catégorie")
plt.plot()