/*
 *  RXPattern.hpp
 *  Roxane
 *
 *  Created by Bruno Causse on 20/09/05.
 *  Copyleft 2005-2025 personnel.
 *
 */

#ifndef RXPATTERN_HPP
#define RXPATTERN_HPP

#include <iostream>



class alignas(16) RXPattern {
        
public:
    
    short diag_5a;
    short diag_5b;
    short diag_5c;
    short diag_5d;
    
    short diag_6a;
    short diag_6b;
    short diag_6c;
    short diag_6d;
    
    short diag_7a;
    short diag_7b;
    short diag_7c;
    short diag_7d;
    
    short diag_8a;
    short diag_8b;
    
    short hv_4a;
    short hv_4b;
    short hv_4c;
    short hv_4d;
    
    short hv_3a;
    short hv_3b;
    short hv_3c;
    short hv_3d;
    
    int corner11a;
    int corner11b;
    int corner11c;
    int corner11d;
    
    int edge_1;
    int edge_2;
    int edge_3;
    int edge_4;
    
    
    //set Black disc
    void set_BLACK_A1();  void set_BLACK_B1();  void set_BLACK_C1();  void set_BLACK_D1();  void set_BLACK_E1();  void set_BLACK_F1();  void set_BLACK_G1();  void set_BLACK_H1();
    void set_BLACK_A2();  void set_BLACK_B2();  void set_BLACK_C2();  void set_BLACK_D2();  void set_BLACK_E2();  void set_BLACK_F2();  void set_BLACK_G2();  void set_BLACK_H2();
    void set_BLACK_A3();  void set_BLACK_B3();  void set_BLACK_C3();  void set_BLACK_D3();  void set_BLACK_E3();  void set_BLACK_F3();  void set_BLACK_G3();  void set_BLACK_H3();
    void set_BLACK_A4();  void set_BLACK_B4();  void set_BLACK_C4();  void set_BLACK_D4();  void set_BLACK_E4();  void set_BLACK_F4();  void set_BLACK_G4();  void set_BLACK_H4();
    void set_BLACK_A5();  void set_BLACK_B5();  void set_BLACK_C5();  void set_BLACK_D5();  void set_BLACK_E5();  void set_BLACK_F5();  void set_BLACK_G5();  void set_BLACK_H5();
    void set_BLACK_A6();  void set_BLACK_B6();  void set_BLACK_C6();  void set_BLACK_D6();  void set_BLACK_E6();  void set_BLACK_F6();  void set_BLACK_G6();  void set_BLACK_H6();
    void set_BLACK_A7();  void set_BLACK_B7();  void set_BLACK_C7();  void set_BLACK_D7();  void set_BLACK_E7();  void set_BLACK_F7();  void set_BLACK_G7();  void set_BLACK_H7();
    void set_BLACK_A8();  void set_BLACK_B8();  void set_BLACK_C8();  void set_BLACK_D8();  void set_BLACK_E8();  void set_BLACK_F8();  void set_BLACK_G8();  void set_BLACK_H8();
    
    //set White disc
    void set_WHITE_A1();  void set_WHITE_B1();  void set_WHITE_C1();  void set_WHITE_D1();  void set_WHITE_E1();  void set_WHITE_F1();  void set_WHITE_G1();  void set_WHITE_H1();
    void set_WHITE_A2();  void set_WHITE_B2();  void set_WHITE_C2();  void set_WHITE_D2();  void set_WHITE_E2();  void set_WHITE_F2();  void set_WHITE_G2();  void set_WHITE_H2();
    void set_WHITE_A3();  void set_WHITE_B3();  void set_WHITE_C3();  void set_WHITE_D3();  void set_WHITE_E3();  void set_WHITE_F3();  void set_WHITE_G3();  void set_WHITE_H3();
    void set_WHITE_A4();  void set_WHITE_B4();  void set_WHITE_C4();  void set_WHITE_D4();  void set_WHITE_E4();  void set_WHITE_F4();  void set_WHITE_G4();  void set_WHITE_H4();
    void set_WHITE_A5();  void set_WHITE_B5();  void set_WHITE_C5();  void set_WHITE_D5();  void set_WHITE_E5();  void set_WHITE_F5();  void set_WHITE_G5();  void set_WHITE_H5();
    void set_WHITE_A6();  void set_WHITE_B6();  void set_WHITE_C6();  void set_WHITE_D6();  void set_WHITE_E6();  void set_WHITE_F6();  void set_WHITE_G6();  void set_WHITE_H6();
    void set_WHITE_A7();  void set_WHITE_B7();  void set_WHITE_C7();  void set_WHITE_D7();  void set_WHITE_E7();  void set_WHITE_F7();  void set_WHITE_G7();  void set_WHITE_H7();
    void set_WHITE_A8();  void set_WHITE_B8();  void set_WHITE_C8();  void set_WHITE_D8();  void set_WHITE_E8();  void set_WHITE_F8();  void set_WHITE_G8();  void set_WHITE_H8();
    
    //flip Black disc
                           void flip_BLACK_B1();  void flip_BLACK_C1();  void flip_BLACK_D1();  void flip_BLACK_E1();  void flip_BLACK_F1();  void flip_BLACK_G1();
    void flip_BLACK_A2();  void flip_BLACK_B2();  void flip_BLACK_C2();  void flip_BLACK_D2();  void flip_BLACK_E2();  void flip_BLACK_F2();  void flip_BLACK_G2();  void flip_BLACK_H2();
    void flip_BLACK_A3();  void flip_BLACK_B3();  void flip_BLACK_C3();  void flip_BLACK_D3();  void flip_BLACK_E3();  void flip_BLACK_F3();  void flip_BLACK_G3();  void flip_BLACK_H3();
    void flip_BLACK_A4();  void flip_BLACK_B4();  void flip_BLACK_C4();  void flip_BLACK_D4();  void flip_BLACK_E4();  void flip_BLACK_F4();  void flip_BLACK_G4();  void flip_BLACK_H4();
    void flip_BLACK_A5();  void flip_BLACK_B5();  void flip_BLACK_C5();  void flip_BLACK_D5();  void flip_BLACK_E5();  void flip_BLACK_F5();  void flip_BLACK_G5();  void flip_BLACK_H5();
    void flip_BLACK_A6();  void flip_BLACK_B6();  void flip_BLACK_C6();  void flip_BLACK_D6();  void flip_BLACK_E6();  void flip_BLACK_F6();  void flip_BLACK_G6();  void flip_BLACK_H6();
    void flip_BLACK_A7();  void flip_BLACK_B7();  void flip_BLACK_C7();  void flip_BLACK_D7();  void flip_BLACK_E7();  void flip_BLACK_F7();  void flip_BLACK_G7();  void flip_BLACK_H7();
                           void flip_BLACK_B8();  void flip_BLACK_C8();  void flip_BLACK_D8();  void flip_BLACK_E8();  void flip_BLACK_F8();  void flip_BLACK_G8();
    
