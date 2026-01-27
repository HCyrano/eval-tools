import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import lsqr
from scipy.sparse.linalg import lsmr
from pathlib import Path

def compter_occurrences_par_index(A_csr):
    """
    Calcule le nombre d'occurrences de chaque index (colonne) dans une matrice CSR.

    Args:
        A_csr (csr_matrix): La matrice creuse au format CSR.

    Returns:
        np.ndarray: Un vecteur 1D de taille N (nombre de colonnes)
                    où chaque élément est le nombre d'occurrences (somme des non-zeros)
                    pour l'index de colonne correspondant.
    """

    # 1. Transposer la matrice (A^T)
    # Les colonnes de A deviennent les lignes de A_T.
    # A_T = A_csr.transpose()

    # Si A_csr est déjà une matrice creuse efficace pour les opérations par colonne
    # (comme CSC), le transpose().tocsr() est rapide. Assurons-nous d'avoir un format
    # optimisé pour les sommes par LIGNE sur A_T, c'est-à-dire CSR ou CSC.
    # Dans ce cas, A_T sera généralement au format CSC, ce qui est très bien
    # pour les sommes de colonnes (qui sont des sommes de lignes sur A_T).
    
    # 2. Calculer la somme des éléments le long de l'axe 1 (les lignes de A_T)
    # Le résultat est une matrice colonne (N, 1) ou une matrice ligne (1, N).
    # On utilise .A pour convertir la matrice creuse résultat en tableau NumPy dense.
    # n_occurrences = A_T.sum(axis=1).A.flatten()

    # Alternative plus concise :
    n_occurrences = A_csr.sum(axis=0).A.flatten()
    # sum(axis=0) calcule directement la somme par colonne sur la matrice A.
    # Bien que CSR soit optimisé pour les lignes, SciPy gère l'efficacité
    # de cette opération pour vous en interne.

    return n_occurrences

# ----------------------------------------------------------
# estime le poids des patterns pour le stage (60-n_empty)
# ----------------------------------------------------------


#recupere le paramettre
# --- Suggestion pour l'argument
if len(sys.argv) < 2:
    print("Usage: python solve.py <stage_number>")
    sys.exit(1)

try:
    stage = int(sys.argv[1])
except ValueError:
    print("Erreur: Le numéro de stage doit être un entier.")
    sys.exit(1)
    
#nombre total d'index possible
n_index = 560844

DATA_DIR = Path("datas_norm")

WEIGHTS_DIR = Path("weights")
# Créer le répertoire de sortie s'il n'existe pas
WEIGHTS_DIR.mkdir(exist_ok=True)

OCC_DIR = Path("n_occs")
# Créer le répertoire de sortie s'il n'existe pas
OCC_DIR.mkdir(exist_ok=True)


datas_in = [DATA_DIR / f"data_{stage:02}.txt"]
weight_out = WEIGHTS_DIR / f"weight_{stage:02}.txt"
n_occ_out = OCC_DIR / f"n_occ_{stage:02}.txt"


rows = []
cols = []
data = []

scores = []

row_offset = 0  # compteur global
for data_in in datas_in:
    print(data_in)
    try:
    
        with open(data_in, "r") as f:
            for i, line in enumerate(f):
                vals = list(map(int, line.split()))
                *indices, score = vals
                u, counts = np.unique(indices, return_counts=True)
                
                # Décalage des indices de ligne
                global_i = i + row_offset
                
                rows.extend([global_i] * len(u))
                cols.extend(u.tolist())
                data.extend(counts.tolist())
                scores.append(score)
            
            # après chaque fichier, on met à jour le décalage
            row_offset += i + 1
        
        '''
        #idem mais sans s'occuper des doublons
        #Sans np.unique, les doublons sont laissés tels quels, donc dans la matrice COO, plusieurs entrées (i, j) identiques coexistent.
        #Or, dans SciPy : coo_matrix.sum_duplicates() est souvent appelé automatiquement quand tu convertis la matrice en CSR/CSC
        # = les deux versions sont identique
        with open(data_in, "r") as f:
            for i, line in enumerate(f):
                vals = list(map(int, line.split()))
                *indices, score = vals
                
                # Décalage des indices de ligne
                global_i = i + row_offset

                rows.extend([global_i]*len(indices))
                cols.extend(indices)
                data.extend([1]*len(indices))   # chaque occurrence compte pour 1
                scores.append(score)
        '''

    except Exception as e:
        print('cannot open', data_in, e)

# création de la matrice creuse

# fixe la taille de la matrice
n_rows = len(scores)
n_cols = n_index  # indices entre 0 et n
A = csr_matrix((data, (rows, cols)), shape=(n_rows, n_cols))

'''
# shape=(n_rows, n_cols) est deduit automatiquement
A = csr_matrix((data, (rows, cols)))
'''
print()
print(f"matrix size : {A.shape}")
print(A.nnz, "valeurs non nulles")

# Calcul du vecteur d'occurrences
vecteur_occurrences = compter_occurrences_par_index(A)

print()
print(f"vecteur size : {len(vecteur_occurrences)}")
print(np.count_nonzero(vecteur_occurrences), "valeurs non nulles")
print()

# save au ft txt identique a weigth
np.savetxt(n_occ_out, vecteur_occurrences, fmt="%d")

