import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import lsqr
from scipy.sparse.linalg import lsmr
from pathlib import Path


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

DATA_DIR = Path("datas_norm")
WEIGHTS_DIR = Path("weights")

# Créer le répertoire de sortie s'il n'existe pas
WEIGHTS_DIR.mkdir(exist_ok=True)

filenames_in = [DATA_DIR / f"data_norm_{stage:02}.txt"]
filename_out = WEIGHTS_DIR / f"weight_{stage:02}.txt"


rows = []
cols = []
data = []

scores = []

row_offset = 0  # compteur global
for filename_in in filenames_in:
    print(filename_in)
    try:
    
        with open(filename_in, "r") as f:
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
        with open(filename_in, "r") as f:
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
        print('cannot open', filename_in, e)

    # création de la matrice creuse

# fixe la taille de la matrice
n_rows = len(scores)
n_cols = 383697  # indices entre 0 et n
A = csr_matrix((data, (rows, cols)), shape=(n_rows, n_cols))

'''
# shape=(n_rows, n_cols) est deduit automatiquement
A = csr_matrix((data, (rows, cols)))
'''
print()
print(f"matrix size : {A.shape}")
print(A.nnz, "valeurs non nulles")

# -----------------------------
# Résolution du système Ax = b
# -----------------------------
x = lsqr(A, scores)[0]  # renvoie la solution au sens des moindres carrés


#x = lsmr(A, scores)[0]  # renvoie la solution au sens des moindres carrés


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
# Sauvegarde de x
# -----------------------------

np.savetxt(filename_out, x, fmt="%.6f")
#np.save("weigth/weigth_27.npy", x)

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
    
print("--------------------------------------------------------------------------------")

