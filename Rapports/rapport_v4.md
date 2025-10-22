# Rapport d'avancement - 4ème semaine

Pendant cette 4ème semaine de projet, nous tentons d'améliorer la prise en compte de la surface des bâtiments dans la prédiction, et nous nous intéressons à un nouvel attribut à prédire : le nombre de logements.

## 1. Création d'une nouvelle mesure de distance

La semaine précédente, nous avions utilisé cette formule pour calculer la "proximité" entre 2 bâtiments de centroïdes $(x_i, y_i)$ et de surface $s_i$ :
<p align="center">$d = \sqrt{(x_1 - x_2)² + (y_1 - y_2)² + (s_1 - s_2)²}$</p>

La surface est considérée comme une 3ème coordonnée dans le calcul ; or ce n'est pas le rôle de cette donnée.\
Pour qu'elle soit prise en compte de façon plus appropriée, nous avons introduit une pondération dans la formule de distance grâce à un facteur $\lambda$ compris entre 0 et 1, qui permet selon sa valeur de faire peser davantage les coordonnées géographiques ou la surface des bâtiments :
<p align="center">$d = \sqrt{\lambda[(x_1 - x_2)² + (y_1 - y_2)²] + (1 - \lambda)(s_1 - s_2)²}$</p>

Nous avons réalisé une série de tests pour $\lambda \in$ {0, 0.2, 0.4, 0.6, 0.8, 1}, afin d'observer comment l'intégration de la surface des bâtiments est la plus pertinente. Le nombre de voisins $k$ varie toujours entre 1 et 10.

Nous en avons profité pour rendre les résultats plus exploitables, en :
* limitant les histogrammes en abscisse à 60 m (les bâtiments plus hauts étant très rares et presque invisibles sur les graphiques) ;
* découpant les histogrammes en 60 intervalles pour les rendre plus précis (et étudier concrètement l'influence du facteur $\lambda$) ;
* distinguant 3 valeurs différentes de MAE selon la hauteur des bâtiments : basse (- 10 m), moyenne (10 - 30 m) et haute (+ 30 m).

On obtient les résultats suivants :

**1-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-30) | MAE (+30) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 7.4 | 4.0 | 7.0 | 22.0 | 0.00 |
| **0.2** | 4.6 | 2.0 | 4.1 | 13.0 | 0.50 |
| **0.4** | 4.5 | 1.9 | 3.9 | 13.2 | 0.52 |
| **0.6** | 4.5 | 1.8 | 3.8 | 12.5 | 0.53 |
| **0.8** | 4.4 | 1.8 | 3.7 | 12.1 | 0.55 |
| **1** | 4.5 | 1.7 | 3.7 | 14.8 | 0.53 |

\
**2-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-30) | MAE (+30) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 6.3 | 3.3 | 6.2 | 21.4 | 0.08 |
| **0.2** | 4.1 | 1.8 | 3.7 | 13.7 | 0.61 |
| **0.4** | 4.0 | 1.8 | 3.6 | 13.0 | 0.63 |
| **0.6** | 3.9 | 1.7 | 3.5 | 12.6 | 0.64 |
| **0.8** | 3.9 | 1.7 | 3.4 | 12.5 | 0.64 |
| **1** | 4.1 | 1.7 | 3.5 | 15.1 | 0.61 |

