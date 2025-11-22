#!/usr/bin/env python3
"""
LSQR implémenté en PyTorch (sparse, compatible Mac M1/M2/M3 via MPS quand disponible).

Usage:
    python solve_pytorch_lsqr.py <stage_number>

Remarques:
- Le script lit les fichiers 'datas_norm/data_norm_{stage:02}.txt' comme ton script d'origine.
- Sauvegarde les poids dans 'weights/weight_{stage:02}.txt'.
- Référence: ton script initial uploadé: /mnt/data/solve.py
"""
import sys
import time
from pathlib import Path
import numpy as np
import torch

# ----------------------------
# Device
# ----------------------------
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("Device: mps (Metal GPU)")
else:
    device = torch.device("cpu")
    print("Device: cpu")

# ----------------------------
# Arguments
# ----------------------------
if len(sys.argv) < 2:
    print("Usage: python solve_pytorch_lsqr.py <stage_number>")
    sys.exit(1)

try:
    stage = int(sys.argv[1])
except ValueError:
    print("Stage must be an integer")
    sys.exit(1)

DATA_DIR = Path("datas_norm")
WEIGHTS_DIR = Path("weights")
WEIGHTS_DIR.mkdir(exist_ok=True)

filename_in = DATA_DIR / f"data_norm_{stage:02}.txt"
filename_out = WEIGHTS_DIR / f"weight_{stage:02}.txt"

# ----------------------------
# Lecture du fichier -> COO lists
# ----------------------------
rows = []
cols = []
data = []
scores = []

print(f"Reading {filename_in} ...")
t0 = time.time()
with open(filename_in, "r") as f:
    for i, line in enumerate(f):
        parts = line.strip().split()
        if not parts:
            continue
        vals = list(map(int, parts))
        *indices, score = vals
        if len(indices) == 0:
            # still keep a score for a row, but no nonzeros
            scores.append(score)
            continue
        u, counts = np.unique(indices, return_counts=True)
        rows.extend([i] * len(u))
        cols.extend(u.tolist())
        data.extend(counts.tolist())
        scores.append(score)

t_read = time.time() - t0
print(f"Read finished in {t_read:.2f}s")
rows = np.array(rows, dtype=np.int64)
cols = np.array(cols, dtype=np.int64)
data = np.array(data, dtype=np.float32)
scores = np.array(scores, dtype=np.float32)

n_rows = len(scores)
n_cols = int(cols.max() + 1) if cols.size > 0 else 0
nnz = data.size
print(f"Matrix approx shape: ({n_rows}, {n_cols}), nnz={nnz}")

if n_rows == 0 or n_cols == 0:
    print("Empty matrix detected. Exiting.")
    sys.exit(0)

# ----------------------------
# Build sparse COO tensor on chosen device
# ----------------------------
t0 = time.time()
indices = torch.tensor(np.vstack((rows, cols)), dtype=torch.int64)
values = torch.tensor(data, dtype=torch.float32)
A = torch.sparse_coo_tensor(indices, values, size=(n_rows, n_cols), dtype=torch.float32)
# Try to put A on device; if backend cannot place sparse on device, we'll keep it on CPU but vectors on device.
try:
    A = A.coalesce().to(device)
    sparse_on_device = True
except Exception:
    # fallback: keep A on CPU (this is common for some backends), but move vectors to device
    A = A.coalesce().to("cpu")
    sparse_on_device = False

y = torch.tensor(scores, dtype=torch.float32, device=device)
t_build = time.time() - t0
print(f"Sparse tensor built in {t_build:.2f}s (sparse_on_device={sparse_on_device})")

# Helper functions for sparse-dense matmul that handle device fallbacks
def matvec_A(v):
    """Compute A @ v where v is dense vector (torch tensor) on device or cpu.
       Returns dense vector on same device as y.
    """
    # ensure v is 1D tensor on CPU if A is on CPU, else on device
    if not sparse_on_device:
        # move v to cpu for multiplication, then back to device
        v_cpu = v.detach().to("cpu")
        res_cpu = torch.sparse.mm(A, v_cpu.unsqueeze(1)).squeeze(1)
        return res_cpu.to(device)
    else:
        res = torch.sparse.mm(A, v.unsqueeze(1)).squeeze(1)
        # result will be on same device as A (hopefully device)
        if res.device != device:
            return res.to(device)
        return res

def matvec_AT(u):
    """Compute A^T @ u where u is dense vector (torch tensor) on device or cpu.
       Returns dense vector on same device as y.
    """
    if not sparse_on_device:
        u_cpu = u.detach().to("cpu")
        # build transpose sparse by swapping indices
        idx = A._indices()
        vals = A._values()
        # create sparse transpose on CPU
        trans_idx = torch.stack((idx[1], idx[0]), dim=0)
        A_T = torch.sparse_coo_tensor(trans_idx, vals, size=(n_cols, n_rows))
        res_cpu = torch.sparse.mm(A_T.coalesce(), u_cpu.unsqueeze(1)).squeeze(1)
        return res_cpu.to(device)
    else:
        idx = A._indices()
        vals = A._values()
        trans_idx = torch.stack((idx[1], idx[0]), dim=0)
        A_T = torch.sparse_coo_tensor(trans_idx, vals, size=(n_cols, n_rows)).coalesce().to(A.device)
        res = torch.sparse.mm(A_T, u.unsqueeze(1)).squeeze(1)
        if res.device != device:
            return res.to(device)
        return res

