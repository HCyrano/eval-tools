//
//  main.cpp
//  Evaluation
//
//  Created by Causse Bruno on 05/11/2025.
//

#include <iostream>

#include "RXBitBoard.hpp"
#include "RXBBpatterns.hpp"

int main(int argc, const char * argv[]) {
    // insert code here...
    
    RXBBPatterns board;
    
    std::string othellier = "XXXOXXXXOXXXXXXXOOXXXXXXOOOXXXXXOOOXXOO-OOOOO---OOOOOOO-OOOOOOO- X";
    
    board.build(othellier);
    
    std::cout << board << std::endl;
    
    
    return EXIT_SUCCESS;
}
