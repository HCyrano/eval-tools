//
//  RXPatternGenerate.hpp
//  Evaluation
//
//  Created by Causse Bruno on 07/11/2025.
//

#ifndef RXPATTERGENERATE_HPP
#define RXPATTERGENERATE_HPP

#include <vector>


#include "RXConstantes.hpp"
#include "RXBitBoard.hpp"

// symId           : identifiant du type de symétrie appliqué au pattern
// squares         : ensemble de cases (squares) définissant la forme du pattern
class RXFeature {
    public:
    int symID;
    std::vector<int> squares;
    

    // Constructeur pratique
    RXFeature(int id, std::vector<int> sq)
    : symID(id), squares(std::move(sq)) {};

};


class RXPatternGenerate {
    
    std::vector<std::vector<unsigned int>> rotates = {
        // 0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10,  11,  12,  13,  14,  15
        
        //pas de symetrie
        {  0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10,  11,  12,  13,  14,  15},        // 0
        //symetrie simple
        {  0},                                                                          // 1
        {  1,  0},                                                                      // 2
        {  2,  1,  0},                                                                  // 3
        {  3,  2,  1,  0},                                                              // 4
        {  4,  3,  2,  1,  0},                                                          // 5
        {  5,  4,  3,  2,  1,  0},                                                      // 6
        {  6,  5,  4,  3,  2,  1,  0},                                                  // 7
        {  7,  6,  5,  4,  3,  2,  1,  0},                                              // 8
        {  8,  7,  6,  5,  4,  3,  2,  1,  0},                                          // 9
        {  9,  8,  7,  6,  5,  4,  3,  2,  1,  0},                                      // 10
        { 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,   0},                                 // 11
        { 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,   1,   0},                            // 12
        { 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,   2,   1,   0},                       // 13
        { 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,   3,   2,   1,   0},                  // 14
        { 14, 13, 12, 11, 10,  9,  8,  7,  6,  5,   4,   3,   2,   1,   0},             // 15
        { 15, 14, 13, 12, 11, 10,  9,  8,  7,  6,   5,   4,   3,   2,   1,   0},        // 16
        
        // symetrie corner 4/3/3/1
        { 10,  9,  8,  7,  4,  5,  6,  3,  2,  1,   0},                                 // 17
        // symetrie corner 2 bords 5 + X & corner 4/3/2/1
        {  9,  8,  7,  6,  4,  5,  3,  2,  1,  0},                                      // 18
        // hyper diagonale
        {  9,  8,  7,  3,  4,  5,  6,  2,  1,  0},                                      // 19
        // corner 5/3/2/1/1
        { 11, 10,  9,  8,  7,  5,  6,  4,  3,  2,   1,   0},                            // 20
        // corner 4/4/3/2 ou corner 5/3/3/1/1
        { 12, 11, 10,  9,  8,  5,  6,  7,  4,  3,   2,   1,   0},                       // 21
        // corner 5/4/3/2/1
        { 14, 13, 12, 11, 10,  9,  6,  7,  8,  5,  4,  3,   2,   1,   0}                // 22

    };


    std::vector<std::vector<unsigned int>> pattern_info = {
        
        //[{last index of pattern, offset index global, n_index local, rotate index}
/*
        //diag_5
        {3, 0, 243, 5},
        //diag_6
        {7, 243, 729, 6},
        //diag_7
        {11, 972, 2187, 7},
        //diag_8
        {13, 3159, 6561, 8},
        // hyper diag
        {17, 9720, 59049, 19},

        // edge + 2x
        {21, 68769, 59049, 10},
        // edge ALT 6+4
        {25, 127818, 59049, 10},
        // edge 4/2/4
        {29, 186867, 59049, 10},
        // edge 2*(3/2)
        {33, 245916, 59049, 10},

        // hv_2
        {37, 304965, 6561, 8},
        // hv_3
        {41, 311526, 6561, 8},
        // hv_4
        {45, 318087, 6561, 8},
        
        // corner 4/3/3/1
        {49, 324648, 177147, 17},
        // corner 2*5
        {57, 501795, 59049, 0},

        // 560 844 indexs
*/

        //diag_5
        {3, 0, 243, 5},
        //diag_6
        {7, 243, 729, 6},
        //diag_7
        {11, 972, 2187, 7},
        //diag_8
        {13, 3159, 6561, 8},
        // hyper diag
        {17, 9720, 59049, 19},

        // edge 8+8
        {21, 68769, 59049, 10},
        // edge 4/2/4
        {25, 186867, 59049, 10},

        // hv_3
        {29, 311526, 6561, 8},
        // hv_4
        {33, 318087, 6561, 8},
        
        // corner 4/3/3/1
        {37, 324648, 177147, 17},

    };


