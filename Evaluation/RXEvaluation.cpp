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


static void check_read(const std::ifstream& stream, const char* filename, unsigned int pattern, unsigned int stage = 0) {
    if (!stream) {
        std::cerr << "CRITICAL ERROR: Lecture échouée dans " << filename
                  << " (pattern=" << pattern << ", stage=" << stage << ")" << std::endl;
        std::exit(EXIT_FAILURE);
    }
}


void RXEvaluation::load() {

    // --- weight_v11.bin ---
    std::ifstream from_w("/Users/caussebruno/Documents/developpement/Evaluation/weight_v11.bin", std::ios::binary);
    if (!from_w) {
        std::cerr << "CRITICAL ERROR: Impossible de charger weight_v12.bin" << std::endl;
        std::exit(EXIT_FAILURE);
    }

    for (unsigned int iStage = 0; iStage < 60; iStage++) {
        for (unsigned int id_patt = 0; id_patt < N_PATTERNS; ++id_patt) {

            eval_w[iStage][id_patt] = new short[sizes[id_patt]];
            from_w.read(reinterpret_cast<char*>(eval_w[iStage][id_patt]), sizeof(short) * sizes[id_patt]);
            check_read(from_w, "weight_v12.bin", id_patt, iStage);

            if (id_patt > 1)
                eval_w[iStage][id_patt] += sizes[id_patt] / 2;
        }
    }

    from_w.close();

#ifdef FACT_MACH
    // --- fm_w0.txt ---
    std::ifstream from_w0("/Users/caussebruno/Documents/developpement/Evaluation/fm_w0_v11.txt");
    if (!from_w0) {
        std::cerr << "CRITICAL ERROR: Impossible de charger fm_w0_v11.txt" << std::endl;
        std::exit(EXIT_FAILURE);
    }

    for (unsigned int iStage = 0; iStage < 60; iStage++) {
        if (!(from_w0 >> eval_w0[iStage])) {
            std::cerr << "CRITICAL ERROR: fm_w0.txt contient moins de 60 entiers (arrêt à l'index "
                      << iStage << ")" << std::endl;
            std::exit(EXIT_FAILURE);
        }
    }

    from_w0.close();


    // --- fm_V.bin ---
    std::ifstream from_V("/Users/caussebruno/Documents/developpement/Evaluation/fm_V_v11.bin", std::ios::binary);
    if (!from_V) {
        std::cerr << "CRITICAL ERROR: Impossible de charger fm_V_v11.bin" << std::endl;
        std::exit(EXIT_FAILURE);
    }

    for (unsigned int id_patt = 0; id_patt < N_PATTERNS; ++id_patt) {

        eval_V[id_patt] = new Vec_short[sizes[id_patt]];
        // Lecture donnée par donnée pour ignorer le padding
        for (unsigned int i = 0; i < sizes[id_patt]; ++i) {
            from_V.read(reinterpret_cast<char*>(eval_V[id_patt][i].data), sizeof(short) * RANK);
        }
        check_read(from_V, "fm_V.bin", id_patt);

        if (id_patt > 1)
            eval_V[id_patt] += sizes[id_patt] / 2;
    }

    from_V.close();
#endif
    
    
}


void RXEvaluation::unload() {

    for (unsigned int iStage = 0; iStage < 60; iStage++) {
        for (unsigned int id_patt = 0; id_patt < N_PATTERNS; ++id_patt) {

            if (id_patt > 1)
                eval_w[iStage][id_patt] -= sizes[id_patt] / 2;
            delete[] eval_w[iStage][id_patt];
            eval_w[iStage][id_patt] = nullptr;
        }
    }

#ifdef FACT_MACH
    for (unsigned int id_patt = 0; id_patt < N_PATTERNS; ++id_patt) {

        if (id_patt > 1)
            eval_V[id_patt] -= sizes[id_patt] / 2;
        delete[] eval_V[id_patt];
        eval_V[id_patt] = nullptr;
    }
#endif
    
}