    //flip White disc
                           void flip_WHITE_B1();  void flip_WHITE_C1();  void flip_WHITE_D1();  void flip_WHITE_E1();  void flip_WHITE_F1();  void flip_WHITE_G1();
    void flip_WHITE_A2();  void flip_WHITE_B2();  void flip_WHITE_C2();  void flip_WHITE_D2();  void flip_WHITE_E2();  void flip_WHITE_F2();  void flip_WHITE_G2();  void flip_WHITE_H2();
    void flip_WHITE_A3();  void flip_WHITE_B3();  void flip_WHITE_C3();  void flip_WHITE_D3();  void flip_WHITE_E3();  void flip_WHITE_F3();  void flip_WHITE_G3();  void flip_WHITE_H3();
    void flip_WHITE_A4();  void flip_WHITE_B4();  void flip_WHITE_C4();  void flip_WHITE_D4();  void flip_WHITE_E4();  void flip_WHITE_F4();  void flip_WHITE_G4();  void flip_WHITE_H4();
    void flip_WHITE_A5();  void flip_WHITE_B5();  void flip_WHITE_C5();  void flip_WHITE_D5();  void flip_WHITE_E5();  void flip_WHITE_F5();  void flip_WHITE_G5();  void flip_WHITE_H5();
    void flip_WHITE_A6();  void flip_WHITE_B6();  void flip_WHITE_C6();  void flip_WHITE_D6();  void flip_WHITE_E6();  void flip_WHITE_F6();  void flip_WHITE_G6();  void flip_WHITE_H6();
    void flip_WHITE_A7();  void flip_WHITE_B7();  void flip_WHITE_C7();  void flip_WHITE_D7();  void flip_WHITE_E7();  void flip_WHITE_F7();  void flip_WHITE_G7();  void flip_WHITE_H7();
                           void flip_WHITE_B8();  void flip_WHITE_C8();  void flip_WHITE_D8();  void flip_WHITE_E8();  void flip_WHITE_F8();  void flip_WHITE_G8();
    
    void clear();
    
    /* DEBUG */
    friend std::ostream& operator<<(std::ostream& os, RXPattern& pattern);

    
};

inline void RXPattern::clear() {
    
    diag_5a = 0;
    diag_5b = 0;
    diag_5c = 0;
    diag_5d = 0;
    
    diag_6a = 0;
    diag_6b = 0;
    diag_6c = 0;
    diag_6d = 0;
    
    diag_7a = 0;
    diag_7b = 0;
    diag_7c = 0;
    diag_7d = 0;
    
    diag_8a = 0;
    diag_8b = 0;
    
    hv_4a = 0;
    hv_4b = 0;
    hv_4c = 0;
    hv_4d = 0;
    
    hv_3a = 0;
    hv_3b = 0;
    hv_3c = 0;
    hv_3d = 0;
    
    corner11a = 0;
    corner11b = 0;
    corner11c = 0;
    corner11d = 0;
        
    edge_1 = 0;
    edge_2 = 0;
    edge_3 = 0;
    edge_4 = 0;
        
    
}


inline void RXPattern::set_BLACK_A1() { edge_1    -=        81; edge_4    -=    177147; corner11a -=         1; diag_8a   -=         1; };
inline void RXPattern::set_BLACK_B1() { edge_1    -=       243; edge_4    -=    531441; corner11a -=         3; diag_7a   -=         1; };
inline void RXPattern::set_BLACK_C1() { edge_1    -=       729; corner11a -=         9; hv_3a     -=         1; diag_6a   -=         1; };
inline void RXPattern::set_BLACK_D1() { edge_1    -=      2187; corner11a -=        27; hv_4a     -=         1; diag_5a   -=         1; };
inline void RXPattern::set_BLACK_E1() { edge_1    -=      6561; corner11b -=      2187; hv_4b     -=      2187; diag_5d   -=        81; };
inline void RXPattern::set_BLACK_F1() { edge_1    -=     19683; corner11b -=      6561; hv_3b     -=      2187; diag_6d   -=       243; };
inline void RXPattern::set_BLACK_G1() { edge_1    -=     59049; edge_2    -=        27; corner11b -=     19683; diag_7d   -=       729; };
inline void RXPattern::set_BLACK_H1() { edge_1    -=    177147; edge_2    -=        81; corner11b -=         1; diag_8b   -=      2187; };

inline void RXPattern::set_BLACK_A2() { edge_1    -=        27; edge_4    -=     59049; corner11a -=     19683; diag_7c   -=       729; };
inline void RXPattern::set_BLACK_B2() { edge_1    -=         9; edge_4    -=   1594323; corner11a -=     59049; diag_8a   -=         3; };
inline void RXPattern::set_BLACK_C2() { edge_1    -=         3; corner11a -=        81; hv_3a     -=         3; diag_7a   -=         3; };
inline void RXPattern::set_BLACK_D2() { edge_1    -=         1; hv_4a     -=         3; diag_6a   -=         3; diag_5d   -=        27; };
inline void RXPattern::set_BLACK_E2() { edge_1    -=  14348907; hv_4b     -=       729; diag_6d   -=        81; diag_5a   -=         3; };
inline void RXPattern::set_BLACK_F2() { edge_1    -=   4782969; corner11b -=       729; hv_3b     -=       729; diag_7d   -=       243; };
inline void RXPattern::set_BLACK_G2() { edge_1    -=   1594323; edge_2    -=         9; corner11b -=     59049; diag_8b   -=       729; };
inline void RXPattern::set_BLACK_H2() { edge_1    -=    531441; edge_2    -=       243; corner11b -=         3; diag_7b   -=         1; };

