# Rapport d'avancement - 5ème semaine

Pendant cette 5ème semaine de projet, nous nous intéressons à un nouvel attribut à prédire : le nombre de logements.

## 1. Explication du processus

Pour cette nouvelle prédiction, on prend désormais en compte les coordonnées géographiques des centroïdes, la surface des bâtiments, et on décide d'ajouter le volume. En effet, on sait d'après cette référence bibliographique [À INSÉRER] que la surface, la hauteur et le volume d'un bâtiment sont corrélés ; on se demande donc si l'ajout de cette information supplémentaire permet ou non d'améliorer la prédiction.\
Le volume des bâtiments n'étant pas fourni dans la couche de données issue de la BD TOPO, on peut ajouter simplement une estimation de cette valeur à partir de la surface $s$ et de la hauteur $h$ :

<p align="center">$v = s * h$</p>

Pour intégrer ce volume dans le calcul de distance, on décide de lui donner un poids équivalent à la surface, qui est toujours dépendante d'un paramètre $\lambda$ permettant de pondérer davantage la distance par rapport aux coordonnées géographiques $(x, y)$ ou aux surface $s$ et volume $v$, d'où la formule :

<p align="center">$d = \sqrt{\lambda[(x_1 - x_2)² + (y_1 - y_2)²] + (1 - \lambda)[(s_1 - s_2)² + (v_1 - v_2)²]}$</p>

Un autre élément important concerne le format des valeurs prédites : contrairement à la hauteur qui est réelle, le nombre de logements est nécessairement un entier naturel.\
Il est donc nécessaire de discrétiser les prédictions obtenues, ce que l'on fait en les arrondissant à l'entier le plus proche ; bien que cela ait également un impact sur la qualité de la valeur prédite.\
\
Le nombre de logements à estimer pouvant grandement varier entre une petite maison individuelle (1 logement) et un grand immeuble (plusieurs centaines de logements), on choisit là encore de répartir la MAE en 3 catégories :
* $-$ de 10 logements
* 10 à 100 logements
* $+$ de 100 logements

## 2. Résultats

On obtient les résultats suivants :

| **Histogramme réel** | ![](./img/rv5/ref.png) |
|:---------:|:---------:|

\
**1-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-100) | MAE (+100) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 10.7 | 1.3 logts | 11.6 logts | 61.0 logts | 0.50 | ![](./img/rv5/pred_k1_lambd0.0.png) |
| **0.2** | 11.0 | 1.2 logts | 10.9 logts | 61.0 logts | 0.47 | ![](./img/rv5/pred_k1_lambd0.2.png) |
| **0.4** | 10.8 | 1.2 logts | 10.7 logts | 60.0 logts | 0.49 | ![](./img/rv5/pred_k1_lambd0.4.png) |
| **0.6** | 10.8 | 1.2 logts | 10.5 logts | 61.9 logts | 0.49 | ![](./img/rv5/pred_k1_lambd0.6.png) |
| **0.8** | 10.6 | 1.1 logts | 10.5 logts | 61.0 logts | 0.50 | ![](./img/rv5/pred_k1_lambd0.8.png) |
| **1** | 13.6 | 1.8 logts | 14.2 logts | 95.2 logts | 0.19 | ![](./img/rv5/pred_k1_lambd1.0.png) |

\
**2-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-100) | MAE (+100) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 9.4 | 1.3 logts | 10.0 logts | 59.6 logts | 0.61 | ![](./img/rv5/pred_k2_lambd0.0.png) |
| **0.2** | 9.2 | 1.1 logts | 9.5 logts | 56.2 logts | 0.63 | ![](./img/rv5/pred_k2_lambd0.2.png) |
| **0.4** | 9.3 | 1.1 logts | 9.5 logts | 58.5 logts | 0.62 | ![](./img/rv5/pred_k2_lambd0.4.png) |
| **0.6** | 9.2 | 1.1 logts | 9.4 logts | 58.0 logts | 0.63 | ![](./img/rv5/pred_k2_lambd0.6.png) |
| **0.8** | 9.1 | 1.1 logts | 9.4 logts | 57.0 logts | 0.64 | ![](./img/rv5/pred_k2_lambd0.8.png) |
| **1** | 12.5 | 1.9 logts | 13.1 logts | 96.1 logts | 0.31 | ![](./img/rv5/pred_k2_lambd1.0.png) |

