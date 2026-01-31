//
//  main.cpp
//  Evaluation
//
//  Created by Causse Bruno on 05/11/2025.
//

#include <iostream>

#include "RXBitBoard.hpp"
#include "RXBBPatterns.hpp"
#include "RXPatternGenerate.hpp"

int main(int argc, const char * argv[]) {
 

    RXPatternGenerate* gen = new RXPatternGenerate();

/*
    //generation des index globaux et du score d'une position stage par stage
    for(int stage = 0; stage<60; ++stage)
        gen->stage_to_data(stage);


    //affiche les pattern et leur pattern miroir
    gen->display();

    gen->write_eval();

    gen->rawdata_to_stage();

    gen->generate_method();
 
    gen->encode_eval();


*/
 
    gen->encode_eval();
    delete gen;

    return EXIT_SUCCESS;
}
