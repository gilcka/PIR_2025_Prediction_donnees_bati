import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from rename import rename

shp_file = "couches/quimper/bat_resi_complet_svxy_quimper.shp"
BD_complet = gpd.read_file(shp_file)

# Copie des données utiles de la couche
lst_id = list(BD_complet["ID"])
lst_X = np.array(BD_complet[["NATURE", "USAGE1", "LEGER", "DATE_APP", "s"]])
lst_Y = np.array(BD_complet[["HAUTEUR"]])
rename(lst_X)

# Préparation des jeux de données
N = len(lst_X) # nombre total de bâtiments

seeds = [42, 87, 15, 23, 66]
full_MAE_tot = []
for s in seeds:       
    X_train, X_test, Y_train, Y_test, id_train, id_test = train_test_split(lst_X, lst_Y, lst_id, test_size = 0.2, train_size = 0.8, random_state = s)
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
    list_MAE_tot.append(MAE_tot)
    full_MAE_tot.append(list_MAE_tot)
    
    R2 = r2_score(lst_reel, lst_pred)
    print(f"R2 :\t\t\t\t{R2:.2f}")
    print("")


list_MAE_tot_m = np.mean( np.array(full_MAE_tot), axis=0 )
list_MAE_tot_s = np.std( np.array(full_MAE_tot), axis=0 )

print(list_MAE_tot_m)
"""
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
"""