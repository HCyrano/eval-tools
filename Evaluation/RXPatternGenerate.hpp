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
    
    std::vector<std::vector<unsigned int>> pattern_info = {
        
        //{id_end, offset_id, n_index}
        
        //diag_5
        {3, 0, 243},
        //diag_6
        {7, 243, 729},
        //diag_7
        {11, 972, 2187},
        //diag_8
        {13, 3159, 6561},
        // edge + 2x
        {17, 9720, 59049},
        // hv_2
        {21, 68769, 6561},
        // hv_3
        {25, 75330, 6561},
        // hv_4
        {29, 81891, 6561},
        // corner 2 bord 5 + X
        {33, 88452, 59049},
        // corner 2*5
        {41, 147501, 59049},
        // corner 4/3/3/1
        {45, 206550, 177147}
        
    };

    std::vector<std::vector<unsigned int>> pattern_sym = {
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
        
        { 15, 14, 13, 12, 11, 10,  9,  8,  7,  6,   5,   4,   3,   2,   1,   0},        // 13
        
        // symetrie corner 4/3/2/1
        { 10,  9,  8,  7,  4,  5,  6,  3,  2,  1,   0},                                 // 14
        // symetrie corner 2 bords 5 + X
        {  9,  8,  7,  6,  4,  5,  3,  2,  1,  0}                                       // 15

    };


    std::vector<RXFeature> pattern_def = {
        
        /*
         // diag_4
         { 4, { A4, B3, C2, D1}},
         { 4, { E1, F2, G3, H4}},
         { 4, { H5, G6, F7, E8}},
         { 4, { D8, C7, B6, A5}},
         */
        //  diag_5
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
        
        // edge + 2x
        { 10, { B2, A1, B1, C1, D1, E1, F1, G1, H1, G2}},
        { 10, { G2, H1, H2, H3, H4, H5, H6, H7, H8, G7}},
        { 10, { G7, H8, G8, F8, E8, D8, C8, B8, A8, B7}},
        { 10, { B7, A8, A7, A6, A5, A4, A3, A2, A1, B2}},
        
        // hv_2
        { 8, { A2, B2, C2, D2, E2, F2, G2, H2}},
        { 8, { G1, G2, G3, G4, G5, G6, G7, G8}},
        { 8, { H7, G7, F7, E7, D7, C7, B7, A7}},
        { 8, { B8, B7, B6, B5, B4, B3, B2, B1}},
        
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
        
        // corner 2 bord 5 + X
        { 15, { A5, A4, A3, A2, A1, B2, B1, C1, D1, E1}},
        { 15, { D1, E1, F1, G1, H1, G2, H2, H3, H4, H5}},
        { 15, { H4, H5, H6, H7, H8, G7, G8, F8, E8, D8}},
        { 15, { E8, D8, C8, B8, A8, B7, A7, A6, A5, A4}},
        
        // corner 2*5
        { 0, { E2, D2, C2, B2, A2, A1, B1, C1, D1, E1}},
        { 0, { G5, G4, G3, G2, G1, H1, H2, H3, H4, H5}},
        { 0, { D7, E7, F7, G7, H7, H8, G8, F8, E8, D8}},
        { 0, { B4, B5, B6, B7, B8, A8, A7, A6, A5, A4}},
        { 0, { D2, E2, F2, G2, H2, H1, G1, F1, E1, D1}},
        { 0, { G4, G5, G6, G7, G8, H8, H7, H6, H5, H4}},
        { 0, { E7, D7, C7, B7, A7, A8, B8, C8, D8, E8}},
        { 0, { B5, B4, B3, B2, B1, A1, A2, A3, A4, A5}},
        
        // corner 4/3/3/1
        { 14, { A4, B3, A3, A2, A1, B2, C3, B1, C1, C2, D1}},
        { 14, { E1, F2, F1, G1, H1, G2, F3, H2, H3, G3, H4}},
        { 14, { H5, G6, H6, H7, H8, G7, F6, G8, F8, F7, E8}},
        { 14, { D8, C7, C8, B8, A8, B7, C6, A7, A6, B6, A5}},
        /*
         // 2 bords
         { 11, { D2, C2, B2, A2, A1, B1, C1, D1, E1, F1, G1, H1, H2, G2, F2, E2}},
         { 11, { G4, G3, G2, G1, H1, H2, H3, H4, H5, H6, H7, H8, G8, G7, G6, G5}},
         { 11, { E7, F7, G7, H7, H8, G8, F8, E8, D8, C8, B8, A8, A7, B7, C7, D7}},
         { 11, { B5, B6, B7, B8, A8, A7, A6, A5, A4, A3, A2, A1, B1, B2, B3, B4}},
         */
    };
    
    
        


    void generate_method(std::string signature, unsigned int color, unsigned int offset);

    public:


    void display();
    int id_sym(int index, int sym_id);

    void generate_method();
    
    void egrcd_rawdata_to_stage();
    void stage_to_data(const unsigned int stage);
    
    void write_eval(const unsigned int stage);
    void norm_weight(float* weights, short* weigths_out, unsigned int id_start, unsigned int n_weights, unsigned int sym);

};

#endif
