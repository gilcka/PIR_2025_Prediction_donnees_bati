# Rapport d'avancement - 4ème semaine

Pendant cette 4ème semaine de projet, nous tentons d'améliorer la prise en compte de la surface des bâtiments dans la prédiction, et nous nous intéressons à un nouvel attribut à prédire : le nombre de logements.

## 1. Création d'une nouvelle mesure de distance

La semaine précédente, nous avions utilisé cette formule pour calculer la "proximité" entre 2 bâtiments de centroïdes $(x_i, y_i)$ et de surface $s_i$ :
<p align="center">$d = \sqrt{(x_1 - x_2)² + (y_1 - y_2)² + (s_1 - s_2)²}$</p>

La surface est considérée comme une 3ème coordonnée dans le calcul ; or ce n'est pas le rôle de cette donnée.\
Pour qu'elle soit prise en compte de façon plus appropriée, nous avons introduit une pondération dans la formule de distance grâce à un facteur $\lambda$ compris entre 0 et 1, qui permet selon sa valeur de faire peser davantage les coordonnées géographiques ou la surface des bâtiments :
<p align="center">$d = \sqrt{\lambda[(x_1 - x_2)² + (y_1 - y_2)²] + (1 - \lambda)(s_1 - s_2)²}$</p>

En Python, l'implémentation nécessite de créer une fonction de distance personnalisée, prenant en argument 2 objets $x$, $y$ et renvoyant la distance scalaire attendue. On la renseigne ensuite lors de l'appel à la fonction KNNImputer de Scikit-Learn, avec le paramètre 'metric'.

Nous avons réalisé une série de tests pour $\lambda \in$ {0, 0.2, 0.4, 0.6, 0.8, 1}, afin d'observer pour quelle valeur l'intégration de la surface des bâtiments est la plus pertinente. Le nombre de voisins $k$ varie toujours entre 1 et 10.

Nous en avons profité pour rendre les résultats plus exploitables, en :
* limitant les histogrammes en abscisse à 60 m (les bâtiments plus hauts étant très rares et presque invisibles sur les graphiques) ;
* découpant les histogrammes en 60 intervalles pour les rendre plus précis (et étudier concrètement l'influence du facteur $\lambda$) ;
* distinguant 3 valeurs différentes de MAE selon la hauteur des bâtiments : basse (- 10 m), moyenne (10 - 30 m) et haute (+ 30 m).

On obtient les résultats suivants :

| **Histogramme réel** | ![](./img/rv4/ref.png) |
|:---------:|:---------:|

\
**1-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-30) | MAE (+30) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 7.4 | 4.0 m | 7.0 m | 22.0 m | 0.00 | ![](./img/rv4/pred_k1_lambd0.0.png) |
| **0.2** | 4.6 | 2.0 m | 4.1 m | 13.0 m | 0.50 | ![](./img/rv4/pred_k1_lambd0.2.png) |
| **0.4** | 4.5 | 1.9 m | 3.9 m | 13.2 m | 0.52 | ![](./img/rv4/pred_k1_lambd0.4.png) |
| **0.6** | 4.5 | 1.8 m | 3.8 m | 12.5 m | 0.53 | ![](./img/rv4/pred_k1_lambd0.6.png) |
| **0.8** | 4.4 | 1.8 m | 3.7 m | 12.1 m | 0.55 | ![](./img/rv4/pred_k1_lambd0.8.png) |
| **1** | 4.5 | 1.7 m | 3.7 m | 14.8 m | 0.53 | ![](./img/rv4/pred_k1_lambd1.0.png) |

\
**2-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-30) | MAE (+30) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 6.3 | 3.3 m | 6.2 m | 21.4 m | 0.08 | ![](./img/rv4/pred_k2_lambd0.0.png) |
| **0.2** | 4.1 | 1.8 m | 3.7 m | 13.7 m | 0.61 | ![](./img/rv4/pred_k2_lambd0.2.png) |
| **0.4** | 4.0 | 1.8 m | 3.6 m | 13.0 m | 0.63 | ![](./img/rv4/pred_k2_lambd0.4.png) |
| **0.6** | 3.9 | 1.7 m | 3.5 m | 12.6 m | 0.64 | ![](./img/rv4/pred_k2_lambd0.6.png) |
| **0.8** | 3.9 | 1.7 m | 3.4 m | 12.5 m | 0.64 | ![](./img/rv4/pred_k2_lambd0.8.png) |
| **1** | 4.1 | 1.7 m | 3.5 m | 15.1 m | 0.61 | ![](./img/rv4/pred_k2_lambd1.0.png) |

\
**3-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-30) | MAE (+30) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 5.8 | 3.1 m | 5.9 m | 20.9 m | 0.20 | ![](./img/rv4/pred_k3_lambd0.0.png) |
| **0.2** | 3.9 | 1.8 m | 3.6 m | 14.0 m | 0.64 | ![](./img/rv4/pred_k3_lambd0.2.png) |
| **0.4** | 3.9 | 1.7 m | 3.5 m | 13.5 m | 0.65 | ![](./img/rv4/pred_k3_lambd0.4.png) |
| **0.6** | 3.8 | 1.7 m | 3.4 m | 13.3 m | 0.66 | ![](./img/rv4/pred_k3_lambd0.6.png) |
| **0.8** | 3.8 | 1.6 m | 3.4 m | 13.5 m | 0.67 | ![](./img/rv4/pred_k3_lambd0.8.png) |
| **1** | 4.0 | 1.7 m | 3.5 m | 16.2 m | 0.63 | ![](./img/rv4/pred_k3_lambd1.0.png) |

\
**4-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-30) | MAE (+30) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 5.6 | 2.8 m | 5.8 m | 21.0 m | 0.26 | ![](./img/rv4/pred_k4_lambd0.0.png) |
| **0.2** | 3.9 | 1.7 m | 3.5 m | 14.3 m | 0.65 | ![](./img/rv4/pred_k4_lambd0.2.png) |
| **0.4** | 3.8 | 1.7 m | 3.4 m | 14.1 m | 0.66 | ![](./img/rv4/pred_k4_lambd0.4.png) |
| **0.6** | 3.8 | 1.7 m | 3.4 m | 13.8 m | 0.67 | ![](./img/rv4/pred_k4_lambd0.6.png) |
| **0.8** | 3.7 | 1.6 m | 3.3 m | 14.1 m | 0.67 | ![](./img/rv4/pred_k4_lambd0.8.png) |
| **1** | 4.0 | 1.7 m | 3.5 m | 16.7 m | 0.63 | ![](./img/rv4/pred_k4_lambd1.0.png) |

\
**5-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-30) | MAE (+30) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 5.5 | 2.8 m | 5.7 m | 21.1 m | 0.29 | ![](./img/rv4/pred_k5_lambd0.0.png) |
| **0.2** | 3.8 | 1.7 m | 3.5 m | 14.7 m | 0.66 | ![](./img/rv4/pred_k5_lambd0.2.png) |
| **0.4** | 3.8 | 1.7 m | 3.4 m | 14.5 m | 0.67 | ![](./img/rv4/pred_k5_lambd0.4.png) |
| **0.6** | 3.7 | 1.7 m | 3.4 m | 14.4 m | 0.67 | ![](./img/rv4/pred_k5_lambd0.6.png) |
| **0.8** | 3.7 | 1.6 m | 3.3 m | 14.7 m | 0.68 | ![](./img/rv4/pred_k5_lambd0.8.png) |
| **1** |  |  |  |  |  |  |
