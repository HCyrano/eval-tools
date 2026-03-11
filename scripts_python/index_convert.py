"""
index_convert.py
Utilitaire de conversion entre index global et index local pour les patterns de Roxane.

Usage:
    python index_convert.py global <global_index>
    python index_convert.py local <id_patt> <local_index>
    python index_convert.py mirror <id_patt> <local_index>
    python index_convert.py          (lance les tests de cohérence)

Exemples:
    python index_convert.py global 250
    python index_convert.py local 2 10
    python index_convert.py mirror 2 10
"""

import sys

# --- Définition des patterns ---
# mobility player, mobility opponent
# diag5, diag6, diag7, diag8
# edge+2X, edge 2*(3+XF), edge 2*5
# hv2, hv3, hv4
# corner 4/3/3/1
index_offset = [24, 24, 243, 729, 2187, 6561, 59049, 59049, 59049, 6561, 6561, 6561, 177147]

PATTERN_NAMES = [
    "mobility_player",
    "mobility_opponent",
    "diag5",
    "diag6",
    "diag7",
    "diag8",
    "edge+2X",
    "edge_2*(3+XF)",
    "edge_2*5",
    "hv2",
    "hv3",
    "hv4",
    "corner_4/3/3/1",
]

N_PATTERNS = len(index_offset)

type_rotate = [0, 0, 5, 6, 7, 8, 10, 10, 0, 8, 8, 8, 17]

rotates = [
    [  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15],  # 0  pas de symétrie
    [  0],                                                                 # 1
    [  1,  0],                                                             # 2
    [  2,  1,  0],                                                         # 3
    [  3,  2,  1,  0],                                                     # 4
    [  4,  3,  2,  1,  0],                                                 # 5  diag5
    [  5,  4,  3,  2,  1,  0],                                             # 6  diag6
    [  6,  5,  4,  3,  2,  1,  0],                                         # 7  diag7
    [  7,  6,  5,  4,  3,  2,  1,  0],                                     # 8  diag8 / hv
    [  8,  7,  6,  5,  4,  3,  2,  1,  0],                                 # 9
    [  9,  8,  7,  6,  5,  4,  3,  2,  1,  0],                             # 10 edge+2X / edge2*(3+XF)
    [ 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  0],                         # 11
    [ 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  0],                     # 12
    [ 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  0],                 # 13
    [ 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  0],             # 14
    [ 14, 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  0],         # 15
    [ 15, 14, 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  0],     # 16
    [ 10,  9,  8,  7,  4,  5,  6,  3,  2,  1,  0],                         # 17 corner 4/3/3/1
    [  9,  8,  7,  6,  4,  5,  3,  2,  1,  0],                             # 18
    [  9,  8,  7,  3,  4,  5,  6,  2,  1,  0],                             # 19
    [ 11, 10,  9,  8,  7,  5,  6,  4,  3,  2,  1,  0],                     # 20
    [ 12, 11, 10,  9,  8,  5,  6,  7,  4,  3,  2,  1,  0],                 # 21
    [ 14, 13, 12, 11, 10,  9,  6,  7,  8,  5,  4,  3,  2,  1,  0],         # 22
]


# ---------------------------------------------------------------------------
# index_rotate : index local -> index local miroir (symétrie du pattern)
# ---------------------------------------------------------------------------

def index_rotate(local_index: int, id_patt: int) -> int:
    """
    Retourne l'index local du pattern symétrique (miroir géométrique).
    Opère en codage ternaire {-1, 0, 1}.
    id_rot == 0 signifie pas de symétrie -> retourne local_index inchangé.
    """
    id_rot = type_rotate[id_patt]
    if id_rot == 0:
        return local_index

    rotated = 0
    x = local_index
    n_squares = len(rotates[id_rot])

    for i in range(n_squares):
        # Division entière C++ (troncation vers zéro)
        quotient = int(float(x) / 3.0)
        r = x - 3 * quotient
        x = quotient

        if r == 2:
            r = -1
            x += 1
        elif r == -2:
            r = 1
            x -= 1

        rotated += r * (3 ** rotates[id_rot][i])

    return rotated


