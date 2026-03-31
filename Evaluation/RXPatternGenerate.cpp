//
//  RXPatternGenerate.cpp
//  Evaluation
//
//  Created by Causse Bruno on 07/11/2025.
//

#include <stdio.h>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <cstring> // Pour std::memcpy
#include <cmath>


#include "arm_neon.h"



#include "RXPatternGenerate.hpp"
#include "RXMove.hpp"
#include "RXPattern.hpp"
#include "RXBitBoard.hpp"
#include "RXBBPatterns.hpp"


// Affiche la disposition du motif (pattern) sur l’othellier,
// en montrant les cases concernées et leur ordre
// affiche egalement le pattern symetrique
void RXPatternGenerate::display() {
    
    std::cout << "nombre de  patterns : " << std::size(pattern_def) << std::endl;

    std::cout << "affichage pattern : " << std::endl;
    for(int i = 0; i<std::size(pattern_def); ++i) {
        const auto& f = pattern_def[i];
        std::cout << "name: " << "patt[" << std::setw(2) << i << "]" << " symID: " << f.symID << ", squares: ";

        std::cout << "\n  A B C D E F G H " << std::endl;
        for(int iLine = 1; iLine<=8; iLine++) {
            std::cout  << iLine << " ";
            for(int iPosition = (9-iLine)*8 - 1; iPosition>(8-iLine)*8-1; iPosition--) {
                bool find = false;
                for(int id = 0; id < std::size(f.squares); id++)
                    if(iPosition == f.squares[id]) {
                        if(id>=10)
                            std::cout  << (char)('A' + (id-10)) << " ";
                        else
                            std::cout  << id << " ";
                        find = true;
                    }
                        
                if(find == false)
                    std::cout  << ". ";
                
            }
            std::cout  << iLine << std::endl;
        }
        std::cout << "  A B C D E F G H \n" << std::endl;
        
        std::cout << "  pattern symetrique" << std::endl;

        std::cout << "\n  A B C D E F G H " << std::endl;
        for(int iLine = 1; iLine<=8; iLine++) {
            std::cout  << iLine << " ";
            for(int iPosition = (9-iLine)*8 - 1; iPosition>(8-iLine)*8-1; iPosition--) {
                bool find = false;
                for(int id = 0; id < std::size(f.squares); id++)
                    if(iPosition == f.squares[rotates[f.symID][id]]) {
                        if(id>=10)
                            std::cout  << (char)('A' + (id-10)) << " ";
                        else
                            std::cout  << id << " ";
                        find = true;
                    }
                        
                if(find == false)
                    std::cout  << ". ";
                
            }
            std::cout  << iLine << std::endl;
        }
        std::cout << "  A B C D E F G H \n" << std::endl;

        std::cout << '\n';
    }


};

// Retourne l'indice du motif symétrique par rapport à l'indice du motif donné
int RXPatternGenerate::index_rotate(int index, int sym_id) {
    
    if(sym_id == 0) //pas de symetrie
        return index;
    
    int id_sym = 0;
    
    int x = index;
    unsigned long n_squares = std::size(rotates[sym_id]);
    
    for(int i = 0; i<n_squares; ++i) {
        int r = x % 3;
        x/= 3;
        
        if(r == 2){
            r = -1;
            x += 1;
        } else if (r == -2) {  // cas si % renvoie négatif
            r =  1;
            x -= 1;
        }

        id_sym += r * pow3[rotates[sym_id][i]];
        
    }
    
    return id_sym;
};


// Génère automatiquement les méthodes 'set' et 'flip' pour l’othellier,
// en suivant la définition des motifs (patterns) utilisés
void RXPatternGenerate::generate_method() {


    std::string signature = "inline void RXPattern::set_BLACK_";
    unsigned int color = BLACK;
    unsigned int offset = 1;
    
    generate_method(signature, color, offset);
    
    std::cout << std::endl;
    
    signature = "inline void RXPattern::set_WHITE_";
    color = WHITE;
    offset = 1;

    generate_method(signature, color, offset);
    
    std::cout << std::endl;

    signature = "inline void RXPattern::flip_BLACK_";
    color = BLACK;
    offset = 2;

    generate_method(signature, color, offset);
    
    std::cout << std::endl;

    signature = "inline void RXPattern::flip_WHITE_";
    color = WHITE;
    offset = 2;

    generate_method(signature, color, offset);
    
    std::cout << std::endl;

};

void RXPatternGenerate::generate_method(std::string signature, unsigned int color, unsigned int offset) {
    
    for(int pos = A1; pos >= H8; --pos) {
 
        if((pos-7)%8  == 0)
            std::cout << std::endl;

        if(offset == 2 && (pos == A1 || pos == A8 || pos == H1 || pos == H8))
            continue;
        
        
        std::cout << signature << RXMove::index_to_coord(pos) << "() { ";
        
        for(int i = 0; i<std::size(pattern_def); ++i) {
            const auto& f = pattern_def[i];
            
            unsigned int id = 0;
            for (int s : f.squares) {
                if (pos == s) {
                    std::cout  << "patt[" << std::setw(2) << i << "] " << (color == BLACK? " -= ":" += ") << std::setw(7) << offset*pow3[id] << "; ";
                    break;
                }
                ++id;
            }

        }
            
        std::cout << "};" <<std::endl;
        
    }
    
};


