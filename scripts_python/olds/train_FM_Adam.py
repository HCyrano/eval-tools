"""
train_FM_Adam.py  —  FM global pour Roxane (moteur Othello)
=============================================================
Architecture :
  score = w[stage]·x + w0[stage] + inter_FM(x, V)
           ↑                ↑              ↑
    figé (chargé       appris (1       partagé tous
    depuis weights/)   scalaire/stage)    les stages

- w[stage] : chargés depuis weights/weight_{stage:02}.txt, jamais modifiés
- w0[stage]: 60 scalaires appris (biais par stage)
- V        : matrice (rank × N_INDEX) partagée, apprise sur tous les stages

- Mode --preload : charge tous les stages en RAM
- lr avec décroissance exponentielle
- Early stopping si plus de convergence

Export en virgule fixe ×256 (int16), cohérent avec les tables eval C++.

Usage :
  python train_FM_Adam.py --epochs 20 --rank 8 --preload
  python train_FM_Adaml.py --epochs 20 --resume --preload
  python train_FM_Adam.py --epochs 3 --stages 30-39    # test streaming
"""

import argparse
import numpy as np
import pickle
from pathlib import Path
from time import time

# =============================================================================
# Config
# =============================================================================

N_INDEX    = 383745
N_STAGES   = 60

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
# Chargement des poids linéaires par stage (figés)
# =============================================================================

def charger_weights(stages):
    """Charge les poids linéaires w[stage] depuis weights/weight_{stage:02}.txt.
    Retourne un dict {stage: np.array(N_INDEX, float32)}.
    Les stages sans fichier reçoivent un vecteur nul avec avertissement."""
    print(f"\nChargement des poids linéaires depuis {WEIGHTS_DIR}/...")
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
        print(f"  ⚠️  Fichiers manquants (vecteur nul) : stages {manquants}")
    return w_by_stage


# =============================================================================
# Chargement des données
# =============================================================================

def charger_stage(stage):
    """Charge les données d'un stage.
    Chaque ligne : indices... score  (nombre variable d'indices, score en dernier)
    Retourne (indices_mat, counts_mat, scores) où :
      - indices_mat : (n, K)  indices uniques par ligne (paddé avec 0, neutralisé par counts=0)
      - counts_mat  : (n, K)  comptages correspondants
      - scores      : (n,)
    K = nombre max d'index uniques par ligne.
    """
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
            idx_raw = vals[:-1]   # tout sauf le dernier = indices
            score   = vals[-1]    # dernier = score
            u, c    = np.unique(idx_raw, return_counts=True)
            indices_list.append(u.astype(np.int32))
            counts_list.append(c.astype(np.float32))
            scores_list.append(score)

    if not indices_list:
        return None, None, None

    # Padding à longueur fixe K
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
# Préchargement
# =============================================================================

def preload_all(stages):
    """Charge tous les stages en RAM.
    Retourne (all_indices, all_counts, all_scores, all_stage_ids).
    Aligne tous les stages sur le K global (max des K par stage).
    """
    print(f"\nPréchargement de {len(stages)} stages en RAM...")
    t0 = time()

    # Premier pass
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

    # Second pass : aligner sur K_global
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
          f"—  {mem_go:.2f} Go  ({fmt_time(time()-t0)})")
    return all_indices, all_counts, all_scores, all_stage_ids


# =============================================================================
# Prédiction FM  (avec comptages)
# =============================================================================

def fm_predict(indices_mat, counts_mat, w_stage, w0_stage, V):
    """
    score = w0_stage + sum(counts * w_stage[indices]) + inter_FM(V, indices, counts)
    indices_mat : (n, K)  int32
    counts_mat  : (n, K)  float32  — comptages (0 pour le padding)
    w_stage     : (N_INDEX,) float32
    w0_stage    : float
    V           : (rank, N_INDEX) float32
    """
    linear   = w0_stage + (counts_mat * w_stage[indices_mat]).sum(axis=1)
    V_vals   = V[:, indices_mat].transpose(1, 2, 0)              # (n, K, rank)
    cV       = counts_mat[:, :, np.newaxis] * V_vals              # (n, K, rank)
    sum_cV   = cV.sum(axis=1)                                     # (n, rank)
    sum_c2V2 = (counts_mat[:, :, np.newaxis] ** 2 * V_vals ** 2).sum(axis=1)
    inter    = 0.5 * ((sum_cV ** 2) - sum_c2V2).sum(axis=1)
    return (linear + inter).astype(np.float32)


