/*
 *  RXEvaluation.hpp
 *  Roxane
 *
 *  Created by Bruno Causse on 06/08/05.
 *  Copyleft 2005-2025 personnel.
 *
 */

#ifndef RXEVALUATION_HPP
#define RXEVALUATION_HPP

#include <iostream>

#include "RXConstantes.hpp"
#include "RXPattern.hpp"

static constexpr unsigned int RANK = 8;


struct Vec_8 {
    short data[RANK];
    
    short& operator[](int i){return data[i];}
};

class alignas(64) RXEvaluation {
    
    static constexpr unsigned int sizes[15] = {24, 24, 243, 729, 2187, 6561, 59049, 59049, 59049, 6561, 6561, 6561, 177147};

    
    public :
    
    static void load();
    static void unload();
    
    static std::string get_version() {
            return "K 2026-03-03";
        }

    
    alignas(64) static inline short* eval_w[60][13] = {};
    alignas(64) static inline int eval_w0[60];
    alignas(64) static inline Vec_8* eval_V[13] = {};





        
};


#endif