// Transforme les données brutes en données structurées,
// organisées par stage
void RXPatternGenerate::rawdata_to_stage() {
    
    std::string dir_str = "/Users/caussebruno/Documents/developpement/database/Roxane";
    //std::string file_name_in = "/Users/caussebruno/Documents/developpement/database/edax/LotK-6Mpositions-MG24@80-EG32@80-24@100-resultatFinal.txt";

    for( unsigned int stage = 0; stage<60; ++stage){
        
        //std::string file_name_in;
        std::string file_name_out;
        
        std::ostringstream oss_out;
        oss_out << std::setw(2) << std::setfill('0') << stage;
        file_name_out = dir_str + "/stages/stage_" + oss_out.str() + ".txt";
        
        std::cout << file_name_out << std::endl;
        
        std::ofstream ofs(file_name_out.c_str());
        
        if(ofs) {
            
            for(int i = 1; i <= 8; ++i) {
                
                std::ostringstream oss_in;
                oss_in << std::setw(2) << std::setfill('0') << i;
                std::string file_name_in = dir_str + "/base_" + oss_in.str() + ".txt";
                
                
                std::ifstream in(file_name_in.c_str());
                if(in) {
                    
                    std::string line;
                    
                    while(std::getline(in, line)){
                        
                        auto n_empty = std::count(line.begin(), line.begin() + std::min<size_t>(64, line.size()), '-');
                        
                        if(stage == 60-n_empty) {
                            
                            ofs << line << std::endl;
                            
                        }
                    }
                    in.close();
                } else {
                    std::cout << "erreur lecture : " << file_name_in.c_str() << std::endl;
                }
                
                
                
            }
            
            ofs.close();
        }
    }
    
};

// la methode realise le traitement suivant
// lecture du fichier texte : stage_xx.txt
// produit un othellier et les index des patterns
// transforme les index en index canoniques puis en index globaux
// ecrit un fichier texte data_xx.txt contenant les index globaux et le score associé

// les dossiers stages_WS/ et datas/ doivent existés

/*
void RXPatternGenerate::stage_to_data(const unsigned int stage) {
    
    std::string dir_str = "/Users/caussebruno/Documents/developpement/";
    
    std::ostringstream oss;
    oss << std::setw(2) << std::setfill('0') << stage;
    
    std::string file_name_in = dir_str + "/database/Edax_Egrcd_Roxane/stages_WS/stage_" + oss.str() + ".txt";
    std::string file_name_out = dir_str + "/Evaluation/datas/data_" + oss.str() + ".txt";
    
    std::ofstream ofs(file_name_out.c_str());
    
    if(ofs) {

        std::ifstream in(file_name_in.c_str());
        if(in) {
            
            std::string line;
            
            while(std::getline(in, line)) {
                
                std::stringstream ss;
                int score;
                ss << line.substr(line.find(" ")+1);
                ss >> score;
                
                std::string othellier = line.substr(0, 65) + 'X';
                
                RXBBPatterns sBoard;
                sBoard.build(othellier);
                
                std::ostringstream oss;
                int* patt = sBoard.pattern->patt;
                for(int id_patt = 0; id_patt<std::size(sBoard.pattern->patt); ++id_patt) {
                    
                    //find pattern description
                    unsigned int id_info = 0;
                    for(; id_info < std::size(pattern_info); ++id_info)
                        if(pattern_info[id_info][0] >= id_patt )
                            break;
                    
                    //canonisation de l'index
                    int pattern_ID = index_rotate(patt[id_patt], pattern_def[id_patt].symID);
                    pattern_ID = std::min(patt[id_patt],pattern_ID);
                    //transformation index local => index global
                    pattern_ID += pattern_info[id_info][2]/2;
                    pattern_ID += pattern_info[id_info][1];
                    
                    oss << pattern_ID << " ";
                    
                }
                
                oss << score;
                
                ofs << oss.str() << std::endl;
                    
            }

            
            in.close();
        }

        ofs.close();
    }
    

};
 */

