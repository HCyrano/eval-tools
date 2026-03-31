import sys
from collections import Counter
from pathlib import Path
import math


# --- definition des patterns ---
# a implementer nanuellement en fonctions des patterns choisis

# mobility player and opponent
# diag4, diag5, diag6, diag7, diag8
# edge+2X, edge 6+4, edge 2*5
# hv2, hv3, hv4
# corner9
index_offset = [24, 24, 81, 243, 729, 2187, 6561, 59049, 59049, 59049, 6561, 6561, 6561, 19683]
type_rotate  = [ 0,  0,  4,   5,   6,    7,    8,    10,    10,     0,    8,    8,    8,    23]

# ATTENTION : verifier "cas particulier mobility"

# 🔄 --- Conversion entre Index Global et Index Local/Individuel ---
#
# Cette section contient les fonctions essentielles pour manipuler les indices
# lorsque l'espace d'indexation est divisé en patterns successifs.
#
# L'index global ('global_index') est la position séquentielle absolue dans l'ensemble
# des patterns. Il est utilisé pour le stockage général.
#
# L'index local ('local_index') est la position séquentielle relative à son pattern spécifique,
# une fois que les décalages (offsets) des patterns ont été retirés.
# et l'offset relatifs egalement
#
# La conversion entre ces deux formes est cruciale pour l'adressage interne
# et les calculs de symétrie, qui opèrent sur l'index local.

