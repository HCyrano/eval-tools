Génération d'une evaluation

mix de c++ et python:

1) Avoir une base normalisée
	lire le PDF : Gestion Base de Données
	
	apres avoir realiser les etapes: la base normalisée se trouve:
	dedups/dedup_xx.txt
	
	deplacer ce dossier dans Evaluation/
	
2) definir les patterns

	cette partie est essentiellement manuel et concerme plusieurs c++ et script
	
	c++:
		definir les patterrns :
		
			fichier PatternGenerate.h :
		       	
        	{type de symetrie, { case_0, case_1, case_N}},
        	
        	//  diag_5
        	{ 5, { A5, B4, C3, D2, E1}},
        	{ 5, { D1, E2, F3, G4, H5}},
        	{ 5, { H4, G5, F6, E7, D8}},
        	{ 5, { E8, D7, C6, B5, A4}},
        	
        	.../...
        	
        definir les infos de pattern :
 
        	{last index of pattern, offset index global, n_index local, rotate index}
        
        	//diag_5
        	{3, 0, 243, 5},
        	
        	.../...

 		verifier ou definir les infos de symetrie dans rotates
 		
 		a ce stade on peut generer les fonctions set et flip de RXPattern :
 		les copier coller dans RXPattern.h
 		ne pas oublier de modifier dans la definition de class
 		    int patt["n_patt"];
 		    
 	script python
 		
 		solve.py
 			
 			ligne 63 : fixer le nombre total d'indice:
 			
 		norm_data.py
 		
 			# --- definition des patterns ---
			# a implementer nanuellement en fonctions des patterns choisis ex:
			# diag5, diag6, diag7, diag8
			# edge+X, hv2, hv3, hv4
			# corner 2bords5+X, corner2x5, corner11
			
index_offset = [243, 729, 2187, 6561, 59049, 6561, 6561, 6561, 59049, 59049, 177147]
type_rotate  = [  5,   6,    7,    8,    10,    8,    8,    8,    15,     0,     14]

			verifier ou definir les infos de symetrie dans rotates :
			
			definir le seuil d'occurence souhaité :
			ligne 177 :occurence_min = 100
			
			
3) executer la methode c++ stage_to_data()

	un dossier datas/data__xx.txt est créé
	
	2b) on peut verifier la normalisation des index du stage par verif_norm.py "stage"
	
4) normaliser ce dossier

	3a) les 9 1er stages [0, 8] sont simplement a recopier manuellement en modifiant le nom de fichiers
	le nombre d'occurences des patterns etant trop faible.
	
	3b) a partir de stage__09 grouper les stage par 3 (n-1, n, n+1) pour plus de données
	et un lissage entre les stages

	3c) ne conserver que si le nombre d'occurences de l'index du pattern
	et son inverse dépasse un seuil (ex : 100)
	
	readme_norm_data.txt
	
	
5) calculer les poids par index et stage

	solve_wrapper.py
	
	ecrit deux fichiers par stage
		weight_xx.txt et n_occ_xx.txt
		
		le 1er contient le poids de l'index
		le second le nombre d'occurence de l'index
		
6) écrire l'évaluation

	c++ 
		write_eval()
