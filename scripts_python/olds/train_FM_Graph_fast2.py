"""
train_FM_Graph_fast.py  —  FM global pour Roxane (moteur Othello)
=================================================================
Identique a train_FM_Graph.py avec une seule optimisation :
  adam_step et fm_predict compiles avec numba @njit -> gain ~3x a 5x

Prerequis :
  pip install numba

Premier lancement : ~30s de compilation JIT (cache=True -> 1 seule fois)
Lancements suivants : demarrage immediat depuis le cache.

Usage :
  python train_FM_Graph_fast.py --epochs 20 --rank 16 --preload
  python train_FM_Graph_fast.py --epochs 20 --resume --preload
  python train_FM_Graph_fast.py --epochs 3 --stages 30-39
"""

import argparse
import numpy as np
import pickle
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from time import time
from numba import njit

# =============================================================================
# Config
# =============================================================================

N_INDEX  = 383745
N_STAGES = 60

DATA_DIR    = Path("datas")
WEIGHTS_DIR = Path("weights")
MODELS_DIR  = Path("models_fm")
MODELS_DIR.mkdir(exist_ok=True)

CHECKPOINT = MODELS_DIR / "fm_global_checkpoint.pkl"
MODEL_PKL  = MODELS_DIR / "model_fm_global.pkl"
FM_W0_TXT  = MODELS_DIR / "fm_w0.txt"
FM_V_BIN   = MODELS_DIR / "fm_V.bin"

SCALE = 256


# =============================================================================
# Utilitaire temps
# =============================================================================

def fmt_time(seconds):
    if seconds < 60:
        return f"{seconds:.1f}s"
    m, s = divmod(int(seconds), 60)
    if m < 60:
        return f"{m}m{s:02d}s"
    h, m = divmod(m, 60)
    return f"{h}h{m:02d}m{s:02d}s"


# =============================================================================
# Chargement des poids lineaires par stage (figes)
# =============================================================================

def charger_weights(stages):
    print(f"\nChargement des poids lineaires depuis {WEIGHTS_DIR}/...")
    w_by_stage = {}
    manquants  = []
    for stage in stages:
        path = WEIGHTS_DIR / f"weight_{stage:02}.txt"
        if path.exists():
            w_by_stage[stage] = np.loadtxt(path, dtype=np.float32)
            nnz = (w_by_stage[stage] != 0).sum()
            print(f"  stage {stage:02d} : {nnz:>8,} poids non-nuls / {N_INDEX}")
        else:
            w_by_stage[stage] = np.zeros(N_INDEX, dtype=np.float32)
            manquants.append(stage)
    if manquants:
        print(f"  Fichiers manquants (vecteur nul) : stages {manquants}")
    return w_by_stage


# =============================================================================
# Chargement des donnees
# =============================================================================

def charger_stage(stage):
    path = DATA_DIR / f"data_{stage:02}.txt"
    if not path.exists():
        return None, None, None

    indices_list, counts_list, scores_list = [], [], []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            vals    = list(map(int, line.split()))
            idx_raw = vals[:-1]
            score   = vals[-1]
            u, c    = np.unique(idx_raw, return_counts=True)
            indices_list.append(u.astype(np.int32))
            counts_list.append(c.astype(np.float32))
            scores_list.append(score)

    if not indices_list:
        return None, None, None

    K = max(len(u) for u in indices_list)
    n = len(scores_list)
    indices_mat = np.zeros((n, K), dtype=np.int32)
    counts_mat  = np.zeros((n, K), dtype=np.float32)
    for i, (u, c) in enumerate(zip(indices_list, counts_list)):
        indices_mat[i, :len(u)] = u
        counts_mat[i,  :len(u)] = c

    return (indices_mat,
            counts_mat,
            np.array(scores_list, dtype=np.float32))


# =============================================================================
# Prechargement
# =============================================================================

