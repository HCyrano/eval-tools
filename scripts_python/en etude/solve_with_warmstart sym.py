import sys
import numpy as np
from scipy.sparse import csr_matrix
# from scipy.sparse.linalg import lsqr
from scipy.sparse.linalg import lsmr
from pathlib import Path

# Constantes en haut
N_INDEX = 442794  # Nombre total d'indices possibles


def compter_occurrences_par_index(A_csr):
 """
    Calcule le nombre d'occurrences de chaque index (colonne) dans une matrice CSR.
    Utilise la valeur absolue pour éviter que les 1 et -1 ne s'annulent.
    """
    # On crée une copie des données en valeur absolue
    # A_csr.data contient uniquement les valeurs non nulles
    data_abs = np.abs(A_csr.data)
    
    # On crée une matrice temporaire partageant les mêmes indices mais avec data_abs
    A_abs = csr_matrix((data_abs, A_csr.indices, A_csr.indptr), shape=A_csr.shape)
    
    # Maintenant sum(axis=0) compte correctement chaque apparition
    n_occurrences = np.asarray(A_abs.sum(axis=0)).flatten()
    
    return n_occurrences

# ----------------------------------------------------------
# estime le poids des patterns pour le stage (60-n_empty)
# ----------------------------------------------------------


#recupere le paramettre
# --- Suggestion pour l'argument
if len(sys.argv) < 2:
    print("Usage: python solve_with_warmstart.py <stage_number>")
    sys.exit(1)

try:
    stage = int(sys.argv[1])
except ValueError:
    print("Erreur: Le numéro de stage doit être un entier.")
    sys.exit(1)
    

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

row_count = 0  # compteur global
# --- Logique simplifiée pour données pré-traitées ---
for line in f:
    if not line.strip(): continue

    vals = list(map(int, line.split()))
    *indices_globaux_pretraités, score = vals
    
    counts = {}
    # On avance de 2 en 2
    for i in range(0, len(indices_globaux_pretraités), 2):
        g_idx_p = indices_globaux_pretraités[i]     # Pattern Player
        g_idx_o = indices_globaux_pretraités[i + 1] # Pattern Opponent
        
        # On incrémente pour le Player
        counts[g_idx_p] = counts.get(g_idx_p, 0) + 1
        # On décrémente pour l'Opponent
        counts[g_idx_o] = counts.get(g_idx_o, 0) - 1
        
    for g_idx, val in counts.items():
        if val != 0:
            rows.append(row_count)
            cols.append(g_idx)
            data.append(val)
    
    scores.append(score)
    row_count += 1
    
    except Exception as e:
        print('cannot open', data_in, e)

        

# sécurité si ce n'était pas déjà un array en passe en float32
scores = np.asarray(scores, dtype=np.float32)


# création de la matrice creuse

# fixe la taille de la matrice
n_rows = len(scores)
n_cols = N_INDEX  # indices entre 0 et n
A = csr_matrix((data, (rows, cols)), shape=(n_rows, n_cols))

# --- 1. Identification des colonnes utiles ---
# On ne garde que les colonnes qui apparaissent au moins une fois
vecteur_occurrences = compter_occurrences_par_index(A)
indices_actifs = np.where(vecteur_occurrences > 0)[0]
n_actifs = len(indices_actifs)

print(f"Compression : {n_cols} colonnes -> {n_actifs} colonnes utiles")

# --- 2. Réduction de la matrice A ---
# On ne garde que les colonnes utiles pour le calcul
A_reduite = A[:, indices_actifs]

print()
print(f"matrix A reduite size : {A_reduite.shape}")
print(A_reduite.nnz, "valeurs non nulles")
print()


# sauve au fornat txt
np.savetxt(n_occ_out, vecteur_occurrences, fmt="%d")

# --- 3. Gestion du Warm Start (x0) ---
x0 = None
x0_reduit = None
if stage > 0 :
    path_x0 = WEIGHTS_DIR / f"weight_{stage-1:02}.txt"
    if path_x0.exists():
        print(f"Log: Initialisation de x (mappé) avec {path_x0}")
        x0 = np.loadtxt(path_x0).astype(np.float32)
        # On ne garde que les valeurs correspondant aux indices actifs actuels
        x0_reduit = x0[indices_actifs]
    else:
        print("Log: Pas de warm start trouvé.")

# -----------------------------------
# --- 4. Résolution du système Ax = b
# -----------------------------------
#x = lsqr(A, scores)[0]  # renvoie la solution au sens des moindres carrés

# Un damp entre 1e-4 (très léger) et 1e-1 (plus fort)
# Stabilité temporelle : Cela empêche un stage particulier d'envoyer tes poids "dans le décor".
# l'évolution de stage en stage sera plus fluide.
x_reduit = lsmr(A_reduite, scores, x0=x0_reduit, atol=1e-4, btol=1e-4, damp=1e-3)[0]

# x_reduit = lsmr(A_reduite, scores, x0=x0_reduit)[0]  # renvoie la solution au sens des moindres carrés

# --- 5. Expansion (Reverse Mapping) ---
# On recrée le vecteur complet de taille 560844
x_complet = np.zeros(N_INDEX, dtype=np.float32)
x_complet[indices_actifs] = x_reduit

# Utiliser x_complet pour la suite (sauvegarde et résidus)
x = x_complet

# -----------------------------
# Après la résolution x = lsmr(...)
# Réincorporation des poids absents avec décroissance (*0,9)
#les index absents vont mourir peu a peu
# -----------------------------
if x0 is not None:
    # 1. Identifier les colonnes absentes dans le stage actuel
    features_absentes = (vecteur_occurrences == 0)
    
    # 2. Identifier les poids qui étaient NON NULS dans x0
    poids_preexistants = (x0 != 0)
    
    # 3. Masque final : Absent dans ce stage ET était présent dans x0
    masque_decroissance = features_absentes & poids_preexistants
    
    # 4. Réincorporer les poids absents avec décroissance de 10%
    x[masque_decroissance] = x0[masque_decroissance] * 0.9
    
    # Statistiques
    nb_decroissance = np.sum(masque_decroissance)
    
    if nb_decroissance > 0:
        print(f"Log: {nb_decroissance} poids absents réincorporés avec décroissance (×0.9).")
    else:
        print("Log: Aucun poids absent à réincorporer.")

        
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

# pour la clareté des formules
y = scores

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
pseudo_R2 = 1 - (residual_norm**2) / (baseline_residual_norm**2) if baseline_residual_norm != 0 else np.nan

# affichage
print()
print(f"||Ax - scores||_2 = {residual_norm:.6f}")
print(f"RMSE = {rmse:.6f}")
print(f"MAE  = {mae:.6f}")
print(f"Résidu relatif = {relative_error:.6e}")
print(f"Baseline (||y - mean||_2) = {baseline_residual_norm:.6f}")
print(f"Pseudo-R^2 = {pseudo_R2:.6f}")


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
    