\
**3-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-100) | MAE (+100) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 8.9 | 1.2 logts | 9.3 logts | 59.1 logts | 0.66 | ![](./img/rv5/pred_k3_lambd0.0.png) |
| **0.2** | 8.7 | 1.0 logts | 8.9 logts | 58.8 logts | 0.67 | ![](./img/rv5/pred_k3_lambd0.2.png) |
| **0.4** | 8.7 | 1.0 logts | 8.9 logts | 58.8 logts | 0.67 | ![](./img/rv5/pred_k3_lambd0.4.png) |
| **0.6** | 8.6 | 1.0 logts | 8.9 logts | 57.1 logts | 0.68 | ![](./img/rv5/pred_k3_lambd0.6.png) |
| **0.8** | 8.6 | 1.0 logts | 8.9 logts | 56.5 logts | 0.68 | ![](./img/rv5/pred_k3_lambd0.8.png) |
| **1** | 12.3 | 1.9 logts | 12.7 logts | 101.3 logts | 0.33 | ![](./img/rv5/pred_k3_lambd1.0.png) |

\
**4-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-100) | MAE (+100) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 8.6 | 1.2 logts | 9.1 logts | 58.8 logts | 0.68 | ![](./img/rv5/pred_k4_lambd0.0.png) |
| **0.2** | 8.4 | 1.0 logts | 8.7 logts | 58.3 logts | 0.69 | ![](./img/rv5/pred_k4_lambd0.2.png) |
| **0.4** | 8.5 | 1.0 logts | 8.6 logts | 58.6 logts | 0.69 | ![](./img/rv5/pred_k4_lambd0.4.png) |
| **0.6** | 8.3 | 1.0 logts | 8.6 logts | 57.1 logts | 0.70 | ![](./img/rv5/pred_k4_lambd0.6.png) |
| **0.8** | 8.3 | 1.0 logts | 8.6 logts | 55.9 logts | 0.70 | ![](./img/rv5/pred_k4_lambd0.8.png) |
| **1** | 12.3 | 2.0 logts | 12.4 logts | 102.8 logts | 0.34 | ![](./img/rv5/pred_k4_lambd1.0.png) |

\
**5-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-100) | MAE (+100) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 8.4 | 1.1 logts | 8.8 logts | 58.2 logts | 0.69 | ![](./img/rv5/pred_k5_lambd0.0.png) |
| **0.2** | 8.3 | 1.0 logts | 8.5 logts | 56.9 logts | 0.70 | ![](./img/rv5/pred_k5_lambd0.2.png) |
| **0.4** | 8.3 | 1.0 logts | 8.5 logts | 57.2 logts | 0.70 | ![](./img/rv5/pred_k5_lambd0.4.png) |
| **0.6** | 8.2 | 1.0 logts | 8.4 logts | 56.8 logts | 0.71 | ![](./img/rv5/pred_k5_lambd0.6.png) |
| **0.8** | 8.1 | 1.0 logts | 8.4 logts | 55.5 logts | 0.71 | ![](./img/rv5/pred_k5_lambd0.8.png) |
| **1** | 12.2 | 2.0 logts | 12.3 logts | 103.6 logts | 0.35 | ![](./img/rv5/pred_k5_lambd1.0.png) |

\
**6-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-100) | MAE (+100) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 8.3 | 1.2 logts | 8.7 logts | 58.1 logts | 0.70 | ![](./img/rv5/pred_k6_lambd0.0.png) |
| **0.2** | 8.2 | 1.0 logts | 8.4 logts | 57.5 logts | 0.71 | ![](./img/rv5/pred_k6_lambd0.2.png) |
| **0.4** | 8.1 | 1.0 logts | 8.3 logts | 56.5 logts | 0.71 | ![](./img/rv5/pred_k6_lambd0.4.png) |
| **0.6** | 8.0 | 1.0 logts | 8.2 logts | 55.8 logts | 0.72 | ![](./img/rv5/pred_k6_lambd0.6.png) |
| **0.8** | 8.0 | 1.0 logts | 8.3 logts | 55.8 logts | 0.72 | ![](./img/rv5/pred_k6_lambd0.8.png) |
| **1** | 12.2 | 2.1 logts | 12.2 logts | 104.9 logts | 0.34 | ![](./img/rv5/pred_k6_lambd1.0.png) |

\
**7-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-100) | MAE (+100) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 8.3 | 1.1 logts | 8.5 logts | 58.3 logts | 0.70 | ![](./img/rv5/pred_k7_lambd0.0.png) |
| **0.2** | 8.1 | 1.0 logts | 8.2 logts | 57.3 logts | 0.71 | ![](./img/rv5/pred_k7_lambd0.2.png) |
| **0.4** | 8.0 | 1.0 logts | 8.3 logts | 55.9 logts | 0.72 | ![](./img/rv5/pred_k7_lambd0.4.png) |
| **0.6** | 8.0 | 1.0 logts | 8.2 logts | 55.4 logts | 0.72 | ![](./img/rv5/pred_k7_lambd0.6.png) |
| **0.8** | 8.0 | 1.0 logts | 8.2 logts | 54.7 logts | 0.72 | ![](./img/rv5/pred_k7_lambd0.8.png) |
| **1** | 12.2 | 2.1 logts | 12.1 logts | 106.3 logts | 0.34 | ![](./img/rv5/pred_k7_lambd1.0.png) |

