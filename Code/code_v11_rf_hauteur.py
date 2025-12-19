import numpy as np
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import OneHotEncoder

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
lst_X = np.array(BD_complet[["NATURE", "USAGE1", "LEGER", "DATE_APP", "SURFACE"]])

columns_final = []

# Encodage one hot
enc = OneHotEncoder(handle_unknown='ignore')
nat = lst_X[:, 0].reshape(len(lst_X), 1)
enc_nat_out = enc.fit_transform(nat).toarray()
feature_names = enc.get_feature_names_out()
for i in range(len(feature_names)):
    columns_final.append('NATURE' + feature_names[i][2:])

us1 = lst_X[:, 1].reshape(len(lst_X), 1)
enc_us1_out = enc.fit_transform(us1).toarray()
feature_names = enc.get_feature_names_out()
for i in range(len(feature_names)):
    columns_final.append('USAGE1' + feature_names[i][2:])

leg = lst_X[:, 2].reshape(len(lst_X), 1)
enc_leg_out = enc.fit_transform(leg).toarray()
feature_names = enc.get_feature_names_out()
for i in range(len(feature_names)):
    columns_final.append('LEGER' + feature_names[i][2:])

vect = np.hstack((enc_nat_out, enc_us1_out, enc_leg_out, lst_X[:, 3:]))

# Modification format DATE_APP
for l in vect:
    date_app = l[-2]
    if date_app != None:
        l[-2] = int(date_app[0:4])
    else:
        l[-2] = 0
        
columns_final += ['DATE_APP', 'SURFACE']

lst_Y = np.array(BD_complet[["HAUTEUR"]])
BD_complet['ERR_HT'] = np.nan

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

BD_complet.to_file("rf_paris_err_hauteur.gpkg") # export GPKG

plt.figure()
plt.hist(lst_reel, color='g', bins=[i for i in range(110)], edgecolor='k', alpha=0.7, label="Réalité")
plt.hist(lst_pred, bins=[i for i in range(110)], edgecolor='k', alpha=0.7, label="Prédiction")
plt.yscale('log')
plt.title("Prédiction de l'attribut HAUTEUR à Paris")
plt.xlabel("Hauteur (m)")
plt.ylabel("Fréquence")
plt.grid()
plt.legend(loc='best')
plt.savefig("plot.png")

plt.figure().set_figwidth(10)
importances = regressor.feature_importances_
std = np.std([tree.feature_importances_ for tree in regressor.estimators_], axis=0)
forest_importances = pd.Series(importances, index=columns_final)

# Moyennage entre voisins
attributs = {}
for a in range(len(forest_importances)):
    att = columns_final[a]
    if att == 'NATURE_Arène ou théâtre antique': # simplification des noms
        att = 'NATURE_Arène'
    elif att == 'NATURE_Fort, blockhaus, casemate':
        att = 'NATURE_Fort'
    elif att == 'NATURE_Industriel, agricole ou commercial':
        att = 'NATURE_Indus, agri, commerce'
    elif att == 'USAGE1_Commercial et services':
        att = 'USAGE1_Commerce, services'
    if att in attributs.keys():
        attributs[att].append((importances[a], std[a]))
    else:
        attributs[att] = [(importances[a], std[a])]
lst_att = list(attributs.keys())
lst_att.sort()
importances_tot, std_tot = [], []

for att in lst_att:
    sum_imp_a, sum_std_a = 0, 0
    for i in range(len(attributs[att])):
        imp_i, std_i = attributs[att][i]
        sum_imp_a += imp_i
        sum_std_a += std_i
    importances_tot.append(sum_imp_a)
    std_tot.append(sum_std_a)

for k in range(len(importances_tot)-1) :
    i_min = k
    for i in range(k+1, len(importances_tot)) :
        if importances_tot[i] < importances_tot[i_min] :
            i_min = i
    importances_tot[k], importances_tot[i_min] = importances_tot[i_min], importances_tot[k]
    lst_att[k], lst_att[i_min] = lst_att[i_min], lst_att[k]
    std_tot[k], std_tot[i_min] = std_tot[i_min], std_tot[k]
       
fig, ax = plt.subplots(figsize=(8, 0.25 * len(lst_att)))
ax.barh(lst_att, importances_tot, xerr=std_tot)
ax.set_title("Importance des attributs (MDI)")
ax.set_xlabel("MDI")
fig.tight_layout()