inline void RXPattern::set_BLACK_A3() { edge_4    -=     19683; corner11a -=      6561; hv_3c     -=      2187; diag_6c   -=       243; };
inline void RXPattern::set_BLACK_B3() { edge_4    -=   4782969; corner11a -=       729; hv_3c     -=       729; diag_7c   -=       243; };
inline void RXPattern::set_BLACK_C3() { corner11a -=       243; hv_3a     -=         9; hv_3c     -=       243; diag_8a   -=         9; diag_5d   -=         9; };
inline void RXPattern::set_BLACK_D3() { hv_3c     -=        81; hv_4a     -=         9; diag_7a   -=         9; diag_6d   -=        27; };
inline void RXPattern::set_BLACK_E3() { hv_3c     -=        27; hv_4b     -=       243; diag_7d   -=        81; diag_6a   -=         9; };
inline void RXPattern::set_BLACK_F3() { corner11b -=       243; hv_3b     -=       243; hv_3c     -=         9; diag_8b   -=       243; diag_5a   -=         9; };
inline void RXPattern::set_BLACK_G3() { edge_2    -=         3; corner11b -=        81; hv_3c     -=         3; diag_7b   -=         3; };
inline void RXPattern::set_BLACK_H3() { edge_2    -=       729; corner11b -=         9; hv_3c     -=         1; diag_6b   -=         1; };

inline void RXPattern::set_BLACK_A4() { edge_4    -=      6561; corner11a -=      2187; hv_4c     -=      2187; diag_5c   -=        81; };
inline void RXPattern::set_BLACK_B4() { edge_4    -=  14348907; hv_4c     -=       729; diag_6c   -=        81; diag_5d   -=         3; };
inline void RXPattern::set_BLACK_C4() { hv_3a     -=        27; hv_4c     -=       243; diag_7c   -=        81; diag_6d   -=         9; };
inline void RXPattern::set_BLACK_D4() { hv_4a     -=        27; hv_4c     -=        81; diag_8a   -=        27; diag_7d   -=        27; };
inline void RXPattern::set_BLACK_E4() { hv_4b     -=        81; hv_4c     -=        27; diag_8b   -=        81; diag_7a   -=        27; };
inline void RXPattern::set_BLACK_F4() { hv_3b     -=        81; hv_4c     -=         9; diag_7b   -=         9; diag_6a   -=        27; };
inline void RXPattern::set_BLACK_G4() { edge_2    -=         1; hv_4c     -=         3; diag_6b   -=         3; diag_5a   -=        27; };
inline void RXPattern::set_BLACK_H4() { edge_2    -=      2187; corner11b -=        27; hv_4c     -=         1; diag_5b   -=         1; };

inline void RXPattern::set_BLACK_A5() { edge_4    -=      2187; corner11d -=        27; hv_4d     -=         1; diag_5d   -=         1; };
inline void RXPattern::set_BLACK_B5() { edge_4    -=         1; hv_4d     -=         3; diag_6d   -=         3; diag_5c   -=        27; };
inline void RXPattern::set_BLACK_C5() { hv_3a     -=        81; hv_4d     -=         9; diag_7d   -=         9; diag_6c   -=        27; };
inline void RXPattern::set_BLACK_D5() { hv_4a     -=        81; hv_4d     -=        27; diag_8b   -=        27; diag_7c   -=        27; };
inline void RXPattern::set_BLACK_E5() { hv_4b     -=        27; hv_4d     -=        81; diag_8a   -=        81; diag_7b   -=        27; };
inline void RXPattern::set_BLACK_F5() { hv_3b     -=        27; hv_4d     -=       243; diag_7a   -=        81; diag_6b   -=         9; };
inline void RXPattern::set_BLACK_G5() { edge_2    -=  14348907; hv_4d     -=       729; diag_6a   -=        81; diag_5b   -=         3; };
inline void RXPattern::set_BLACK_H5() { edge_2    -=      6561; corner11c -=      2187; hv_4d     -=      2187; diag_5a   -=        81; };

inline void RXPattern::set_BLACK_A6() { edge_4    -=       729; corner11d -=         9; hv_3d     -=         1; diag_6d   -=         1; };
inline void RXPattern::set_BLACK_B6() { edge_4    -=         3; corner11d -=        81; hv_3d     -=         3; diag_7d   -=         3; };
inline void RXPattern::set_BLACK_C6() { corner11d -=       243; hv_3a     -=       243; hv_3d     -=         9; diag_8b   -=         9; diag_5c   -=         9; };
inline void RXPattern::set_BLACK_D6() { hv_3d     -=        27; hv_4a     -=       243; diag_7b   -=        81; diag_6c   -=         9; };
inline void RXPattern::set_BLACK_E6() { hv_3d     -=        81; hv_4b     -=         9; diag_7c   -=         9; diag_6b   -=        27; };
inline void RXPattern::set_BLACK_F6() { corner11c -=       243; hv_3b     -=         9; hv_3d     -=       243; diag_8a   -=       243; diag_5b   -=         9; };
inline void RXPattern::set_BLACK_G6() { edge_2    -=   4782969; corner11c -=       729; hv_3d     -=       729; diag_7a   -=       243; };
inline void RXPattern::set_BLACK_H6() { edge_2    -=     19683; corner11c -=      6561; hv_3d     -=      2187; diag_6a   -=       243; };

inline void RXPattern::set_BLACK_A7() { edge_3    -=    531441; edge_4    -=       243; corner11d -=         3; diag_7d   -=         1; };
inline void RXPattern::set_BLACK_B7() { edge_3    -=   1594323; edge_4    -=         9; corner11d -=     59049; diag_8b   -=         3; };
inline void RXPattern::set_BLACK_C7() { edge_3    -=   4782969; corner11d -=       729; hv_3a     -=       729; diag_7b   -=       243; };
inline void RXPattern::set_BLACK_D7() { edge_3    -=  14348907; hv_4a     -=       729; diag_6b   -=        81; diag_5c   -=         3; };
inline void RXPattern::set_BLACK_E7() { edge_3    -=         1; hv_4b     -=         3; diag_6c   -=         3; diag_5b   -=        27; };
inline void RXPattern::set_BLACK_F7() { edge_3    -=         3; corner11c -=        81; hv_3b     -=         3; diag_7c   -=         3; };
inline void RXPattern::set_BLACK_G7() { edge_2    -=   1594323; edge_3    -=         9; corner11c -=     59049; diag_8a   -=       729; };
inline void RXPattern::set_BLACK_H7() { edge_2    -=     59049; edge_3    -=        27; corner11c -=     19683; diag_7a   -=       729; };