def preload_all(stages):
    print(f"\nPrechargement de {len(stages)} stages en RAM...")
    t0 = time()

    data_by_stage = {}
    K_global = 0
    for stage in stages:
        t_s = time()
        idx, cnt, sc = charger_stage(stage)
        if idx is None:
            continue
        data_by_stage[stage] = (idx, cnt, sc)
        K_global = max(K_global, idx.shape[1])
        print(f"  stage {stage:02d} : {len(sc):>9,} lignes  K={idx.shape[1]}  ({fmt_time(time()-t_s)})")

    all_indices, all_counts, all_scores, all_stage_ids = [], [], [], []
    for stage, (idx, cnt, sc) in data_by_stage.items():
        n, K = idx.shape
        if K < K_global:
            idx_pad = np.zeros((n, K_global), dtype=np.int32)
            cnt_pad = np.zeros((n, K_global), dtype=np.float32)
            idx_pad[:, :K] = idx
            cnt_pad[:, :K] = cnt
            idx, cnt = idx_pad, cnt_pad
        all_indices.append(idx)
        all_counts.append(cnt)
        all_scores.append(sc)
        all_stage_ids.append(np.full(len(sc), stage, dtype=np.int32))

    all_indices   = np.concatenate(all_indices,   axis=0)
    all_counts    = np.concatenate(all_counts,    axis=0)
    all_scores    = np.concatenate(all_scores,    axis=0)
    all_stage_ids = np.concatenate(all_stage_ids, axis=0)

    mem_go = (all_indices.nbytes + all_counts.nbytes +
              all_scores.nbytes + all_stage_ids.nbytes) / 1e9
    print(f"Total : {len(all_scores):,} lignes  K_global={K_global}  "
          f"  {mem_go:.2f} Go  ({fmt_time(time()-t0)})")
    return all_indices, all_counts, all_scores, all_stage_ids


# =============================================================================
# Prediction FM — compile numba (cache=True : compilee une seule fois)
# =============================================================================

@njit(cache=True)
def fm_predict(indices_mat, counts_mat, w_stage, w0_stage, V):
    """
    indices_mat : (n, K)  int32
    counts_mat  : (n, K)  float32
    w_stage     : (N_INDEX,) float32
    w0_stage    : float32
    V           : (rank, N_INDEX) float32
    """
    n    = indices_mat.shape[0]
    K    = indices_mat.shape[1]
    rank = V.shape[0]
    out  = np.empty(n, dtype=np.float32)

    for i in range(n):
        # Partie lineaire
        lin = w0_stage
        for k in range(K):
            lin += counts_mat[i, k] * w_stage[indices_mat[i, k]]

        # Partie FM
        inter = np.float32(0.0)
        for r in range(rank):
            s1 = np.float32(0.0)
            s2 = np.float32(0.0)
            for k in range(K):
                v  = V[r, indices_mat[i, k]] * counts_mat[i, k]
                s1 += v
                s2 += v * v
            inter += s1 * s1 - s2
        out[i] = lin + np.float32(0.5) * inter

    return out


# =============================================================================
# Step Adam — compile numba
# Identique a l'original, traduit en style numba-compatible (pas de np.unique)
# =============================================================================

