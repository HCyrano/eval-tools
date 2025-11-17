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
    // insert code here...
            
    RXPatternGenerate gen;
/*
    for(int stage = 0; stage<60; ++stage)
        gen.stage_to_data(stage);
*/
    
    gen.generate_method();
    
    return EXIT_SUCCESS;
}