def get_local_index(global_index):
    
    id = global_index
        
    for i in range(len(index_offset)):
        if id < index_offset[i]:
            break
        id -= index_offset[i]
        
    if i < 2: # cas particulier mobility
        return id
		        
    return id - ((index_offset[i]-1)//2), i

def get_global_index(local_index, id_offset):
    
    id = local_index
    
    if id_offset > 1: # cas particulier mobility
    	id += ((index_offset[id_offset]-1)//2)
        
    for i in range(id_offset):
        id += index_offset[i]
        
    return id
# --- end ---




# --- definition de la methode index_rotate ---
# retourne l'index du pattern rotate

rotates = [
        # pas de symetrie
        [  0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10,  11,  12,  13,  14,  15],        # 0
        # symetrie simple
        [  0],                                                                          # 1
        [  1,  0],                                                                      # 2
        [  2,  1,  0],                                                                  # 3
        [  3,  2,  1,  0],                                                              # 4
        [  4,  3,  2,  1,  0],                                                          # 5
        [  5,  4,  3,  2,  1,  0],                                                      # 6
        [  6,  5,  4,  3,  2,  1,  0],                                                  # 7
        [  7,  6,  5,  4,  3,  2,  1,  0],                                              # 8
        [  8,  7,  6,  5,  4,  3,  2,  1,  0],                                          # 9
        [  9,  8,  7,  6,  5,  4,  3,  2,  1,  0],                                      # 10
        [ 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,   0],                                 # 11
        [ 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,   1,   0],                            # 12
        [ 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,   2,   1,   0],                       # 13
        [ 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,   3,   2,   1,   0],                  # 14
        [ 14, 13, 12, 11, 10,  9,  8,  7,  6,  5,   4,   3,   2,   1,   0],             # 15
        [ 15, 14, 13, 12, 11, 10,  9,  8,  7,  6,   5,   4,   3,   2,   1,   0],        # 16

        # symetrie corner 4/3/3/1
        [ 10,  9,  8,  7,  4,  5,  6,  3,  2,  1,   0],                                 # 17
        # symetrie corner 2 bords 5 + X & corner 4/3/2/1
        [  9,  8,  7,  6,  4,  5,  3,  2,  1,  0],                                      # 18
        # hyper diagonale
        [  9,  8,  7,  3,  4,  5,  6,  2,  1,  0],                                      # 19
        # corner 5/3/2/1/1
        [ 11, 10,  9,  8,  7,  5,  6,  4,  3,  2,   1,   0],                            # 20
        # corner 4/4/3/2 ou corner 5/3/3/1/1
        [ 12, 11, 10,  9,  8,  5,  6,  7,  4,  3,   2,   1,   0],                       # 21
        #  corner 5/4/3/2/1
        [ 14, 13, 12, 11, 10,  9,  6,  7,  8,  5,   4,   3,   2,   1,   0],             # 22
        # corner9
        [  8,  7,  6,  3,  4,  5,  2,  1,  0]                                           # 23
        ]

def index_rotate(index, id_patt):
    
    #index du pattern definit son modele de rotation
    id_rot = type_rotate[id_patt]

    if id_rot == 0:
        return index

    id = index
    rotated_index = 0
    
    #nb de cases du pattern
    n_squares = len(rotates[id_rot])
    
    for i in range(n_squares):
    
        # 1. Simuler la division entière C++ (troncation vers zéro)
        # float(id) / 3.0 s'assure d'avoir un float pour la division
        quotient_c = int(float(id) / 3.0)
        
        # 2. Simuler le modulo C++ (r = dividende - diviseur * quotient)
        # Le reste aura le même signe que 'id'
        r = id - 3 * quotient_c
        
        # Le nouveau quotient pour la prochaine itération est le quotient C++
        id = quotient_c
        
        if r == 2:
            r = -1
            id += 1
        elif r == -2:
            r = 1
            id -= 1
        
        rotated_index += r * 3**rotates[id_rot][i]
    
    return rotated_index
    
# --- end ---

'''
# --- Somme les occurrences d'un index et de son index inverse. ---

def sommer_occurrences_symetriques(compte: dict) -> dict:
    
    compte_final = {}
    indices_traites = set()

    # Parcourir les clés du dictionnaire initial
    for global_index, occurence in compte.items():
        
        # Si l'index a déjà été traité (parce que c'était le symétrique
        # d'un index précédent), on l'ignore.
        if global_index in indices_traites:
            continue
            
        # 1 retrouver l'index local et son type de pattern
        local_index, id_patt = get_local_index(global_index)
        
        # 2 Calculer l'index inverse (blanc <=> noir)
        # qui est forcement canonique (-)
        local_index_inverse = -index_rotate(local_index, id_patt)
                
        # 3 Calculer l'index global du
        global_index_inverse = get_global_index(local_index_inverse, id_patt)

        # 2. Récupérer l'occurrence du symétrique (0 si l'index n'existe pas dans le dict)
        occurence_inverse = compte.get(global_index_inverse, 0)
        
        # 3. Calculer la somme
        somme_occurrences = occurence + occurence_inverse
        
        # 4. Stocker la somme pour les deux indices
        compte_final[global_index] = somme_occurrences
        compte_final[global_index_inverse] = somme_occurrences
        
        # 5. Marquer les deux indices comme traités
        indices_traites.add(global_index)
        indices_traites.add(global_index_inverse)
        
    return compte_final
    
# --- end ---

'''

# 🛑 ATTENTION : Cette fonction est maintenant VIDE, car nous ne sommons plus.
# La fonction originale retournait un dictionnaire de sommes, ici nous retournons
# simplement le compte brut.
def sommer_occurrences_symetriques(compte: dict) -> dict:
    # On retourne le dictionnaire de comptage brut
    return compte
    
# --- end ---


#recupere le paramettre
# --- Suggestion pour l'argument
if len(sys.argv) < 3:
    print("Usage: python norm_data.py <stage_number> <n_occs_min>")
    sys.exit(1)

try:
    stage = int(sys.argv[1])
    N_OCCS_MIN = int(sys.argv[2])
except ValueError:
    print("Erreur: Le numéro de stage doit être un entier.")
    sys.exit(1)


# bornage inferieur et superieur des stages a normaliser
stage_borne_inf = 9
stage_borne_sup = 60
stage = max(stage, stage_borne_inf)


# Construire la liste des fichiers input

DATA_DIR = Path("datas_WS")
DATA_NORM_DIR = Path("datas_norm")

# Créer le répertoire de sortie s'il n'existe pas
DATA_NORM_DIR.mkdir(exist_ok=True)


filenames_in = []

path = Path(DATA_DIR / f"data_{stage:02}.txt")
if path.exists():
    filenames_in.append(str(path)) # Convertir en str pour le reste du code


filename_out =  DATA_NORM_DIR / f"data_{stage:02}.txt"

# 1) Lecture unique des fichiers d'entrée
all_lines = []   # contiendra toutes les lignes déjà découpées en valeurs
all_indices = [] # pour compter globalement les occurrences


for filename_in in filenames_in:
    with open(filename_in, "r") as f:
        for line in f:
            vals = list(map(int, line.split()))
            all_lines.append(vals)
            # On ne compte pas le dernier élément (score)
            all_indices.extend(vals[:-1])            
            
# 2) Compter les occurrences
compte = Counter(all_indices)

# cas particulier mobility
# S'assurer que chaque indice de 0 à 47 (mobility) > 0 a au moins 50 occurrences pour ne pas etre supprimé
for i in range(48):
    if compte[i] != 0:
    	compte[i] = max(compte[i], N_OCCS_MIN)

# 3) somme des occurences du pattern et son pattern inverses
compte_final = sommer_occurrences_symetriques(compte)

# 3) Déterminer les index à supprimer ( < N_OCCS_MIN)
a_supprimer = {idx for idx, occ in compte_final.items() if occ < N_OCCS_MIN}

# --- Affichage explicite des statistiques ---
total_patterns_unique = len(compte_final)
nb_suppr = len(a_supprimer)
pourcentage_suppr = (nb_suppr / total_patterns_unique * 100) if total_patterns_unique > 0 else 0

print(f"--- Statistiques de normalisation (Stage {stage:02}) ---")
print(f"Nombre total de patterns uniques : {total_patterns_unique}")
print(f"Nombre de patterns à supprimer   : {nb_suppr} ({pourcentage_suppr:.2f}%)")
print(f"Seuil d'occurrence choisi        : {N_OCCS_MIN}")
print(f"Nombre de patterns conservés     : {total_patterns_unique - nb_suppr}")
print("-" * 48)

# 4) Écriture directe du fichier filtré
with open(filename_out, "w") as f:
    for vals in all_lines:
        # Séparer les valeurs à filtrer et le score
        *indices, score = vals
        filtres = [str(v) for v in indices if v not in a_supprimer]
        filtres.append(str(score))  # le score est toujours conservé
        f.write(" ".join(filtres) + "\n")
