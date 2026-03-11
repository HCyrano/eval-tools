import sys
import numpy as np
import pickle
from scipy.sparse import csr_matrix
from pathlib import Path
from time import time

# =============================================================================
# Factorization Machine — SGD sur V uniquement, w linéaires FIXES
# lr avec décroissance exponentielle + early stopping
# =============================================================================

def fmt_time(seconds):
    if seconds < 60:
        return f"{seconds:.1f}s"
    m, s = divmod(int(seconds), 60)
    if m < 60:
        return f"{m}m{s:02d}s"
    h, m = divmod(m, 60)
    return f"{h}h{m:02d}m{s:02d}s"


class FMRegression:
    def __init__(self, rank=8, n_iter=100, lr=0.02, lr_decay=0.95,
                 l2_reg_V=0.001, random_state=None,
                 w_init=None, w0_init=0.0, batch_size=2048,
                 early_stopping=10, min_delta=0.0001):
        self.rank           = rank
        self.n_iter         = n_iter
        self.lr             = lr
        self.lr_decay       = lr_decay
        self.l2_reg_V       = l2_reg_V
        self.random_state   = random_state
        self.w_init         = w_init
        self.w0_init        = w0_init
        self.batch_size     = batch_size
        self.early_stopping = early_stopping  # nb iters sans amélioration
        self.min_delta      = min_delta        # gain minimum significatif

    def _fm_predict(self, X):
        X2   = X.copy(); X2.data **= 2
        XV   = X.dot(self.V_.T)
        V2   = self.V_ ** 2
        X2V2 = X2.dot(V2.T)
        inter = 0.5 * np.sum(XV ** 2 - X2V2, axis=1)
        return X.dot(self.w_) + self.w0_ + inter

    def predict(self, X):
        return self._fm_predict(X.astype(np.float64))

    def fit(self, X, y):
        t_fit_start = time()
        n, p = X.shape
        rng  = np.random.RandomState(self.random_state)

        self.w_  = (self.w_init.copy().astype(np.float64)
                    if self.w_init is not None else np.zeros(p))
        self.w0_ = float(self.w0_init)

        X  = X.astype(np.float64)
        X2 = X.copy(); X2.data **= 2

        active_cols = np.unique(X.nonzero()[1])
        print(f"  Features actives : {len(active_cols)} / {p}")

        self.V_ = np.zeros((self.rank, p), dtype=np.float64)
        self.V_[:, active_cols] = rng.normal(0, 0.01, (self.rank, len(active_cols)))

        r_linear  = y - (X.dot(self.w_) + self.w0_)
        rmse_base = np.sqrt(np.mean(r_linear ** 2))
        print(f"  RMSE baseline linéaire : {rmse_base:.6f}")
        print(f"  lr={self.lr:.4f}  decay={self.lr_decay:.3f}  "
              f"lr_final≈{self.lr * self.lr_decay**(self.n_iter-1):.5f}  "
              f"early_stopping={self.early_stopping}  min_delta={self.min_delta}")

        best_rmse     = rmse_base
        best_V        = self.V_.copy()
        lr            = self.lr
        no_improve    = 0          # compteur iters sans amélioration

        for it in range(self.n_iter):
            t_iter = time()
            idx    = rng.permutation(n)
            total_loss = 0.0

            for start in range(0, n, self.batch_size):
                batch = idx[start:start + self.batch_size]
                Xb    = X[batch]
                X2b   = X2[batch]

                XVb     = Xb.dot(self.V_.T)
                V2      = self.V_ ** 2
                X2V2b   = X2b.dot(V2.T)
                inter_b = 0.5 * np.sum(XVb ** 2 - X2V2b, axis=1)

                yhat_b = Xb.dot(self.w_) + self.w0_ + inter_b
                err_b  = yhat_b - y[batch]
                total_loss += np.sum(err_b ** 2)

                for f in range(self.rank):
                    xvf = XVb[:, f]
                    g   = (Xb.T.dot(err_b * xvf)
                           - X2b.T.dot(err_b) * self.V_[f])
                    g   = np.asarray(g).flatten()
                    self.V_[f] -= lr * (g / len(batch) + self.l2_reg_V * self.V_[f])

                self.V_ = np.clip(self.V_, -20, 20)

            rmse       = np.sqrt(total_loss / n)
            gain       = rmse_base - rmse
            t_iter_dur = time() - t_iter
            t_elapsed  = time() - t_fit_start
            t_remain   = t_iter_dur * (self.n_iter - it - 1)

            # Early stopping bookkeeping
            if rmse < best_rmse - self.min_delta:
                best_rmse  = rmse
                best_V     = self.V_.copy()
                no_improve = 0
                marker     = ""
            else:
                no_improve += 1
                marker     = f"  [sans amélioration : {no_improve}/{self.early_stopping}]"

            print(f"  iter {it+1:3d}/{self.n_iter} — RMSE : {rmse:.6f}  "
                  f"(gain : {gain:+.6f})  lr={lr:.5f}  "
                  f"[{fmt_time(t_iter_dur)}/iter  "
                  f"écoulé:{fmt_time(t_elapsed)}  "
                  f"restant:~{fmt_time(t_remain)}]"
                  f"{marker}")

            if no_improve >= self.early_stopping:
                print(f"\n  *** Early stopping à iter {it+1} "
                      f"({self.early_stopping} iters sans gain > {self.min_delta}) ***")
                break

            lr *= self.lr_decay

        t_total = time() - t_fit_start
        self.V_ = best_V
        print(f"\n  Meilleur RMSE train : {best_rmse:.6f}  "
              f"(gain : {rmse_base - best_rmse:+.6f})  "
              f"durée totale : {fmt_time(t_total)}")
        return self