@njit(cache=True)
def adam_step(indices_b, counts_b, scores_b, w_stage, w0_stage, V,
              m_V, v_V, m_w0, v_w0, lr, l2_V, t,
              beta1=0.9, beta2=0.999, eps=1e-8):
    """
    indices_b : (b, K) int32
    counts_b  : (b, K) float32
    V         : (rank, N_INDEX) float32  — modifie en place
    m_V, v_V  : (rank, N_INDEX) float32  — modifie en place
    """
    b    = indices_b.shape[0]
    K    = indices_b.shape[1]
    rank = V.shape[0]

    # --- Forward + erreur ---
    yhat = fm_predict(indices_b, counts_b, w_stage, w0_stage, V)
    err  = yhat - scores_b   # (b,)

    # --- Gradient w0 ---
    g_w0 = np.float32(0.0)
    for i in range(b):
        g_w0 += err[i]
    g_w0 /= b

    m_w0   = beta1 * m_w0 + (1.0 - beta1) * g_w0
    v_w0   = beta2 * v_w0 + (1.0 - beta2) * g_w0 * g_w0
    m_w0_h = m_w0 / (1.0 - beta1 ** t)
    v_w0_h = v_w0 / (1.0 - beta2 ** t)
    w0_stage -= lr * m_w0_h / (np.sqrt(v_w0_h) + eps)

    # --- Gradient V : accumulation sparse ---
    # On collecte les indices uniques du batch
    flat_len = b * K
    flat_idx = np.empty(flat_len, dtype=np.int32)
    for i in range(b):
        for k in range(K):
            flat_idx[i * K + k] = indices_b[i, k]

    # Tri pour trouver les uniques (equivalent np.unique sans return_inverse)
    flat_sorted = np.sort(flat_idx)
    n_uniq = 1
    for i in range(1, flat_len):
        if flat_sorted[i] != flat_sorted[i - 1]:
            n_uniq += 1

    uniq = np.empty(n_uniq, dtype=np.int32)
    uniq[0] = flat_sorted[0]
    ui = 1
    for i in range(1, flat_len):
        if flat_sorted[i] != flat_sorted[i - 1]:
            uniq[ui] = flat_sorted[i]
            ui += 1

    # grad_small : (rank, n_uniq)
    grad_small = np.zeros((rank, n_uniq), dtype=np.float32)

    # Calcul sum_cV par sample
    sum_cV = np.zeros((b, rank), dtype=np.float32)
    for i in range(b):
        for k in range(K):
            c = counts_b[i, k]
            if c == 0.0:
                continue
            idx = indices_b[i, k]
            for r in range(rank):
                sum_cV[i, r] += c * V[r, idx]

    # Accumulation du gradient dans grad_small
    for i in range(b):
        e_i = err[i] / b
        for k in range(K):
            c = counts_b[i, k]
            if c == 0.0:
                continue
            idx = indices_b[i, k]
            # Position de idx dans uniq (recherche binaire)
            lo, hi = 0, n_uniq - 1
            while lo < hi:
                mid = (lo + hi) // 2
                if uniq[mid] < idx:
                    lo = mid + 1
                else:
                    hi = mid
            ui2 = lo
            for r in range(rank):
                h_ik = c * (sum_cV[i, r] - c * V[r, idx])
                grad_small[r, ui2] += e_i * h_ik

    # Gradient clipping
    grad_norm = np.float32(0.0)
    for r in range(rank):
        for j in range(n_uniq):
            grad_norm += grad_small[r, j] * grad_small[r, j]
    grad_norm = np.sqrt(grad_norm)
    if grad_norm > 10.0:
        scale = np.float32(10.0) / grad_norm
        for r in range(rank):
            for j in range(n_uniq):
                grad_small[r, j] *= scale

    # Mise a jour Adam sur les colonnes actives uniquement
    bc1 = np.float32(1.0) - np.float32(beta1) ** t
    bc2 = np.float32(1.0) - np.float32(beta2) ** t
    for j in range(n_uniq):
        col = uniq[j]
        for r in range(rank):
            g = grad_small[r, j]
            m_V[r, col] = beta1 * m_V[r, col] + (1.0 - beta1) * g
            v_V[r, col] = beta2 * v_V[r, col] + (1.0 - beta2) * g * g
            m_h = m_V[r, col] / bc1
            v_h = v_V[r, col] / bc2
            V[r, col] -= lr * (m_h / (np.sqrt(v_h) + eps) + l2_V * V[r, col])
            if V[r, col] >  10.0: V[r, col] =  np.float32(10.0)
            if V[r, col] < -10.0: V[r, col] = np.float32(-10.0)

    # MSE
    mse = np.float32(0.0)
    for i in range(b):
        mse += err[i] * err[i]
    mse /= b

    return w0_stage, m_w0, v_w0, mse


# =============================================================================
# Export int16
# =============================================================================

def to_int16(arr):
    return np.round(arr * SCALE).clip(-32768, 32767).astype(np.int16)


def export_fixed_point(w0_vec, V, stages):
    w0_ints = {s: int(round(w0_vec[s] * SCALE)) for s in stages}
    with open(FM_W0_TXT, "w") as f:
        for s in range(N_STAGES):
            f.write(f"{w0_ints.get(s, 0)}\n")

    V_aos = to_int16(V).T  # (N_INDEX, rank)
    V_aos.tofile(FM_V_BIN)

    rank    = V.shape[0]
    size_mb = (V.size * 2) / 1024 ** 2
    print(f"  Export int16 x256 :")
    print(f"    {FM_W0_TXT}  ({N_STAGES} lignes, une par stage)")
    print(f"    {FM_V_BIN}   ({rank}x{N_INDEX} int16, {size_mb:.1f} Mo)")
    V_err = np.max(np.abs(V - to_int16(V).astype(np.float32) / SCALE))
    print(f"    Erreur quant. max V : {V_err:.6f}")


# =============================================================================
# Warmup JIT (compile une fois avant la boucle)
# =============================================================================