\
**8-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-100) | MAE (+100) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 8.2 | 1.1 logts | 8.5 logts | 57.9 logts | 0.71 | ![](./img/rv5/pred_k8_lambd0.0.png) |
| **0.2** | 8.1 | 1.0 logts | 8.2 logts | 56.8 logts | 0.72 | ![](./img/rv5/pred_k8_lambd0.2.png) |
| **0.4** | 7.9 | 1.0 logts | 8.2 logts | 54.6 logts | 0.73 | ![](./img/rv5/pred_k8_lambd0.4.png) |
| **0.6** | 7.9 | 1.0 logts | 8.1 logts | 54.0 logts | 0.73 | ![](./img/rv5/pred_k8_lambd0.6.png) |
| **0.8** | 7.9 | 1.0 logts | 8.1 logts | 54.6 logts | 0.73 | ![](./img/rv5/pred_k8_lambd0.8.png) |
| **1** | 12.2 | 2.1 logts | 12.1 logts | 107.0 logts | 0.35 | ![](./img/rv5/pred_k8_lambd1.0.png) |

\
**9-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-100) | MAE (+100) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 8.1 | 1.1 logts | 8.4 logts | 57.6 logts | 0.71 | ![](./img/rv5/pred_k9_lambd0.0.png) |
| **0.2** | 8.0 | 1.0 logts | 8.1 logts | 56.4 logts | 0.72 | ![](./img/rv5/pred_k9_lambd0.2.png) |
| **0.4** | 7.9 | 1.0 logts | 8.1 logts | 55.4 logts | 0.73 | ![](./img/rv5/pred_k9_lambd0.4.png) |
| **0.6** | 7.8 | 1.0 logts | 8.1 logts | 54.1 logts | 0.73 | ![](./img/rv5/pred_k9_lambd0.6.png) |
| **0.8** | 7.8 | 1.0 logts | 8.1 logts | 54.8 logts | 0.73 | ![](./img/rv5/pred_k9_lambd0.8.png) |
| **1** | 12.2 | 2.2 logts | 12.1 logts | 107.5 logts | 0.34 | ![](./img/rv5/pred_k9_lambd1.0.png) |

\
**10-NN**
| $\lambda$ | RMSE | MAE (-10) | MAE (10-100) | MAE (+100) | R² | Prédiction |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| **0** | 8.1 | 1.1 logts | 8.3 logts | 57.3 logts | 0.72 | ![](./img/rv5/pred_k10_lambd0.0.png) |
| **0.2** | 7.9 | 1.0 logts | 8.0 logts | 56.2 logts | 0.73 | ![](./img/rv5/pred_k10_lambd0.2.png) |
| **0.4** | 7.8 | 1.0 logts | 8.0 logts | 55.4 logts | 0.73 | ![](./img/rv5/pred_k10_lambd0.4.png) |
| **0.6** |  |  logts |  logts |  logts |  | ![](./img/rv5/pred_k10_lambd0.6.png) |
| **0.8** |  |  logts |  logts |  logts |  | ![](./img/rv5/pred_k10_lambd0.8.png) |
| **1** |  |  logts |  logts |  logts |  | ![](./img/rv5/pred_k10_lambd1.0.png) |

Contrairement à la prédiction de la hauteur, on constate que l'influence du facteur $\lambda$ est faible car nous obtenons des résultats très similaires quelle que soit sa valeur, sauf pour $\lambda = 0$ et $\lambda = 1$ où la prédiction est moins bonne.\
On constate cependant que la qualité du résultat obtenu s'améliore légèrement mais continuellement en augmentant le nombre de voisins ; bien que la hausse du coefficient R² ne prenne que très peu en compte les bâtiments avec beaucoup de logements car très minoritaires comparés aux logements individuels dans notre jeu de données (est de Paris).\
\
Globalement, on observe les erreurs moyennes absolues suivantes :
* 1 logement pour les bâtiments de - de 10 logements (~ 10% d'erreur) ;
* 8 logements pour les bâtiments de 10 à 100 logements (~ 15% d'erreur) ;
* 55 logements pour les bâtiments de + de 100 logements (~ 50% d'erreur).