void RXPatternGenerate::stage_to_data(const unsigned int stage) {
    
    std::string dir_str = "/Users/caussebruno/Documents/developpement/";
    
    std::ostringstream oss;
    oss << std::setw(2) << std::setfill('0') << stage;
    
    std::cout << "stage " << oss.str() << std::endl;
    
    std::string file_name_in = dir_str + "/database/Edax_Egrcd_Roxane/stages/stage_" + oss.str() + ".txt";
    std::string file_name_out = dir_str + "/Evaluation/datas/data_" + oss.str() + ".txt";

//    std::string file_name_in = dir_str + "/database/Edax_Egrcd_Roxane/stages_WS/stage_" + oss.str() + ".txt";
//    std::string file_name_out = dir_str + "/Evaluation/datas_WS/data_" + oss.str() + ".txt";
    
    std::ofstream ofs(file_name_out.c_str());
    
    if(ofs) {

        std::ifstream in(file_name_in.c_str());
        if(in) {
            
            std::string line;
            std::ostringstream oss;
            
            int mobility_max = pattern_info[0][2] - 1;

            while(std::getline(in, line)) {
                
                oss.str(""); // Vider le contenu
                oss.clear(); // Réinitialiser les flags

                
                std::stringstream ss;
                int score;
                ss << line.substr(line.find(" ")+1);
                ss >> score;
                
                std::string othellier = line.substr(0, 65) + 'X';
                
                RXBBPatterns sBoard;
                sBoard.build(othellier);
                
                //mobility
                uint64x2_t mobilities = sBoard.board.dual_count_legal_moves();
                int mob_player   = std::min(mobility_max, static_cast<int>(vgetq_lane_u64(mobilities, 0)));
                oss << mob_player << " ";
                int mob_opponent = std::min(mobility_max, static_cast<int>(vgetq_lane_u64(mobilities, 1)));
                oss << (mob_opponent+(pattern_info[1][1])) << " ";
                
                /*
                if(mob_player == 0)
                    std::cout << line << std::endl;
                */
                
                unsigned long long filled = sBoard.board.discs[BLACK] | sBoard.board.discs[WHITE];

                
                int* patt = sBoard.pattern->patt;
                for(int id_patt = 0; id_patt<std::size(sBoard.pattern->patt); ++id_patt) {
                    
                    //ici ce sont les indices reels de patterns il faut les decaler de 2 pour inclure les mobilités
                    
                    // On saute explicitement les indices Alternatifs
                    // 18, 19, 20, 21
                    if((id_patt > 21 && id_patt <= 25)) {
                        continue;
                    }
                    
                    int id_patt_2 = id_patt;

                    if(id_patt == 18 && ((filled & 0x8142000000000000ULL) == 0)) {         //A1 H1 B2 G2
                        id_patt_2 += 4;
                    } else if(id_patt == 19 && ((filled & 0x0102000000000201ULL) == 0)) {  //H1 G2 G7 H8
                        id_patt_2 += 4;
                    } else if(id_patt == 20 && ((filled & 0x0000000000004281ULL) == 0)) {  //B7 G7 A8 H8
                        id_patt_2 += 4;
                    } else if(id_patt == 21 && ((filled & 0x8040000000004080ULL) == 0)) {  //A1 B2 B7 A8
                        id_patt_2 += 4;
//                    } else if((id_patt == 46) && ((filled & 0x8040000000000000ULL) == 0)) {
//                        id_patt_2 += 4;
//                    } else if((id_patt == 47) && ((filled & 0x0102000000000000ULL) == 0)) {
//                        id_patt_2 += 4;
//                    } else if((id_patt == 48) && ((filled & 0x0000000000000201ULL) == 0)) {
//                        id_patt_2 += 4;
//                    } else if((id_patt == 49) && ((filled & 0x0000000000004080ULL) == 0)) {
//                        id_patt_2 += 4;
                    }

                    //find pattern description
                    unsigned int id_info = 0;
                    for(; id_info < std::size(pattern_info); ++id_info)
                        if(pattern_info[id_info][0] >= (id_patt_2 + 2) ) // add mobilities pattern
                            break;
 
                    //canonisation de l'index
                    int pattern_ID = index_rotate(patt[id_patt_2], pattern_info[id_info][3]);
                    pattern_ID = std::min(patt[id_patt_2],pattern_ID);
                    //transformation index local => index global
                    pattern_ID += pattern_info[id_info][2]/2;
                    pattern_ID += pattern_info[id_info][1];
                    
                    oss << pattern_ID << " ";
                    
                }
                
                oss << score;
                
                ofs << oss.str() << std::endl;
                    
            }

            
            in.close();
        }

        ofs.close();
    }
    
    std::cout << std::endl;

}

void RXPatternGenerate::RMSE(const unsigned int stage) {
    
    std::string dir_str = "/Users/caussebruno/Documents/developpement/";
    
    std::ostringstream oss;
    oss << std::setw(2) << std::setfill('0') << stage;
        
    std::string file_name_in = dir_str + "/database/Edax_Egrcd_Roxane/stages/stage_" + oss.str() + ".txt";


    std::ifstream in(file_name_in.c_str());
    if(in) {
        
        std::string line;
        
        // Accumulateurs RMSE
        double sum_sq_err = 0.0;
        long   n_positions = 0;
        
        while(std::getline(in, line)) {
                        
            std::stringstream ss;
            int score;
            ss << line.substr(line.find(" ")+1);
            ss >> score;
            
            std::string othellier = line.substr(0, 65) + 'X';
            
            RXBBPatterns sBoard;
            sBoard.build(othellier);

#ifdef FACT_MACH
            int eval = sBoard.get_score(true);
#else
            int eval = sBoard.get_score();
#endif

            
            // Calcul du RMSE
            double err = static_cast<double>(eval - score);
            sum_sq_err += err * err;
            ++n_positions;
            
            
        }
        
        // Affichage RMSE du stage
        if(n_positions > 0) {
            double rmse = std::sqrt(sum_sq_err / static_cast<double>(n_positions));
            std::cout << "stage " << oss.str()
#ifdef FACT_MACH
            << "  RMSE FM= " << std::fixed << std::setprecision(4) << rmse
#else
            << "  RMSE= " << std::fixed << std::setprecision(4) << rmse
#endif
            << std::endl;
        } else {
            std::cout << "  stage " << oss.str() << "  aucune position" << std::endl;
        }
        
        in.close();
    }

    
    std::cout << std::endl;

}

/**
 * @brief Écrit les poids d'évaluation des stages dans un fichier binaire normalisé.
 *
 * Cette fonction lit les poids bruts stage par stage à partir d'un fichier texte,
 * applique des normalisations ( moyenne des poids symetriques et miroirs)
 * et écrit les résultats, stage par stage, dans un format binaire.
 * */