inline void RXPattern::set_BLACK_A8() { edge_3    -=    177147; edge_4    -=        81; corner11d -=         1; diag_8b   -=         1; };
inline void RXPattern::set_BLACK_B8() { edge_3    -=     59049; edge_4    -=        27; corner11d -=     19683; diag_7b   -=       729; };
inline void RXPattern::set_BLACK_C8() { edge_3    -=     19683; corner11d -=      6561; hv_3a     -=      2187; diag_6b   -=       243; };
inline void RXPattern::set_BLACK_D8() { edge_3    -=      6561; corner11d -=      2187; hv_4a     -=      2187; diag_5b   -=        81; };
inline void RXPattern::set_BLACK_E8() { edge_3    -=      2187; corner11c -=        27; hv_4b     -=         1; diag_5c   -=         1; };
inline void RXPattern::set_BLACK_F8() { edge_3    -=       729; corner11c -=         9; hv_3b     -=         1; diag_6c   -=         1; };
inline void RXPattern::set_BLACK_G8() { edge_2    -=    531441; edge_3    -=       243; corner11c -=         3; diag_7c   -=         1; };
inline void RXPattern::set_BLACK_H8() { edge_2    -=    177147; edge_3    -=        81; corner11c -=         1; diag_8a   -=      2187; };





inline void RXPattern::set_WHITE_A1() { edge_1    +=        81; edge_4    +=    177147; corner11a +=         1; diag_8a   +=         1; };
inline void RXPattern::set_WHITE_B1() { edge_1    +=       243; edge_4    +=    531441; corner11a +=         3; diag_7a   +=         1; };
inline void RXPattern::set_WHITE_C1() { edge_1    +=       729; corner11a +=         9; hv_3a     +=         1; diag_6a   +=         1; };
inline void RXPattern::set_WHITE_D1() { edge_1    +=      2187; corner11a +=        27; hv_4a     +=         1; diag_5a   +=         1; };
inline void RXPattern::set_WHITE_E1() { edge_1    +=      6561; corner11b +=      2187; hv_4b     +=      2187; diag_5d   +=        81; };
inline void RXPattern::set_WHITE_F1() { edge_1    +=     19683; corner11b +=      6561; hv_3b     +=      2187; diag_6d   +=       243; };
inline void RXPattern::set_WHITE_G1() { edge_1    +=     59049; edge_2    +=        27; corner11b +=     19683; diag_7d   +=       729; };
inline void RXPattern::set_WHITE_H1() { edge_1    +=    177147; edge_2    +=        81; corner11b +=         1; diag_8b   +=      2187; };

inline void RXPattern::set_WHITE_A2() { edge_1    +=        27; edge_4    +=     59049; corner11a +=     19683; diag_7c   +=       729; };
inline void RXPattern::set_WHITE_B2() { edge_1    +=         9; edge_4    +=   1594323; corner11a +=     59049; diag_8a   +=         3; };
inline void RXPattern::set_WHITE_C2() { edge_1    +=         3; corner11a +=        81; hv_3a     +=         3; diag_7a   +=         3; };
inline void RXPattern::set_WHITE_D2() { edge_1    +=         1; hv_4a     +=         3; diag_6a   +=         3; diag_5d   +=        27; };
inline void RXPattern::set_WHITE_E2() { edge_1    +=  14348907; hv_4b     +=       729; diag_6d   +=        81; diag_5a   +=         3; };
inline void RXPattern::set_WHITE_F2() { edge_1    +=   4782969; corner11b +=       729; hv_3b     +=       729; diag_7d   +=       243; };
inline void RXPattern::set_WHITE_G2() { edge_1    +=   1594323; edge_2    +=         9; corner11b +=     59049; diag_8b   +=       729; };
inline void RXPattern::set_WHITE_H2() { edge_1    +=    531441; edge_2    +=       243; corner11b +=         3; diag_7b   +=         1; };

inline void RXPattern::set_WHITE_A3() { edge_4    +=     19683; corner11a +=      6561; hv_3c     +=      2187; diag_6c   +=       243; };
inline void RXPattern::set_WHITE_B3() { edge_4    +=   4782969; corner11a +=       729; hv_3c     +=       729; diag_7c   +=       243; };
inline void RXPattern::set_WHITE_C3() { corner11a +=       243; hv_3a     +=         9; hv_3c     +=       243; diag_8a   +=         9; diag_5d   +=         9; };
inline void RXPattern::set_WHITE_D3() { hv_3c     +=        81; hv_4a     +=         9; diag_7a   +=         9; diag_6d   +=        27; };
inline void RXPattern::set_WHITE_E3() { hv_3c     +=        27; hv_4b     +=       243; diag_7d   +=        81; diag_6a   +=         9; };
inline void RXPattern::set_WHITE_F3() { corner11b +=       243; hv_3b     +=       243; hv_3c     +=         9; diag_8b   +=       243; diag_5a   +=         9; };
inline void RXPattern::set_WHITE_G3() { edge_2    +=         3; corner11b +=        81; hv_3c     +=         3; diag_7b   +=         3; };
inline void RXPattern::set_WHITE_H3() { edge_2    +=       729; corner11b +=         9; hv_3c     +=         1; diag_6b   +=         1; };

inline void RXPattern::set_WHITE_A4() { edge_4    +=      6561; corner11a +=      2187; hv_4c     +=      2187; diag_5c   +=        81; };
inline void RXPattern::set_WHITE_B4() { edge_4    +=  14348907; hv_4c     +=       729; diag_6c   +=        81; diag_5d   +=         3; };
inline void RXPattern::set_WHITE_C4() { hv_3a     +=        27; hv_4c     +=       243; diag_7c   +=        81; diag_6d   +=         9; };
inline void RXPattern::set_WHITE_D4() { hv_4a     +=        27; hv_4c     +=        81; diag_8a   +=        27; diag_7d   +=        27; };
inline void RXPattern::set_WHITE_E4() { hv_4b     +=        81; hv_4c     +=        27; diag_8b   +=        81; diag_7a   +=        27; };
inline void RXPattern::set_WHITE_F4() { hv_3b     +=        81; hv_4c     +=         9; diag_7b   +=         9; diag_6a   +=        27; };
inline void RXPattern::set_WHITE_G4() { edge_2    +=         1; hv_4c     +=         3; diag_6b   +=         3; diag_5a   +=        27; };
inline void RXPattern::set_WHITE_H4() { edge_2    +=      2187; corner11b +=        27; hv_4c     +=         1; diag_5b   +=         1; };

