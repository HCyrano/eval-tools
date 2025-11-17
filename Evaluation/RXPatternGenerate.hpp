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

// lastPatternType : marque la fin du type de pattern,
//                   utile pour le calcul de offset_patt
// symId           : identifiant du type de symétrie appliqué au pattern
// squares         : ensemble de cases (squares) définissant la forme du pattern
class RXFeature {
    public:
    bool lastPatternType;
    int symID;
    std::vector<int> squares;
    

    // Constructeur pratique
    RXFeature(bool id_type, int id, std::vector<int> sq)
    : lastPatternType(id_type), symID(id), squares(std::move(sq)) {};

};


class RXPatternGenerate {
    
    std::vector<RXFeature> eval = {
        
        /*
         // diag_4
         { 81, 1, { A4, B3, C2, D1}},
         { 81, 1, { E1, F2, G3, H4}},
         { 81, 1, { H5, G6, F7, E8}},
         { 81, 1, { D8, C7, B6, A5}},
         */
        //  diag_5
        { false, 2, { A5, B4, C3, D2, E1}},
        { false, 2, { D1, E2, F3, G4, H5}},
        { false, 2, { H4, G5, F6, E7, D8}},
        {  true, 2, { E8, D7, C6, B5, A4}},
        
        // diag_6
        { false, 3, { A6, B5, C4, D3, E2, F1}},
        { false, 3, { C1, D2, E3, F4, G5, H6}},
        { false, 3, { H3, G4, F5, E6, D7, C8}},
        {  true, 3, { F8, E7, D6, C5, B4, A3}},
        
        // diag_7
        { false, 4, { A7, B6, C5, D4, E3, F2, G1}},
        { false, 4, { B1, C2, D3, E4, F5, G6, H7}},
        { false, 4, { H2, G3, F4, E5, D6, C7, B8}},
        {  true, 4, { G8, F7, E6, D5, C4, B3, A2}},
        
        // diag_8
        { false, 5, { A1, B2, C3, D4, E5, F6, G7, H8}},
        {  true, 5, { A8, B7, C6, D5, E4, F3, G2, H1}},
        
        // edge + 2x
        { false, 7, { B2, A1, B1, C1, D1, E1, F1, G1, H1, G2}},
        { false, 7, { G2, H1, H2, H3, H4, H5, H6, H7, H8, G7}},
        { false, 7, { G7, H8, G8, F8, E8, D8, C8, B8, A8, B7}},
        {  true, 7, { B7, A8, A7, A6, A5, A4, A3, A2, A1, B2}},
        
        // hv_2
        { false, 5, { A2, B2, C2, D2, E2, F2, G2, H2}},
        { false, 5, { G1, G2, G3, G4, G5, G6, G7, G8}},
        { false, 5, { H7, G7, F7, E7, D7, C7, B7, A7}},
        {  true, 5, { B8, B7, B6, B5, B4, B3, B2, B1}},
        
        // hv_3
        { false, 5, { A3, B3, C3, D3, E3, F3, G3, H3}},
        { false, 5, { F1, F2, F3, F4, F5, F6, F7, F8}},
        { false, 5, { H6, G6, F6, E6, D6, C6, B6, A6}},
        {  true, 5, { C8, C7, C6, C5, C4, C3, C2, C1}},
        
        // hv_4
        { false, 5, { A4, B4, C4, D4, E4, F4, G4, H4}},
        { false, 5, { E1, E2, E3, E4, E5, E6, E7, E8}},
        { false, 5, { H5, G5, F5, E5, D5, C5, B5, A5}},
        {  true, 5, { D8, D7, D6, D5, D4, D3, D2, D1}},
        
        // corner 2 bord 5 + X
        { false, 13, { A5, A4, A3, A2, A1, B2, B1, C1, D1, E1}},
        { false, 13, { D1, E1, F1, G1, H1, G2, H2, H3, H4, H5}},
        { false, 13, { H4, H5, H6, H7, H8, G7, G8, F8, E8, D8}},
        {  true, 13, { E8, D8, C8, B8, A8, B7, A7, A6, A5, A4}},
        
        // corner 2*5
        { false, 0, { E2, D2, C2, B2, A2, A1, B1, C1, D1, E1}},
        { false, 0, { G5, G4, G3, G2, G1, H1, H2, H3, H4, H5}},
        { false, 0, { D7, E7, F7, G7, H7, H8, G8, F8, E8, D8}},
        { false, 0, { B4, B5, B6, B7, B8, A8, A7, A6, A5, A4}},
        { false, 0, { D2, E2, F2, G2, H2, H1, G1, F1, E1, D1}},
        { false, 0, { G4, G5, G6, G7, G8, H8, H7, H6, H5, H4}},
        { false, 0, { E7, D7, C7, B7, A7, A8, B8, C8, D8, E8}},
        {  true, 0, { B5, B4, B3, B2, B1, A1, A2, A3, A4, A5}},
        
        // corner 4/3/3/1
        { false, 12, { A4, B3, A3, A2, A1, B2, C3, B1, C1, C2, D1}},
        { false, 12, { E1, F2, F1, G1, H1, G2, F3, H2, H3, G3, H4}},
        { false, 12, { H5, G6, H6, H7, H8, G7, F6, G8, F8, F7, E8}},
        {  true, 12, { D8, C7, C8, B8, A8, B7, C6, A7, A6, B6, A5}},
        /*
         // 2 bords
         { 43043721, 11, { D2, C2, B2, A2, A1, B1, C1, D1, E1, F1, G1, H1, H2, G2, F2, E2}},
         { 43043721, 11, { G4, G3, G2, G1, H1, H2, H3, H4, H5, H6, H7, H8, G8, G7, G6, G5}},
         { 43043721, 11, { E7, F7, G7, H7, H8, G8, F8, E8, D8, C8, B8, A8, A7, B7, C7, D7}},
         { 43043721, 11, { B5, B6, B7, B8, A8, A7, A6, A5, A4, A3, A2, A1, B1, B2, B3, B4}},
         */
    };
    
    std::vector<std::vector<unsigned int>> sym = {
        //  0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10,  11,  12
        
        {  0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10,  11,  12,  13,  14,  15},        // 0
        
        {  3,  2,  1,  0},                                                              // 1
        {  4,  3,  2,  1,  0},                                                          // 2
        {  5,  4,  3,  2,  1,  0},                                                      // 3
        {  6,  5,  4,  3,  2,  1,  0},                                                  // 4
        {  7,  6,  5,  4,  3,  2,  1,  0},                                              // 5
        {  8,  7,  6,  5,  4,  3,  2,  1,  0},                                          // 6
        {  9,  8,  7,  6,  5,  4,  3,  2,  1,  0},                                      // 7
        { 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,   0},                                 // 8
        { 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,   1,   0},                            // 9
        { 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,   2,   1,   0},                       // 10
        { 15, 14, 13, 12, 11, 10,  9,  8,  7,  6,   5,   4,   3,   2,   1,   0},        // 11
        
        { 10,  9,  8,  7,  4,  5,  6,  3,  2,  1,   0},                                 // 12
        {  9,  8,  7,  6,  4,  5,  3,  2,  1,  0}                                       // 13

    };
    
        


    void generate_method(std::string signature, unsigned int color, unsigned int offset);

    public:


    void display();
    int id_sym(int index, int sym_id);
    int patt_id(RXBitBoard board, RXFeature f);

    void generate_method();
    
    void egrcd_rawdata_to_stage();
    void stage_to_data(const unsigned int stage);

};

#endif