void RXPatternGenerate::write_eval() {
    
    //nombre d'index globaux
    const unsigned int n_index = N_INDEX;
    
    std::string dir_str = "/Users/caussebruno/Documents/developpement/Evaluation";
    
    std::string file_name_out = dir_str + "/weight_v12.bin";
    // 2. Ouvrir le fichier en mode ecriture binaire
    // ios::out pour l'ecriture et ios::binary pour le mode binaire
    std::ofstream out(file_name_out, std::ios::out | std::ios::binary);
    

    if (out.is_open()) {

        for(unsigned int stage = 0; stage<60; ++stage) {
            
            std::cout << "stage : " << stage << std::endl;
            
            std::ostringstream oss;
            oss << std::setw(2) << std::setfill('0') << stage;
            
//            std::string file_weigths_in = dir_str + "/weights_SG_W5_P3/weight_" + oss.str() + ".txt";
            std::string file_weigths_in = dir_str + "/weights/weight_" + oss.str() + ".txt";
            std::string file_n_occs_in = dir_str + "/n_occs/n_occ_" + oss.str() + ".txt";

            float* weigths_in = new float[n_index];
            int* n_occs_in = new int[n_index];
            
            float weigth = 0.0f;
            int n_occ = 0;
            
            std::ifstream weigths_ifs(file_weigths_in.c_str());
            std::ifstream n_occs_ifs(file_n_occs_in.c_str());

            
            if (weigths_ifs.is_open() && n_occs_ifs.is_open()) {
                std::cout << "Ouverture des fichiers reussies. Lecture des donnees..." << std::endl;
                
                // 2. Boucle de lecture jusqu'a la fin du fichier (ou erreur)
                // La condition 'fichier >> valeur_lue' est vraie tant qu'un float peut etre lu.
                unsigned int i = 0;
                while (weigths_ifs >> weigth && n_occs_ifs >> n_occ) {
                    // 3. Ajout de la valeur lue dans le tableau
                    weigths_in[i] = weigth;
                    n_occs_in[i] = n_occ;
                    ++i;
                }
                
                // 4. Verification de la raison de la sortie de la boucle
                if (weigths_ifs.eof() && n_occs_ifs.eof()) {
                    // Sortie normale : la fin des fichiers a été atteinte.
                    std::cout << "Lecture terminee : Fin du fichier atteinte." << std::endl;
                } else if (weigths_ifs.fail() && n_occs_ifs.fail() && i != 0) {
                    // La derniere tentative de lecture a echouee (ex: caractere non-numerique)
                    std::cerr << "Attention : La lecture a ete interrompue par une entree non-valide." << std::endl;
                } else if (weigths_ifs.fail() && n_occs_ifs.fail() && i == 0) {
                    // Aucune valeur n'a pu être lue (fichier vide ou premier element non-float)
                    std::cerr << "Erreur : Le fichier est vide ou la premiere entree n'est pas un float." << std::endl;
                }
                
                // 5. Fermeture des fichiers
                weigths_ifs.close();
                n_occs_ifs.close();
                
            } else {
                std::cerr << "Erreur : Impossible d'ouvrir le/les fichier(s) '" << file_weigths_in << "' '" << file_n_occs_in << "'" << std::endl;
                return;
            }
            
            
            short* weigths_out= new short[n_index];
            

            for(unsigned int id_patt = 0; id_patt < std::size(pattern_info); ++id_patt)
                if(id_patt == 0) {
                    for(int i = 0; i<24; i++)
                        weigths_out[i] = weigths_in[i]*256; //mobility player
                } else if(id_patt == 1) {
                    for(int i = 24; i<48; i++)
                        weigths_out[i] = weigths_in[i]*256; //mobility opponent
                } else {
                    norm_weight(weigths_in, n_occs_in, weigths_out, pattern_info[id_patt][1], pattern_info[id_patt][2], pattern_info[id_patt][3]);
                }
            
            
            // 4. Ecriture des donnees
            // weigths_out retourne un pointeur vers le premier element
            out.write(
                reinterpret_cast<const char*>(weigths_out), // Pointeur casté
                sizeof(short)*n_index                       // Taille en octets
            );

            if (out.good()) {
                std::cout << "Ecriture reussie de " << n_index
                          << " short (" << sizeof(short)*n_index << " octets)." << std::endl;
            } else {
                std::cerr << "Erreur lors de l'ecriture des donnees." << std::endl;
            }

            // LIBERER LA MEMOIRE à la fin de chaque itération
            delete[] weigths_in;
            delete[] n_occs_in;
            delete[] weigths_out;

            std::cout << std::endl;

        }
    } else {
        std::cerr << "Erreur : Impossible d'ouvrir le fichier '" << file_name_out << "'" << std::endl;
    }

    // 5. Fermeture du fichier
    out.close();

    
}

