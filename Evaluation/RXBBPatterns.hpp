/*
 *  RXBBPatterns.hpp
 *  Roxane
 *
 *  Created by Bruno Causse on 31/07/05.
 *  Copyleft 2005-2025 personnel.
 *
 */

#ifndef RXBBPATTERN_HPP
#define RXBBPATTERN_HPP

#include <cmath>
#include <arm_neon.h>

#include "RXConstantes.hpp"
#include "RXBitBoard.hpp"
#include "RXPattern.hpp"
#include "RXEvaluation.hpp"


class RXBBPatterns {
    
    void set_BLACK(const int pos);
    void set_WHITE(const int pos);
    
    // move functions
#define func(pos)   void update_patterns_BLACK_##pos(RXMove& move) const; \
void update_patterns_WHITE_##pos(RXMove& move) const
    
    func(A1); func(B1); func(C1); func(D1); func(E1); func(F1); func(G1); func(H1);
    func(A2); func(B2); func(C2); func(D2); func(E2); func(F2); func(G2); func(H2);
    func(A3); func(B3); func(C3); func(D3); func(E3); func(F3); func(G3); func(H3);
    func(A4); func(B4); func(C4);                     func(F4); func(G4); func(H4);
    func(A5); func(B5); func(C5);                     func(F5); func(G5); func(H5);
    func(A6); func(B6); func(C6); func(D6); func(E6); func(F6); func(G6); func(H6);
    func(A7); func(B7); func(C7); func(D7); func(E7); func(F7); func(G7); func(H7);
    func(A8); func(B8); func(C8); func(D8); func(E8); func(F8); func(G8); func(H8);
#undef func

    public :

    RXBitBoard board;
    RXPattern* pattern;

    
    RXBBPatterns();
    
    //constructeur par copie
    RXBBPatterns(const RXBBPatterns& src);
    
    RXBBPatterns& operator=(const RXBBPatterns& src);
    
    ~RXBBPatterns();
    
    void build(const std::string& init);
    
    void do_move(RXMove& move);
    void undo_move(const RXMove& move);
    
    
    
    void (RXBBPatterns::*update_patterns[64][2])(RXMove& move) const;
    void init_update_patterns();
    
    void reset();
    
    double get_n_nodes() const { return board.get_n_nodes(); }
    int get_n_empty() const { return board.n_empty; }
    
    int final_score() const;
    int get_score(const bool useFM = true) const;
    int get_score(const RXMove& move, const bool useFM = true) const;
        
    /* DEBUG */
    friend std::ostream& operator<<(std::ostream& os, RXBBPatterns& sBoard);
    
};

__attribute__((always_inline))
inline RXBBPatterns& RXBBPatterns::operator=(const RXBBPatterns& src) {

    // Optimization: Skip self-assignment check to avoid branch misprediction.
    // Safe because 'pattern' pointers are stable (allocated at startup,
    // never reassigned or deleted during search).
//    if(this != &src) {
    
        board = src.board;
    
        *pattern = *(src.pattern); //copy

//    }
    
    return *this;
}


__attribute__((always_inline))
inline void RXBBPatterns::do_move(RXMove& move) {
    board.do_move(move);
    move.undo_pattern = pattern;
    pattern = move.pattern;
}

__attribute__((always_inline))
inline void RXBBPatterns::undo_move(const RXMove& move) {
    pattern = move.undo_pattern;
    board.undo_move(move);
}

//track bug HASH 24/01/2025
inline int RXBBPatterns::final_score() const {
    int score = board.final_score();
    if(score<0)
        return (-MAX_SCORE+1) + (score + 64);
    return (MAX_SCORE-1) + (score-64);
}

// =============================================================================
// Refactored get_score() and get_score(RXMove&).
// The shared logic is encapsulated within acc_score(), which is called by both variants.
// =============================================================================

