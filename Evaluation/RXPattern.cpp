//
//  RXPattern..cpp
//  Evaluation
//
//  Created by Causse Bruno on 07/11/2025.
//

#include "RXPattern.hpp"


std::ostream& operator<<(std::ostream& os, RXPattern& pattern) {

/*
    
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
*/
    os << "diag_5a = " << pattern.diag_5a << std::endl;
    os << "diag_5b = " << pattern.diag_5b << std::endl;
    os << "diag_5c = " << pattern.diag_5c << std::endl;
    os << "diag_5d = " << pattern.diag_5d << std::endl;
    os << std::endl;
    os << "diag_6a = " << pattern.diag_6a << std::endl;
    os << "diag_6b = " << pattern.diag_6b << std::endl;
    os << "diag_6c = " << pattern.diag_6c << std::endl;
    os << "diag_6d = " << pattern.diag_6d << std::endl;
    os << std::endl;
    os << "diag_7a = " << pattern.diag_7a << std::endl;
    os << "diag_7b = " << pattern.diag_7b << std::endl;
    os << "diag_7c = " << pattern.diag_7c << std::endl;
    os << "diag_7d = " << pattern.diag_7d << std::endl;
    os << std::endl;
    os << "diag_8a = " << pattern.diag_8a << std::endl;
    os << "diag_8b = " << pattern.diag_8b << std::endl;


    return os;

}