# =============================================================================
# Step Adam  (gradient sur w0_stage et V uniquement, w_stage figé)
# =============================================================================

def adam_step(indices_b, counts_b, scores_b, w_stage, w0_stage, V,
              m_V, v_V, m_w0, v_w0, lr, l2_V, t,
              beta1=0.9, beta2=0.999, eps=1e-8):
    """
    indices_b : (b, K) int32
    counts_b  : (b, K) float32
    m_V, v_V  : moments Adam pour V  (rank, N_INDEX)
    m_w0, v_w0: moments Adam pour w0 (scalaires)
    t         : pas global (pour bias correction)
    Met à jour w0_stage et V. w_stage jamais modifié.
    """
    b    = len(scores_b)
    rank = V.shape[0]

    yhat = fm_predict(indices_b, counts_b, w_stage, w0_stage, V)
    err  = yhat - scores_b                                        # (b,)

    # --- Gradient w0 ---
    g_w0   = err.mean()
    m_w0   = beta1 * m_w0 + (1 - beta1) * g_w0
    v_w0   = beta2 * v_w0 + (1 - beta2) * g_w0 ** 2
    m_w0_h = m_w0 / (1 - beta1 ** t)
    v_w0_h = v_w0 / (1 - beta2 ** t)
    w0_stage -= lr * m_w0_h / (np.sqrt(v_w0_h) + eps)

    # --- Gradient V ---
    V_vals   = V[:, indices_b].transpose(1, 2, 0)                # (b, K, rank)
    cV       = counts_b[:, :, np.newaxis] * V_vals                # (b, K, rank)
    sum_cV   = cV.sum(axis=1)                                     # (b, rank)
    h        = counts_b[:, :, np.newaxis] * (sum_cV[:, np.newaxis, :] - cV)
    weighted = err[:, np.newaxis, np.newaxis] * h / b

    grad_V   = np.zeros_like(V)
    flat_idx = indices_b.ravel()
    flat_w   = weighted.reshape(-1, rank)
    np.add.at(grad_V, (slice(None), flat_idx), flat_w.T)

    # Gradient clipping
    grad_norm = np.linalg.norm(grad_V)
    if grad_norm > 10.0:
        grad_V *= 10.0 / grad_norm

    # Mise à jour Adam pour V
    m_V   = beta1 * m_V  + (1 - beta1) * grad_V
    v_V   = beta2 * v_V  + (1 - beta2) * grad_V ** 2
    m_V_h = m_V / (1 - beta1 ** t)
    v_V_h = v_V / (1 - beta2 ** t)
    V -= lr * (m_V_h / (np.sqrt(v_V_h) + eps) + l2_V * V)
    np.clip(V, -10, 10, out=V)

    return w0_stage, V, m_V, v_V, m_w0, v_w0, float(np.mean(err ** 2))


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
            
    # AoS : pour chaque index global, les RANK composantes sont contiguës
    V_aos = to_int16(V).T  # (N_INDEX, rank)
    V_aos.tofile(FM_V_BIN)
    
    rank    = V.shape[0]
    size_mb = (V.size * 2) / 1024**2
    print(f"  Export int16 ×256 :")
    print(f"    {FM_W0_TXT}  ({N_STAGES} lignes, une par stage)")
    print(f"    {FM_V_BIN}   ({rank}×{N_INDEX} int16, {size_mb:.1f} Mo)")
    V_err = np.max(np.abs(V - to_int16(V).astype(np.float32) / SCALE))
    print(f"    Erreur quant. max V : {V_err:.6f}")