inline void RXPattern::set_WHITE_A5() { edge_4    +=      2187; corner11d +=        27; hv_4d     +=         1; diag_5d   +=         1; };
inline void RXPattern::set_WHITE_B5() { edge_4    +=         1; hv_4d     +=         3; diag_6d   +=         3; diag_5c   +=        27; };
inline void RXPattern::set_WHITE_C5() { hv_3a     +=        81; hv_4d     +=         9; diag_7d   +=         9; diag_6c   +=        27; };
inline void RXPattern::set_WHITE_D5() { hv_4a     +=        81; hv_4d     +=        27; diag_8b   +=        27; diag_7c   +=        27; };
inline void RXPattern::set_WHITE_E5() { hv_4b     +=        27; hv_4d     +=        81; diag_8a   +=        81; diag_7b   +=        27; };
inline void RXPattern::set_WHITE_F5() { hv_3b     +=        27; hv_4d     +=       243; diag_7a   +=        81; diag_6b   +=         9; };
inline void RXPattern::set_WHITE_G5() { edge_2    +=  14348907; hv_4d     +=       729; diag_6a   +=        81; diag_5b   +=         3; };
inline void RXPattern::set_WHITE_H5() { edge_2    +=      6561; corner11c +=      2187; hv_4d     +=      2187; diag_5a   +=        81; };

inline void RXPattern::set_WHITE_A6() { edge_4    +=       729; corner11d +=         9; hv_3d     +=         1; diag_6d   +=         1; };
inline void RXPattern::set_WHITE_B6() { edge_4    +=         3; corner11d +=        81; hv_3d     +=         3; diag_7d   +=         3; };
inline void RXPattern::set_WHITE_C6() { corner11d +=       243; hv_3a     +=       243; hv_3d     +=         9; diag_8b   +=         9; diag_5c   +=         9; };
inline void RXPattern::set_WHITE_D6() { hv_3d     +=        27; hv_4a     +=       243; diag_7b   +=        81; diag_6c   +=         9; };
inline void RXPattern::set_WHITE_E6() { hv_3d     +=        81; hv_4b     +=         9; diag_7c   +=         9; diag_6b   +=        27; };
inline void RXPattern::set_WHITE_F6() { corner11c +=       243; hv_3b     +=         9; hv_3d     +=       243; diag_8a   +=       243; diag_5b   +=         9; };
inline void RXPattern::set_WHITE_G6() { edge_2    +=   4782969; corner11c +=       729; hv_3d     +=       729; diag_7a   +=       243; };
inline void RXPattern::set_WHITE_H6() { edge_2    +=     19683; corner11c +=      6561; hv_3d     +=      2187; diag_6a   +=       243; };

inline void RXPattern::set_WHITE_A7() { edge_3    +=    531441; edge_4    +=       243; corner11d +=         3; diag_7d   +=         1; };
inline void RXPattern::set_WHITE_B7() { edge_3    +=   1594323; edge_4    +=         9; corner11d +=     59049; diag_8b   +=         3; };
inline void RXPattern::set_WHITE_C7() { edge_3    +=   4782969; corner11d +=       729; hv_3a     +=       729; diag_7b   +=       243; };
inline void RXPattern::set_WHITE_D7() { edge_3    +=  14348907; hv_4a     +=       729; diag_6b   +=        81; diag_5c   +=         3; };
inline void RXPattern::set_WHITE_E7() { edge_3    +=         1; hv_4b     +=         3; diag_6c   +=         3; diag_5b   +=        27; };
inline void RXPattern::set_WHITE_F7() { edge_3    +=         3; corner11c +=        81; hv_3b     +=         3; diag_7c   +=         3; };
inline void RXPattern::set_WHITE_G7() { edge_2    +=   1594323; edge_3    +=         9; corner11c +=     59049; diag_8a   +=       729; };
inline void RXPattern::set_WHITE_H7() { edge_2    +=     59049; edge_3    +=        27; corner11c +=     19683; diag_7a   +=       729; };

inline void RXPattern::set_WHITE_A8() { edge_3    +=    177147; edge_4    +=        81; corner11d +=         1; diag_8b   +=         1; };
inline void RXPattern::set_WHITE_B8() { edge_3    +=     59049; edge_4    +=        27; corner11d +=     19683; diag_7b   +=       729; };
inline void RXPattern::set_WHITE_C8() { edge_3    +=     19683; corner11d +=      6561; hv_3a     +=      2187; diag_6b   +=       243; };
inline void RXPattern::set_WHITE_D8() { edge_3    +=      6561; corner11d +=      2187; hv_4a     +=      2187; diag_5b   +=        81; };
inline void RXPattern::set_WHITE_E8() { edge_3    +=      2187; corner11c +=        27; hv_4b     +=         1; diag_5c   +=         1; };
inline void RXPattern::set_WHITE_F8() { edge_3    +=       729; corner11c +=         9; hv_3b     +=         1; diag_6c   +=         1; };
inline void RXPattern::set_WHITE_G8() { edge_2    +=    531441; edge_3    +=       243; corner11c +=         3; diag_7c   +=         1; };
inline void RXPattern::set_WHITE_H8() { edge_2    +=    177147; edge_3    +=        81; corner11c +=         1; diag_8a   +=      2187; };








inline void RXPattern::flip_BLACK_B1() { edge_1    -=       486; edge_4    -=   1062882; corner11a -=         6; diag_7a   -=         2; };
inline void RXPattern::flip_BLACK_C1() { edge_1    -=      1458; corner11a -=        18; hv_3a     -=         2; diag_6a   -=         2; };
inline void RXPattern::flip_BLACK_D1() { edge_1    -=      4374; corner11a -=        54; hv_4a     -=         2; diag_5a   -=         2; };
inline void RXPattern::flip_BLACK_E1() { edge_1    -=     13122; corner11b -=      4374; hv_4b     -=      4374; diag_5d   -=       162; };
inline void RXPattern::flip_BLACK_F1() { edge_1    -=     39366; corner11b -=     13122; hv_3b     -=      4374; diag_6d   -=       486; };
inline void RXPattern::flip_BLACK_G1() { edge_1    -=    118098; edge_2    -=        54; corner11b -=     39366; diag_7d   -=      1458; };