//normalise les poids pour les index miroirs et inverses des patterns
void RXPatternGenerate::norm_weight(float* weigths_in, int* n_occs_in, short* weigths_out, unsigned int id_start, unsigned int n_index_local, unsigned int id_rot) {
    
    // offset pour retrouver le codage ternaire {-1, 0, 1} = {noir, vide, blanc}
    unsigned int offset_local = n_index_local/2;
    
    std::vector<bool> processed_index(n_index_local, false);
    
    // parcourt la moitié des index
    for(int i = 0; i <= offset_local; i++) {
        
        
        if(processed_index[i])
            continue;
        
        
        //calule l'index inverse et les index miroir en codage naturel
        int p_idx = i;
        int p_inv = (n_index_local-1) - p_idx;
        
        //pour les index miroirs passage par le mode ternaire avant de retrouver le codage naturel
        int p_sym_idx = index_rotate(p_idx-offset_local, id_rot) + offset_local;
        int p_sym_inv = index_rotate(p_inv-offset_local, id_rot) + offset_local;
        
        
        //index traité
        processed_index[p_idx]     = true;
        processed_index[p_inv]     = true;
        processed_index[p_sym_idx] = true;
        processed_index[p_sym_inv] = true;
        
        
        //calcule des index globaux
        p_idx     += id_start;
        p_inv     += id_start;
        p_sym_idx += id_start;
        p_sym_inv += id_start;
        

        /*
        //les poids calculés sont dans les indices canoniques
        //mix weights
        //idee mixer les poids avec ponderation des occurences
        double temp = (n_occs_in[p_idx] * weigths_in[p_idx]) - (n_occs_in[p_sym_inv] * weigths_in[p_sym_inv]);
        temp /= (n_occs_in[p_idx]+n_occs_in[p_sym_inv]);
                             
        short weight = static_cast<short>(std::round(temp*256));
        
        //save
        weigths_out[p_idx]      =  weight;
        weigths_out[p_inv]      = -weight;
        weigths_out[p_sym_idx]  =  weight;
        weigths_out[p_sym_inv]  = -weight;
        */
        

        //on ne mixe pas les poids (semble meilleur)

        short weight_B = static_cast<short>(std::round(weigths_in[p_idx]*256));
        short weight_W = static_cast<short>(std::round(weigths_in[p_sym_inv]*256));

        weigths_out[p_idx]      =  weight_B;
        weigths_out[p_inv]      =  weight_W;
        weigths_out[p_sym_idx]  =  weight_B;
        weigths_out[p_sym_inv]  =  weight_W;
        

    }

}




void RXPatternGenerate::write_FM() {
    
    
    std::string dir_str = "/Users/caussebruno/Documents/developpement/Evaluation" ;
    
    std::string file_name_out = dir_str + "/fm_V_v11.bin";
    // 2. Ouvrir le fichier en mode ecriture binaire
    // ios::out pour l'ecriture et ios::binary pour le mode binaire
    std::ofstream out(file_name_out, std::ios::out | std::ios::binary);
    

    if (out.is_open()) {
        
        std::string file_fm_in = dir_str + "/models_fm/fm_V.bin";
        std::ifstream fm_ifs(file_fm_in.c_str(), std::ios::binary);

        short* fm_in = new short[N_INDEX * RANK]();
                
        if (fm_ifs.is_open()) {
            std::cout << "Ouverture du fichier reussie. Lecture des donnees..." << std::endl;
            
            // 2. Boucle de lecture jusqu'a la fin du fichier (ou erreur)
            // La condition 'fichier >> valeur_lue' est vraie tant qu'un float peut etre lu.
            
            //mobility player id_patt = 0
            fm_ifs.read(reinterpret_cast<char*> (fm_in), sizeof(short)*N_INDEX * RANK);
            
            // 4. Verification de la raison de la sortie de la boucle
            if (fm_ifs.eof()) {
                // Sortie normale : la fin des fichiers a été atteinte.
                std::cout << "Lecture terminee : Fin du fichier atteinte." << std::endl;
            } else if (fm_ifs.fail()) {
                // La derniere tentative de lecture a echouee (ex: caractere non-numerique)
                std::cerr << "Attention : La lecture a ete interrompue" << std::endl;
            }
            
            // 5. Fermeture des fichiers
            fm_ifs.close();
            
        } else {
            std::cerr << "Erreur : Impossible d'ouvrir le fichier '" << file_fm_in << "'" << std::endl;
            return;
        }
                
        for(unsigned int id_patt = 0; id_patt < std::size(pattern_info); ++id_patt){
            if(id_patt > 1) //mobility
                norm_fm(fm_in, pattern_info[id_patt][1], pattern_info[id_patt][2], pattern_info[id_patt][3]);
        }
    
    
        // 4. Ecriture des donnees
        // weigths_out retourne un pointeur vers le premier element
        // écriture en AoS directement
        out.write(
            reinterpret_cast<const char*>(fm_in), // Pointeur casté
                  sizeof(short)*N_INDEX*RANK      // Taille en octets
        );

        if (out.good()) {
            std::cout << "Ecriture reussie de " << N_INDEX*RANK
            << " short (" << sizeof(short)*N_INDEX*RANK << " octets)." << std::endl;
        } else {
            std::cerr << "Erreur lors de l'ecriture des donnees." << std::endl;
        }
    
        // LIBERER LA MEMOIRE à la fin de chaque itération
        delete[] fm_in;
    
        std::cout << std::endl;
    
    } else {
        std::cerr << "Erreur : Impossible d'ouvrir le fichier '" << file_name_out << "'" << std::endl;
    }

    // 5. Fermeture du fichier
    out.close();

}

