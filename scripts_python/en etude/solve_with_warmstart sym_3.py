import sys
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import lsmr
from pathlib import Path

# --- Configuration ---
N_INDEX = 442794  
TRAIN_RATIO = 0.8  # Ajouté : ratio pour le split train/validation

def compter_occurrences_par_index(A_csr):
    """Calcule le nombre d'occurrences réelles (non nulles) par colonne."""
    data_abs = np.abs(A_csr.data)
    A_abs = csr_matrix((data_abs, A_csr.indices, A_csr.indptr), shape=A_csr.shape)
    n_occurrences = np.asarray(A_abs.sum(axis=0)).flatten()
    return n_occurrences

def calculer_metriques(matrice, poids, cibles, nom_set):
    """Calcule et affiche les performances du modèle."""
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

# --- Initialisation ---
if len(sys.argv) < 2:
    print("Usage: python solve_with_warmstart.py <stage_number>")
    sys.exit(1)

try:
    stage = int(sys.argv[1])
    np.random.seed(stage)

except ValueError:
    print("Erreur: Le numéro de stage doit être un entier.")
    sys.exit(1)

DATA_DIR = Path("datas_norm")
WEIGHTS_DIR = Path("weights")
OCC_DIR = Path("n_occs")

WEIGHTS_DIR.mkdir(exist_ok=True)
OCC_DIR.mkdir(exist_ok=True)

datas_in = [DATA_DIR / f"data_{stage:02}.txt"]
weight_out = WEIGHTS_DIR / f"weight_{stage:02}.txt"
n_occ_out = OCC_DIR / f"n_occ_{stage:02}.txt"

rows, cols, data, scores = [], [], [], []
row_count = 0

# --- Lecture des données ---
for data_path in datas_in:
    if not data_path.exists():
        print(f"Attention: {data_path} introuvable.")
        continue
    
    print(f"Chargement de : {data_path}")
    try:
        with open(data_path, "r") as f:
            for line in f:
                if not line.strip(): continue
                
                vals = list(map(int, line.split()))
                *indices_globaux, score = vals
                
                counts = {}
                # Logique alternée [P, O, P, O...]
                for i in range(0, len(indices_globaux), 2):
                    g_idx_p = indices_globaux[i]
                    g_idx_o = indices_globaux[i + 1]
                    
                    counts[g_idx_p] = counts.get(g_idx_p, 0) + 1
                    counts[g_idx_o] = counts.get(g_idx_o, 0) - 1
                
                for g_idx, val in counts.items():
                    if val != 0:
                        rows.append(row_count)
                        cols.append(g_idx)
                        data.append(val)
                
                scores.append(score)
                row_count += 1
    except Exception as e:
        print(f"Erreur lors de la lecture de {data_path}: {e}")

if row_count == 0:
    print("Erreur: Aucune donnée chargée.")
    sys.exit(1)

scores = np.asarray(scores, dtype=np.float64)
A = csr_matrix((data, (rows, cols)), shape=(row_count, N_INDEX))

# --- 1. Séparation Train / Validation ---
indices_shuffled = np.random.permutation(row_count)
split_idx = int(row_count * TRAIN_RATIO)

idx_train = indices_shuffled[:split_idx]
idx_val = indices_shuffled[split_idx:]

A_train = A[idx_train, :]
scores_train = scores[idx_train]
A_val = A[idx_val, :]
scores_val = scores[idx_val]

print(f"Données : {len(idx_train)} train / {len(idx_val)} validation")

# --- 1b. Normalisation des scores (calculée sur le train uniquement) ---
# LSMR converge mieux quand la cible est centrée et d'écart-type ~1.
# On sauvegarde mu/sigma pour dénormaliser les poids ensuite.
scores_mu = scores_train.mean()
scores_sigma = scores_train.std()
if scores_sigma == 0:
    scores_sigma = 1.0  # garde-fou si tous les scores sont identiques

scores_train_norm = (scores_train - scores_mu) / scores_sigma


print(f"Normalisation scores : µ={scores_mu:.3f}  σ={scores_sigma:.3f}  "
      f"(plage train normalisée : [{scores_train_norm.min():.2f}, {scores_train_norm.max():.2f}])")

# --- 2. Réduction aux colonnes actives ---
vecteur_occurrences_train = compter_occurrences_par_index(A_train)
indices_actifs = np.where(vecteur_occurrences_train > 0)[0]
A_train_reduite = A_train[:, indices_actifs]

print(f"Compression : {N_INDEX} -> {len(indices_actifs)} colonnes utiles")

# Sauvegarde des occurrences totales (Train + Val) pour diagnostic
vecteur_occurrences_global = compter_occurrences_par_index(A)
np.savetxt(n_occ_out, vecteur_occurrences_global, fmt="%d")

# --- 3. Gestion du Warm Start ---
x0_reduit = None
x0 = None
if stage > 0:
    path_x0 = WEIGHTS_DIR / f"weight_{stage-1:02}.txt"
    if path_x0.exists():
        print(f"Log: Warm start avec {path_x0}")
        x0 = np.loadtxt(path_x0).astype(np.float64)
        if len(x0) == N_INDEX:
            # x0 est dans l'espace original → on le ramène dans l'espace normalisé
            # pour qu'il serve de bon point de départ à LSMR
            x0_reduit = x0[indices_actifs] / scores_sigma
        else:
            print("Attention: Taille de x0 incohérente, warm start ignoré.")

# --- 4. Résolution (LSMR) sur scores normalisés ---
print("Résolution du système (LSMR)...")
x_reduit_norm = lsmr(A_train_reduite, scores_train_norm, x0=x0_reduit, atol=1e-4, btol=1e-4, damp=1e-3)[0]

# Dénormalisation : les poids sont dans l'espace normalisé → on revient à l'échelle originale.
# y_norm = A @ w_norm  =>  (y - µ)/σ = A @ w_norm  =>  y = A @ (σ * w_norm) + µ
# Le biais µ est absorbé globalement (matrice centrée), on le réintègre via les poids.
x_reduit = x_reduit_norm * scores_sigma

# Expansion vers le vecteur complet
x = np.zeros(N_INDEX, dtype=np.float64)
x[indices_actifs] = x_reduit

# --- 5. Décroissance des poids absents ---
if x0 is not None:
    # x0 et x sont tous les deux dans l'espace original → comparaison directe
    masque_decroissance = (vecteur_occurrences_train == 0) & (x0 != 0)
    x[masque_decroissance] = x0[masque_decroissance] * 0.9
    print(f"Log: {np.sum(masque_decroissance)} poids maintenus (décroissance 0.9)")

# --- 6. Évaluation ---
calculer_metriques(A_train, x, scores_train, "TRAIN")
res_val = calculer_metriques(A_val, x, scores_val, "VALIDATION")

# Sauvegarde des poids
np.savetxt(weight_out, x, fmt="%.6f")

# --- 7. Analyse des résidus ---
print("\nAnalyse de la précision (Validation) :")
N_val = len(res_val)
inc = 1
prev_mask = np.zeros_like(res_val, dtype=bool)

while inc <= 64: # Réduit à 64 pour la lisibilité, Othello dépasse rarement 64 pions
    mask = (res_val >= -inc) & (res_val <= inc)
    new_elements = np.sum(mask & ~prev_mask)
    pct = (np.sum(mask) / N_val) * 100
    print(f"Erreur dans [-{inc:2}, {inc:2}] : {new_elements:6} nouveaux (Total: {pct:6.2f}%)")
    prev_mask = mask
    inc *= 2

print(f"\nTerminé. Fichier généré : {weight_out}")