inline void RXPattern::flip_BLACK_A2() { edge_1    -=        54; edge_4    -=    118098; corner11a -=     39366; diag_7c   -=      1458; };
inline void RXPattern::flip_BLACK_B2() { edge_1    -=        18; edge_4    -=   3188646; corner11a -=    118098; diag_8a   -=         6; };
inline void RXPattern::flip_BLACK_C2() { edge_1    -=         6; corner11a -=       162; hv_3a     -=         6; diag_7a   -=         6; };
inline void RXPattern::flip_BLACK_D2() { edge_1    -=         2; hv_4a     -=         6; diag_6a   -=         6; diag_5d   -=        54; };
inline void RXPattern::flip_BLACK_E2() { edge_1    -=  28697814; hv_4b     -=      1458; diag_6d   -=       162; diag_5a   -=         6; };
inline void RXPattern::flip_BLACK_F2() { edge_1    -=   9565938; corner11b -=      1458; hv_3b     -=      1458; diag_7d   -=       486; };
inline void RXPattern::flip_BLACK_G2() { edge_1    -=   3188646; edge_2    -=        18; corner11b -=    118098; diag_8b   -=      1458; };
inline void RXPattern::flip_BLACK_H2() { edge_1    -=   1062882; edge_2    -=       486; corner11b -=         6; diag_7b   -=         2; };

inline void RXPattern::flip_BLACK_A3() { edge_4    -=     39366; corner11a -=     13122; hv_3c     -=      4374; diag_6c   -=       486; };
inline void RXPattern::flip_BLACK_B3() { edge_4    -=   9565938; corner11a -=      1458; hv_3c     -=      1458; diag_7c   -=       486; };
inline void RXPattern::flip_BLACK_C3() { corner11a -=       486; hv_3a     -=        18; hv_3c     -=       486; diag_8a   -=        18; diag_5d   -=        18; };
inline void RXPattern::flip_BLACK_D3() { hv_3c     -=       162; hv_4a     -=        18; diag_7a   -=        18; diag_6d   -=        54; };
inline void RXPattern::flip_BLACK_E3() { hv_3c     -=        54; hv_4b     -=       486; diag_7d   -=       162; diag_6a   -=        18; };
inline void RXPattern::flip_BLACK_F3() { corner11b -=       486; hv_3b     -=       486; hv_3c     -=        18; diag_8b   -=       486; diag_5a   -=        18; };
inline void RXPattern::flip_BLACK_G3() { edge_2    -=         6; corner11b -=       162; hv_3c     -=         6; diag_7b   -=         6; };
inline void RXPattern::flip_BLACK_H3() { edge_2    -=      1458; corner11b -=        18; hv_3c     -=         2; diag_6b   -=         2; };

inline void RXPattern::flip_BLACK_A4() { edge_4    -=     13122; corner11a -=      4374; hv_4c     -=      4374; diag_5c   -=       162; };
inline void RXPattern::flip_BLACK_B4() { edge_4    -=  28697814; hv_4c     -=      1458; diag_6c   -=       162; diag_5d   -=         6; };
inline void RXPattern::flip_BLACK_C4() { hv_3a     -=        54; hv_4c     -=       486; diag_7c   -=       162; diag_6d   -=        18; };
inline void RXPattern::flip_BLACK_D4() { hv_4a     -=        54; hv_4c     -=       162; diag_8a   -=        54; diag_7d   -=        54; };
inline void RXPattern::flip_BLACK_E4() { hv_4b     -=       162; hv_4c     -=        54; diag_8b   -=       162; diag_7a   -=        54; };
inline void RXPattern::flip_BLACK_F4() { hv_3b     -=       162; hv_4c     -=        18; diag_7b   -=        18; diag_6a   -=        54; };
inline void RXPattern::flip_BLACK_G4() { edge_2    -=         2; hv_4c     -=         6; diag_6b   -=         6; diag_5a   -=        54; };
inline void RXPattern::flip_BLACK_H4() { edge_2    -=      4374; corner11b -=        54; hv_4c     -=         2; diag_5b   -=         2; };

inline void RXPattern::flip_BLACK_A5() { edge_4    -=      4374; corner11d -=        54; hv_4d     -=         2; diag_5d   -=         2; };
inline void RXPattern::flip_BLACK_B5() { edge_4    -=         2; hv_4d     -=         6; diag_6d   -=         6; diag_5c   -=        54; };
inline void RXPattern::flip_BLACK_C5() { hv_3a     -=       162; hv_4d     -=        18; diag_7d   -=        18; diag_6c   -=        54; };
inline void RXPattern::flip_BLACK_D5() { hv_4a     -=       162; hv_4d     -=        54; diag_8b   -=        54; diag_7c   -=        54; };
inline void RXPattern::flip_BLACK_E5() { hv_4b     -=        54; hv_4d     -=       162; diag_8a   -=       162; diag_7b   -=        54; };
inline void RXPattern::flip_BLACK_F5() { hv_3b     -=        54; hv_4d     -=       486; diag_7a   -=       162; diag_6b   -=        18; };
inline void RXPattern::flip_BLACK_G5() { edge_2    -=  28697814; hv_4d     -=      1458; diag_6a   -=       162; diag_5b   -=         6; };
inline void RXPattern::flip_BLACK_H5() { edge_2    -=     13122; corner11c -=      4374; hv_4d     -=      4374; diag_5a   -=       162; };

inline void RXPattern::flip_BLACK_A6() { edge_4    -=      1458; corner11d -=        18; hv_3d     -=         2; diag_6d   -=         2; };
inline void RXPattern::flip_BLACK_B6() { edge_4    -=         6; corner11d -=       162; hv_3d     -=         6; diag_7d   -=         6; };
inline void RXPattern::flip_BLACK_C6() { corner11d -=       486; hv_3a     -=       486; hv_3d     -=        18; diag_8b   -=        18; diag_5c   -=        18; };
inline void RXPattern::flip_BLACK_D6() { hv_3d     -=        54; hv_4a     -=       486; diag_7b   -=       162; diag_6c   -=        18; };
inline void RXPattern::flip_BLACK_E6() { hv_3d     -=       162; hv_4b     -=        18; diag_7c   -=        18; diag_6b   -=        54; };
inline void RXPattern::flip_BLACK_F6() { corner11c -=       486; hv_3b     -=        18; hv_3d     -=       486; diag_8a   -=       486; diag_5b   -=        18; };
inline void RXPattern::flip_BLACK_G6() { edge_2    -=   9565938; corner11c -=      1458; hv_3d     -=      1458; diag_7a   -=       486; };
inline void RXPattern::flip_BLACK_H6() { edge_2    -=     39366; corner11c -=     13122; hv_3d     -=      4374; diag_6a   -=       486; };

