/*
 *  RXEvaluation.cpp
 *  Roxane
 *
 *  Created by Bruno Causse on 06/08/05.
 *  Copyleft 2005-2025 personnel.
 *
 */

#include <fstream>

#include "RXEvaluation.hpp"


void RXEvaluation::load() {
    
    
    //create tables
    
    std::ifstream from("/Users/caussebruno/Documents/developpement/Roxane/build/weight_v10.bin", std::ios::binary);
    if(from) {
        
        //chargement des donnees & decalage des tables
        for(unsigned int iStage = 0; iStage<60; iStage++) {
            
            for(unsigned int id_patt = 0; id_patt < 15; ++id_patt) {
                
                eval_w[iStage][id_patt] = new short[sizes[id_patt]];
                from.read(reinterpret_cast<char*> (eval_w[iStage][id_patt]), sizeof(short)*sizes[id_patt]);
                
                if(id_patt == 0 || id_patt == 1)
                    continue;
                
                eval_w[iStage][id_patt] += sizes[id_patt]/2;
            }
        }
                
    } else {
        std::cout << "erreur chargement eval" << std::endl;
    }
    
    from.close();
    
    
    std::ifstream from_0("/Users/caussebruno/Documents/developpement/Roxane/build/fm_w0.bin");
    if(from_0) {
        
        for(unsigned int iStage = 0; iStage<60; iStage++)
            if (!(from_0 >> eval_w0[iStage])) {
                std::cerr << "Erreur : Lecture interrompue à l'index " << iStage << ". Le fichier contient moins de 60 entiers." << std::endl;
                break;
            }
    } else {
        std::cout << "erreur chargement fm_0" << std::endl;
    }

    from_0.close();

    
    std::ifstream from_fm("/Users/caussebruno/Documents/developpement/Roxane/build/fm_V.bin", std::ios::binary);
    if(from_fm) {
        
        for(unsigned int id_patt = 0; id_patt < 15; ++id_patt) {
            
            eval_V[id_patt] = new Vec_8[sizes[id_patt]];
            from_fm.read(reinterpret_cast<char*> (eval_V[id_patt]), sizeof(Vec_8)*sizes[id_patt]);
            
            if(id_patt > 1)
                eval_V[id_patt] += sizes[id_patt]/2;
        }
                
    } else {
        std::cout << "erreur chargement eval_V" << std::endl;
    }

    from_fm.close();


    
};

void RXEvaluation::unload() {
    
    //delete tables

    for(unsigned int iStage = 0; iStage<60; iStage++) {
        
        for(unsigned int id_patt = 0; id_patt < 15; ++id_patt) {
            
            if(id_patt > 1)
                eval_w[iStage][id_patt] -= sizes[id_patt]/2;
            delete[] eval_w[iStage][id_patt];
            eval_w[iStage][id_patt] = nullptr;

            
        }
    }
    
    for(unsigned int id_patt = 0; id_patt < 15; ++id_patt) {
        
        if(id_patt > 1)
            eval_V[id_patt] -= sizes[id_patt]/2;
        delete[] eval_V[id_patt];
        eval_V[id_patt] = nullptr;
        
    }


};