# ----------------------------
# LSQR iterative solver (implementation simple & robust)
# Based on bidiagonalization (Golub-Kahan) with updates.
# Stopping criteria: max_iter, tolerance on residual norm or small beta/alpha.
# ----------------------------
def lsqr_torch(A_matvec, A_transpose_matvec, b, max_iter=2000, atol=1e-6, btol=1e-6, verbose=False):
    """
    LSQR implementation that only uses A_matvec(v) and A_transpose_matvec(u).
    b: torch.tensor (device)
    Returns x (numpy array on CPU), info dict
    """
    device_local = b.device
    m = b.shape[0]
    n = n_cols

    x = torch.zeros(n, dtype=torch.float32, device=device_local)

    # initialize
    u = b.clone()
    beta = torch.norm(u).item()
    if beta > 0:
        u = u / beta
    else:
        # zero rhs -> solution zero
        return x.cpu().numpy(), {"iter": 0, "beta": 0.0, "resid_norm": 0.0}

    v = A_transpose_matvec(u)
    alpha = torch.norm(v).item()
    if alpha > 0:
        v = v / alpha
    else:
        # A^T b == 0 => x=0
        return x.cpu().numpy(), {"iter": 0, "alpha": 0.0, "resid_norm": beta}

    w = v.clone()

    phi_bar = beta
    rho_bar = alpha

    # variables for stopping
    normr = beta
    normA = 0.0
    normA2 = 0.0
    normx = 0.0

    for it in range(1, max_iter + 1):
        # bidiagonalization step
        # u = A v - alpha u
        u = A_matvec(v) - (alpha * u)
        beta = torch.norm(u).item()
        if beta > 0:
            u = u / beta

        v = A_transpose_matvec(u) - (beta * v)
        alpha = torch.norm(v).item()
        if alpha > 0:
            v = v / alpha

        # update norms
        normA2 = normA2 + alpha * alpha + beta * beta
        normA = np.sqrt(normA2)

        # apply previous rotation
        rho = np.sqrt(rho_bar * rho_bar + beta * beta)
        if rho == 0:
            c = 1.0
            s = 0.0
        else:
            c = rho_bar / rho
            s = beta / rho

        theta = s * alpha
        rho_bar = -c * alpha
        phi = c * phi_bar
        phi_bar = s * phi_bar

        # update x and w
        # x = x + (phi / rho) * w
        x = x + (phi / rho) * w
        # w = v - (theta / rho) * w
        w = v - (theta / rho) * w

        # residual norm estimate
        normr = abs(phi_bar)

        # stopping conditions (similar to scipy's lsqr)
        # check if residual small relative to b norm
        if verbose and (it % 10 == 0 or it == 1):
            print(f"it={it}, est_resid={normr:.4e}, alpha={alpha:.4e}, beta={beta:.4e}")

        if normr <= (atol * torch.norm(b).item() + btol):
            break

    # final residual computed on device
    # compute residual = A @ x - b
    Ax = A_matvec(x)
    resid_vec = Ax - b
    resid_norm = torch.norm(resid_vec).item()

    info = {
        "iter": it,
        "resid_norm": resid_norm,
        "est_resid": normr,
        "normA": normA,
    }
    return x.cpu().detach().numpy(), info

# ----------------------------
# Run LSQR
# ----------------------------
print("\nRunning LSQR...")
t0 = time.time()
x_vec, info = lsqr_torch(matvec_A, matvec_AT, y, max_iter=5000, atol=1e-6, btol=1e-6, verbose=True)
t_solve = time.time() - t0
print(f"LSQR finished in {t_solve:.2f}s, iterations={info['iter']}, resid_norm={info['resid_norm']:.6e}")

# ----------------------------
# Save solution
# ----------------------------
np.savetxt(filename_out, x_vec, fmt="%.6f")
print(f"Saved weights -> {filename_out}")

# ----------------------------
# Compute metrics (on CPU numpy)
# ----------------------------
print("\nEvaluation metrics (CPU)...")
x_torch = torch.from_numpy(x_vec).to(device)
y_pred = matvec_A(x_torch).cpu().numpy()
residuals = y_pred - scores
resid_norm = np.linalg.norm(residuals)
rmse = resid_norm / np.sqrt(len(scores))
mae = np.mean(np.abs(residuals))
baseline_norm = np.linalg.norm(scores - np.mean(scores))
pseudo_R2 = 1 - (resid_norm**2) / (baseline_norm**2) if baseline_norm != 0 else np.nan

print(f"||Ax - scores||_2 = {resid_norm:.6f}")
print(f"RMSE = {rmse:.6f}")
print(f"MAE  = {mae:.6f}")
print(f"Pseudo-R^2 = {pseudo_R2:.6f}")

print("\nDone.")
