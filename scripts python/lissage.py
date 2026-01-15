import numpy as np
import os
from scipy.signal import savgol_filter
from pathlib import Path


# --- Configuration à Ajuster ---
# nombre de fichiers d'entrée [0; 59]
NUM_FILES = 60
# **Taille de la fenêtre (W) :** Doit être IMPAIR. (Ex: 5, 9, 15). 
# Plus W est grand, plus le lissage est fort.
WINDOW_SIZE = 5  
# **Degré du polynôme (P) :** Généralement 2 ou 3. Ne doit pas être >= W.
POLYNOMIAL_ORDER = 2

WEIGHTS_DIR = Path("weights")

FILE_NAME_BASE = 'weight_'
FILE_EXTENSION = '.txt'

# Répertoire de sortie pour les 60 fichiers lissés
OUTPUT_DIR = f'weights_SG_W{WINDOW_SIZE}_P{POLYNOMIAL_ORDER}'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def smooth_and_rewrite_files():
    """
    Lit 60 fichiers, applique un lissage Savitzky-Golay (fenêtre glissante pondérée) 
    sur la séquence de 60 valeurs pour chaque ligne, puis réécrit 60 fichiers.
    """
    print("--- Démarrage du lissage Savitzky-Golay ---")
    print(f"Fenêtre : {WINDOW_SIZE} points | Polynôme : Degré {POLYNOMIAL_ORDER}")
    
    if WINDOW_SIZE % 2 == 0 or WINDOW_SIZE >= NUM_FILES:
        print(f"Erreur de configuration : WINDOW_SIZE ({WINDOW_SIZE}) doit être impair et inférieur à NUM_FILES ({NUM_FILES}).")
        return

    # 1. Chargement des données dans une matrice (nb weigths x 60 Fichiers)
    all_data = []
    
    for file_num in range(0, NUM_FILES):
        input_filename = WEIGHTS_DIR / f"{FILE_NAME_BASE}{file_num:02d}{FILE_EXTENSION}"
        try:
            data = np.loadtxt(input_filename)
            all_data.append(data)
        except Exception as e:
            print(f"Erreur de lecture du fichier {input_filename}: {e}")
            return
            
    # La matrice finale a la forme (nb patterns weight, 60)
    data_matrix = np.stack(all_data, axis=1)
    NUM_LINES = data_matrix.shape[0]
    print(f"Toutes les données ({NUM_LINES} lignes) chargées en mémoire.")
    
    # 2. Lissage Vectorisé de la Matrice
    
    # savgol_filter est appelé avec 'axis=1', ce qui applique le filtre 
    # le long de la dimension des 60 fichiers (les colonnes). 
    # Il traite les patterns weight simultanément.
    print(f"Application du filtre SG sur la matrice ({NUM_LINES}x{NUM_FILES})...")
    
    smoothed_matrix = savgol_filter(data_matrix, 
                                    window_length=WINDOW_SIZE, 
                                    polyorder=POLYNOMIAL_ORDER,
                                    axis=1) 
    
    print("Lissage terminé. Matrice lissée prête.")

    # 3. Sauvegarder les 60 colonnes lissées dans 60 fichiers séparés
    print("\nÉcriture des 60 nouveaux fichiers lissés...")
    
    for file_num in range(0, NUM_FILES):
        # La colonne (index file_num) de la matrice lissée
        column_data = smoothed_matrix[:, file_num]
        
        output_filename = f"{FILE_NAME_BASE}{file_num:02d}{FILE_EXTENSION}"
        output_filepath = os.path.join(OUTPUT_DIR, output_filename)
        
        # Enregistrement des données avec 8 décimales de précision
        np.savetxt(output_filepath, column_data, fmt='%.8f')
        
    print("\n--- Opération Terminée avec Succès ---")
    print(f"Les 60 fichiers lissés sont dans le dossier : {OUTPUT_DIR}")


if __name__ == "__main__":
    smooth_and_rewrite_files()