inline void RXPattern::flip_BLACK_A7() { edge_3    -=   1062882; edge_4    -=       486; corner11d -=         6; diag_7d   -=         2; };
inline void RXPattern::flip_BLACK_B7() { edge_3    -=   3188646; edge_4    -=        18; corner11d -=    118098; diag_8b   -=         6; };
inline void RXPattern::flip_BLACK_C7() { edge_3    -=   9565938; corner11d -=      1458; hv_3a     -=      1458; diag_7b   -=       486; };
inline void RXPattern::flip_BLACK_D7() { edge_3    -=  28697814; hv_4a     -=      1458; diag_6b   -=       162; diag_5c   -=         6; };
inline void RXPattern::flip_BLACK_E7() { edge_3    -=         2; hv_4b     -=         6; diag_6c   -=         6; diag_5b   -=        54; };
inline void RXPattern::flip_BLACK_F7() { edge_3    -=         6; corner11c -=       162; hv_3b     -=         6; diag_7c   -=         6; };
inline void RXPattern::flip_BLACK_G7() { edge_2    -=   3188646; edge_3    -=        18; corner11c -=    118098; diag_8a   -=      1458; };
inline void RXPattern::flip_BLACK_H7() { edge_2    -=    118098; edge_3    -=        54; corner11c -=     39366; diag_7a   -=      1458; };

inline void RXPattern::flip_BLACK_B8() { edge_3    -=    118098; edge_4    -=        54; corner11d -=     39366; diag_7b   -=      1458; };
inline void RXPattern::flip_BLACK_C8() { edge_3    -=     39366; corner11d -=     13122; hv_3a     -=      4374; diag_6b   -=       486; };
inline void RXPattern::flip_BLACK_D8() { edge_3    -=     13122; corner11d -=      4374; hv_4a     -=      4374; diag_5b   -=       162; };
inline void RXPattern::flip_BLACK_E8() { edge_3    -=      4374; corner11c -=        54; hv_4b     -=         2; diag_5c   -=         2; };
inline void RXPattern::flip_BLACK_F8() { edge_3    -=      1458; corner11c -=        18; hv_3b     -=         2; diag_6c   -=         2; };
inline void RXPattern::flip_BLACK_G8() { edge_2    -=   1062882; edge_3    -=       486; corner11c -=         6; diag_7c   -=         2; };







inline void RXPattern::flip_WHITE_B1() { edge_1    +=       486; edge_4    +=   1062882; corner11a +=         6; diag_7a   +=         2; };
inline void RXPattern::flip_WHITE_C1() { edge_1    +=      1458; corner11a +=        18; hv_3a     +=         2; diag_6a   +=         2; };
inline void RXPattern::flip_WHITE_D1() { edge_1    +=      4374; corner11a +=        54; hv_4a     +=         2; diag_5a   +=         2; };
inline void RXPattern::flip_WHITE_E1() { edge_1    +=     13122; corner11b +=      4374; hv_4b     +=      4374; diag_5d   +=       162; };
inline void RXPattern::flip_WHITE_F1() { edge_1    +=     39366; corner11b +=     13122; hv_3b     +=      4374; diag_6d   +=       486; };
inline void RXPattern::flip_WHITE_G1() { edge_1    +=    118098; edge_2    +=        54; corner11b +=     39366; diag_7d   +=      1458; };

inline void RXPattern::flip_WHITE_A2() { edge_1    +=        54; edge_4    +=    118098; corner11a +=     39366; diag_7c   +=      1458; };
inline void RXPattern::flip_WHITE_B2() { edge_1    +=        18; edge_4    +=   3188646; corner11a +=    118098; diag_8a   +=         6; };
inline void RXPattern::flip_WHITE_C2() { edge_1    +=         6; corner11a +=       162; hv_3a     +=         6; diag_7a   +=         6; };
inline void RXPattern::flip_WHITE_D2() { edge_1    +=         2; hv_4a     +=         6; diag_6a   +=         6; diag_5d   +=        54; };
inline void RXPattern::flip_WHITE_E2() { edge_1    +=  28697814; hv_4b     +=      1458; diag_6d   +=       162; diag_5a   +=         6; };
inline void RXPattern::flip_WHITE_F2() { edge_1    +=   9565938; corner11b +=      1458; hv_3b     +=      1458; diag_7d   +=       486; };
inline void RXPattern::flip_WHITE_G2() { edge_1    +=   3188646; edge_2    +=        18; corner11b +=    118098; diag_8b   +=      1458; };
inline void RXPattern::flip_WHITE_H2() { edge_1    +=   1062882; edge_2    +=       486; corner11b +=         6; diag_7b   +=         2; };

inline void RXPattern::flip_WHITE_A3() { edge_4    +=     39366; corner11a +=     13122; hv_3c     +=      4374; diag_6c   +=       486; };
inline void RXPattern::flip_WHITE_B3() { edge_4    +=   9565938; corner11a +=      1458; hv_3c     +=      1458; diag_7c   +=       486; };
inline void RXPattern::flip_WHITE_C3() { corner11a +=       486; hv_3a     +=        18; hv_3c     +=       486; diag_8a   +=        18; diag_5d   +=        18; };
inline void RXPattern::flip_WHITE_D3() { hv_3c     +=       162; hv_4a     +=        18; diag_7a   +=        18; diag_6d   +=        54; };
inline void RXPattern::flip_WHITE_E3() { hv_3c     +=        54; hv_4b     +=       486; diag_7d   +=       162; diag_6a   +=        18; };
inline void RXPattern::flip_WHITE_F3() { corner11b +=       486; hv_3b     +=       486; hv_3c     +=        18; diag_8b   +=       486; diag_5a   +=        18; };
inline void RXPattern::flip_WHITE_G3() { edge_2    +=         6; corner11b +=       162; hv_3c     +=         6; diag_7b   +=         6; };
inline void RXPattern::flip_WHITE_H3() { edge_2    +=      1458; corner11b +=        18; hv_3c     +=         2; diag_6b   +=         2; };

