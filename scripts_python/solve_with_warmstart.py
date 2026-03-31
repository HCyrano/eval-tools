import sys
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import lsmr
from pathlib import Path

# --- Configuration ---
N_INDEX = 226362  
TRAIN_RATIO = 0.80 #utilisé pour les stages: [9; 60[

def compter_occurrences_par_index(A_csr):
    """Calcule le nombre d'occurrences de chaque colonne dans une matrice CSR."""
    return np.asarray(A_csr.sum(axis=0)).flatten()

def calculer_metriques(matrice, poids, cibles, nom_set):
    """Calcule et affiche les performances du modèle."""
    if len(cibles) == 0:
        return None
        
    y_pred = matrice @ poids
    residuals = y_pred - cibles
    
    residual_norm = np.linalg.norm(residuals)
    rmse = residual_norm / np.sqrt(len(cibles))
    mae = np.mean(np.abs(residuals))
    
    y_mean = np.mean(cibles)
    baseline_norm = np.linalg.norm(cibles - y_mean)
    pseudo_R2 = 1 - (residual_norm**2) / (baseline_norm**2) if baseline_norm != 0 else 0
    
    print(f"\n--- Métriques {nom_set} ---")
    print(f"RMSE      : {rmse:.6f}")
    print(f"MAE       : {mae:.6f}")
    print(f"Pseudo-R² : {pseudo_R2:.6f}")
    return residuals

# --- Gestion des arguments ---
if len(sys.argv) < 2:
    print("Usage: python solve_with_warmstart_2.py <stage_number>")
    sys.exit(1)

try:
    stage = int(sys.argv[1])
    np.random.seed(stage)
except ValueError:
    print("Erreur: Le numéro de stage doit être un entier.")
    sys.exit(1)

# --- Chemins ---
DATA_DIR = Path("datas_norm")
WEIGHTS_DIR = Path("weights")
OCC_DIR = Path("n_occs")

for d in [WEIGHTS_DIR, OCC_DIR]: d.mkdir(exist_ok=True)

data_in_path = DATA_DIR / f"data_{stage:02}.txt"
weight_out = WEIGHTS_DIR / f"weight_{stage:02}.txt"
n_occ_out = OCC_DIR / f"n_occ_{stage:02}.txt"

# --- Chargement des données ---
rows, cols, data, scores = [], [], [], []
row_count = 0

print(f"Chargement de {data_in_path}...")
try:
    with open(data_in_path, "r") as f:
        for line in f:
            if not line.strip(): continue
            vals = list(map(int, line.split()))
            *indices, score = vals
            u, counts = np.unique(indices, return_counts=True)
            
            rows.extend([row_count] * len(u))
            cols.extend(u.tolist())
            data.extend(counts.tolist())
            scores.append(score)
            row_count += 1
except Exception as e:
    print(f"Erreur lecture: {e}")
    sys.exit(1)

scores = np.asarray(scores, dtype=np.float64)
A = csr_matrix((data, (rows, cols)), shape=(len(scores), N_INDEX))

# --- 1. Séparation Train / Validation ---
n_samples = A.shape[0]

if stage < 9:
    # Mode FULL TRAIN : Pas de validation
    print(f"Log: Stage {stage} < 9 -> Mode 100% Train (Pas de validation)")
    idx_train = np.arange(n_samples)
    idx_val = np.array([], dtype=int)
else:
    # Mode Validation classique
    indices_shuffled = np.random.permutation(n_samples)
    split_idx = int(n_samples * TRAIN_RATIO)
    idx_train = indices_shuffled[:split_idx]
    idx_val = indices_shuffled[split_idx:]

A_train = A[idx_train, :]
scores_train = scores[idx_train]
A_val = A[idx_val, :]
scores_val = scores[idx_val]

print(f"Données : {len(idx_train)} train / {len(idx_val)} validation")

# --- 2. Réduction aux colonnes actives ---
vecteur_occurrences = compter_occurrences_par_index(A_train)
indices_actifs = np.where(vecteur_occurrences > 0)[0]
A_train_reduite = A_train[:, indices_actifs]

print(f"Compression : {N_INDEX} -> {len(indices_actifs)} colonnes utiles")
vecteur_occurrences_complet = compter_occurrences_par_index(A)
np.savetxt(n_occ_out, vecteur_occurrences_complet, fmt="%d")

# --- 3. Gestion du Warm Start (x0) ---
x0 = None
x0_reduit = None
if stage > 0:
    path_x0 = WEIGHTS_DIR / f"weight_{stage-1:02}.txt"
    if path_x0.exists():
        print(f"Log: Warm start avec {path_x0}")
        x0 = np.loadtxt(path_x0).astype(np.float64)
        x0_reduit = x0[indices_actifs]

# --- 4. Résolution (LSMR) ---
print("Résolution du système...")
x_reduit = lsmr(A_train_reduite, scores_train, x0=x0_reduit, atol=1e-4, btol=1e-4, damp=1e-3)[0]

x = np.zeros(N_INDEX, dtype=np.float64)
x[indices_actifs] = x_reduit

# --- 5. Décroissance des poids absents ---
if x0 is not None:
    features_absentes = (vecteur_occurrences == 0)
    poids_preexistants = (x0 != 0)
    masque_decroissance = features_absentes & poids_preexistants
    x[masque_decroissance] = x0[masque_decroissance] * 0.9
    print(f"Log: {np.sum(masque_decroissance)} poids maintenus avec décroissance (0.9)")

# --- 6. Évaluation ---
res_train = calculer_metriques(A_train, x, scores_train, "TRAIN")
res_val = calculer_metriques(A_val, x, scores_val, "VALIDATION")

# Sauvegarde des poids
np.savetxt(weight_out, x, fmt="%.6f")

# --- 7. Analyse des résidus ---
# On choisit les résidus à analyser : Priorité à la Validation, sinon Train
if res_val is not None:
    res_a_analyser = res_val
    nom_analyse = "Validation"
else:
    res_a_analyser = res_train
    nom_analyse = "Train (Mode Full)"

print(f"\nAnalyse de la précision ({nom_analyse}) :")
N_total = len(res_a_analyser)
inc = 1
prev_mask = np.zeros_like(res_a_analyser, dtype=bool)

while inc <= 128:
    mask = (res_a_analyser >= -inc) & (res_a_analyser <= inc)
    new_elements = np.sum(mask & ~prev_mask)
    count_total = np.sum(mask)
    pct = (count_total / N_total) * 100
    print(f"Erreur dans [-{inc:3}, {inc:3}] : {new_elements:6} nouveaux (Total: {pct:6.2f}%)")
    prev_mask = mask
    inc *= 2
    
print(f"\nFini. Poids sauvegardés dans {weight_out}")
