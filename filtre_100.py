import sys
from collections import Counter

stage = int(sys.argv[1])

# Construire la liste des fichiers input
filenames_in = []
filenames_in.append(f"datas/data_{stage:02}.txt")

if stage > 9:
    filenames_in.insert(0, f"datas/data_{stage-1:02}.txt")

if 8 < stage < 59:
    filenames_in.append(f"datas/data_{stage+1:02}.txt")

filename_out = f"datas_norm/data_norm_{stage:02}.txt"

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
a_supprimer = {idx for idx, occ in compte.items() if occ < 100}
print(len(a_supprimer))

# 4) Écriture directe du fichier filtré
with open(filename_out, "w") as f:
    for vals in all_lines:
        # Séparer les valeurs à filtrer et le score
        *indices, score = vals
        filtres = [str(v) for v in indices if v not in a_supprimer]
        filtres.append(str(score))  # le score est toujours conservé
        f.write(" ".join(filtres) + "\n")
