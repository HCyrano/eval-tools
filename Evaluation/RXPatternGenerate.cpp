//
//  RXPatternGenerate.cpp
//  Evaluation
//
//  Created by Causse Bruno on 07/11/2025.
//

#include <stdio.h>
#include <iostream>
#include <iomanip>


#include "RXPatternGenerate.hpp"
#include "RXMove.hpp"
#include "RXBitBoard.hpp"

void RXPatternGenerate::display() {
    
    std::cout << "nombre de  patterns : " << std::size(eval) << std::endl;

    std::cout << "affichage pattern : " << std::endl;
    for (const auto& f : eval) {
        std::cout << "name: " << f.name << " symID: " << f.symID << ", squares: ";

        std::cout << "\n  A B C D E F G H " << std::endl;
        for(int iLine = 1; iLine<=8; iLine++) {
            std::cout  << iLine << " ";
            for(int iPosition = (9-iLine)*8 - 1; iPosition>(8-iLine)*8-1; iPosition--) {
                bool find = false;
                for(int id = 0; id < std::size(f.square); id++)
                    if(iPosition == f.square[id]) {
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
                for(int id = 0; id < std::size(f.square); id++)
                    if(iPosition == f.square[sym[f.symID][id]]) {
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

    for(unsigned int id_1 = 0; id_1<std::size(f.square); ++id_1) {
        unsigned int id_2 = f.square[sym[f.symID][id_1]];
        
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

void RXPatternGenerate::generate_method() {
    
    for (const auto& f : eval)
        std::cout << "int " << f.name << ";" << std::endl;

    std::cout << std::endl;

    for (const auto& f : eval)
        std::cout << f.name << " = 0;" << std::endl;

    std::cout << std::endl;

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

    signature = "inline void RXPattern::flip_WHITE_";
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
        
        for (const auto& f : eval) {
            std::string name = f.name;
            
            unsigned int id = 0;
            for (int s : f.square) {
                if (pos == s) {
                    std::cout << std::setw(11) << name << (color == BLACK? " -= ":" += ") << std::setw(7) << offset*pow3[id] << "; ";
                    break;
                }
                ++id;
            }
        }
            
            
        std::cout << "};" <<std::endl;
        
    }
    
};

