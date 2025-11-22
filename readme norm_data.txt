Ce script est un outil de post-traitement statistique appliqué à une base de
motifs déjà normalisés spatialement (rotation/miroir). La canonicalisation*
spatiale n’est plus effectuée ici.

Le script :

1) Charge les données de plusieurs stages adjacents
2) Compte les occurrences de chaque motif
3) Fusionne le compte avec celui de son motif inverse couleur
4) Supprime les motifs dont la fréquence cumulée est inférieure à un seuil
5) Réécrit le fichier en supprimant ces motifs ligne par ligne

Ce filtrage conserve uniquement les motifs statistiquement significatifs,
réduisant l’espace d’entrée et améliorant la généralisation du modèle.


*Le jeu de données a été pré-normalisé par l'application des symétries spatiales
(rotations ou miroirs).
Ce script ne réalise pas la canonicalisation spatiale (rotations/miroirs) :
celle-ci est censée être effectuée en amont lors de la génération des données.
Ici, chaque motif est déjà présent sous sa forme spatiale canonique.
(Forme canonique : l'indice le plus petit parmi toutes les variations spatiales
– rotation ou miroir – du motif).

Le script effectue uniquement une normalisation couleur en fusionnant l'occurrence
de chaque motif avec celle de son motif inverse couleur.



1) les index identiques sur la meme ligne (une ligne == un othellier) sont bien prit
en compte dans le calcul du nombre d'occurences

2) gestion des index

les methodes get_local_index, get_global_index permettent de passer des indices locaux
aux globaux et inversement

codage local :

-1 == pion noir
 0 == case vide
 1 == poin blanc
 
un pattern est un ensemble de cases ordonnées (par exemple une ligne)
 
l'indice d'un motif de ce pattern est codé : en base 3
 
sq_0 * 3**0 + sq_1 * 3**1 ... + sq_n * 3**n (sq_n appartient a {-1, 0, 1})
 
donc pour un pattern 5 cases les indices sont dans l'espace [-121, 121]
 
codage globaux :
 
les indices sont translatés dans un espace positifs
 
en reprenant l'exemple du "pattern 5" l'espace de codage devient [0, 242]
 
l'ensemble des indices des patterns de l'othellier sont mis bout a bout
en decalant les indices des patterns differents par un offset de l'ensemble
des espaces de codage des patterns precedent

3) Normalisation Couleur (Symétrie M et M')
Ce script applique une normalisation par symétrie couleur :
il somme les occurrences de l'indice canonique M et de son
indice canonique inverse couleur M' (obtenu par l'opposé de l'indice local).
Cette opération garantit que le motif est évalué de manière agnostique par
rapport à la couleur, en regroupant le compte des 4 formes initiales du motif, qui sont:
Le motif M
Le motif miroir (déjà converti M par le prétraitement)
Le motif inverse couleur M'
Le motif inverse couleur miroir (déjà converti M' par le prétraitement)

4) on elimine de la base de donnée les patterns dont les occurrences
sont inférieures a un seuil n_occurences
 