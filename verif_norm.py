import sys
from collections import Counter
from pathlib import Path
import math

# --- definition des patterns ---
# a implementer nanuellement en fonctions des patterns choisis

index_offset = [243, 729, 2187, 6561, 59049, 6561, 6561, 6561, 59049, 59049, 177147]
type_rotate  = [  5,   6,    7,    8,    10,    8,    8,    8,    15,     0,     14]

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
        
    return id - ((index_offset[i]-1)//2), i

def get_global_index(local_index, id_offset):
    
    id = local_index
    id += ((index_offset[id_offset]-1)//2)
        
    for i in range(id_offset):
        id += index_offset[i]
        
    return id
# --- end ---




# --- definition de la methode index_rotate ---
# retourne l'index du pattern rotate

rotates = [
             [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
             [0],
             [1, 0],
             [2, 1, 0],
             [3, 2, 1, 0],
             [4, 3, 2, 1, 0],
             [5, 4, 3, 2, 1, 0],
             [6, 5, 4, 3, 2, 1, 0],
             [7, 6, 5, 4, 3, 2, 1, 0],
             [8, 7, 6, 5, 4, 3, 2, 1, 0],
             [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
             [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
             [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
             [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
             [10, 9, 8, 7, 4, 5, 6, 3, 2, 1, 0],
             [9, 8, 7, 6, 4, 5, 3, 2, 1, 0]
        ]

def index_rotate(index, id_patt):
    
    id = index
    rotated_index = 0
    
    #index du pattern definit son index de rotation
    id_rot = type_rotate[id_patt]
    
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


def est_canonique(global_index):
    """
    Vérifie qu'un index global est bien sous forme canonique
    (réduction rotationnelle déjà appliquée).
    Retourne True si c'est correct, False sinon.
    """

    # 1) Convertir en index local
    local_index, pattern_id = get_local_index(global_index)

    # 2) Générer toutes la rotation possible pour ce pattern
    rotated_index = index_rotate(local_index, pattern_id)

    # 4) Si l’index actuel n'est pas le minimum → pas canonique
    return local_index <= rotated_index

def valider_fichier_normalisation(path):
    erreurs = []
    with open(path, "r") as f:
        for num_ligne, line in enumerate(f, start=1):
            vals = list(map(int, line.split()))
            for idx in vals[:-1]:  # ignorer le score
                if not est_canonique(idx):
                    #sys.exit(1)
                    erreurs.append((num_ligne, idx))
    
    return erreurs

erreurs = valider_fichier_normalisation("datas/data_28.txt")

if erreurs:
    print("⚠ Normalisation NON valide.")
    for ligne, idx in erreurs[:10]:
        print(f"Ligne {ligne}: index {idx} n'est pas canonique")
else:
    print("✔ Base entièrement normalisée.")
    


