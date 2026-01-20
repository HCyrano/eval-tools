import sys
import collections

def count_empty(board):
    return board.count('-')

def analyze_deviations(file_path):
    deviations = []
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    i = 0
    while i < len(lines) - 1:
        # split() sépare par les espaces : [0]=score, [1]=othellier, [2]=joueur...
        parts1 = lines[i].split()
        parts2 = lines[i+1].split()
        
        if len(parts1) < 2 or len(parts2) < 2:
            i += 1
            continue

        board1 = parts1[1]
        board2 = parts2[1]
        
        empty1 = board1.count('-')
        empty2 = board2.count('-')
        
        # CAS SPÉCIAL : Si on voit deux plateaux de départ (50 vides)
        if empty1 == 50 and empty2 == 50:
            # Si les othelliers sont strictement identiques, 
            # c'est un match retour sans variation -> Coup 1
            if board1 == board2:
                deviations.append(1)
                i += 2
            else:
                # Si les othelliers sont différents (ou si c'est deux "Aller" de suite)
                # On applique ta convention du Coup 0
                deviations.append(0)
                i += 1
        else:
            # CAS GÉNÉRAL
            deviations.append(50 - empty2 + 1)
            i += 2
            
    return deviations
    
    
def print_stats(deviations):
    if not deviations:
        print("Aucune donnée à traiter.")
        return

    stats = collections.Counter(deviations)
    total = len(deviations)
    
    print(f"\n{'Coup de déviation':<25} | {'Nombre':<10} | {'Pourcentage':<10}")
    print("-" * 50)
    
    # Le tri numérique placera le '0' en premier
    for move in sorted(stats.keys()):
        count = stats[move]
        percentage = (count / total) * 100
        
        if move == 0:
            label = "Coup 0 (Aucune variation)"
        else:
            label = f"Coup {move}"
            
        print(f"{label:<25} | {count:<10} | {percentage:>8.2f}%")
    
    print("-" * 50)
    print(f"{'TOTAL':<25} | {total:<10} | 100.00%")

# --- Exécution ---
if __name__ == "__main__":
    # Vérifie si l'utilisateur a fourni un nom de fichier
    if len(sys.argv) < 2:
        print("Usage: python comptage_deviation.py <nom_du_fichier.txt>")
    else:
        nom_fichier = sys.argv[1] # Récupère le premier argument après le nom du script
        try:
            results = analyze_deviations(nom_fichier)
            print_stats(results)
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{nom_fichier}' est introuvable.")
        except Exception as e:
            print(f"Une erreur est survenue : {e}")