// -----------------------------------------------------------------------------
// Evaluates the board score using a hybrid Linear + Factorization Machine model.
// Called with precalculated mobilities
// -----------------------------------------------------------------------------
inline int acc_score(const int   stage,
                          const int   color,
                          const int*  __restrict p,
                          const int   mob_player,
                          const int   mob_opponent,
                          const auto& tab_eval,
                          const bool useFM = true)
{
    const short* __restrict const mob_P  = tab_eval[0];
    const short* __restrict const mob_O  = tab_eval[1];
    const short* __restrict const diag5  = tab_eval[2];
    const short* __restrict const diag6  = tab_eval[3];
    const short* __restrict const diag7  = tab_eval[4];
    const short* __restrict const diag8  = tab_eval[5];
    const short* __restrict const edge1  = tab_eval[6];
    const short* __restrict const edge2  = tab_eval[7];
    const short* __restrict const edge3  = tab_eval[8];
    const short* __restrict const hv2    = tab_eval[9];
    const short* __restrict const hv3    = tab_eval[10];
    const short* __restrict const hv4    = tab_eval[11];
    const short* __restrict const corner = tab_eval[12];

    // -------------------------------------------------------------------------
    // Precomputed indices (Calculated once, reused by both linear and FM stages)
    // -------------------------------------------------------------------------
    const int cp0  = color*p[0],  cp1  = color*p[1],  cp2  = color*p[2],  cp3  = color*p[3];
    const int cp4  = color*p[4],  cp5  = color*p[5],  cp6  = color*p[6],  cp7  = color*p[7];
    const int cp8  = color*p[8],  cp9  = color*p[9],  cp10 = color*p[10], cp11 = color*p[11];
    const int cp12 = color*p[12], cp13 = color*p[13];
    const int cp14 = color*p[14], cp15 = color*p[15], cp16 = color*p[16], cp17 = color*p[17];
    const int cp18 = color*p[18], cp19 = color*p[19], cp20 = color*p[20], cp21 = color*p[21];
    const int cp22 = color*p[22], cp23 = color*p[23], cp24 = color*p[24], cp25 = color*p[25];
    const int cp26 = color*p[26], cp27 = color*p[27], cp28 = color*p[28], cp29 = color*p[29];
    const int cp30 = color*p[30], cp31 = color*p[31], cp32 = color*p[32], cp33 = color*p[33];
    const int cp34 = color*p[34], cp35 = color*p[35], cp36 = color*p[36], cp37 = color*p[37];
    const int cp38 = color*p[38], cp39 = color*p[39], cp40 = color*p[40], cp41 = color*p[41];
    const int cp42 = color*p[42], cp43 = color*p[43], cp44 = color*p[44], cp45 = color*p[45];

    // -------------------------------------------------------------------------
    // Linear Evaluation: Standard weight accumulation for mobility and patterns
    // -------------------------------------------------------------------------
    int
    eval  = mob_P[mob_player];
    eval += mob_O[mob_opponent];

    eval += diag5[cp0]  + diag5[cp1]  + diag5[cp2]  + diag5[cp3];
    eval += diag6[cp4]  + diag6[cp5]  + diag6[cp6]  + diag6[cp7];
    eval += diag7[cp8]  + diag7[cp9]  + diag7[cp10] + diag7[cp11];
    eval += diag8[cp12] + diag8[cp13];

    eval += edge1[cp14] + edge1[cp15] + edge1[cp16] + edge1[cp17];
    eval += edge2[cp18] + edge2[cp19] + edge2[cp20] + edge2[cp21];
    eval += edge3[cp22] + edge3[cp23] + edge3[cp24] + edge3[cp25]
          + edge3[cp26] + edge3[cp27] + edge3[cp28] + edge3[cp29];

    eval += hv2[cp30] + hv2[cp31] + hv2[cp32] + hv2[cp33];
    eval += hv3[cp34] + hv3[cp35] + hv3[cp36] + hv3[cp37];
    eval += hv4[cp38] + hv4[cp39] + hv4[cp40] + hv4[cp41];

    eval += corner[cp42] + corner[cp43] + corner[cp44] + corner[cp45];

    // -------------------------------------------------------------------------
    // FM Correction: Captures non-linear interactions between features
    // -------------------------------------------------------------------------
#ifdef FACT_MACH

    if (useFM && (stage > 9 && stage < 55)) {

        eval += RXEvaluation::eval_w0[stage];

#ifdef __ARM_NEON
        
#ifdef RANK8

        int32x4_t sum_lo   = vdupq_n_s32(0);
        int32x4_t sum_hi   = vdupq_n_s32(0);
        int32x4_t sumsq_lo = vdupq_n_s32(0);
        int32x4_t sumsq_hi = vdupq_n_s32(0);

        auto acc = [&](const Vec_short* V, int idx) __attribute__((always_inline)) {
            int16x8_t vdata = vld1q_s16(V[idx].data);
            int32x4_t vlo   = vmovl_s16(vget_low_s16(vdata));
            int32x4_t vhi   = vmovl_s16(vget_high_s16(vdata));
            sum_lo   = vaddq_s32(sum_lo,   vlo);
            sum_hi   = vaddq_s32(sum_hi,   vhi);
            sumsq_lo = vmlaq_s32(sumsq_lo, vlo, vlo);
            sumsq_hi = vmlaq_s32(sumsq_hi, vhi, vhi);
        };
#else
        
        // Déclaration des accumulateurs — 2 paires lo/hi pour couvrir 16 lanes
        int32x4_t sum_0 = vdupq_n_s32(0);    // lanes  0..3
        int32x4_t sum_1 = vdupq_n_s32(0);    // lanes  4..7
        int32x4_t sum_2 = vdupq_n_s32(0);    // lanes  8..11
        int32x4_t sum_3 = vdupq_n_s32(0);    // lanes 12..15

        int32x4_t sumsq_0 = vdupq_n_s32(0);
        int32x4_t sumsq_1 = vdupq_n_s32(0);
        int32x4_t sumsq_2 = vdupq_n_s32(0);
        int32x4_t sumsq_3 = vdupq_n_s32(0);

        auto acc = [&](const Vec_short* V, int idx) __attribute__((always_inline)) {

            const short* base = V[idx].data;

            int16x8_t v_lo = vld1q_s16(base);        // lanes  0..7
            int16x8_t v_hi = vld1q_s16(base + 8);    // lanes  8..15

            // Élargissement int16 → int32 immédiat
            int32x4_t w0 = vmovl_s16(vget_low_s16(v_lo));
            int32x4_t w1 = vmovl_s16(vget_high_s16(v_lo));
            int32x4_t w2 = vmovl_s16(vget_low_s16(v_hi));
            int32x4_t w3 = vmovl_s16(vget_high_s16(v_hi));

            // Sommes
            sum_0 = vaddq_s32(sum_0, w0);
            sum_1 = vaddq_s32(sum_1, w1);
            sum_2 = vaddq_s32(sum_2, w2);
            sum_3 = vaddq_s32(sum_3, w3);

            // Carrés via vmlaq (int32 × int32 → int32)
            sumsq_0 = vmlaq_s32(sumsq_0, w0, w0);
            sumsq_1 = vmlaq_s32(sumsq_1, w1, w1);
            sumsq_2 = vmlaq_s32(sumsq_2, w2, w2);
            sumsq_3 = vmlaq_s32(sumsq_3, w3, w3);
        };
        
#endif
        
#else

        int sum_vx[RANK]    = {};
        int sum_vx_sq[RANK] = {};

        auto acc = [&](const Vec_short* V, int idx) __attribute__((always_inline)) {
            const Vec_short& vec = V[idx];
            for (unsigned int f = 0; f < RANK; ++f) {
                short v = vec[f];
                sum_vx[f]    += v;
                sum_vx_sq[f] += (long)v * v;
            }
        };

#endif  // __ARM_NEON

        // mobilités
        acc(RXEvaluation::eval_V[0], mob_player);
        acc(RXEvaluation::eval_V[1], mob_opponent);

        // diag 5
        const Vec_short* v2 = RXEvaluation::eval_V[2];
        acc(v2, cp0);
        acc(v2, cp1);
        acc(v2, cp2);
        acc(v2, cp3);

        // diag 6
        const Vec_short* v3 = RXEvaluation::eval_V[3];
        acc(v3, cp4);
        acc(v3, cp5);
        acc(v3, cp6);
        acc(v3, cp7);

        // diag 7
        const Vec_short* v4 = RXEvaluation::eval_V[4];
        acc(v4, cp8);
        acc(v4, cp9);
        acc(v4, cp10);
        acc(v4, cp11);

        // diag 8
        const Vec_short* v5 = RXEvaluation::eval_V[5];
        acc(v5, cp12);
        acc(v5, cp13);

        // edge +2X
        const Vec_short* v6 = RXEvaluation::eval_V[6];
        acc(v6, cp14);
        acc(v6, cp15);
        acc(v6, cp16);
        acc(v6, cp17);

        // edge 2*(3+XF)
        const Vec_short* v7 = RXEvaluation::eval_V[7];
        acc(v7, cp18);
        acc(v7, cp19);
        acc(v7, cp20);
        acc(v7, cp21);
        
        // edge 2*5
        const Vec_short* v8 = RXEvaluation::eval_V[8];
        acc(v8, cp22);
        acc(v8, cp23);
        acc(v8, cp24);
        acc(v8, cp25);
        acc(v8, cp26);
        acc(v8, cp27);
        acc(v8, cp28);
        acc(v8, cp29);

        // hv2
        const Vec_short* v9 = RXEvaluation::eval_V[9];
        acc(v9,  cp30);
        acc(v9,  cp31);
        acc(v9,  cp32);
        acc(v9,  cp33);

        // hv3
        const Vec_short* v10 = RXEvaluation::eval_V[10];
        acc(v10, cp34);
        acc(v10, cp35);
        acc(v10, cp36);
        acc(v10, cp37);

        // hv4
        const Vec_short* v11 = RXEvaluation::eval_V[11];
        acc(v11, cp38);
        acc(v11, cp39);
        acc(v11, cp40);
        acc(v11, cp41);

        // corner 4/3/3/1
        const Vec_short* v12 = RXEvaluation::eval_V[12];
        acc(v12, cp42);
        acc(v12, cp43);
        acc(v12, cp44);
        acc(v12, cp45);
        

#ifdef __ARM_NEON
        
#ifdef RANK8
        int32x4_t res_lo = vsubq_s32(vmulq_s32(sum_lo, sum_lo), sumsq_lo);
        int32x4_t res_hi = vsubq_s32(vmulq_s32(sum_hi, sum_hi), sumsq_hi);
        int fm_interaction = vaddvq_s32(vaddq_s32(res_lo, res_hi));
#else

        // FM = Σ (sum²  - sumsq)
        int32x4_t res0 = vsubq_s32(vmulq_s32(sum_0, sum_0), sumsq_0);
        int32x4_t res1 = vsubq_s32(vmulq_s32(sum_1, sum_1), sumsq_1);
        int32x4_t res2 = vsubq_s32(vmulq_s32(sum_2, sum_2), sumsq_2);
        int32x4_t res3 = vsubq_s32(vmulq_s32(sum_3, sum_3), sumsq_3);

        int fm_interaction = vaddvq_s32(
            vaddq_s32(vaddq_s32(res0, res1),
                      vaddq_s32(res2, res3))
        );
        

#endif
        
#else
        int fm_interaction = 0;
        for (unsigned int f = 0; f < RANK; ++f)
            fm_interaction += sum_vx[f] * sum_vx[f] - sum_vx_sq[f];
#endif

        eval += fm_interaction / (2 * 256);
    }
#endif  // FACT_MACH

    if (eval > 0) eval += 128; else eval -= 128;
    return eval / 256;
}


