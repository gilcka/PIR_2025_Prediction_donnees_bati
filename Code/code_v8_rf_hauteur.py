import numpy as np
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from code_v7_rf_rename import rename

shp_file = "couches/quimper/bati_complet_quimper.shp"
BD_complet = gpd.read_file(shp_file)
for i in range(len(BD_complet)):
    if np.isnan(BD_complet.loc[i, 'HAUTEUR']):
        BD_complet = BD_complet.drop(i, axis=0)
# Construction des centroïdes
BD_complet['X'] = BD_complet['geometry'].centroid.x
BD_complet['Y'] = BD_complet['geometry'].centroid.y
# Calcul de la surface
BD_complet['SURFACE'] = BD_complet['geometry'].area
# Calcul des plus proches voisins
n_voisins = 6
lst_id = np.array(BD_complet['ID'])
lst_coords = np.array(BD_complet[['X', 'Y']])
neigh = NearestNeighbors(n_neighbors=n_voisins)
neigh.fit(lst_coords)
nn_dist, nn_id = neigh.kneighbors(lst_coords, return_distance=True)
index = pd.DataFrame(np.array(BD_complet.index).reshape(len(BD_complet), 1), columns = ['Index'])
BD_complet = pd.DataFrame(np.hstack((index.to_numpy(), BD_complet.to_numpy())))
print(len(BD_complet))
vect = BD_complet[['NATURE', 'USAGE1', 'LEGER', 'DATE_APP', 'SURFACE']].to_numpy()

dist = nn_dist[:, 0].reshape(len(vect), 1)
vect = np.hstack((vect, dist))

for k in range (n_voisins-1) :
    id_ = pd.DataFrame(nn_id[:, k+1], columns = ['Index'])
    df_merged = id_.merge(BD_complet, on='Index', how='inner')
    data_k = df_merged[['NATURE', 'USAGE1', 'LEGER', 'DATE_APP', 'SURFACE']].to_numpy()
    vect = np.hstack((vect, data_k)) 
    dist_k = nn_dist[:, k+1].reshape(len(vect), 1)
    vect = np.hstack((vect, dist_k))


# Copie des données utiles de la couche

# lst_X = np.array(BD_complet[["NATURE", "USAGE1", "LEGER", "DATE_APP", "s"]])
lst_Y = np.array(BD_complet[["HAUTEUR"]])
rename(vect)
BD_complet['ERR_HT'] = None

# Préparation des jeux de données
N = len(vect) # nombre total de bâtiments


full_MAE_tot = []     
X_train, X_test, Y_train, Y_test, id_train, id_test = train_test_split(vect, lst_Y, lst_id, test_size = 0.2, train_size = 0.8, random_state = 42)
id_train, id_test = list(id_train), list(id_test)
N_test = len(X_test)
      

# KNN
        
## Prédiction
list_MAE_1 = []
list_MAE_2 = []
list_MAE_3 = []
list_MAE_tot = []

# lambda_values = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]

lst_pred = []
lst_reel = []
sum_MSE = 0
sum_MAE_1, sum_MAE_2, sum_MAE_3, sum_MAE_tot = 0, 0, 0, 0
N_test_1, N_test_2, N_test_3, N_test_tot = 0, 0, 0, 0
regressor = RandomForestRegressor(criterion='absolute_error')
regressor.fit(X_train, Y_train.ravel())
out = regressor.predict(X_test)
for j in range(N_test):
    val_pred = out[j]
    lst_pred.append(val_pred)
    bat_index = lst_id.index(id_test[j])
    val_reel = lst_Y[bat_index][0]
    lst_reel.append(val_reel)
    BD_complet.loc[bat_index, 'ERR_HT'] = np.abs(val_pred - val_reel) # ajout dans la couche
    # print(id_test[j], '| Préd :', val_pred, '| Réel :', val_reel)
    sum_MSE += (val_pred - val_reel) ** 2
    if val_reel <= 10:
        sum_MAE_1 += np.abs(val_pred - val_reel)
        N_test_1 += 1
    elif val_reel > 10 and val_reel < 30:
        sum_MAE_2 += np.abs(val_pred - val_reel)
        N_test_2 += 1
    elif val_reel > 30:
        sum_MAE_3 += np.abs(val_pred - val_reel)
        N_test_3 += 1
    sum_MAE_tot += np.abs(val_pred - val_reel)
    N_test_tot += 1
    
## Erreurs
# print(str(5) + "-NN" + "\t\tLambda : " + str(lambda_val))
RMSE = np.sqrt(sum_MSE / N_test)
print(f"RMSE :\t\t\t{RMSE:.2f}")
if N_test_1 != 0 :
    MAE_1 = sum_MAE_1 / N_test_1
    list_MAE_1.append(MAE_1)
    print(f"MAE (-10 m) :\t{MAE_1:.2f} m")
if N_test_2 != 0 :
    MAE_2 = sum_MAE_2 / N_test_2
    list_MAE_2.append(MAE_2)
    print(f"MAE (10-30 m) :\t{MAE_2:.2f} m")
if N_test_3 != 0 :
    MAE_3 = sum_MAE_3 / N_test_3
    list_MAE_3.append(MAE_3)
    print(f"MAE (+30 m) :\t{MAE_3:.2f} m")

MAE_tot = sum_MAE_tot / N_test_tot
R2 = r2_score(lst_reel, lst_pred)
print(f"MAE : {MAE_tot:.2f} m")
print(f"R2 : {R2:.2f}")
print("")

BD_complet.to_file("rf_quimper_err_hauteur.gpkg") # export GPKG

plt.figure()
plt.hist(lst_reel, color='g', bins=[i for i in range(30)], edgecolor='k', alpha=0.8, label="Réalité")
plt.hist(lst_pred, bins=[i for i in range(30)], edgecolor='k', alpha=0.8, label="Prédiction")
plt.yscale('log')
plt.title("Prédiction de l'attribut HAUTEUR à Quimper (résidentiel)")
plt.xlabel("Hauteur (m)")
plt.ylabel("Fréquence")
plt.grid()
plt.legend(loc='best')
plt.savefig("plot.png")