# =============================================================================
# Script principal
# =============================================================================

N_INDEX     = 383745
TRAIN_RATIO = 0.80
WEIGHTS_DIR = Path("weights")


def compter_occurrences_par_index(A_csr):
    return np.asarray(A_csr.sum(axis=0)).flatten()


def calculer_metriques_fm(model, matrice, cibles, nom_set):
    if len(cibles) == 0:
        return None
    t0        = time()
    y_pred    = model.predict(matrice)
    residuals = y_pred - cibles

    residual_norm = np.linalg.norm(residuals)
    rmse = residual_norm / np.sqrt(len(cibles))
    mae  = np.mean(np.abs(residuals))

    y_mean        = np.mean(cibles)
    baseline_norm = np.linalg.norm(cibles - y_mean)
    pseudo_R2     = 1 - (residual_norm**2) / (baseline_norm**2) if baseline_norm != 0 else 0

    print(f"\n--- Métriques {nom_set} (Factorization Machine) ---")
    print(f"RMSE      : {rmse:.6f}")
    print(f"MAE       : {mae:.6f}")
    print(f"Pseudo-R² : {pseudo_R2:.6f}")
    print(f"Temps predict : {fmt_time(time()-t0)}")
    return residuals


# --- Arguments ---
if len(sys.argv) < 2:
    print("Usage: python solve_FM.py <stage_number>")
    sys.exit(1)

try:
    stage = int(sys.argv[1])
    np.random.seed(stage)
except ValueError:
    print("Erreur: Le numéro de stage doit être un entier.")
    sys.exit(1)

t_global = time()

# --- Chemins ---
DATA_DIR   = Path("datas")
MODELS_DIR = Path("models_fm")
OCC_DIR    = Path("n_occs")
for d in [MODELS_DIR, OCC_DIR]:
    d.mkdir(exist_ok=True)

data_in_path = DATA_DIR    / f"data_{stage:02}.txt"
model_out    = MODELS_DIR  / f"model_fm_{stage:02}.pkl"
n_occ_out    = OCC_DIR     / f"n_occ_{stage:02}.txt"
weight_in    = WEIGHTS_DIR / f"weight_{stage:02}.txt"

# --- Poids linéaires ---
w_init = None
if weight_in.exists():
    print(f"Chargement des poids linéaires depuis {weight_in}...")
    w_init = np.loadtxt(weight_in)
    print(f"  {(w_init != 0).sum()} poids non-nuls sur {len(w_init)}")
else:
    print(f"⚠️  {weight_in} introuvable.")

# --- Données ---
t0 = time()
rows, cols, data, scores = [], [], [], []
row_count = 0
print(f"Chargement de {data_in_path}...")
try:
    with open(data_in_path, "r") as f:
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
print(f"Chargement : {fmt_time(time()-t0)}")

# --- Train / Validation ---
n_samples = A.shape[0]
if stage < 9:
    print(f"Log: Stage {stage} < 9 -> Mode 100% Train")
    idx_train = np.arange(n_samples)
    idx_val   = np.array([], dtype=int)
else:
    indices_shuffled = np.random.permutation(n_samples)
    split_idx        = int(n_samples * TRAIN_RATIO)
    idx_train        = indices_shuffled[:split_idx]
    idx_val          = indices_shuffled[split_idx:]

A_train      = A[idx_train, :]
scores_train = scores[idx_train]
A_val        = A[idx_val,   :]
scores_val   = scores[idx_val]

print(f"Données : {len(idx_train)} train / {len(idx_val)} validation")

vecteur_occurrences_complet = compter_occurrences_par_index(A)
np.savetxt(n_occ_out, vecteur_occurrences_complet, fmt="%d")

# --- Entraînement ---
print("Entraînement FM (SGD sur V, w fixes)...")
fm = FMRegression(
    n_iter          = 100,
    rank            = 8,
    lr              = 0.02,
    lr_decay        = 0.95,
    l2_reg_V        = 0.001,
    random_state    = stage,
    w_init          = w_init,
    w0_init         = 0.0,
    batch_size      = 2048,
    early_stopping  = 10,
    min_delta       = 0.0001,
)
fm.fit(A_train, scores_train)

# --- Évaluation ---
res_train = calculer_metriques_fm(fm, A_train, scores_train, "TRAIN")
res_val   = calculer_metriques_fm(fm, A_val,   scores_val,   "VALIDATION")

# --- Sauvegarde ---
with open(model_out, "wb") as f:
    pickle.dump(fm, f)
print(f"Modèle sauvegardé dans {model_out}")

# --- Analyse des résidus ---
res_a_analyser = res_val if res_val is not None else res_train
if res_a_analyser is not None:
    print(f"\nAnalyse de la précision :")
    N_total   = len(res_a_analyser)
    inc       = 1
    prev_mask = np.zeros_like(res_a_analyser, dtype=bool)
    while inc <= 128:
        mask         = (res_a_analyser >= -inc) & (res_a_analyser <= inc)
        new_elements = np.sum(mask & ~prev_mask)
        pct          = (np.sum(mask) / N_total) * 100
        print(f"Erreur dans [-{inc:3}, {inc:3}] : {new_elements:6} nouveaux (Total: {pct:6.2f}%)")
        prev_mask = mask
        inc *= 2

print(f"\n[OK] Stage {stage} terminé en {fmt_time(time()-t_global)}")