void RXPatternGenerate::norm_fm(short* fm_in, unsigned int id_start,
                                 unsigned int n_index_local, unsigned int id_rot) {

    unsigned int offset_local = n_index_local / 2;

    // Snapshot de la région : lectures depuis fm_orig, écritures dans fm_in
    std::vector<short> fm_orig(fm_in + id_start * RANK,
                               fm_in + (id_start + n_index_local) * RANK);

    auto get = [&](unsigned int local_idx, unsigned int r) -> short {
        return fm_orig[local_idx * RANK + r];
    };
    auto set = [&](unsigned int global_idx, unsigned int r, short val) {
        fm_in[global_idx * RANK + r] = val;
    };

    std::vector<bool> processed_index(n_index_local, false);

    for (unsigned int i = 0; i < n_index_local; i++) {

        if (processed_index[i]) continue;

        int p_idx     = i;
        int p_inv     = (n_index_local - 1) - p_idx;
        int p_sym_idx = index_rotate(p_idx - (int)offset_local, id_rot) + offset_local;
        int p_sym_inv = index_rotate(p_inv - (int)offset_local, id_rot) + offset_local;

        if (p_sym_idx < 0 || p_sym_idx >= (int)n_index_local ||
            p_sym_inv < 0 || p_sym_inv >= (int)n_index_local) continue;

        for (unsigned int r = 0; r < RANK; r++) {
            set(id_start + p_sym_idx, r, get(p_idx,     r));
            set(id_start + p_inv,     r, get(p_sym_inv, r));
        }

        processed_index[p_idx]     = true;
        processed_index[p_inv]     = true;
        processed_index[p_sym_idx] = true;
        processed_index[p_sym_inv] = true;
    }
}