# =============================================================================
# Main
# =============================================================================

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--epochs",          type=int,   default=20)
    p.add_argument("--rank",            type=int,   default=8)
    p.add_argument("--lr",              type=float, default=0.001)
    p.add_argument("--lr_decay",        type=float, default=1.0,
                   help="Multiplicateur lr par époque")
    p.add_argument("--l2_V",            type=float, default=0.001)
    p.add_argument("--batch",           type=int,   default=4096)
    p.add_argument("--stages",          type=str,   default=f"0-{N_STAGES-1}")
    p.add_argument("--resume",          action="store_true")
    p.add_argument("--seed",            type=int,   default=42)
    p.add_argument("--preload",         action="store_true")
    p.add_argument("--early_stopping",  type=int,   default=5,
                   help="Arrêt si pas d'amélioration sur N époques consécutives")
    p.add_argument("--min_delta",       type=float, default=0.0001,
                   help="Gain minimum considéré comme amélioration")
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

    print(f"Stages : {len(stages)}  ({stages[0]}..{stages[-1]})")
    print(f"rank={args.rank}  lr={args.lr}  decay={args.lr_decay}  "
          f"l2_V={args.l2_V}  batch={args.batch}  "
          f"preload={'oui' if args.preload else 'non'}")
    print(f"early_stopping={args.early_stopping}  min_delta={args.min_delta}")

    # --- Chargement des poids linéaires figés ---
    w_by_stage = charger_weights(stages)

    # --- Préchargement données ---
    if args.preload:
        all_indices, all_counts, all_scores, all_stage_ids = preload_all(stages)
        n_total = len(all_scores)

    # --- Baseline (poids linéaires seuls, avant init V) ---
    if not (args.resume and CHECKPOINT.exists()):
        print("\nRMSE baseline (poids linéaires seuls)...")
        total_mse_base = 0.0
        total_n_base   = 0
        for stage in stages:
            indices_mat, counts_mat, scores = charger_stage(stage)
            if indices_mat is None:
                continue
            yhat = (counts_mat * w_by_stage[stage][indices_mat]).sum(axis=1)
            total_mse_base += np.sum((yhat - scores) ** 2)
            total_n_base   += len(scores)
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
        print(f"  Époque {start_epoch}, RMSE={best_rmse:.6f}, "
              f"no_improve={no_improve}, lr={lr:.6f}, adam_t={adam_t}")
    else:
        print("\nInitialisation...")
        w0_vec = np.zeros(N_STAGES, dtype=np.float32)
        V      = np.zeros((args.rank, N_INDEX), dtype=np.float32)
        print("  Calcul des colonnes actives globales...")
        active_cols = np.unique(
            np.concatenate([np.where(w_by_stage[s] != 0)[0] for s in stages]))
        V[:, active_cols] = rng.normal(0, 0.001, (args.rank, len(active_cols))).astype(np.float32)
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

    # --- Boucle epochs ---
    for epoch in range(start_epoch, args.epochs):
        t_epoch   = time()
        total_mse = 0.0
        total_n   = 0

        print(f"\n{'='*60}")
        print(f"Époque {epoch+1}/{args.epochs}  lr={lr:.6f}")
        print(f"{'='*60}")

        if args.preload:
            perm      = rng.permutation(n_total)
            n_batches = (n_total + args.batch - 1) // args.batch
            log_every = max(1, n_batches // 10)

            for bi, start in enumerate(range(0, n_total, args.batch)):
                batch      = perm[start:start + args.batch]
                indices_b  = all_indices[batch]
                counts_b   = all_counts[batch]
                scores_b   = all_scores[batch]
                stage_ids  = all_stage_ids[batch]

                for stage in np.unique(stage_ids):
                    mask     = stage_ids == stage
                    idx_s    = indices_b[mask]
                    cnt_s    = counts_b[mask]
                    scores_s = scores_b[mask]
                    (w0_vec[stage], V, m_V, v_V,
                     m_w0[stage], v_w0[stage], mse) = adam_step(
                        idx_s, cnt_s, scores_s,
                        w_by_stage[stage], w0_vec[stage],
                        V, m_V, v_V, m_w0[stage], v_w0[stage],
                        lr, args.l2_V, adam_t
                    )
                    adam_t    += 1
                    total_mse += mse * mask.sum()
                    total_n   += mask.sum()

                if (bi + 1) % log_every == 0 or bi == n_batches - 1:
                    rmse      = np.sqrt(total_mse / total_n)
                    t_elapsed = time() - t_epoch
                    pct       = (bi + 1) / n_batches
                    t_remain  = t_elapsed / pct * (1 - pct) if pct > 0 else 0
                    print(f"  [{bi+1:5d}/{n_batches}  {pct*100:5.1f}%]  "
                          f"RMSE : {rmse:.6f}  "
                          f"écoulé:{fmt_time(t_elapsed)}  "
                          f"restant:~{fmt_time(t_remain)}")
        else:
            order    = rng.permutation(len(stages))
            t_stages = []
            for si, sidx in enumerate(order):
                t_stage = time()
                stage   = stages[sidx]
                indices_mat, counts_mat, scores = charger_stage(stage)
                if indices_mat is None:
                    continue
                n    = len(scores)
                perm = rng.permutation(n)
                for start in range(0, n, args.batch):
                    batch = perm[start:start + args.batch]
                    (w0_vec[stage], V, m_V, v_V,
                     m_w0[stage], v_w0[stage], mse) = adam_step(
                        indices_mat[batch], counts_mat[batch], scores[batch],
                        w_by_stage[stage], w0_vec[stage],
                        V, m_V, v_V, m_w0[stage], v_w0[stage],
                        lr, args.l2_V, adam_t
                    )
                    adam_t    += 1
                    total_mse += mse * len(batch)
                    total_n   += len(batch)
                t_stages.append(time() - t_stage)
                if (si + 1) % 10 == 0 or si == len(order) - 1:
                    rmse      = np.sqrt(total_mse / total_n)
                    t_elapsed = time() - t_epoch
                    t_remain  = np.mean(t_stages) * (len(stages) - si - 1)
                    print(f"  [{si+1:3d}/{len(stages)}]  RMSE : {rmse:.6f}  "
                          f"écoulé:{fmt_time(t_elapsed)}  "
                          f"restant:~{fmt_time(t_remain)}  "
                          f"({fmt_time(np.mean(t_stages))}/stage)")

        t_epoch_dur = time() - t_epoch
        rmse_epoch  = np.sqrt(total_mse / total_n)

        # --- Early stopping ---
        if rmse_epoch < best_rmse - args.min_delta:
            best_rmse  = rmse_epoch
            no_improve = 0
            marker     = "  ✓ nouveau meilleur"
            with open(MODEL_PKL, "wb") as f:
                pickle.dump({"w0_vec": w0_vec, "V": V, "rank": args.rank,
                             "rmse": best_rmse, "epoch": epoch,
                             "stages": stages}, f)
            export_fixed_point(w0_vec, V, stages)
        else:
            no_improve += 1
            marker     = f"  [sans amélioration : {no_improve}/{args.early_stopping}]"

        t_remain_total = t_epoch_dur * (args.epochs - epoch - 1)
        print(f"\n→ RMSE époque {epoch+1} : {rmse_epoch:.6f}  "
              f"durée : {fmt_time(t_epoch_dur)}  "
              f"restant total : ~{fmt_time(t_remain_total)}"
              f"{marker}")

        lr *= args.lr_decay
        with open(CHECKPOINT, "wb") as f:
            pickle.dump({"w0_vec": w0_vec, "V": V, "epoch": epoch,
                         "best_rmse": best_rmse, "rank": args.rank,
                         "no_improve": no_improve, "lr": lr,
                         "adam_t": adam_t,
                         "m_V": m_V, "v_V": v_V,
                         "m_w0": m_w0, "v_w0": v_w0,
                         "stages": stages}, f)
        print(f"  Checkpoint sauvegardé.")

        if no_improve >= args.early_stopping:
            print(f"\n*** Early stopping à époque {epoch+1} "
                  f"({args.early_stopping} époques sans gain > {args.min_delta}) ***")
            break

    # --- w0 appris ---
    print("\nw0_vec appris :")
    for s in stages:
        print(f"  stage {s:02d} : w0={w0_vec[s]:.4f}")

    # --- Évaluation finale ---
    print(f"\n{'='*60}")
    print("Évaluation finale (tous les stages)")
    print(f"{'='*60}")
    for stage in sorted(stages):
        t0 = time()
        indices_mat, counts_mat, scores = charger_stage(stage)
        if indices_mat is None:
            continue
        yhat     = fm_predict(indices_mat, counts_mat, w_by_stage[stage], w0_vec[stage], V)
        rmse     = float(np.sqrt(np.mean((yhat - scores) ** 2)))
        mae      = float(np.mean(np.abs(yhat - scores)))
        # Baseline = poids linéaires seuls (sans w0, sans FM)
        yhat_lin = (counts_mat * w_by_stage[stage][indices_mat]).sum(axis=1)
        rmse_lin = float(np.sqrt(np.mean((yhat_lin - scores) ** 2)))
        print(f"  Stage {stage:02d}  RMSE={rmse:.4f}  MAE={mae:.4f}  "
              f"(baseline linéaire={rmse_lin:.4f}  gain={rmse_lin-rmse:+.4f})  "
              f"({fmt_time(time()-t0)})")
        
    print(f"\nMeilleur RMSE : {best_rmse:.6f}")
    print(f"[OK] Terminé en {fmt_time(time()-t_global)}")


if __name__ == "__main__":
    main()