def warmup_jit(rank):
    """Declenche la compilation numba avec un mini-batch factice."""
    print("  Compilation JIT numba (cache=True, une seule fois)...")
    t0 = time()
    b_dummy  = np.zeros((4, 5),  dtype=np.int32)
    c_dummy  = np.zeros((4, 5),  dtype=np.float32)
    s_dummy  = np.zeros(4,       dtype=np.float32)
    w_dummy  = np.zeros(N_INDEX, dtype=np.float32)
    V_dummy  = np.zeros((rank, N_INDEX), dtype=np.float32)
    mV_dummy = np.zeros_like(V_dummy)
    vV_dummy = np.zeros_like(V_dummy)
    fm_predict(b_dummy, c_dummy, w_dummy, np.float32(0.0), V_dummy)
    adam_step(b_dummy, c_dummy, s_dummy, w_dummy, np.float32(0.0),
              V_dummy, mV_dummy, vV_dummy,
              np.float32(0.0), np.float32(0.0),
              np.float32(0.001), np.float32(0.001), np.int64(1))
    print(f"  JIT pret en {fmt_time(time()-t0)}")


# =============================================================================
# Main
# =============================================================================

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--epochs",         type=int,   default=20)
    p.add_argument("--rank",           type=int,   default=16)
    p.add_argument("--lr",             type=float, default=0.001)
    p.add_argument("--lr_decay",       type=float, default=1.0,
                   help="Multiplicateur lr par epoque")
    p.add_argument("--l2_V",           type=float, default=0.001)
    p.add_argument("--batch",          type=int,   default=4096)
    p.add_argument("--stages",         type=str,   default=f"0-{N_STAGES-1}")
    p.add_argument("--resume",         action="store_true")
    p.add_argument("--seed",           type=int,   default=42)
    p.add_argument("--preload",        action="store_true")
    p.add_argument("--early_stopping", type=int,   default=5,
                   help="Arret si pas d'amelioration sur N epoques consecutives")
    p.add_argument("--min_delta",      type=float, default=0.0001,
                   help="Gain minimum considere comme amelioration")
    p.add_argument("--val_split",      type=float, default=0.1,
                   help="Fraction des donnees reservee a la validation (defaut: 0.1)")
    return p.parse_args()


def parse_stages(s):
    if "-" in s and "," not in s:
        a, b = s.split("-")
        return list(range(int(a), int(b) + 1))
    return [int(x) for x in s.split(",")]