def local_mirror(local_index: int, id_patt: int) -> tuple:
    """
    Retourne les 4 index locaux liés par symétrie pour (local_index, id_patt) :
      - idx_orig  : l'index lui-même
      - idx_inv   : l'index inverse (noir <-> blanc)  = -(idx_orig)
      - idx_sym   : le miroir géométrique
      - idx_s_inv : le miroir de l'inverse
    """
    idx_orig  = local_index
    idx_inv   = -local_index
    idx_sym   = index_rotate(local_index, id_patt)
    idx_s_inv = index_rotate(-local_index, id_patt)   # == -idx_sym pour symétrie linéaire
    return idx_orig, idx_inv, idx_sym, idx_s_inv

# Précalcul des bornes globales de chaque pattern
# pattern i occupe les index globaux [global_start[i], global_start[i] + index_offset[i] - 1]
global_start = []
acc = 0
for size in index_offset:
    global_start.append(acc)
    acc += size
N_INDEX = acc  # = 383745


def is_mobility(id_patt: int) -> bool:
    return id_patt < 2


def offset_local(id_patt: int) -> int:
    """Décalage ternaire : 0 pour mobilité, (size-1)//2 pour les autres."""
    if is_mobility(id_patt):
        return 0
    return (index_offset[id_patt] - 1) // 2


# ---------------------------------------------------------------------------
# global -> local
# ---------------------------------------------------------------------------

def global_to_local(global_index: int) -> tuple:
    """
    Convertit un index global en (local_index, id_patt).

    L'index local est centré sur 0 pour les patterns non-mobilité
    (codage ternaire {-1, 0, 1} = {noir, vide, blanc}).
    Pour la mobilité il commence à 0.

    Retourne (local_index, id_patt).
    """
    if global_index < 0 or global_index >= N_INDEX:
        raise ValueError(f"Index global {global_index} hors bornes [0, {N_INDEX - 1}]")

    id_patt = 0
    remaining = global_index
    for i in range(N_PATTERNS):
        if remaining < index_offset[i]:
            id_patt = i
            break
        remaining -= index_offset[i]

    # remaining est l'index naturel base-0 dans le pattern
    local_index = remaining - offset_local(id_patt)

    return local_index, id_patt


# ---------------------------------------------------------------------------
# local -> global
# ---------------------------------------------------------------------------

def local_to_global(local_index: int, id_patt: int) -> int:
    """
    Convertit un (local_index, id_patt) en index global.

    local_index est centré sur 0 pour les patterns non-mobilité,
    et commence à 0 pour la mobilité.
    """
    if id_patt < 0 or id_patt >= N_PATTERNS:
        raise ValueError(f"id_patt {id_patt} hors bornes [0, {N_PATTERNS - 1}]")

    lo = -offset_local(id_patt)
    hi = index_offset[id_patt] - 1 - offset_local(id_patt)
    if local_index < lo or local_index > hi:
        raise ValueError(
            f"local_index {local_index} hors bornes [{lo}, {hi}] pour id_patt={id_patt}"
        )

    natural = local_index + offset_local(id_patt)   # base 0
    global_index = global_start[id_patt] + natural

    return global_index


# ---------------------------------------------------------------------------
# Affichage détaillé
# ---------------------------------------------------------------------------

def describe_global(global_index: int):
    local_index, id_patt = global_to_local(global_index)
    print(f"Index global   : {global_index}")
    print(f"Pattern        : [{id_patt}] {PATTERN_NAMES[id_patt]}")
    print(f"Taille pattern : {index_offset[id_patt]}")
    print(f"Début global   : {global_start[id_patt]}")
    print(f"Index naturel  : {global_index - global_start[id_patt]}  (base 0, avant centrage)")
    print(f"Index local    : {local_index}  (centré sur 0{' - mobilité' if is_mobility(id_patt) else ''})")


def describe_mirror(id_patt: int, local_index: int):
    id_rot = type_rotate[id_patt]
    orig, inv, sym, s_inv = local_mirror(local_index, id_patt)
    print(f"Pattern        : [{id_patt}] {PATTERN_NAMES[id_patt]}  (id_rot={id_rot})")
    print(f"Index local    : {orig:8d}   (entrée)")
    print(f"Inverse        : {inv:8d}   (noir <-> blanc)")
    print(f"Miroir         : {sym:8d}   (symétrie géométrique)")
    print(f"Miroir inverse : {s_inv:8d}   (miroir + noir <-> blanc)")
    if id_rot == 0:
        print("  [pas de symétrie géométrique pour ce pattern]")
    global_index = local_to_global(local_index, id_patt)
    lo = -offset_local(id_patt)
    hi = index_offset[id_patt] - 1 - offset_local(id_patt)
    print(f"Pattern        : [{id_patt}] {PATTERN_NAMES[id_patt]}")
    print(f"Plage locale   : [{lo}, {hi}]")
    print(f"Index local    : {local_index}")
    print(f"Offset local   : {offset_local(id_patt)}")
    print(f"Index naturel  : {local_index + offset_local(id_patt)}  (base 0)")
    print(f"Début global   : {global_start[id_patt]}")
    print(f"Index global   : {global_index}")


