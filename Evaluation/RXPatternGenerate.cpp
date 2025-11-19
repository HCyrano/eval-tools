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


#include "RXPatternGenerate.hpp"
#include "RXMove.hpp"
#include "RXPattern.hpp"
#include "RXBitBoard.hpp"
#include "RXBBPatterns.hpp"


// Affiche la disposition du motif (pattern) sur l’othellier,
// en montrant les cases concernées et leur ordre
// affiche egalement le pattern symetrique
void RXPatternGenerate::display() {
    
    std::cout << "nombre de  patterns : " << std::size(eval) << std::endl;

    std::cout << "affichage pattern : " << std::endl;
    for(int i = 0; i<std::size(eval); ++i) {
        const auto& f = eval[i];
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
                    if(iPosition == f.squares[sym[f.symID][id]]) {
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

int RXPatternGenerate::patt_id(RXBitBoard board, RXFeature f) {
    
    int patt_id_1 = 0;
    int patt_id_2 = 0;

    for(unsigned int id_1 = 0; id_1<std::size(f.squares); ++id_1) {
        unsigned int id_2 = f.squares[sym[f.symID][id_1]];
        
        unsigned long long pos_1 = 0x1ULL<<id_1;
        
        if(board.discs[BLACK] & pos_1) {
            patt_id_1 -= pow3[id_1];
            patt_id_2 -= pow3[id_2];
        } else if(board.discs[WHITE] & pos_1) {
            patt_id_1 += pow3[id_1];
            patt_id_2 += pow3[id_2];
        }

    }
    
    return patt_id_1 <= patt_id_2 ? patt_id_1: patt_id_2;
    
}

// Retourne l'indice du motif symétrique par rapport à l'indice du motif donné
int RXPatternGenerate::id_sym(int index, int sym_id) {
    
    int id_sym = 0;
    
    int x = index;
    unsigned long n_squares = std::size(sym[sym_id]);
    
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

        id_sym += r * pow3[sym[sym_id][i]];
        
    }
    
    return id_sym;
};


// Génère automatiquement les méthodes 'set' et 'flip' pour l’othellier,
// en suivant la définition des motifs (patterns) utilisés
void RXPatternGenerate::generate_method() {
    
    std::cout << "int patt[" << std::size(eval) << "];" << std::endl;

    std::cout << std::endl;
    
    std::cout << "std::vector<unsigned int> offset_patt = {" << std::endl;
    
    unsigned int offset_patt = 0;
    for(unsigned int i = 0; i<std::size(eval); ++i) {
        
        offset_patt = pow3[std::size(eval[i].squares)]/2;
        std::cout << std::setw(6) << offset_patt << ", " ;

        if(eval[i].lastPatternType)
            std::cout << std::endl; ;

    }

    std::cout << "};" << std::endl;

    std::cout << std::endl;

    std::cout << "std::vector<unsigned int> offset_index = {" << std::endl;
    
    unsigned int offset_index = 0;
    for(unsigned int i = 0; i<std::size(eval); ++i) {
        const auto& f = eval[i];
        if(f.lastPatternType) {
            std::cout << std::setw(6) << offset_index << "," << std::endl ;
            offset_index += pow3[std::size(f.squares)];
        } else {
            std::cout << std::setw(6) << offset_index << ", " ;
        }
        
    }
    
    std::cout << offset_index << std::endl;

    std::cout << "};" << std::endl;

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
        
        for(int i = 0; i<std::size(eval); ++i) {
            const auto& f = eval[i];
            
            unsigned int id = 0;
            for (int s : f.squares) {
                if (pos == s) {
                    std::cout  << "patt[" << std::setw(2) << i << "] " << (color == BLACK? " -= ":" += ") << std::setw(7) << offset*pow3[id] << "; ";
                    break;
                }
                ++id;
            }

        }
        
//        for (const auto& f : eval) {
//            std::string name = f.name;
//            
//            unsigned int id = 0;
//            for (int s : f.square) {
//                if (pos == s) {
//                    std::cout << std::setw(11) << name << (color == BLACK? " -= ":" += ") << std::setw(7) << offset*pow3[id] << "; ";
//                    break;
//                }
//                ++id;
//            }
//        }
            
            
        std::cout << "};" <<std::endl;
        
    }
    
};


// Transforme les données brutes de la base 'egaroucid' en données structurées,
// organisées par stage
void RXPatternGenerate::egrcd_rawdata_to_stage() {
    
    std::string dir_str = "/Users/caussebruno/Documents/developpement/Evaluation";

    for( unsigned int stage = 0; stage<60; ++stage){
        
        std::string file_name_in;
        std::string file_name_out;
        
        std::ostringstream oss_out;
        oss_out << std::setw(2) << std::setfill('0') << stage;
        file_name_out = dir_str + "/stages/stage_" + oss_out.str() + ".txt";
        
        std::cout << file_name_out << std::endl;
        
        std::ofstream ofs(file_name_out.c_str());
        
        if(ofs) {
            
            for(int i = 0; i <= 25; ++i) {
                
                std::ostringstream oss_in;
                oss_in << std::setw(7) << std::setfill('0') << i;
                file_name_in = dir_str + "/Egaroucid_Train_Data/0001_egaroucid_7_5_1_lv17/" + oss_in.str() + ".txt";
                
                
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
                }
                
                
                
            }
            
            ofs.close();
        }
    }
    
};