def main():
    args     = parse_args()
    rng      = np.random.RandomState(args.seed)
    t_global = time()
    stages   = [s for s in parse_stages(args.stages)
                if (DATA_DIR / f"data_{s:02}.txt").exists()]

    if not stages:
        print("Aucun fichier data trouve. Lance depuis le repertoire Evaluation/")
        return

    print(f"Stages : {len(stages)}  ({stages[0]}..{stages[-1]})")
    print(f"rank={args.rank}  lr={args.lr}  decay={args.lr_decay}  "
          f"l2_V={args.l2_V}  batch={args.batch}  "
          f"preload={'oui' if args.preload else 'non'}")
    print(f"early_stopping={args.early_stopping}  min_delta={args.min_delta}  "
          f"val_split={args.val_split:.0%}")

    # --- Chargement des poids lineaires figes ---
    w_by_stage = charger_weights(stages)

    # --- Prechargement donnees ---
    if args.preload:
        all_indices, all_counts, all_scores, all_stage_ids = preload_all(stages)
        n_total = len(all_scores)

        # --- Split train / val (90/10) reproductible ---
        val_n   = int(n_total * args.val_split)
        perm_tv = rng.permutation(n_total)
        val_idx   = perm_tv[:val_n]
        train_idx = perm_tv[val_n:]

        val_indices   = all_indices[val_idx]
        val_counts    = all_counts[val_idx]
        val_scores    = all_scores[val_idx]
        val_stage_ids = all_stage_ids[val_idx]

        all_indices   = all_indices[train_idx]
        all_counts    = all_counts[train_idx]
        all_scores    = all_scores[train_idx]
        all_stage_ids = all_stage_ids[train_idx]
        n_total       = len(all_scores)

        print(f"Split : {n_total:,} train  /  {val_n:,} val  "
              f"({100*(1-args.val_split):.0f}/{100*args.val_split:.0f})")

    # --- Baseline ---
    if not (args.resume and CHECKPOINT.exists()):
        print("\nRMSE baseline (poids lineaires seuls)...")
        total_mse_base = 0.0
        total_n_base   = 0
        for stage in stages:
            idx, cnt, sc = charger_stage(stage)
            if idx is None:
                continue
            yhat = (cnt * w_by_stage[stage][idx]).sum(axis=1)
            total_mse_base += np.sum((yhat - sc) ** 2)
            total_n_base   += len(sc)
        print(f"  RMSE baseline : {np.sqrt(total_mse_base / total_n_base):.6f}\n")

    # --- Init ou reprise ---
    if args.resume and CHECKPOINT.exists():
        print(f"\nReprise depuis {CHECKPOINT}")
        with open(CHECKPOINT, "rb") as f:
            ckpt = pickle.load(f)
        w0_vec      = ckpt["w0_vec"]
        V           = ckpt["V"]
        start_epoch = ckpt["epoch"] + 1
        best_rmse   = ckpt.get("best_rmse", float("inf"))
        no_improve  = ckpt.get("no_improve", 0)
        lr          = ckpt.get("lr", args.lr)
        adam_t      = ckpt.get("adam_t", 1)
        m_V         = ckpt.get("m_V",  np.zeros_like(V))
        v_V         = ckpt.get("v_V",  np.zeros_like(V))
        m_w0        = ckpt.get("m_w0", np.zeros(N_STAGES, dtype=np.float32))
        v_w0        = ckpt.get("v_w0", np.zeros(N_STAGES, dtype=np.float32))
        print(f"  Epoque {start_epoch}, RMSE={best_rmse:.6f}, "
              f"no_improve={no_improve}, lr={lr:.6f}, adam_t={adam_t}")
    else:
        print("\nInitialisation...")
        w0_vec = np.zeros(N_STAGES, dtype=np.float32)
        V      = np.zeros((args.rank, N_INDEX), dtype=np.float32)
        active_cols = np.unique(
            np.concatenate([np.where(w_by_stage[s] != 0)[0] for s in stages]))
        V[:, active_cols] = rng.normal(0, 0.01, (args.rank, len(active_cols))).astype(np.float32)
        print(f"  Colonnes actives : {len(active_cols):,} / {N_INDEX}  "
              f"({100*len(active_cols)/N_INDEX:.1f}%)")
        m_V         = np.zeros_like(V)
        v_V         = np.zeros_like(V)
        m_w0        = np.zeros(N_STAGES, dtype=np.float32)
        v_w0        = np.zeros(N_STAGES, dtype=np.float32)
        adam_t      = 1
        start_epoch = 0
        best_rmse   = float("inf")
        no_improve  = 0
        lr          = args.lr

    # --- Warmup JIT (compile numba avant la boucle) ---
    print("\nInitialisation JIT...")
    warmup_jit(args.rank)

    # =========================================================================
    # Boucle epochs — identique a l'original
    # =========================================================================
    for epoch in range(start_epoch, args.epochs):
        t_epoch   = time()
        total_mse = 0.0
        total_n   = 0

        print(f"\n{'='*60}")
        print(f"Epoque {epoch+1}/{args.epochs}  lr={lr:.6f}")
        print(f"{'='*60}")

        if args.preload:
            perm      = rng.permutation(n_total)
            n_batches = (n_total + args.batch - 1) // args.batch
            log_every = max(1, n_batches // 10)

            for bi, start in enumerate(range(0, n_total, args.batch)):
                batch     = perm[start:start + args.batch]
                indices_b = all_indices[batch]
                counts_b  = all_counts[batch]
                scores_b  = all_scores[batch]
                stage_ids = all_stage_ids[batch]

                for stage in np.unique(stage_ids):
                    mask     = stage_ids == stage
                    idx_s    = indices_b[mask]
                    cnt_s    = counts_b[mask]
                    scores_s = scores_b[mask]

                    w0_new, m_w0_new, v_w0_new, mse = adam_step(
                        idx_s, cnt_s, scores_s,
                        w_by_stage[stage], np.float32(w0_vec[stage]),
                        V, m_V, v_V,
                        np.float32(m_w0[stage]), np.float32(v_w0[stage]),
                        np.float32(lr), np.float32(args.l2_V), np.int64(adam_t)
                    )
                    w0_vec[stage]  = w0_new
                    m_w0[stage]    = m_w0_new
                    v_w0[stage]    = v_w0_new
                    adam_t        += 1
                    total_mse     += mse * mask.sum()
                    total_n       += mask.sum()

                if (bi + 1) % log_every == 0 or bi == n_batches - 1:
                    rmse      = np.sqrt(total_mse / total_n)
                    t_elapsed = time() - t_epoch
                    pct       = (bi + 1) / n_batches
                    t_remain  = t_elapsed / pct * (1 - pct) if pct > 0 else 0
                    print(f"  [{bi+1:5d}/{n_batches}  {pct*100:5.1f}%]  "
                          f"RMSE : {rmse:.6f}  "
                          f"ecoulé:{fmt_time(t_elapsed)}  "
                          f"restant:~{fmt_time(t_remain)}")
        else:
            order    = rng.permutation(len(stages))
            t_stages = []
            for si, sidx in enumerate(order):
                t_stage = time()
                stage   = stages[sidx]
                idx, cnt, sc = charger_stage(stage)
                if idx is None:
                    continue
                n    = len(sc)
                perm = rng.permutation(n)
                for start in range(0, n, args.batch):
                    batch = perm[start:start + args.batch]
                    w0_new, m_w0_new, v_w0_new, mse = adam_step(
                        idx[batch], cnt[batch], sc[batch],
                        w_by_stage[stage], np.float32(w0_vec[stage]),
                        V, m_V, v_V,
                        np.float32(m_w0[stage]), np.float32(v_w0[stage]),
                        np.float32(lr), np.float32(args.l2_V), np.int64(adam_t)
                    )
                    w0_vec[stage]  = w0_new
                    m_w0[stage]    = m_w0_new
                    v_w0[stage]    = v_w0_new
                    adam_t        += 1
                    total_mse     += mse * len(batch)
                    total_n       += len(batch)
                t_stages.append(time() - t_stage)
                if (si + 1) % 10 == 0 or si == len(order) - 1:
                    rmse      = np.sqrt(total_mse / total_n)
                    t_elapsed = time() - t_epoch
                    t_remain  = np.mean(t_stages) * (len(stages) - si - 1)
                    print(f"  [{si+1:3d}/{len(stages)}]  RMSE : {rmse:.6f}  "
                          f"ecoulé:{fmt_time(t_elapsed)}  "
                          f"restant:~{fmt_time(t_remain)}  "
                          f"({fmt_time(np.mean(t_stages))}/stage)")

        t_epoch_dur = time() - t_epoch
        rmse_train  = np.sqrt(total_mse / total_n)

        # --- RMSE validation ---
        if args.preload and val_n > 0:
            val_mse   = 0.0
            val_total = 0
            for stage in np.unique(val_stage_ids):
                mask     = val_stage_ids == stage
                idx_v    = val_indices[mask]
                cnt_v    = val_counts[mask]
                sc_v     = val_scores[mask]
                yhat_v   = fm_predict(idx_v, cnt_v, w_by_stage[stage],
                                      np.float32(w0_vec[stage]), V)
                val_mse   += np.sum((yhat_v - sc_v) ** 2)
                val_total += mask.sum()
            rmse_val = float(np.sqrt(val_mse / val_total))
            rmse_ref = rmse_val          # early stopping sur val
            val_str  = f"  RMSE_val={rmse_val:.6f}"
        else:
            rmse_val = None
            rmse_ref = rmse_train        # fallback si pas de preload
            val_str  = ""

        # --- Early stopping ---
        if rmse_ref < best_rmse - args.min_delta:
            best_rmse  = rmse_ref
            no_improve = 0
            marker     = "  nouveau meilleur"
            with open(MODEL_PKL, "wb") as f:
                pickle.dump({"w0_vec": w0_vec, "V": V, "rank": args.rank,
                             "rmse": best_rmse, "epoch": epoch,
                             "stages": stages}, f)
            export_fixed_point(w0_vec, V, stages)
        else:
            no_improve += 1
            marker     = f"  [sans amelioration : {no_improve}/{args.early_stopping}]"

        t_remain_total = t_epoch_dur * (args.epochs - epoch - 1)
        print(f"\n-> Epoque {epoch+1}  RMSE_train={rmse_train:.6f}{val_str}  "
              f"duree:{fmt_time(t_epoch_dur)}  "
              f"restant:~{fmt_time(t_remain_total)}"
              f"{marker}")

        lr *= args.lr_decay
        with open(CHECKPOINT, "wb") as f:
            pickle.dump({"w0_vec": w0_vec, "V": V, "epoch": epoch,
                         "best_rmse": best_rmse, "rank": args.rank,
                         "no_improve": no_improve, "lr": lr,
                         "adam_t": adam_t,
                         "m_V": m_V, "v_V": v_V,
                         "m_w0": m_w0, "v_w0": v_w0,
                         "stages": stages,
                         "rmse_val": rmse_val}, f)
        print(f"  Checkpoint sauvegarde.")

        if no_improve >= args.early_stopping:
            print(f"\n*** Early stopping a epoque {epoch+1} "
                  f"({args.early_stopping} epoques sans gain > {args.min_delta}) ***")
            break

    # --- w0 appris ---
    print("\nw0_vec appris :")
    for s in stages:
        print(f"  stage {s:02d} : w0={w0_vec[s]:.4f}")

    # --- Evaluation finale ---
    print(f"\n{'='*60}")
    print("Evaluation finale (tous les stages)")
    print(f"{'='*60}")
    stages_plot, rmse_fm_plot, rmse_lin_plot = [], [], []
    rmse_val_plot = []

    for stage in sorted(stages):
        t0 = time()
        idx, cnt, sc = charger_stage(stage)
        if idx is None:
            continue

        # RMSE globale (comme avant) — sur toutes les donnees du stage
        yhat     = fm_predict(idx, cnt, w_by_stage[stage], np.float32(w0_vec[stage]), V)
        rmse     = float(np.sqrt(np.mean((yhat - sc) ** 2)))
        mae      = float(np.mean(np.abs(yhat - sc)))
        yhat_lin = (cnt * w_by_stage[stage][idx]).sum(axis=1)
        rmse_lin = float(np.sqrt(np.mean((yhat_lin - sc) ** 2)))

        # RMSE val par stage (si preload + val disponible)
        if args.preload and val_n > 0:
            mask_v = val_stage_ids == stage
            if mask_v.sum() > 0:
                yhat_v   = fm_predict(val_indices[mask_v], val_counts[mask_v],
                                      w_by_stage[stage], np.float32(w0_vec[stage]), V)
                rmse_v   = float(np.sqrt(np.mean((yhat_v - val_scores[mask_v]) ** 2)))
            else:
                rmse_v = float("nan")
        else:
            rmse_v = float("nan")

        print(f"  Stage {stage:02d}  RMSE={rmse:.4f}  RMSE_val={rmse_v:.4f}  MAE={mae:.4f}  "
              f"(baseline={rmse_lin:.4f}  gain={rmse_lin-rmse:+.4f})  "
              f"({fmt_time(time()-t0)})")
        stages_plot.append(stage)
        rmse_fm_plot.append(rmse)
        rmse_lin_plot.append(rmse_lin)
        rmse_val_plot.append(rmse_v)

    # --- Graphe ---
    png_path = MODELS_DIR / "rmse_baseline_vs_fm.png"
    x        = np.arange(len(stages_plot))
    width    = 0.25
    fig, ax  = plt.subplots(figsize=(max(10, len(stages_plot) * 0.4), 5))
    ax.bar(x - width, rmse_lin_plot,  width, label="Baseline (lineaire)", color="#7fb3d3")
    ax.bar(x,         rmse_fm_plot,   width, label="FM (train+val)",      color="#e67e22")
    rmse_val_clean = [v if not np.isnan(v) else 0 for v in rmse_val_plot]
    ax.bar(x + width, rmse_val_clean, width, label="FM (val seule)",      color="#2ecc71")
    ax.set_xlabel("Stage")
    ax.set_ylabel("RMSE")
    baseline_mean = float(np.mean(rmse_lin_plot))
    ax.set_title(f"RMSE Baseline vs FM par stage  "
                 f"(baseline={baseline_mean:.4f}  meilleur FM={best_rmse:.4f})")
    ax.set_xticks(x)
    ax.set_xticklabels([str(s) for s in stages_plot],
                       rotation=90 if len(stages_plot) > 20 else 0)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(png_path, dpi=120)
    plt.close(fig)
    print(f"\n  Graphe sauvegarde : {png_path}")

    print(f"\nMeilleur RMSE (val) : {best_rmse:.6f}")
    print(f"[OK] Termine en {fmt_time(time()-t_global)}")


if __name__ == "__main__":
    main()