# ---------------------------------------------------------------------------
# Tests de cohérence (aller-retour sur les bornes de chaque pattern)
# ---------------------------------------------------------------------------

def run_tests():
    print("=== Tests de cohérence global<->local ===\n")
    errors = 0

    for pid in range(N_PATTERNS):
        lo = -offset_local(pid)
        hi = index_offset[pid] - 1 - offset_local(pid)
        mid = 0

        for local in [lo, mid, hi]:
            g = local_to_global(local, pid)
            local2, pid2 = global_to_local(g)
            ok = (local2 == local and pid2 == pid)
            status = "OK" if ok else f"ERREUR (retour local={local2}, pid={pid2})"
            print(f"  [{pid:2d}] {PATTERN_NAMES[pid]:20s}  local={local:8d} -> global={g:7d} -> {status}")
            if not ok:
                errors += 1
        print()

    print(f"{'Tous les tests OK.' if errors == 0 else f'{errors} erreur(s) détectée(s).'}\n")

    print("=== Tests miroir (double rotation = identité) ===\n")
    for pid in range(N_PATTERNS):
        if type_rotate[pid] == 0:
            continue
        for local in [-5, 0, 7, -offset_local(pid)]:
            lo = -offset_local(pid)
            hi = index_offset[pid] - 1 - offset_local(pid)
            if local < lo or local > hi:
                continue
            sym = index_rotate(local, pid)
            sym2 = index_rotate(sym, pid)
            ok = (sym2 == local)
            status = "OK" if ok else f"ERREUR (double={sym2})"
            print(f"  [{pid:2d}] {PATTERN_NAMES[pid]:20s}  local={local:6d} -> miroir={sym:6d} -> retour={sym2:6d} {status}")
            if not ok:
                errors += 1
    print()
    print(f"{'Tous les tests OK.' if errors == 0 else f'{errors} erreur(s) détectée(s).'}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def interactive_loop():
    print("=== index_convert — mode interactif ===")
    print("Commandes : global <idx>  |  local <id_patt> <idx>  |  mirror <id_patt> <idx>  |  test  |  quit")
    print()
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAu revoir.")
            break

        if not line:
            continue

        parts = line.split()
        mode  = parts[0].lower()

        try:
            if mode in ("q", "quit", "exit"):
                print("Au revoir.")
                break

            elif mode == "global":
                if len(parts) != 2:
                    print("  Usage : global <global_index>")
                    continue
                describe_global(int(parts[1]))

            elif mode == "local":
                if len(parts) != 3:
                    print("  Usage : local <id_patt> <local_index>")
                    continue
                # describe_local n'existe pas dans l'original, on affiche global équivalent
                g = local_to_global(int(parts[2]), int(parts[1]))
                describe_global(g)

            elif mode == "mirror":
                if len(parts) != 3:
                    print("  Usage : mirror <id_patt> <local_index>")
                    continue
                describe_mirror(int(parts[1]), int(parts[2]))

            elif mode in ("test", "tests"):
                run_tests()

            else:
                print("  Commandes : global <idx>  |  local <id_patt> <idx>  |  mirror <id_patt> <idx>  |  test  |  quit")

        except ValueError as e:
            print(f"  Erreur : {e}")

        print()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        interactive_loop()
        sys.exit(0)

    mode = sys.argv[1].lower()

    if mode == "global":
        if len(sys.argv) != 3:
            print("Usage: python index_convert.py global <global_index>")
            sys.exit(1)
        describe_global(int(sys.argv[2]))

    elif mode == "mirror":
        if len(sys.argv) != 4:
            print("Usage: python index_convert.py mirror <id_patt> <local_index>")
            sys.exit(1)
        describe_mirror(int(sys.argv[2]), int(sys.argv[3]))

    elif mode == "local":
        if len(sys.argv) != 4:
            print("Usage: python index_convert.py local <id_patt> <local_index>")
            sys.exit(1)
        g = local_to_global(int(sys.argv[3]), int(sys.argv[2]))
        describe_global(g)

    else:
        print(__doc__)
        sys.exit(1)