void RXPatternGenerate::stage_to_data(const unsigned int stage) {
    
    std::string dir_str = "/Users/caussebruno/Documents/developpement/Evaluation";
    
    std::ostringstream oss;
    oss << std::setw(2) << std::setfill('0') << stage;
    
    std::string file_name_in = dir_str + "/stages/stage_" + oss.str() + ".txt";
    std::string file_name_out = dir_str + "/datas/data_" + oss.str() + ".txt";
    
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
                for(int i = 0; i<std::size(sBoard.pattern->patt); ++i) {
                    
                    //normalisation de l'index:
                    int pattern_ID = id_sym(patt[i], eval[i].symID);
                    pattern_ID = std::min(patt[i],pattern_ID);
                    pattern_ID += sBoard.pattern->offset_patt[i];
                    pattern_ID += sBoard.pattern->offset_index[i];
                    
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


void RXPatternGenerate::write_eval(const unsigned int stage) {
    
    std::string dir_str = "/Users/caussebruno/Documents/developpement/Evaluation";
    
    std::ostringstream oss;
    oss << std::setw(2) << std::setfill('0') << stage;
    
    std::string file_name_in = dir_str + "/weights/weight_" + oss.str() + ".txt";
    
    float weigths_in[383697];
    float weigth = 0.0f;
    
    std::ifstream in(file_name_in.c_str());
    if (in.is_open()) {
            std::cout << "Ouverture du fichier reussie. Lecture des donnees..." << std::endl;
            
            // 2. Boucle de lecture jusqu'a la fin du fichier (ou erreur)
            // La condition 'fichier >> valeur_lue' est vraie tant qu'un float peut etre lu.
            unsigned int i = 0;
            while (in >> weigth) {
                // 3. Ajout de la valeur lue dans le tableau
                weigths_in[i] = weigth;
                ++i;
            }

            // 4. Verification de la raison de la sortie de la boucle
            if (in.eof()) {
                // Sortie normale : la fin du fichier a été atteinte.
                std::cout << "Lecture terminee : Fin du fichier atteinte." << std::endl;
            } else if (in.fail() && i != 0) {
                // La derniere tentative de lecture a echouee (ex: caractere non-numerique)
                std::cerr << "Attention : La lecture a ete interrompue par une entree non-valide." << std::endl;
            } else if (in.fail() && i == 0) {
                 // Aucune valeur n'a pu être lue (fichier vide ou premier element non-float)
                std::cerr << "Erreur : Le fichier est vide ou la premiere entree n'est pas un float." << std::endl;
            }

            // 5. Fermeture du fichier
            in.close();

        } else {
            std::cerr << "Erreur : Impossible d'ouvrir le fichier '" << file_name_in << "'" << std::endl;
            return;
        }
    
        short weigths_out[383697];
        
        //norm_weight(weigths_in, weigths_out, 0, 243, 2);

};

void RXPatternGenerate::norm_weight(float* weigths, short* weigths_out, unsigned int id_start, unsigned int n_weights, unsigned int sym) {
    
    unsigned int id_end = id_start + n_weights;

    for(int i = id_start; i <= id_end/2; i++) {
                
        int p_idx = i;
        int p_inv = (n_weights-1) - p_idx;

        int p_sym_idx = id_sym(p_idx-n_weights/2, 2) + 243/2;
        int p_sym_inv = id_sym(p_inv-n_weights/2, 2) + 243/2;

        float weight_idx = (weigths[p_idx] + weigths[p_sym_idx])/2.0f;
        float weight_inv = (weigths[p_inv] + weigths[p_sym_inv])/2.0f;

        short weight = static_cast<short>(((weight_idx-weight_inv)/2.0f)*256);
        

        weigths_out[p_idx]      =  weight;
        weigths_out[p_inv]      = -weight;
        weigths_out[p_sym_idx]  =  weight;
        weigths_out[p_sym_inv]  = -weight;

        std::cout << "patt[" << std::setw(3) << p_idx << "] = " << weigths_out[p_idx] << std::endl;
        std::cout << "patt[" << std::setw(3) << p_inv << "] = " << weigths_out[p_inv] << std::endl;
        std::cout << "patt[" << std::setw(3) << p_sym_idx << "] = " << weigths_out[p_sym_idx] << std::endl;
        std::cout << "patt[" << std::setw(3) << p_sym_inv << "] = " << weigths_out[p_sym_inv] << std::endl;

        std::cout << std::endl;

    }

};