# --- 2. Préparation du Warm Start (x0) ---
# on initalise x0 avex le X du stage precedent
x0 = None
if stage > 0 :
    path_x0 = WEIGHTS_DIR / f"weight_{stage-1:02}.txt"
    if path_x0 and Path(path_x0).exists():
        print(f"Log: Initialisation de x avec {path_x0}")
        x0 = np.loadtxt(path_x0).astype(np.float32)
        # Sécurité : vérifier la taille
        if x0.shape[0] != n_index:
            print(f"Erreur : x0 a une taille de {x0.shape[0]}, attendu {n_index}")
            x0 = None
    else:
        print("Log: Pas de warm start trouvé, initialisation à zéro.")


# -----------------------------
# Résolution du système Ax = b
# -----------------------------
#x = lsqr(A, scores)[0]  # renvoie la solution au sens des moindres carrés


x = lsmr(A, scores, x0=x0)[0]  # renvoie la solution au sens des moindres carrés

'''
# -----------------------------
# Analyse des poids inchangés
# Features non rencontrées
# -----------------------------
if x0 is not None:
    diff = x - x0
    # On utilise une tolérance très faible pour le flottant
    nb_inchanges = np.sum(np.abs(diff) < 1e-12)
    pct_inchanges = (nb_inchanges / n_index) * 100
    print(f"Log: {nb_inchanges} poids ({pct_inchanges:.2f}%) sont restés identiques au stage précédent.")
'''

# -----------------------------
# Après la résolution x = lsmr(...)
# Analyse des poids inchangés
# & Features non rencontrées
# -----------------------------
if x0 is not None:
    # 1. Identifier les poids qui n'ont pas bougé
    poids_inchanges = (np.abs(x - x0) < 1e-15)
    
    # 2. Identifier les colonnes absentes
    features_absentes = (vecteur_occurrences == 0)
    
    # 3. Identifier les poids qui étaient NON NULS au départ
    poids_preexistants = (x0 != 0)
    
    # Masque final : Inchangé ET Absent ET était présent dans x0
    masque_raz = poids_inchanges & features_absentes & poids_preexistants
    
    # Statistiques réelles
    nb_raz = np.sum(masque_raz)
    
    # Remise à zéro effective
    x[masque_raz] = 0.0
    
    if nb_raz > 0:
        print(f"Log: {nb_raz} poids actifs du passé ont été mis en sommeil (0 occurrence et inchangés).")
    else:
        print("Log: Aucun poids actif n'a été supprimé durant ce stage.")
        
# -----------------------------
# affichage des extremes (utile pour cast en short)
# -----------------------------
print()

maximum = x.max()
minimum = x.min()

print("Max : ", maximum)
print("Min : ", minimum)

nb_non_zero = np.count_nonzero(x)

print("nb de poids differents de zero : ", nb_non_zero)   # 3

# -----------------------------
# Sauvegarde de x en mode texte
# -----------------------------

np.savetxt(weight_out, x, fmt="%.6f")

# -----------------------------
# Vérification des résidus
# -----------------------------

# Convertir les scores en tableau numpy 1D
y = np.asarray(scores, dtype=float).reshape(-1)

# Prédictions du modèle
y_pred = A @ x

# Vecteur des résidus
residuals = y_pred - y

# -----------------------------
# Métriques globales
# -----------------------------

# Norme L2 des résidus
residual_norm = np.linalg.norm(residuals)

# Root Mean Square Error
rmse = residual_norm / np.sqrt(len(y))

# Mean Absolute Error
mae = np.mean(np.abs(residuals))

# Erreur relative (résidu normalisé)
y_norm = np.linalg.norm(y)
relative_error = residual_norm / y_norm if y_norm != 0 else np.nan

# -----------------------------
# Baseline : prédire la moyenne
# -----------------------------
y_mean = np.mean(y)
baseline_residual_norm = np.linalg.norm(y - y_mean)

# Pseudo R² basé sur les normes
pseudo_R2 = 1 - (residual_norm**2) / (baseline_residual_norm**2)

# affichage
print()
print(f"||Ax - scores||_2 = {residual_norm:.6f}")
print(f"RMSE = {rmse:.6f}")
print(f"MAE  = {mae:.6f}")
print(f"Résidu relatif = {relative_error:.6e}")
print(f"Baseline (||y - mean||_2) = {baseline_residual_norm:.6f}")
print(f"Pseudo-R^2 = {pseudo_R2:.6f}")

'''
# histogramme des résidus
plt.figure(figsize=(8,4))
plt.hist(residuals, bins=200, color='skyblue', edgecolor='black')
plt.title("Histogramme des résidus (Ax - scores)")
plt.xlabel("Résidu")
plt.ylabel("Nombre d'observations")
plt.grid(True)
plt.show()
'''

# resid_vec doit être un numpy array
residuals = np.array(residuals)  # sécurité si ce n'était pas déjà un array
N = len(residuals)


# intervalles
print()
inc = 1
count_N = 0
prev_mask = np.zeros_like(residuals, dtype=bool)  # aucun au départ

while inc <= 128:
    mask = (residuals >= -inc) & (residuals <= inc)
    
    # nouveaux éléments = ceux qui sont maintenant inclus mais ne l’étaient pas avant
    new_mask = mask & ~prev_mask
    count_new = np.sum(new_mask)

    # pourcentage globale par rapport à tout l'échantillon
    count_N += count_new
    pct = (count_N / N) * 100

    print(f"erreur dans [-{inc}, {inc}] nouvellement inclus : {count_new} "
          f"({pct:.2f}%)")

    # mettre à jour le masque précédent
    prev_mask = mask
    inc *= 2
    