    std::vector<RXFeature> pattern_def = {
        
        // --------------------- diag ---------------------
        
        // diag_5
        { 5, { A5, B4, C3, D2, E1}},
        { 5, { D1, E2, F3, G4, H5}},
        { 5, { H4, G5, F6, E7, D8}},
        { 5, { E8, D7, C6, B5, A4}},

        // diag_6
        { 6, { A6, B5, C4, D3, E2, F1}},
        { 6, { C1, D2, E3, F4, G5, H6}},
        { 6, { H3, G4, F5, E6, D7, C8}},
        { 6, { F8, E7, D6, C5, B4, A3}},
        
        // diag_7
        { 7, { A7, B6, C5, D4, E3, F2, G1}},
        { 7, { B1, C2, D3, E4, F5, G6, H7}},
        { 7, { H2, G3, F4, E5, D6, C7, B8}},
        { 7, { G8, F7, E6, D5, C4, B3, A2}},
        
        // diag_8
        { 8, { A1, B2, C3, D4, E5, F6, G7, H8}},
        { 8, { A8, B7, C6, D5, E4, F3, G2, H1}},
        
        // hyper diag
        // X X
        // X X X
        //   X X X
        //     X X
        { 19, { C4, B3, A2, A1, B2, C3, D4, B1, C2, D3}},
        { 19, { E3, F2, G1, H1, G2, F3, E4, H2, G3, F4}},
        { 19, { F5, G6, H7, H8, G7, F6, E5, G8, F7, E6}},
        { 19, { D6, C7, B8, A8, B7, C6, D5, A7, B6, C5}},


        // --------------------- edge ---------------------
        
/*
        // edge + 2x
        // X X X X X X X X
        //   X         X
        { 10, { B2, A1, B1, C1, D1, E1, F1, G1, H1, G2}},
        { 10, { G2, H1, H2, H3, H4, H5, H6, H7, H8, G7}},
        { 10, { G7, H8, G8, F8, E8, D8, C8, B8, A8, B7}},
        { 10, { B7, A8, A7, A6, A5, A4, A3, A2, A1, B2}},

        // edge ALT 6+4
        // . X X X X X X .
        // . . X X X X . .
        { 10, { D2, C2, B1, C1, D1, E1, F1, G1, F2, E2}},
        { 10, { G4, G3, H2, H3, H4, H5, H6, H7, G6, G5}},
        { 10, { E7, F7, G8, F8, E8, D8, C8, B8, C7, D7}},
        { 10, { B5, B6, A7, A6, A5, A4, A3, A2, B3, B4}},

        // edge 8+6
        // X X X X X X X X
        // . X X X X X X .
        { 14, { D2, C2, B2, A1, B1, C1, D1, E1, F1, G1, H1, G2, F2, E2}},
        { 14, { G4, G3, G2, H1, H2, H3, H4, H5, H6, H7, H8, G7, G6, G5}},
        { 14, { E7, F7, G7, H8, G8, F8, E8, D8, C8, B8, A8, B7, C7, D7}},
        { 14, { B5, B6, B7, A8, A7, A6, A5, A4, A3, A2, A1, B2, B3, B4}},
*/
        // edge 8+8
        // X X X X X X X X
        // X X X X X X X X
        { 16, { D2, C2, B2, A2, A1, B1, C1, D1, E1, F1, G1, H1, H2, G2, F2, E2}},
        { 16, { G4, G3, G2, G1, H1, H2, H3, H4, H5, H6, H7, H8, G8, G7, G6, G5}},
        { 16, { E7, F7, G7, H7, H8, G8, F8, E8, D8, C8, B8, A8, A7, B7, C7, D7}},
        { 16, { B5, B6, B7, B8, A8, A7, A6, A5, A4, A3, A2, A1, B1, B2, B3, B4}},

        // edge 4/2/4
        // . . X X X X
        // . . . X X
        // . . X X X X
        { 10, { D3, C3, D2, C1, D1, E1, F1, E2, F3, E3}},
        { 10, { F4, F3, G4, H3, H4, H5, H6, G5, F6, F5}},
        { 10, { E6, F6, E7, F8, E8, D8, C8, D7, C6, D6}},
        { 10, { C5, C6, B5, A6, A5, A4, A3, B4, C3, C4}},
/*
        // edge 2*(3/2)
        // X X X . . X X X
        // X X . . . . X X
        { 10, { B2, A2, A1, B1, C1, F1, G1, H1, H2, G2}},
        { 10, { G2, G1, H1, H2, H3, H6, H7, H8, G8, G7}},
        { 10, { G7, H7, H8, G8, F8, C8, B8, A8, A7, B7}},
        { 10, { B7, B8, A8, A7, A6, A3, A2, A1, B1, B2}},

        // --------------------- hv ---------------------

        // hv_2
        { 8, { A2, B2, C2, D2, E2, F2, G2, H2}},
        { 8, { G1, G2, G3, G4, G5, G6, G7, G8}},
        { 8, { H7, G7, F7, E7, D7, C7, B7, A7}},
        { 8, { B8, B7, B6, B5, B4, B3, B2, B1}},
*/
        // hv_3
        { 8, { A3, B3, C3, D3, E3, F3, G3, H3}},
        { 8, { F1, F2, F3, F4, F5, F6, F7, F8}},
        { 8, { H6, G6, F6, E6, D6, C6, B6, A6}},
        { 8, { C8, C7, C6, C5, C4, C3, C2, C1}},
        
        // hv_4
        { 8, { A4, B4, C4, D4, E4, F4, G4, H4}},
        { 8, { E1, E2, E3, E4, E5, E6, E7, E8}},
        { 8, { H5, G5, F5, E5, D5, C5, B5, A5}},
        { 8, { D8, D7, D6, D5, D4, D3, D2, D1}},
        
        // --------------------- corner ---------------------

/*
        // corner 5/4/3/2/1
        // X X X X X
        // X X X X
        // X X X
        // X X
        // X
        {23, {A5, B4, A4, B3, A3, A2, A1, B2, C3, B1, C1, C2, D1, D2, E1}},
        {23, {D1, E2, E1, F2, F1, G1, H1, G2, F3, H2, H3, G3, H4, G4, H5}},
        {23, {H4, G5, H5, G6, H6, H7, H8, G7, F6, G8, F8, F7, E8, E7, D8}},
        {23, {E8, D7, D8, C7, C8, B8, A8, B7, C6, A7, A6, B6, A5, B5, A4}},

        // corner 5/3/2/1/1
        // X X X X X
        // X X X
        // X X
        // X
        // X
        { 20, { A5, A4, A3, B3, A2, A1, B2, B1, C2, C1, D1, E1}},
        { 20, { D1, E1, F1, F2, G1, H1, G2, H2, G3, H3, H4, H5}},
        { 20, { H4, H5, H6, G6, H7, H8, G7, G8, F7, F8, E8, D8}},
        { 20, { E8, D8, C8, C7, B8, A8, B7, A7, B6, A6, A5, A4}},

        // corner 2 edges 5 + X
        // X X X X X
        // X X
        // X
        // X
        // X
        { 18, { A5, A4, A3, A2, A1, B2, B1, C1, D1, E1}},
        { 18, { D1, E1, F1, G1, H1, G2, H2, H3, H4, H5}},
        { 18, { H4, H5, H6, H7, H8, G7, G8, F8, E8, D8}},
        { 18, { E8, D8, C8, B8, A8, B7, A7, A6, A5, A4}},

        // corner ALT :2 edges 5 + X
        // . X X X X
        // X . X X
        // X X
        // X X
        // X
        { 10, { A5, A4, A3, A2, B3, C2, B1, C1, D1, E1}},
        { 10, { D1, E1, F1, G1, F2, G3, H2, H3, H4, H5}},
        { 10, { H4, H5, H6, H7, G6, F7, G8, F8, E8, D8}},
        { 10, { E8, D8, C8, B8, C7, B6, A7, A6, A5, A4}},
 
        //corner 5/3/3/1/1
        // X X X X X
        // X X X
        // X X X
        // X
        // X
        {22, {A5, A4, A3, B3, A2, A1, B2, C3, B1, C2, C1, D1, E1}},
        {22, {D1, E1, F1, F2, G1, H1, G2, F3, H2, G3, H3, H4, H5}},
        {22, {H4, H5, H6, G6, H7, H8, G7, F6, G8, F7, F8, E8, D8}},
        {22, {E8, D8, C8, C7, B8, A8, B7, C6, A7, B6, A6, A5, A4}},
 
        // corner 2*(4/2)
        // . X X X X
        // X . X X
        // X X
        // X X
        // X
        {13, {A5, A4, B4, A3, B3, A2, C3, B1, C2, C1, D2, D1, E1}},
        {13, {D1, E1, E2, F1, F2, G1, F3, H2, G3, H3, G4, H4, H5}},
        {13, {H4, H5, G5, H6, G6, H7, F6, G8, F7, F8, E7, E8, D8}},
        {13, {E8, D8, D7, C8, C7, B8, C6, A7, B6, A6, B5, A5, A4}}

        // corner 4/3/2/1
        // X X X X
        // X X X
        // X X
        // X
        { 18, { A4, B3, A3, A2, A1, B2, B1, C1, C2, D1}},
        { 18, { E1, F2, F1, G1, H1, G2, H2, H3, G3, H4}},
        { 18, { H5, G6, H6, H7, H8, G7, G8, F8, F7, E8}},
        { 18, { D8, C7, C8, B8, A8, B7, A7, A6, B6, A5}},
*/
        // corner 4/3/3/1
        // X X X X
        // X X X
        // X X X
        // X
        { 17, { A4, B3, A3, A2, A1, B2, C3, B1, C1, C2, D1}},
        { 17, { E1, F2, F1, G1, H1, G2, F3, H2, H3, G3, H4}},
        { 17, { H5, G6, H6, H7, H8, G7, F6, G8, F8, F7, E8}},
        { 17, { D8, C7, C8, B8, A8, B7, C6, A7, A6, B6, A5}}
/*
        // corner ALT :4/3/3/1
        //   X X X
        // X   X X
        // X X X
        // X X
        { 11, { A4, B4, A3, B3, A2, C3, B1, C2, C1, D2, D1}},
        { 11, { E1, E2, F1, F2, G1, F3, H2, G3, H3, G4, H4}},
        { 11, { H5, G5, H6, G6, H7, F6, G8, F7, F8, E7, E8}},
        { 11, { D8, D7, C8, C7, B8, C6, A7, B6, A6, B5, A5}},

        // corner 4/4/3/2
        // X X X X
        // X X X X
        // X X X
        // X X
        { 21, { A4, B4, A3, B3, A2, A1, B2, C3, B1, C2, C1, D2, D1}},
        { 21, { E1, E2, F1, F2, G1, H1, G2, F3, H2, G3, H3, G4, H4}},
        { 21, { H5, G5, H6, G6, H7, H8, G7, F6, G8, F7, F8, E7, E8}},
        { 21, { D8, D7, C8, C7, B8, A8, B7, C6, A7, B6, A6, B5, A5}},
 
        // Corner 2*(3/2)
        // . X X X
        // X . X X
        // X X
        // X X
        { 10, { B3, B4, A4, A3, A2, B1, C1, D1, D2, C2}},
        { 10, { F2, E2, E1, F1, G1, H2, H3, H4, G4, G3}},
        { 10, { G6, G5, H5, H6, H7, G8, F8, E8, E7, F7}},
        { 10, { C7, D7, D8, C8, B8, A7, A6, A5, B5, B6}},


        // corner 2*5
        // X X X X X
        // X X X X X
        { 0, { E2, D2, C2, B2, A2, A1, B1, C1, D1, E1}},
        { 0, { G5, G4, G3, G2, G1, H1, H2, H3, H4, H5}},
        { 0, { D7, E7, F7, G7, H7, H8, G8, F8, E8, D8}},
        { 0, { B4, B5, B6, B7, B8, A8, A7, A6, A5, A4}},
        { 0, { D2, E2, F2, G2, H2, H1, G1, F1, E1, D1}},
        { 0, { G4, G5, G6, G7, G8, H8, H7, H6, H5, H4}},
        { 0, { E7, D7, C7, B7, A7, A8, B8, C8, D8, E8}},
        { 0, { B5, B4, B3, B2, B1, A1, A2, A3, A4, A5}}
*/
        

    };
    
    
    void generate_method(std::string signature, unsigned int color, unsigned int offset);

    public:


    void display();
    int index_rotate(int index, int sym_id);

    void generate_method();
    
    void rawdata_to_stage();
    void stage_to_data(const unsigned int stage);
    
    void write_eval();
    void norm_weight(float* weights, int* n_occs_in, short* weigths_out, unsigned int id_start, unsigned int n_weights, unsigned int sym);
    
    void encode_eval();

};

#endif
