import sys
from collections import Counter
from pathlib import Path

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


# bornage inferieur et superieur des stages a normaliser
stage_borne_inf = 9
stage_borne_sup = 60
stage = max(stage_borne_inf, stage)

# nombre d'occurences minimum
condition_filtre = 100

# Construire la liste des fichiers input

DATA_DIR = Path("datas")
DATA_NORM_DIR = Path("datas_norm")

# Créer le répertoire de sortie s'il n'existe pas
DATA_NORM_DIR.mkdir(exist_ok=True)


filenames_in = []
# Créer les chemins avec pathlib
for s in [stage - 1, stage, stage + 1]:
    if stage_borne_inf <= s < stage_borne_sup: # Assurer que l'index du stage est dans la plage
        path = Path(DATA_DIR / f"data_{s:02}.txt")
        if path.exists():
            filenames_in.append(str(path)) # Convertir en str pour le reste du code


filename_out =  DATA_NORM_DIR / f"data_norm_{stage:02}.txt"

# 1) Lecture unique des fichiers d'entrée
all_lines = []   # contiendra toutes les lignes déjà découpées en valeurs
all_indices = [] # pour compter globalement les occurrences

for filename_in in filenames_in:
    print(filename_in)
    with open(filename_in, "r") as f:
        for line in f:
            vals = list(map(int, line.split()))
            all_lines.append(vals)
            # On ne compte pas le dernier élément (score)
            all_indices.extend(vals[:-1])

# 2) Compter les occurrences
compte = Counter(all_indices)

# 3) Déterminer les index à supprimer
a_supprimer = {idx for idx, occ in compte.items() if occ < condition_filtre}
print(len(a_supprimer))

# 4) Écriture directe du fichier filtré
with open(filename_out, "w") as f:
    for vals in all_lines:
        # Séparer les valeurs à filtrer et le score
        *indices, score = vals
        filtres = [str(v) for v in indices if v not in a_supprimer]
        filtres.append(str(score))  # le score est toujours conservé
        f.write(" ".join(filtres) + "\n")
