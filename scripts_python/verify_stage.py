import sys
import numpy as np
from scipy.sparse import csr_matrix
from pathlib import Path

# --- Configuration ---
N_INDEX = 442794

def compter_occurrences_par_index(A_csr):
    return np.asarray(A_csr.sum(axis=0)).flatten()

def calculer_metriques(matrice, poids, cibles, nom_set):
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
    print("Usage: python verify_stage.py <stage_number>")
    print("       python verify_stage.py <data_path> <weight_path>")
    sys.exit(1)

# Mode 1 : numéro de stage (cherche dans datas_norm/ et weights/)
# Mode 2 : chemins directs vers les fichiers
if len(sys.argv) == 2:
    try:
        stage = int(sys.argv[1])
        DATA_DIR = Path("datas")
        WEIGHTS_DIR = Path("weights")
        data_path = DATA_DIR / f"data_{stage:02}.txt"
        weight_path = WEIGHTS_DIR / f"weight_{stage:02}.txt"
        print(f"Vérification du stage {stage}")
    except ValueError:
        print("Erreur: argument invalide. Fournir un entier (stage) ou deux chemins de fichiers.")
        sys.exit(1)
elif len(sys.argv) == 3:
    data_path = Path(sys.argv[1])
    weight_path = Path(sys.argv[2])
    print(f"Vérification avec fichiers directs")
else:
    print("Usage: python verify_stage.py <stage_number>")
    print("       python verify_stage.py <data_path> <weight_path>")
    sys.exit(1)

# --- Vérification existence des fichiers ---
for p in [data_path, weight_path]:
    if not p.exists():
        print(f"Erreur: fichier introuvable -> {p}")
        sys.exit(1)

print(f"Data   : {data_path}")
print(f"Poids  : {weight_path}")

# --- Chargement des poids ---
print("\nChargement des poids...")
weights = np.loadtxt(weight_path, dtype=np.float64)
nnz = np.count_nonzero(weights)
print(f"  {len(weights)} poids chargés, {nnz} non-nuls")

if len(weights) < N_INDEX:
    print(f"  Avertissement: poids incomplets ({len(weights)} < {N_INDEX}), padding avec des zéros")
    weights = np.pad(weights, (0, N_INDEX - len(weights)))
elif len(weights) > N_INDEX:
    print(f"  Avertissement: plus de poids que prévu ({len(weights)} > {N_INDEX}), troncature")
    weights = weights[:N_INDEX]

# --- Chargement des données ---
print(f"\nChargement de {data_path}...")
rows, cols, data, scores = [], [], [], []
row_count = 0

try:
    with open(data_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
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
print(f"  {len(scores)} lignes chargées, {len(data)} entrées sparse")

# --- Calcul des métriques (toutes les données) ---
calculer_metriques(A, weights, scores, "GLOBAL (toutes les données)")

# --- Analyse des résidus ---
y_pred = A @ weights
residuals = y_pred - scores

print(f"\nAnalyse de la précision :")
N_total = len(residuals)
inc = 1
prev_mask = np.zeros_like(residuals, dtype=bool)

while inc <= 128:
    mask = (residuals >= -inc) & (residuals <= inc)
    new_elements = np.sum(mask & ~prev_mask)
    count_total = np.sum(mask)
    pct = (count_total / N_total) * 100
    print(f"Erreur dans [-{inc:3}, {inc:3}] : {new_elements:6} nouveaux (Total: {pct:6.2f}%)")
    prev_mask = mask
    inc *= 2

print("\nTerminé.")
