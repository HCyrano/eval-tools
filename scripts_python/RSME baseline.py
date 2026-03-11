import numpy as np
from pathlib import Path
from scipy.sparse import csr_matrix


DATA_DIR   = Path("datas")
WEIGHTS_DIR = Path("weights")

N_INDEX    = 383745


for stage in range(60):
    data_path   = DATA_DIR   / f"data_{stage:02}.txt"
    weight_path = WEIGHTS_DIR / f"weight_{stage:02}.txt"
    if not data_path.exists() or not weight_path.exists():
        continue

    w = np.loadtxt(weight_path, dtype=np.float32)
    
    rows, cols, data, scores_list = [], [], [], []
    row_count = 0
    with open(data_path) as f:
        for line in f:
            vals = list(map(int, line.split()))
            idx_raw = vals[:-1]   # ← tout sauf le dernier
            score   = vals[-1]

            u, c = np.unique(idx_raw, return_counts=True)
            rows.extend([row_count] * len(u))
            cols.extend(u.tolist())
            data.extend(c.tolist())
            scores_list.append(score)
            row_count += 1

    scores = np.array(scores_list, dtype=np.float32)
    A      = csr_matrix((data, (rows, cols)), shape=(row_count, N_INDEX))
    lin    = A.dot(w)
    rmse   = np.sqrt(np.mean((lin - scores) ** 2))
    print(f"stage {stage:02d}  RMSE baseline : {rmse:.4f}  "
          f"(n={row_count:n}  score_std={scores.std():.2f})")
