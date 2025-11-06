import copy
import random as rd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


shp_file = "couches/quimper/bat_resi_complet_svxy_quimper.shp"
BD_complet = gpd.read_file(shp_file)

# Copie des données utiles de la couche
lst_id = list(BD_complet["ID"])
lst_data = np.array(BD_complet[["x", "y", "s", "v", "NB_LOGTS"]])

# Préparation des jeux de données
N = len(lst_data) # nombre total de bâtiments
"""id_test, lst_train, lst_test = [],  [], []
for i in range(N):
    nb = rd.random()
    if nb > 0.8: # 20% de proba d'être dans le jeu de test
        id_test.append(lst_id[i])
        lst_test.append( list(lst_data[i]) )
        lst_test[-1][-1] = np.nan # suppression du paramètre NB_LOGTS à prédire
    else: # 80% de proba d'être dans le jeu d'entraînement
        lst_train.append( list(lst_data[i]) )"""
        
lst_train, lst_test, id_train, id_test = train_test_split(lst_data, lst_id, test_size = 0.02, train_size = 0.98, random_state = 42)
lst_train, lst_test, id_train, id_test = list(lst_train), list(lst_test), list(id_train), list(id_test)
for l in lst_test:
    l[-1] = np.nan # suppression des valeurs à prédire
 
N_test = len(lst_test)
lst_local = copy.deepcopy(lst_train) # jeu à imputer
      
    
# KNN
        
def custom_distance(x, y, missing_values = np.nan):
    x1, y1, v1 = x[0], x[1], x[3]
    x2, y2, v2 = y[0], y[1], y[3]
    return np.sqrt( lambda_val * ((x1-x2)**2 + (y1-y2)**2) + (1-lambda_val) * (v1-v2)**2 )


## Prédiction
list_MAE_1 = []
list_MAE_2 = []
list_MAE_3 = []
list_MAE_tot = []

lambda_values = [0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]

for lambda_val in lambda_values :
    lst_pred = []
    lst_reel = []
    sum_MSE = 0
    sum_MAE_1, sum_MAE_2, sum_MAE_3, sum_MAE_tot = 0, 0, 0, 0
    N_test_1, N_test_2, N_test_3, N_test_tot = 0, 0, 0, 0
    for j in range(N_test):
        lst_local.append(list(lst_test[j]))
        imputer = KNNImputer(n_neighbors=5, weights="uniform", metric=custom_distance)
        lst_out = imputer.fit_transform(lst_local)
        val_pred = np.round(lst_out[-1][-1])
        lst_pred.append(val_pred)
        bat_index = lst_id.index(id_test[j])
        val_reel = lst_data[bat_index][-1]
        lst_reel.append(val_reel)
        # print(id_test[j], '| Préd :', val_pred, '| Réel :', val_reel)
        lst_local.pop()
        sum_MSE += (val_pred - val_reel) ** 2
        if val_reel <= 1:
            sum_MAE_1 += np.abs(val_pred - val_reel)
            N_test_1 += 1
        elif val_reel > 1 and val_reel < 100:
            sum_MAE_2 += np.abs(val_pred - val_reel)
            N_test_2 += 1
        elif val_reel > 100:
            sum_MAE_3 += np.abs(val_pred - val_reel)
            N_test_3 += 1
        sum_MAE_tot += np.abs(val_pred - val_reel)
        N_test_tot += 1
        
    ## Erreurs
    print(str(5) + "-NN" + "\t\tLambda : " + str(lambda_val))
    RMSE = np.sqrt(sum_MSE / N_test)
    print(f"RMSE :\t\t\t\t{RMSE:.2f}")
    if N_test_1 != 0 :
        MAE_1 = sum_MAE_1 / N_test_1
        list_MAE_1.append(MAE_1)
        print(f"MAE (0-1 logts) :\t\t{MAE_1:.2f} logts")
    if N_test_2 != 0 :
        MAE_2 = sum_MAE_2 / N_test_2
        list_MAE_2.append(MAE_2)
        print(f"MAE (1-100 logts) :\t{MAE_2:.2f} logts")
    if N_test_3 != 0 :
        MAE_3 = sum_MAE_3 / N_test_3
        list_MAE_3.append(MAE_3)
        print(f"MAE (+100 logts) :\t{MAE_3:.2f} logts")
    
    MAE_tot = sum_MAE_tot / N_test_tot
    list_MAE_tot.append(MAE_tot)
    
    R2 = r2_score(lst_reel, lst_pred)
    print(f"R2 :\t\t\t\t\t{R2:.2f}")
    print("")

        
min_MAE = min(list_MAE_tot)
index_min_MAE = list_MAE_tot.index(min_MAE)
lambda_min = lambda_values[index_min_MAE]

# À adapter en fonction du cas
plt.figure()
plt.plot(lambda_values, list_MAE_tot, color = "b", lw = 2, label="Ensemble")
plt.hlines(min_MAE, 0, 1, color = "r", linestyles = 'dashed')
plt.vlines(lambda_min, 0.5, min_MAE, color = "r", linestyles = 'dotted')

plt.text(0, min_MAE, f'{min_MAE:.2f}', 
         color='red', fontsize=10, fontweight='bold',
         verticalalignment='bottom', horizontalalignment='right')
plt.text(lambda_min, 0.5, f'{lambda_min:.2f}', 
         color='red', fontsize=10, fontweight='bold',
         verticalalignment='bottom', horizontalalignment='right')

plt.xlim((0,1))
plt.ylim((0.5, 1))

plt.title("Estimation du Lambda optimal (k = 5)")
plt.xlabel("Lambda")
plt.ylabel("MAE (m)")
plt.legend(loc='best')
plt.show()
