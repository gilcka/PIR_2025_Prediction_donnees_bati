import numpy as np
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import OneHotEncoder

shp_file = "couches/paris-est/bati_total_paris-est.gpkg"
BD_complet = gpd.read_file(shp_file)
for i in range(len(BD_complet)):
    if np.isnan(BD_complet.loc[i, 'HAUTEUR']):
        BD_complet = BD_complet.drop(i, axis=0)
BD_complet.index = range(len(BD_complet))
# Construction des centroïdes
BD_complet['X'] = BD_complet['geometry'].centroid.x
BD_complet['Y'] = BD_complet['geometry'].centroid.y
# Calcul de la surface
BD_complet['SURFACE'] = BD_complet['geometry'].area
# Sauvegarde des noms de colonnes
BD_columns = list(BD_complet.columns)
# Calcul des plus proches voisins
n_voisins = 6
lst_id = list(BD_complet['ID'])
lst_coords = np.array(BD_complet[['X', 'Y']])
neigh = NearestNeighbors(n_neighbors=n_voisins)
neigh.fit(lst_coords)
nn_dist, nn_id = neigh.kneighbors(lst_coords, return_distance=True)
index = np.array(BD_complet.index).reshape(len(BD_complet), 1)
BD_complet = pd.DataFrame(np.hstack((index, BD_complet)), columns=['INDEX'] + BD_columns)
data_0 = np.array(BD_complet[['NATURE', 'USAGE1', 'LEGER', 'DATE_APP', 'SURFACE']])
columns_final = [] # nom des colonnes après construction du vecteur 

# Encodage one hot
enc = OneHotEncoder(handle_unknown='ignore')
vect_nat = data_0[:, 0].reshape(len(data_0), 1)
enc_nat_out = enc.fit_transform(vect_nat).toarray()
for i in range(enc_nat_out.shape[1]):
    columns_final.append(f'NATURE_{i}')

vect_us1 = data_0[:, 1].reshape(len(data_0), 1)
enc_us1_out = enc.fit_transform(vect_us1).toarray()
for i in range(enc_us1_out.shape[1]):
    columns_final.append(f'USAGE1_{i}')

vect_leg = data_0[:, 2].reshape(len(data_0), 1)
enc_leg_out = enc.fit_transform(vect_leg).toarray()
for i in range(enc_leg_out.shape[1]):
    columns_final.append(f'LEGER_{i}')

dist = nn_dist[:, 0].reshape(len(data_0), 1)
vect = np.hstack((enc_nat_out, enc_us1_out, enc_leg_out, data_0[:, 3:], dist))

# Modification format DATE_APP
for l in vect:
    date_app = l[-3]
    if date_app != None:
        l[-3] = int(date_app[0:4])
    else:
        l[-3] = 0
        
columns_final += ['DATE_APP', 'SURFACE', 'DIST']

for k in range(1, n_voisins):
    id_ = pd.DataFrame(nn_id[:, k], columns = ['INDEX'])
    df_merged = id_.merge(BD_complet, on='INDEX', how='left')
    data_k = np.array(df_merged[['NATURE', 'USAGE1', 'LEGER', 'DATE_APP', 'SURFACE']])
    
    vect_nat = data_k[:, 0].reshape(len(data_k), 1)
    enc_nat_out = enc.fit_transform(vect_nat).toarray()
    for i in range(enc_nat_out.shape[1]):
        columns_final.append(f'NATURE_{i}')
    vect_us1 = data_k[:, 1].reshape(len(data_k), 1)
    enc_us1_out = enc.fit_transform(vect_us1).toarray()
    for i in range(enc_us1_out.shape[1]):
        columns_final.append(f'USAGE1_{i}')
    vect_leg = data_k[:, 2].reshape(len(data_k), 1)
    enc_leg_out = enc.fit_transform(vect_leg).toarray()
    for i in range(enc_leg_out.shape[1]):
        columns_final.append(f'LEGER_{i}')
    
    dist_k = nn_dist[:, k].reshape(len(vect), 1)
    vect = np.hstack((vect, enc_nat_out, enc_us1_out, enc_leg_out, data_0[:, 3:], dist_k))
    
    for l in vect:
        date_app = l[-3]
        if date_app != None:
            l[-3] = int(date_app[0:4])
        else:
            l[-3] = 0
            
    columns_final += ['DATE_APP', 'SURFACE', 'DIST']

# Copie des données utiles de la couche
lst_Y = np.array(BD_complet[["HAUTEUR"]])
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
    BD_complet.loc[bat_index, 'ERR_HT'] = val_pred - val_reel # ajout dans la couche
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

BD_complet_gdf = gpd.GeoDataFrame(
    BD_complet, geometry=BD_complet.geometry, crs="EPSG:2154"
)
BD_complet_gdf.to_file("mix_paris-est_err_hauteur.gpkg") # export GPKG

plt.figure()
plt.hist(lst_reel, color='g', bins=[i for i in range(100)], edgecolor='k', alpha=0.8, label="Réalité")
plt.hist(lst_pred, bins=[i for i in range(100)], edgecolor='k', alpha=0.8, label="Prédiction")
plt.yscale('log')
plt.title("Prédiction de l'attribut HAUTEUR à Paris")
plt.xlabel("Hauteur (m)")
plt.ylabel("Fréquence")
plt.grid()
plt.legend(loc='best')
plt.savefig("plot2.png")

plt.figure()
importances = regressor.feature_importances_
std = np.std([tree.feature_importances_ for tree in regressor.estimators_], axis=0)
forest_importances = pd.Series(importances, index=columns_final)
fig, ax = plt.subplots()
forest_importances.plot.bar(yerr=std, ax=ax)
ax.set_title("Importance des attributs (MDI)")
ax.set_ylabel("MDI")
fig.tight_layout()