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
#include "RXSetting.hpp"

#ifdef FACT_MACH

static constexpr unsigned int RANK =
#ifdef RANK8
    8;
#else
    16;
#endif

struct alignas(4*RANK) Vec_short {
    short data[RANK];
    short& operator[](int i)             { return data[i]; }
    const short& operator[](int i) const { return data[i]; }
};

#endif

class alignas(64) RXEvaluation {
    
    static constexpr unsigned int N_PATTERNS = 13;
    static constexpr unsigned int sizes[N_PATTERNS] = {24, 24, 243, 729, 2187, 6561, 59049, 59049, 59049, 6561, 6561, 6561, 177147};
    

    
    public :
    
    static void load();
    static void unload();
    
    static std::string get_version() {
            return "FM16 2026-03-13";
        }

    
    alignas(64) static inline short* eval_w[60][N_PATTERNS] = {};
#ifdef FACT_MACH
    alignas(64) static inline int eval_w0[60];
    alignas(64) static inline Vec_short* eval_V[N_PATTERNS] = {};
#endif





        
};


#endif