inline void RXPattern::flip_WHITE_A4() { edge_4    +=     13122; corner11a +=      4374; hv_4c     +=      4374; diag_5c   +=       162; };
inline void RXPattern::flip_WHITE_B4() { edge_4    +=  28697814; hv_4c     +=      1458; diag_6c   +=       162; diag_5d   +=         6; };
inline void RXPattern::flip_WHITE_C4() { hv_3a     +=        54; hv_4c     +=       486; diag_7c   +=       162; diag_6d   +=        18; };
inline void RXPattern::flip_WHITE_D4() { hv_4a     +=        54; hv_4c     +=       162; diag_8a   +=        54; diag_7d   +=        54; };
inline void RXPattern::flip_WHITE_E4() { hv_4b     +=       162; hv_4c     +=        54; diag_8b   +=       162; diag_7a   +=        54; };
inline void RXPattern::flip_WHITE_F4() { hv_3b     +=       162; hv_4c     +=        18; diag_7b   +=        18; diag_6a   +=        54; };
inline void RXPattern::flip_WHITE_G4() { edge_2    +=         2; hv_4c     +=         6; diag_6b   +=         6; diag_5a   +=        54; };
inline void RXPattern::flip_WHITE_H4() { edge_2    +=      4374; corner11b +=        54; hv_4c     +=         2; diag_5b   +=         2; };

inline void RXPattern::flip_WHITE_A5() { edge_4    +=      4374; corner11d +=        54; hv_4d     +=         2; diag_5d   +=         2; };
inline void RXPattern::flip_WHITE_B5() { edge_4    +=         2; hv_4d     +=         6; diag_6d   +=         6; diag_5c   +=        54; };
inline void RXPattern::flip_WHITE_C5() { hv_3a     +=       162; hv_4d     +=        18; diag_7d   +=        18; diag_6c   +=        54; };
inline void RXPattern::flip_WHITE_D5() { hv_4a     +=       162; hv_4d     +=        54; diag_8b   +=        54; diag_7c   +=        54; };
inline void RXPattern::flip_WHITE_E5() { hv_4b     +=        54; hv_4d     +=       162; diag_8a   +=       162; diag_7b   +=        54; };
inline void RXPattern::flip_WHITE_F5() { hv_3b     +=        54; hv_4d     +=       486; diag_7a   +=       162; diag_6b   +=        18; };
inline void RXPattern::flip_WHITE_G5() { edge_2    +=  28697814; hv_4d     +=      1458; diag_6a   +=       162; diag_5b   +=         6; };
inline void RXPattern::flip_WHITE_H5() { edge_2    +=     13122; corner11c +=      4374; hv_4d     +=      4374; diag_5a   +=       162; };

inline void RXPattern::flip_WHITE_A6() { edge_4    +=      1458; corner11d +=        18; hv_3d     +=         2; diag_6d   +=         2; };
inline void RXPattern::flip_WHITE_B6() { edge_4    +=         6; corner11d +=       162; hv_3d     +=         6; diag_7d   +=         6; };
inline void RXPattern::flip_WHITE_C6() { corner11d +=       486; hv_3a     +=       486; hv_3d     +=        18; diag_8b   +=        18; diag_5c   +=        18; };
inline void RXPattern::flip_WHITE_D6() { hv_3d     +=        54; hv_4a     +=       486; diag_7b   +=       162; diag_6c   +=        18; };
inline void RXPattern::flip_WHITE_E6() { hv_3d     +=       162; hv_4b     +=        18; diag_7c   +=        18; diag_6b   +=        54; };
inline void RXPattern::flip_WHITE_F6() { corner11c +=       486; hv_3b     +=        18; hv_3d     +=       486; diag_8a   +=       486; diag_5b   +=        18; };
inline void RXPattern::flip_WHITE_G6() { edge_2    +=   9565938; corner11c +=      1458; hv_3d     +=      1458; diag_7a   +=       486; };
inline void RXPattern::flip_WHITE_H6() { edge_2    +=     39366; corner11c +=     13122; hv_3d     +=      4374; diag_6a   +=       486; };

inline void RXPattern::flip_WHITE_A7() { edge_3    +=   1062882; edge_4    +=       486; corner11d +=         6; diag_7d   +=         2; };
inline void RXPattern::flip_WHITE_B7() { edge_3    +=   3188646; edge_4    +=        18; corner11d +=    118098; diag_8b   +=         6; };
inline void RXPattern::flip_WHITE_C7() { edge_3    +=   9565938; corner11d +=      1458; hv_3a     +=      1458; diag_7b   +=       486; };
inline void RXPattern::flip_WHITE_D7() { edge_3    +=  28697814; hv_4a     +=      1458; diag_6b   +=       162; diag_5c   +=         6; };
inline void RXPattern::flip_WHITE_E7() { edge_3    +=         2; hv_4b     +=         6; diag_6c   +=         6; diag_5b   +=        54; };
inline void RXPattern::flip_WHITE_F7() { edge_3    +=         6; corner11c +=       162; hv_3b     +=         6; diag_7c   +=         6; };
inline void RXPattern::flip_WHITE_G7() { edge_2    +=   3188646; edge_3    +=        18; corner11c +=    118098; diag_8a   +=      1458; };
inline void RXPattern::flip_WHITE_H7() { edge_2    +=    118098; edge_3    +=        54; corner11c +=     39366; diag_7a   +=      1458; };

inline void RXPattern::flip_WHITE_B8() { edge_3    +=    118098; edge_4    +=        54; corner11d +=     39366; diag_7b   +=      1458; };
inline void RXPattern::flip_WHITE_C8() { edge_3    +=     39366; corner11d +=     13122; hv_3a     +=      4374; diag_6b   +=       486; };
inline void RXPattern::flip_WHITE_D8() { edge_3    +=     13122; corner11d +=      4374; hv_4a     +=      4374; diag_5b   +=       162; };
inline void RXPattern::flip_WHITE_E8() { edge_3    +=      4374; corner11c +=        54; hv_4b     +=         2; diag_5c   +=         2; };
inline void RXPattern::flip_WHITE_F8() { edge_3    +=      1458; corner11c +=        18; hv_3b     +=         2; diag_6c   +=         2; };
inline void RXPattern::flip_WHITE_G8() { edge_2    +=   1062882; edge_3    +=       486; corner11c +=         6; diag_7c   +=         2; };


#endif
