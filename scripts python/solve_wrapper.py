import subprocess
import time

# Configuration
SCRIPT_PATH = "scripts python/solve_with_warmstart.py"
TOTAL_STAGES = 60

for i in range(TOTAL_STAGES):
    print(f"\n{'='*60}")
    print(f"Lancement du STAGE {i:02d} / {TOTAL_STAGES-1}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    # Correction : on sépare bien la commande et l'argument
    # Utilise l'exécutable python3 de ton environnement actuel
    command = ["python3", SCRIPT_PATH, str(i)]
    
    # check=True : lève une exception si le script échoue (évite de boucler dans le vide)
    try:
        result = subprocess.run(command, check=True)
        elapsed = time.time() - start_time
        print(f"\n[OK] Stage {i} terminé en {elapsed:.2f}s")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERREUR] Le stage {i} a échoué. Arrêt du wrapper.")
        break
