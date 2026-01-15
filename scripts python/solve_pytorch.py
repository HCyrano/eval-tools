import sys
import numpy as np
import torch
import torch.nn as nn
from scipy.sparse import csr_matrix
from pathlib import Path

# --- Configuration du Device (Apple Silicon M4) ---
# Utilisation du backend MPS (Metal Performance Shaders) pour le GPU Apple
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print(f"🚀 Accélération activée sur : Apple M4 GPU (MPS)")
else:
    device = torch.device("cpu")
    print("⚠️ MPS non disponible, exécution sur CPU.")

# --- Paramètres de ligne de commande ---
if len(sys.argv) < 2:
    print("Usage: python solve_pytorch.py <stage_number>")
    sys.exit(1)

try:
    stage = int(sys.argv[1])
except ValueError:
    print("Erreur: Le numéro de stage doit être un entier.")
    sys.exit(1)

# Configuration des répertoires
n_index = 383697
DATA_DIR = Path("datas_norm")
WEIGHTS_DIR = Path("weights")
OCC_DIR = Path("n_occs")

WEIGHTS_DIR.mkdir(exist_ok=True)
OCC_DIR.mkdir(exist_ok=True)

data_in_path = DATA_DIR / f"data_norm_{stage:02}.txt"
weight_out = WEIGHTS_DIR / f"weight_{stage:02}.txt"
n_occ_out = OCC_DIR / f"n_occ_{stage:02}.txt"

# --- Chargement et préparation des données ---
rows, cols, data, scores = [], [], [], []
print(f"Lecture de {data_in_path}...")

try:
    with open(data_in_path, "r") as f:
        for i, line in enumerate(f):
            vals = list(map(int, line.split()))
            *indices, score = vals
            # Utilisation de np.unique pour agréger les doublons par ligne
            u, counts = np.unique(indices, return_counts=True)
            
            rows.extend([i] * len(u))
            cols.extend(u.tolist())
            data.extend(counts.tolist())
            scores.append(score)
except Exception as e:
    print(f"Erreur lors de la lecture du fichier : {e}")
    sys.exit(1)

n_rows = len(scores)
print(f"Matrice : {n_rows} lignes x {n_index} colonnes | {len(data)} valeurs non nulles")

# --- Calcul des occurrences (CPU via NumPy) ---
# Opération vectorisée rapide sur CPU avant de charger le GPU
A_cpu = csr_matrix((data, (rows, cols)), shape=(n_rows, n_index))
vecteur_occurrences = A_cpu.sum(axis=0).A.flatten()
np.savetxt(n_occ_out, vecteur_occurrences, fmt="%d")
print(f"Vecteur d'occurrences sauvegardé dans {n_occ_out}")

# --- Préparation PyTorch ---
print("Transfert de la matrice creuse vers la mémoire unifiée (MPS)...")
indices_torch = torch.LongTensor([rows, cols])
values_torch = torch.FloatTensor(data)
# Création d'un tenseur creux (Sparse COO) compatible avec MPS
A_coo = torch.sparse_coo_tensor(indices_torch, values_torch, size=(n_rows, n_index)).to(device)

# Conversion en CSR pour accélérer les produits matriciels répétés
# Le format CSR est optimisé pour les lignes (rows), ce qui accélère torch.mv
A_torch = A_coo.to_sparse_csr()

# Libération de la mémoire intermédiaire
del A_coo, indices_torch, values_torch

b_torch = torch.tensor(scores, dtype=torch.float32).to(device)

# Initialisation du vecteur de poids x (les paramètres à optimiser)
x = torch.zeros(n_index, requires_grad=True, device=device)

# --- Configuration de l'Optimiseur et du Early Stopping ---
optimizer = torch.optim.Adam([x], lr=0.1) 
criterion = nn.MSELoss()

patience = 50           # Nombre d'étapes sans amélioration avant l'arrêt
min_delta = 1e-6        # Seuil d'amélioration significative
best_loss = float('inf')
best_x = None
counter = 0             # Compteur de stagnation

print("\nDébut de la résolution par descente de gradient (Adam)...")

# Boucle d'entraînement
for step in range(5001): 
    optimizer.zero_grad()
    
    # Produit matrice-vecteur accéléré sur GPU M4
    y_pred = torch.mv(A_torch, x)
    
    # Calcul de l'erreur quadratique moyenne
    loss = criterion(y_pred, b_torch)
    loss.backward()
    optimizer.step()
    
    current_loss = loss.item()
    
    # Vérification de l'amélioration (Early Stopping)
    if current_loss < best_loss - min_delta:
        best_loss = current_loss
        # Sauvegarde d'une copie des meilleurs poids trouvés
        best_x = x.detach().clone()
        counter = 0 
    else:
        counter += 1
    
    if step % 100 == 0:
        print(f"Étape {step:4d} | Perte (MSE): {current_loss:.6f} | Stagnation: {counter}/{patience}")

    if counter >= patience:
        print(f"\n🛑 Arrêt prématuré à l'étape {step} : la précision s'est stabilisée.")
        break

# Récupération de la meilleure solution vers le CPU
x_final = best_x.cpu().numpy()

# --- Sauvegarde et Métriques Finales ---
np.savetxt(weight_out, x_final, fmt="%.6f")
print(f"Poids sauvegardés dans {weight_out}")

# Calcul des statistiques de précision sur CPU
y = np.array(scores)
y_pred_final = A_cpu @ x_final
residuals = y_pred_final - y

residual_norm = np.linalg.norm(residuals)
rmse = residual_norm / np.sqrt(len(y))
mae = np.mean(np.abs(residuals))
pseudo_R2 = 1 - (residual_norm**2) / (np.linalg.norm(y - np.mean(y))**2)

print("-" * 55)
print(f"RÉSULTATS FINAUX (Meilleure Perte : {best_loss:.6f})")
print(f"RMSE : {rmse:.6f}")
print(f"MAE  : {mae:.6f}")
print(f"Pseudo-R² : {pseudo_R2:.6f}")
print("-" * 55)

# Analyse de la distribution de l'erreur
N = len(residuals)
inc = 1
prev_mask = np.zeros_like(residuals, dtype=bool)
count_N = 0
while inc <= 128:
    mask = (residuals >= -inc) & (residuals <= inc)
    new_count = np.sum(mask & ~prev_mask)
    count_N += new_count
    print(f"Erreur dans [-{inc:3d}, {inc:3d}] : {new_count:6d} nouveaux ({ (count_N/N)*100 :.2f}%)")
    prev_mask = mask
    inc *= 2

print("\nTraitement terminé avec succès.")