void RXPatternGenerate::encode_eval() {

    //charge l'eval
    RXEvaluation::load();
    
    //creation new patterns
    short* eval_2[60][2];
    
    for(unsigned int iStage = 0; iStage<60; ++iStage) {
        
        //corner 13
        eval_2[iStage][0] = new short[1594323];
        eval_2[iStage][0] += 1594323/2;
        
        //edge 8+6
        eval_2[iStage][1] = new short[4782969];
        eval_2[iStage][1] += 4782969/2;
        
        
        for(int id0 =-1; id0<2; ++id0) {
            for(int id1 =-1; id1<2; ++id1) {
                for(int id2 =-1; id2<2; ++id2) {
                    for(int id3 =-1; id3<2; ++id3) {
                        for(int id4 =-1; id4<2; ++id4) {
                            for(int id5 =-1; id5<2; ++id5) {
                                for(int id6 =-1; id6<2; ++id6) {
                                    for(int id7 =-1; id7<2; ++id7) {
                                        for(int id8 =-1; id8<2; ++id8) {
                                            for(int id9 =-1; id9<2; ++id9) {
                                                for(int idA =-1; idA<2; ++idA) {
                                                    for(int idB =-1; idB<2; ++idB) {
                                                        for(int idC =-1; idC<2; ++idC) {
                                                            
                                                            int pattern_13 = id0*pow3[0] + id1*pow3[1] + id2*pow3[2] + id3*pow3[3]
                                                            + id4*pow3[4] + id5*pow3[5] + id6*pow3[6] + id7*pow3[7]
                                                            + id8*pow3[8] + id9*pow3[9] + idA*pow3[10] + idB*pow3[11]
                                                            + idC*pow3[12];
                                                            
                                                            if(id5 == 0 && id6 == 0) {
                                                                int corner2 = id0*pow3[0] + id1*pow3[1] + id2*pow3[2] + id3*pow3[3] + id4*pow3[4] + id7*pow3[5] + id8*pow3[6] + id9*pow3[7] + idA*pow3[8] + idB*pow3[9] + idC*pow3[10];
                                                                eval_2[iStage][0][pattern_13] = RXEvaluation::eval_w[iStage][14][corner2];
                                                            } else {
                                                                int corner1 = id0*pow3[0] + id3*pow3[1] + id2*pow3[2] + id4*pow3[3] + id5*pow3[4] + id6*pow3[5] + id7*pow3[6] + id8*pow3[7] + idA*pow3[8] + id9*pow3[9] + idC*pow3[10];
                                                                eval_2[iStage][0][pattern_13] = RXEvaluation::eval_w[iStage][13][corner1];
                                                            }
                                                            
                                                            for(int idD =-1; idD<2; ++idD) {
                                                                
                                                                int pattern_14 = pattern_13 + idD*pow3[13];
                                                                
                                                                if (id2 == 0 && id3 == 0 && idA == 0 && idB == 0) {
                                                                    int edge2 = id0*pow3[0] + id1*pow3[1] + id4*pow3[2] + id5*pow3[3] + id6*pow3[4] + id7*pow3[5] + id8*pow3[6] + id9*pow3[7] + idC*pow3[8] + idD*pow3[9];
                                                                    eval_2[iStage][1][pattern_14] = RXEvaluation::eval_w[iStage][7][edge2];
                                                                } else {
                                                                    int edge1 = id2*pow3[0] + id3*pow3[1] + id4*pow3[2] + id5*pow3[3] + id6*pow3[4] + id7*pow3[5] + id8*pow3[6] + id9*pow3[7] + idA*pow3[8] + idB*pow3[9];
                                                                    eval_2[iStage][1][pattern_14] = RXEvaluation::eval_w[iStage][6][edge1];
                                                                }
                                                                
                                                                //                                                            for(int idE =-1; idE<2; ++idE) {
                                                                //
                                                                //
                                                                //                                                                for(int idF =-1; idF<2; ++idF) {
                                                                //
                                                                //                                                                    int pattern_16 = id0*pow3[0] + id1*pow3[1] + id2*pow3[2] + id3*pow3[3]
                                                                //                                                                    + id4*pow3[4] + id5*pow3[5] + id6*pow3[6] + id7*pow3[7]
                                                                //                                                                    + id8*pow3[8] + id9*pow3[9] + idA*pow3[10] + idB*pow3[11]
                                                                //                                                                    + idC*pow3[12] + idD*pow3[13] + idE*pow3[14] + idF*pow3[15];
                                                                //
                                                                //                                                                    int hv2     = id3*pow3[0] + id2*pow3[1] + id1*pow3[2] + id0*pow3[3] + idF*pow3[4] + idE*pow3[5] + idD*pow3[6] + idC*pow3[7];
                                                                //                                                                    int edge3   = id2*pow3[0] + id3*pow3[1] + id4*pow3[2] + id5*pow3[3] + id6*pow3[4] + id9*pow3[5] + idA*pow3[6] + idB*pow3[7] + idC*pow3[8] + idD*pow3[9];
                                                                //                                                                    int edge4a  = idF*pow3[0] + id0*pow3[1] + id1*pow3[2] + id2*pow3[3] + id3*pow3[4] + id4*pow3[5] + id5*pow3[6] + id6*pow3[7] + id7*pow3[8] + id8*pow3[9];
                                                                //                                                                    int edge4b  = id0*pow3[0] + idF*pow3[1] + idE*pow3[2] + idD*pow3[3] + idC*pow3[4] + idB*pow3[5] + idA*pow3[6] + id9*pow3[7] + id8*pow3[8] + id7*pow3[9];
                                                                //
                                                                //                                                                    if (id2 == 0 && id4 == 0 && idB == 0 && idD == 0) {
                                                                //
                                                                //                                                                        int edge2 = id0*pow3[0] + id1*pow3[1] + id5*pow3[2] + id6*pow3[3] + id7*pow3[4] + id8*pow3[5] + id9*pow3[6] + idA*pow3[7] + idE*pow3[8] + idF*pow3[9];
                                                                //
                                                                //                                                                        for(unsigned int iStage = 0; iStage<60; ++iStage) {
                                                                //
                                                                //                                                                            int score  = RXEvaluation::eval[iStage][10][hv2];
                                                                //                                                                            score     += RXEvaluation::eval[iStage][8][edge3];
                                                                //                                                                            score     += RXEvaluation::eval[iStage][9][edge4a];
                                                                //                                                                            score     += RXEvaluation::eval[iStage][9][edge4b];
                                                                //                                                                            score     += RXEvaluation::eval[iStage][7][edge2];
                                                                //
                                                                //                                                                            if(-32768 <= score && score <= 32767)
                                                                //                                                                                eval_2[iStage][0][pattern_16] = score;
                                                                //                                                                            else
                                                                //                                                                                std::cout << "erreur capacité short" << std::endl;
                                                                //
                                                                //                                                                        }
                                                                //
                                                                //                                                                    } else {
                                                                //
                                                                //                                                                        int edge1 = id2*pow3[0] + id4*pow3[1] + id5*pow3[2] + id6*pow3[3] + id7*pow3[4] + id8*pow3[5] + id9*pow3[6] + idA*pow3[7] + idB*pow3[8] + idD*pow3[9];
                                                                //
                                                                //                                                                        for(unsigned int iStage = 0; iStage<60; ++iStage) {
                                                                //
                                                                //                                                                            int score  = RXEvaluation::eval[iStage][10][hv2];
                                                                //                                                                            score     += RXEvaluation::eval[iStage][8][edge3];
                                                                //                                                                            score     += RXEvaluation::eval[iStage][9][edge4a];
                                                                //                                                                            score     += RXEvaluation::eval[iStage][9][edge4b];
                                                                //                                                                            score     += RXEvaluation::eval[iStage][6][edge1];
                                                                //
                                                                //                                                                            if(-32768 <= score && score <= 32767)
                                                                //                                                                                eval_2[iStage][0][pattern_16] = score;
                                                                //                                                                            else
                                                                //                                                                                std::cout << "erreur capacité short" << std::endl;
                                                                //
                                                                //                                                                        }
                                                                //                                                                    }
                                                                //                                                                }
                                                                //                                                            }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    

    //ecriture de l'evaluation
    std::string dir_str = "/Users/caussebruno/Documents/developpement/Evaluation";
    
    std::string file_name_out = dir_str + "/eval_v10.1.bin";
    // 2. Ouvrir le fichier en mode ecriture binaire
    // ios::out pour l'ecriture et ios::binary pour le mode binaire
    std::ofstream out(file_name_out, std::ios::out | std::ios::binary);

    if (out.is_open()) {
        
        for(unsigned int iStage = 0; iStage<60; ++iStage) {
            
            //std::cout << "ecriture stage : " << iStage << std::endl;
            
            //diag 5 id_patt = 2
            RXEvaluation::eval_w[iStage][2] -= 243/2;
            //diag 6 id_patt = 3
            RXEvaluation::eval_w[iStage][3] -= 729/2;
            //diag 7 id_patt = 4
            RXEvaluation::eval_w[iStage][4] -= 2187/2;
            //diag 8 id_patt = 5
            RXEvaluation::eval_w[iStage][5] -= 6561/2;

            eval_2[iStage][1] -= 4782969/2;

            //diag 8 id_patt = 5
            RXEvaluation::eval_w[iStage][8] -= 59049/2;
            //diag 8 id_patt = 5
            RXEvaluation::eval_w[iStage][9] -= 59049/2;

            //hv_2 id_patt = 10
            RXEvaluation::eval_w[iStage][10] -= 6561/2;
            //hv_3 id_patt = 10
            RXEvaluation::eval_w[iStage][11] -= 6561/2;
            //hv_4 id_patt = 11
            RXEvaluation::eval_w[iStage][12] -= 6561/2;

            eval_2[iStage][0] -= 1594323/2;
            
            
            //mob player
            out.write(reinterpret_cast<const char*>(RXEvaluation::eval_w[iStage][0]), 24*sizeof(short));
            //mob opponent
            out.write(reinterpret_cast<const char*>(RXEvaluation::eval_w[iStage][1]), 24*sizeof(short));

            //diag 5
            out.write(reinterpret_cast<const char*>(RXEvaluation::eval_w[iStage][2]), 243*sizeof(short));
            //diag 6
            out.write(reinterpret_cast<const char*>(RXEvaluation::eval_w[iStage][3]), 729*sizeof(short));
            //diag 7
            out.write(reinterpret_cast<const char*>(RXEvaluation::eval_w[iStage][4]), 2187*sizeof(short));
            //diag 8
            out.write(reinterpret_cast<const char*>(RXEvaluation::eval_w[iStage][5]), 6561*sizeof(short));

            // edge 8+6
            out.write(reinterpret_cast<const char*>(eval_2[iStage][1]), 4782969*sizeof(short));
            
            //hv 2
            out.write(reinterpret_cast<const char*>(RXEvaluation::eval_w[iStage][8]), 59049*sizeof(short));
            //hv 3
            out.write(reinterpret_cast<const char*>(RXEvaluation::eval_w[iStage][9]), 59049*sizeof(short));


            //hv 2
            out.write(reinterpret_cast<const char*>(RXEvaluation::eval_w[iStage][10]), 6561*sizeof(short));
            //hv 3
            out.write(reinterpret_cast<const char*>(RXEvaluation::eval_w[iStage][11]), 6561*sizeof(short));
            //hv 4
            out.write(reinterpret_cast<const char*>(RXEvaluation::eval_w[iStage][12]), 6561*sizeof(short));
            
            // corner 5/4/3/2/1
            out.write(reinterpret_cast<const char*>(eval_2[iStage][0]), 1594323*sizeof(short));

            //diag 5 id_patt = 2
            RXEvaluation::eval_w[iStage][2] += 243/2;
            //diag 6 id_patt = 3
            RXEvaluation::eval_w[iStage][3] += 729/2;
            //diag 7 id_patt = 4
            RXEvaluation::eval_w[iStage][4] += 2187/2;
            //diag 8 id_patt = 5
            RXEvaluation::eval_w[iStage][5] += 6561/2;

            //edge3
            RXEvaluation::eval_w[iStage][8] += 59049/2;
            //edge4
            RXEvaluation::eval_w[iStage][9] += 59049/2;

            //hv_2 id_patt = 10
            RXEvaluation::eval_w[iStage][10] += 6561/2;
            //hv_3 id_patt = 11
            RXEvaluation::eval_w[iStage][11] += 6561/2;
            //hv_4 id_patt = 12
            RXEvaluation::eval_w[iStage][12] += 6561/2;
            
            delete eval_2[iStage][0];
            delete eval_2[iStage][1];
        }
    }
    
    // 5. Fermeture du fichier
    out.close();



}

int sigma(const int n_empty, const int depth, const int depth_probcut) {
    
    double sigma;
    
    //edax coefficients
    constexpr double probcut_a = -0.10026799;
    constexpr double probcut_b = 0.31027733;
    constexpr double probcut_c = -0.57772603;
    constexpr double probcut_d = 0.07585621;
    constexpr double probcut_e = 1.16492647;
    constexpr double probcut_f = 5.9171698;
    
    
    sigma= probcut_a * n_empty + probcut_b * depth + probcut_c * depth_probcut;
    sigma = probcut_d * sigma * sigma + probcut_e * sigma + probcut_f;
    
    return static_cast<int>(sigma + 0.5);
}


void RXPatternGenerate::probcut_extrapolate() {
    
    //ecriture de l'evaluation
    std::string dir_str = "/Users/caussebruno/Documents/developpement/Evaluation";
    
    std::string file_name_out = dir_str + "/probcut_extrapolated.txt";
    
    std::ofstream ofs(file_name_out.c_str());
    
    if (ofs.is_open()) {
        
        std::ostringstream oss;
        
        
        for(int n_discs = 8; n_discs <= 35; ++n_discs){
            for(int depth = 30; depth <= 40; ++depth) {
                for(int shallow_depth = 0; shallow_depth <= 18; ++shallow_depth){
                    
                    int d = depth - (n_discs & 1);
                    int shallow = shallow_depth + (n_discs & 1);
                    
                    int stddev = sigma(64-n_discs, d, shallow);
                    
                    oss.str(""); // Vider le contenu
                    oss.clear(); // Réinitialiser les flags
                    
                    oss << n_discs << " " << shallow << " " << d << " " << stddev;
                    
                    for(int i = 0; i < 10; ++i)
                        ofs << oss.str() << std::endl;
                    
                    
                    
                }
            }
        }
        
        ofs.close();
        
    }
}










