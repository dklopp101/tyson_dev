#ifndef OPCODE_H
#define OPCODE_H

#ifdef __cplusplus
extern "C" {
#endif

// #define RAMSIZE         0x7FFFFFFF
// #define WORDSIZE        4
// #define DOUBLE_WORDSIZE 8
// #define WS              WORDSIZE
// #define DWS             DOUBLE_WORDSIZE
// #define WS_BITS         32
// #define DWS_BITS        64
// #define OPCODE_SIZE     1
// #define RECUR_MAX       0x3E8
// #define STACK_SIZE      100000

// #define UINT_SIZE WORDSIZE
// #define INT_SIZE  WORDSIZE

// #define STACK_CODE 200
// #define RAM_CODE   201

// #define NOTYPE_CODE     0
// #define UINT32_CODE     1
// #define INT32_CODE      2 
// #define NOSIGN_CODE     3
// #define ADDR_CODE       4
// #define UINT8_CODE      5

#define OPCOUNT 61 

#define die_op      0
#define nop_op      1
#define nspctr_op   2
#define nspctst_op  3
#define test_die_op 4
#define call_op     5
#define ret_op      6
#define swtch_op    7
#define jmp_op      8
#define je_op       9
#define jn_op      10
#define jl_op      11
#define jg_op      12
#define jls_op     13
#define jgs_op     14
#define loop_op    15
#define lcont_op   16
#define lbrk_op    17
#define psh_op     18
#define pop_op     19
#define pop2_op    20
#define popn_op    21
#define pshfr_op   22
#define poptr_op   23
#define movtr_op   24
#define stktr_op   25
#define cpyr_op    26
#define setr_op    27
#define pshfrr_op  28
#define pshfrs_op  29
#define inc_op     30
#define dec_op     31
#define add_op     32
#define sub_op     33
#define mul_op     34
#define div_op     35
#define mod_op     36
#define incs_op    37
#define decs_op    38
#define adds_op    39
#define subs_op    40
#define muls_op    41
#define divs_op    42
#define mods_op    43
#define and_op     44
#define not_op     45
#define xor_op     46
#define or_op      47
#define lshft_op   48
#define rshft_op   49
#define lrot_op    50
#define rrot_op    51
#define ands_op    52
#define nots_op    53
#define xors_op    54
#define ors_op     55
#define lshfts_op  56
#define rshfts_op  57
#define lrots_op   58
#define rrots_op   59
#define brkp_op    60

#define build_optable()                   \
    void* optable[OPCOUNT] = {            \
        &&die,                            \
        &&nop,                            \
        &&nspctr,                         \
        &&nspctst,                        \
        &&test_die,                       \
        &&call,                           \
        &&ret,                            \
        &&swtch,                          \
        &&jmp,                            \
        &&je,                             \
        &&jn,                             \
        &&jl,                             \
        &&jg,                             \
        &&jls,                            \
        &&jgs,                            \
        &&loop,                           \
        &&lcont,                          \
        &&lbrk,                           \
        &&psh,                            \
        &&pop,                            \
        &&pop2,                           \
        &&popn,                           \
        &&pshfr,                          \
        &&poptr,                          \
        &&movtr,                          \
        &&stktr,                          \
        &&cpyr,                           \
        &&setr,                           \
        &&pshfrr,                         \
        &&pshfrs,                         \
        &&inc,                            \
        &&dec,                            \
        &&add,                            \
        &&sub,                            \
        &&mul,                            \
        &&div,                            \
        &&mod,                            \
        &&incs,                           \
        &&decs,                           \
        &&adds,                           \
        &&subs,                           \
        &&muls,                           \
        &&divs,                           \
        &&mods,                           \
        &&and,                            \
        &&not,                            \
        &&xor,                            \
        &&or,                             \
        &&lshft,                          \
        &&rshft,                          \
        &&lrot,                           \
        &&rrot,                           \
        &&ands,                           \
        &&nots,                           \
        &&xors,                           \
        &&ors,                            \
        &&lshfts,                         \
        &&rshfts,                         \
        &&lrots,                          \
        &&rrots,                          \
        &&brkp                            \
    };

 const char* mnemonic_strings[] = {
    "die",
    "nop",
    "nspctr",
    "nspctst",
    "test_die",
    "call",
    "ret",
    "swtch",
    "jmp",
    "je",
    "jn",
    "jl",
    "jg",
    "jls",
    "jgs",
    "loop",
    "lcont",
    "lbrk",
    "psh",
    "pop",
    "pop2",
    "popn",
    "pshfr",
    "poptr",
    "movtr",
    "stktr",
    "cpyr",
    "setr",
    "pshfrr",
    "pshfrs",
    "inc",
    "dec",
    "add",
    "sub",
    "mul",
    "div",
    "mod",
    "incs",
    "decs",
    "adds",
    "subs",
    "muls",
    "divs",
    "mods",
    "and",
    "not",
    "xor",
    "or",
    "lshft",
    "rshft",
    "lrot",
    "rrot",
    "ands",
    "nots",
    "xors",
    "ors",
    "lshfts",
    "rshfts",
    "lrots",
    "rrots",
    "brkp"
};

#ifdef __cplusplus
}
#endif

#endif // OPCODE.H