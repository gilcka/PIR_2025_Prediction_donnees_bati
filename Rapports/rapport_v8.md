# Rapport d'avancement 8

Pendant cette semaine, nous travaillons sur une nouvelle méthode de prédiction mélangeant K-NN et forêt aléatoire, et nous la comparons avec chacune des 2 méthodes prises indépendamment.

# 1. Implémentation de la nouvelle méthode

Pour réaliser cette nouvelle prédiction, nous commençons par calculer pour chaque bâtiment les 5 autres bâtiments les plus proches (nombre de voisins $k = 5$).\
On utilise pour cela la méthode `NearestNeighbors` de Scikit-Learn, à laquelle on fournit les coordonnées $(x, y)$ des centroïdes des bâtiments, et en la paramétrant pour qu'elle retourne la matrice des distances de chaque bâtiment par rapport à ses plus proches voisins.\
\
Ensuite, on construit un vecteur de forme $(X_0, X_1, ..., X_5)$ avec :

<p align="center">$\forall i \in [0, 5] X_i = ({NATURE}_i, {USAGE1}_i, {LEGER}_i, {DATE APP}_i, {SURFACE}_i, {dist}_{0 \rightarrow i})$</p>

avec $X_0$ le vecteur des attributs du bâtiment courant, les 5 autres vecteurs représentant ceux des voisins.
