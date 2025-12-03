# Rapport d'avancement 9

Pendant cette semaine, nous ajustons le fonctionnement de l'algorithme KNN+RandomForest, et nous testons cette méthode de prédiction sur l'est de Paris.\
En parallèle, nous observons quelques résultats de mauvaises prédictions sur Quimper.

## 1. Ajustement de l'algorithme RandomForest+KNN

La méthode de prédiction mélangeant plus proches voisins et forêt aléatoire semblait fonctionner sur la ville de Quimper, mais l'encodage des données fournies à l'algorithme posait un problème : en remplaçant les valeurs des attributs $NATURE$ et $USAGE$ par des nombres entiers, on introduit un biais dans le fonctionnement du programme.\
En effet, $NATURE = 0$ est considéré comme plus proche de $NATURE = 1$ que $NATURE = 5$ en raison de la hiérarchie des entiers ; or en réalité ces nombres ne sont pas choisis pour classer les natures de bâtiment par ordre de similarité.\
De plus, cette méthode nécessite un processus d'encodage manuel long par le biais d'un second fichier, que l'on préférerais éviter.\
\
Pour corriger cela, on utilise la méthode ```OneHotEncoder``` du module ```sklearn.preprocessing``` qui permet de générer automatiquement, à partir d'une liste de valeurs discrètes d'un attribut, un encodage sous forme de liste binaire (0 ou 1), ce qui évite l'introduction d'un biais lié à la manière d'encoder les données, tout en rendant le code plus clair.\
Nous implémentons cette méthode pour les attributs $NATURE$, $USAGE$ et $LEGER$.\
\
Une autre amélioration que nous apportons à notre algorithme est la gestion de l'importance des attributs.\
Si notre algorithme utilise 6 attributs pour chacun des voisins afin de réaliser une prédiction, il serait intéressant de savoir lesquels sont les plus déterminants, et lesquels plus négligeables : cela permettrait éventuellement d'ajuster les attributs choisis et d'évaluer la pertinence de l'algorithme.\
\
On utilise pour cela le paramètre ```feature_importances``` du RandomForest, qui permet d'indiquer la pondération de chacun des paramètres du calcul avec l'écart-type associé.\
Nous avons tracé graphiquement cette information dans les prédictions sur Paris.

## 2. Prédiction sur Paris

Nous avons testé l'algorithme KNN+RandomForest sur l'est de Paris, en le comparant avec les résultats obtenus par K-NN et RandomForest seuls :

Voici les résultats obtenus pour la prédiction de la hauteur :

* K-NN

| Histogramme | MAE (m) |
|:-:|:-:|
| ![](./img/rv9/knn_paris_total.png) | 2.7 | 

| Détail | *-10 m* | *10-30 m* | *+30 m* |
|:-:|:-:|:-:|:-:|
| **MAE (m)** | 2.0 | 4.0 | 18.8 |

...
  
* RandomForest

| Histogramme | MAE (m) | FeatureImportances |
|:-:|:-:|:-:|
| ![](./img/rv9/rf_paris_total_2.png) | 3.8 | ![](./img/rv9/rf_paris_mdi.png) |

| Détail | *-10 m* | *10-30 m* | *+30 m* |
|:-:|:-:|:-:|:-:|
| **MAE (m)** | 2.7 | 6.2 | 23.2 |

...

* Mix **[EN COURS]**

| Histogramme | MAE (m) | FeatureImportances |
|:-:|:-:|:-:|
| ![](./img/rv9/mix_paris_total.png) | | ![](./img/rv9/mix_paris_mdi.png) |

| Détail | *-10 m* | *10-30 m* | *+30 m* |
|:-:|:-:|:-:|:-:|
| **MAE (m)** |  |  |  |
