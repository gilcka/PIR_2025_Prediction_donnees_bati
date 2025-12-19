import copy
import random as rd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


shp_file = "couches/paris/bati_total_paris.gpkg"
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

# Copie des données utiles de la couche
lst_id = list(BD_complet["ID"])
lst_data = np.array(BD_complet[["X", "Y", "SURFACE", "HAUTEUR"]])

# Préparation des jeux de données
N = len(lst_data) # nombre total de bâtiments

seeds = [42, 87, 15, 23, 66]
full_MAE_tot = []
for s in seeds:       
    lst_train, lst_test, id_train, id_test = train_test_split(lst_data, lst_id, test_size = 0.2, train_size = 0.8, random_state = s)
    lst_train, lst_test, id_train, id_test = list(lst_train), list(lst_test), list(id_train), list(id_test)
    for l in lst_test:
        l[-1] = np.nan # suppression des valeurs à prédire
     
    N_test = len(lst_test)
    lst_local = copy.deepcopy(lst_train) # jeu à imputer
          
    
    # KNN
            
    def custom_distance(x, y, missing_values = np.nan):
        x1, y1, s1 = x[0], x[1], x[2]
        x2, y2, s2 = y[0], y[1], y[2]
        return np.sqrt( lambda_val * ((x1-x2)**2 + (y1-y2)**2) + (1-lambda_val) * (s1-s2)**2 )
    
    
    ## Prédiction
    list_MAE_1 = []
    list_MAE_2 = []
    list_MAE_3 = []
    list_MAE_tot = []
    
    lambda_values = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
    
    for lambda_val in lambda_values :
        lst_pred = []
        lst_reel = []
        sum_MSE = 0
        sum_MAE_1, sum_MAE_2, sum_MAE_3, sum_MAE_tot = 0, 0, 0, 0
        N_test_1, N_test_2, N_test_3, N_test_tot = 0, 0, 0, 0
        for j in range(N_test):
            lst_local.append(list(lst_test[j]))
            imputer = KNNImputer(n_neighbors=6, weights="uniform", metric=custom_distance)
            lst_out = imputer.fit_transform(lst_local)
            val_pred = lst_out[-1][-1]
            lst_pred.append(val_pred)
            bat_index = lst_id.index(id_test[j])
            val_reel = lst_data[bat_index][-1]
            lst_reel.append(val_reel)
            # print(id_test[j], '| Préd :', val_pred, '| Réel :', val_reel)
            lst_local.pop()
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
        print(str(5) + "-NN" + "\t\tLambda : " + str(lambda_val))
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
        list_MAE_tot.append(MAE_tot)
        full_MAE_tot.append(list_MAE_tot)
        
        R2 = r2_score(lst_reel, lst_pred)
        print(f"R2 :\t\t\t\t{R2:.2f}")
        print("")

      
list_MAE_tot_m = np.mean( np.array(full_MAE_tot), axis=0 )
list_MAE_tot_s = np.std( np.array(full_MAE_tot), axis=0 )

min_MAE = min(list_MAE_tot_m)
index_min_MAE = list(list_MAE_tot_m).index(min_MAE)
lambda_min = lambda_values[index_min_MAE]

# À adapter en fonction du cas
plt.figure()
plt.errorbar(lambda_values, list_MAE_tot_m, yerr=list_MAE_tot_s, color = "b", lw=2, label='Courbe moyenne')
plt.hlines(min_MAE, 0, 1, color = "r", linestyles = 'dashed')
plt.vlines(lambda_min, 0.9, min_MAE, color = "r", linestyles = 'dotted')

plt.text(0, min_MAE, f'{min_MAE:.2f}', 
         color='red', fontsize=10, fontweight='bold',
         verticalalignment='bottom', horizontalalignment='right')
plt.text(lambda_min, 0.9, f'{lambda_min:.2f}', 
         color='red', fontsize=10, fontweight='bold',
         verticalalignment='bottom', horizontalalignment='right')

plt.xlim((0,1))
plt.ylim((0.9, 1.6))

plt.title("Estimation du Lambda optimal (k = 5)")
plt.xlabel("Lambda")
plt.ylabel("MAE (m)")
plt.legend(loc='best')
plt.grid()
plt.show()