// -----------------------------------------------------------------------------
//  get_score() — position courante
// -----------------------------------------------------------------------------
inline int RXBBPatterns::get_score(const bool useFM) const
{
    const int stage = 60 - board.n_empty;
    const int color = 1 - 2 * board.player;

    uint64x2_t mob  = board.dual_count_legal_moves();
    const int mob_p = std::min(23, (int)vgetq_lane_u64(mob, 0));
    const int mob_o = std::min(23, (int)vgetq_lane_u64(mob, 1));

    return acc_score(stage, color, pattern->patt,
                          mob_p, mob_o,
                          RXEvaluation::eval_w[stage],
                          useFM);
}


// -----------------------------------------------------------------------------
//  get_score(RXMove&) — après un coup candidat
// -----------------------------------------------------------------------------
inline int RXBBPatterns::get_score(const RXMove& move, const bool useFM) const
{
    const int stage = 61 - board.n_empty;
    const int color = 2 * board.player - 1;

    const unsigned long long discs_player   = board.discs[board.player ^ 1] ^ move.flipped;
    const unsigned long long discs_opponent = (board.discs[board.player] ^ move.flipped) | move.square;

    uint64x2_t mob  = RXBitBoard::dual_count_legal_moves(discs_player, discs_opponent);
    const int mob_p = std::min(23, (int)vgetq_lane_u64(mob, 0));
    const int mob_o = std::min(23, (int)vgetq_lane_u64(mob, 1));

    return acc_score(stage, color, move.pattern->patt,
                          mob_p, mob_o,
                          RXEvaluation::eval_w[stage],
                          useFM);
}


#endif
