SIGNED_SIGNCODE   = 1
UNSIGNED_SIGNCODE = 2
NOSIGN_SIGNCODE   = 3
ADDR_SIGNCODE     = 4

signcode_mnemonic_tbl = { 1 : 'SIGNED-INT',
                          2 : 'UNSIGNED-INT',
                          3 : 'NOSIGN-INT',
                          4 : 'ADDRESS-INT'
}

WORDSIZE    = 4
OPCODE_SIZE = 1

MAX_ID_LEN  = 40
MIN_ID_LEN  = 1

START_LABEL_IDENTIFIER = 'main'
MACRO_KEYWORD          = 'macro'
LABEL_DEF_SUFFIX       = ':'
SIGNED_INT_PREFIX      = '$'
UNSIGNED_INT_PREFIX    = '%'
ADDR_INT_PREFIX        = '@'

# dict mapping mnemonic to their opcodes.
optbl = {
    'die'     :  0,   # 0
    'nop'     :  1,   # 1
    'nspct'   :  2,   # 2
    'nspctst' :  3,   # 3
    'test_die':  4,   # 4
    'call'    :  5,   # 5
    'ret'     :  6,   # 6
    'swtch'   :  7,   # 7
    'jmp'     :  8,   # 8
    'je'      :  9,   # 9
    'jn'      : 10,   # 10
    'jl'      : 11,   # 11
    'jg'      : 12,   # 12
    'jls'     : 13,   # 13
    'jgs'     : 14,   # 14
    'loop'    : 15,   # 15
    'lcont'   : 16,   # 16
    'lbrk'    : 17,   # 17
    'psh'     : 18,   # 18
    'pop'     : 19,   # 19
    'pop2'    : 20,   # 20
    'popn'    : 21,   # 21
    'pshfr'   : 22,   # 22
    'poptr'   : 23,   # 23
    'movtr'   : 24,   # 24
    'stktr'   : 25,   # 25
    'cpyr'    : 26,   # 26
    'setr'    : 27,   # 27
    'pshfrr'  : 28,   # 28
    'pshfrs'  : 29,   # 29
    'inc'     : 30,   # 30
    'dec'     : 31,   # 31
    'add'     : 32,   # 32
    'sub'     : 33,   # 33
    'mul'     : 34,   # 34
    'div'     : 35,   # 35
    'mod'     : 36,   # 36
    'incs'    : 37,   # 37
    'decs'    : 38,   # 38
    'adds'    : 39,   # 39
    'subs'    : 40,   # 40
    'muls'    : 41,   # 41
    'divs'    : 42,   # 42
    'mods'    : 43,   # 43
    'and'     : 44,   # 44
    'not'     : 45,   # 45
    'xor'     : 46,   # 46
    'or'      : 47,   # 47
    'lshft'   : 48,   # 48
    'rshft'   : 49,   # 49
    'lrot'    : 50,   # 50
    'rrot'    : 51,   # 51
    'ands'    : 52,   # 52
    'nots'    : 53,   # 53
    'xors'    : 54,   # 54
    'ors'     : 55,   # 55
    'lshfts'  : 56,   # 56
    'rshfts'  : 57,   # 57
    'lrots'   : 58,   # 58
    'rrots'   : 59    # 59
}


# dict mapping opcodes to their mnemonic.
mnemonic_tbl = {
    0  : 'die',
    1  : 'nop',
    2  : 'nspct',
    3  : 'nspctst',
    4  : 'test_die',
    5  : 'call',
    6  : 'ret',
    7  : 'swtch',
    8  : 'jmp',
    9  : 'je',
    10 : 'jn',
    11 : 'jl',
    12 : 'jg',
    13 : 'jls',
    14 : 'jgs',
    15 : 'loop',
    16 : 'lcont',
    17 : 'lbrk',
    18 : 'psh',
    19 : 'pop',
    20 : 'pop2',
    21 : 'popn',
    22 : 'pshfr',
    23 : 'poptr',
    24 : 'movtr',
    25 : 'stktr',
    26 : 'cpyr',
    27 : 'setr',
    28 : 'pshfrr',
    29 : 'pshfrs',
    30 : 'inc',
    31 : 'dec',
    32 : 'add',
    33 : 'sub',
    34 : 'mul',
    35 : 'div',
    36 : 'mod',
    37 : 'incs',
    38 : 'decs',
    39 : 'adds',
    40 : 'subs',
    41 : 'muls',
    42 : 'divs',
    43 : 'mods',
    44 : 'and',
    45 : 'not',
    46 : 'xor',
    47 : 'or',
    48 : 'lshft',
    49 : 'rshft',
    50 : 'lrot',
    51 : 'rrot',
    52 : 'ands',
    53 : 'nots',
    54 : 'xors',
    55 : 'ors',
    56 : 'lshfts',
    57 : 'rshfts',
    58 : 'lrots',
    59 : 'rrots'
}


# dict mapping opcodes to their sizes in memory.
opsize_tbl = {
    0  : 1,  # 'die'
    1  : 1,  # 'nop'
    2  : 5,  # 'nspct'
    3  : 5,  # 'nspctst'
    4  : 1,  # 'test_die'
    5  : 5,  # 'call'
    6  : 1,  # 'ret'
    7  : 1,  # 'swtch'
    8  : 5,  # 'jmp'
    9  : 5,  # 'je'
    10 : 5,  # 'jn'
    11 : 5,  # 'jl'
    12 : 5,  # 'jg'
    13 : 5,  # 'jls'
    14 : 5,  # 'jgs'
    15 : 13,  # 'loop'
    16 : 1,  # 'lcont'
    17 : 1,  # 'lbrk'
    18 : 5,  # 'psh'
    19 : 1,  # 'pop'
    20 : 1,  # 'pop2'
    21 : 5,  # 'popn'
    22 : 5,  # 'pshfr'
    23 : 5,  # 'poptr'
    24 : 5,  # 'movtr'
    25 : 9,  # 'stktr'
    26 : 9,  # 'cpyr'
    27 : 9,  # 'setr'
    28 : 5,  # 'pshfrr'
    29 : 5,  # 'pshfrs'
    30 : 1,  # 'inc'
    31 : 1,  # 'dec'
    32 : 1,  # 'add'
    33 : 1,  # 'sub'
    34 : 1,  # 'mul'
    35 : 1,  # 'div'
    36 : 1,  # 'mod'
    37 : 1,  # 'incs'
    38 : 1,  # 'decs'
    39 : 1,  # 'adds'
    40 : 1,  # 'subs'
    41 : 1,  # 'muls'
    42 : 1,  # 'divs'
    43 : 1,  # 'mods'
    44 : 1,  # 'and'
    45 : 1,  # 'not'
    46 : 1,  # 'xor'
    47 : 1,  # 'or'
    48 : 1,  # 'lshft'
    49 : 1,  # 'rshft'
    50 : 1,  # 'lrot'
    51 : 1,  # 'rrot'
    52 : 1,  # 'ands'
    53 : 1,  # 'nots'
    54 : 1,  # 'xors'
    55 : 1,  # 'ors'
    56 : 1,  # 'lshfts'
    57 : 1,  # 'rshfts'
    58 : 1,  # 'lrots'
    59 : 1   # 'rrots'
}


# dict that maps opcodes to their operand count.
opargc_tbl = { 
    0  : 0,  # 'die'
    1  : 0,  # 'nop'
    2  : 1,  # 'nspct'
    3  : 1,  # 'nspctst'
    4  : 0,  # 'test_die'
    5  : 1,  # 'call'
    6  : 0,  # 'ret'
    7  : 0,  # 'swtch'
    8  : 1,  # 'jmp'
    9  : 1,  # 'je'
    10 : 1,  # 'jn'
    11 : 1,  # 'jl'
    12 : 1,  # 'jg'
    13 : 1,  # 'jls'
    14 : 1,  # 'jgs'
    15 : 3,  # 'loop'
    16 : 1,  # 'lcont'
    17 : 0,  # 'lbrk'
    18 : 1,  # 'psh'
    19 : 0,  # 'pop'
    20 : 0,  # 'pop2'
    21 : 1,  # 'popn'
    22 : 1,  # 'pshfr'
    23 : 1,  # 'poptr'
    24 : 1,  # 'movtr'
    25 : 2,  # 'stktr'
    26 : 2,  # 'cpyr'
    27 : 2,  # 'setr'
    28 : 1,  # 'pshfrr'
    29 : 1,  # 'pshfrs'
    30 : 0,  # 'inc'
    31 : 0,  # 'dec'
    32 : 0,  # 'add'
    33 : 0,  # 'sub'
    34 : 0,  # 'mul'
    35 : 0,  # 'div'
    36 : 0,  # 'mod'
    37 : 0,  # 'incs'
    38 : 0,  # 'decs'
    39 : 0,  # 'adds'
    40 : 0,  # 'subs'
    41 : 0,  # 'muls'
    42 : 0,  # 'divs'
    43 : 0,  # 'mods'
    44 : 0,  # 'and'
    45 : 0,  # 'not'
    46 : 0,  # 'xor'
    47 : 0,  # 'or'
    48 : 0,  # 'lshft'
    49 : 0,  # 'rshft'
    50 : 0,  # 'lrot'
    51 : 0,  # 'rrot'
    52 : 0,  # 'ands'
    53 : 0,  # 'nots'
    54 : 0,  # 'xors'
    55 : 0,  # 'ors'
    56 : 0,  # 'lshfts'
    57 : 0,  # 'rshfts'
    58 : 0,  # 'lrots'
    59 : 0   # 'rrots'
}

oprtype_tbl = { 
    0  : 0,  # 'die'
    1  : 0,  # 'nop'
    2  : (ADDR_SIGNCODE, UNSIGNED_SIGNCODE),  # 'nspct'
    3  : (ADDR_SIGNCODE, UNSIGNED_SIGNCODE),  # 'nspctst'
    4  : 0,  # 'test_die'
    5  : (ADDR_SIGNCODE, UNSIGNED_SIGNCODE),  # 'call'
    6  : 0,  # 'ret'
    7  : 0,  # 'swtch'
    8  : (ADDR_SIGNCODE, UNSIGNED_SIGNCODE), # 'jmp'
    9  : (ADDR_SIGNCODE, UNSIGNED_SIGNCODE),  # 'je'
    10 : (ADDR_SIGNCODE, UNSIGNED_SIGNCODE),  # 'jn'
    11 : (ADDR_SIGNCODE, UNSIGNED_SIGNCODE),  # 'jl'
    12 : (ADDR_SIGNCODE, UNSIGNED_SIGNCODE),  # 'jg'
    13 : (ADDR_SIGNCODE, UNSIGNED_SIGNCODE),  # 'jls'
    14 : (ADDR_SIGNCODE, UNSIGNED_SIGNCODE), # 'jgs'
    15 : (UNSIGNED_SIGNCODE, (ADDR_SIGNCODE, UNSIGNED_SIGNCODE), (ADDR_SIGNCODE, UNSIGNED_SIGNCODE)), # 'loop'
    16 : 0,  # 'lcont'
    17 : 0,  # 'lbrk'
    18 : (UNSIGNED_SIGNCODE, SIGNED_SIGNCODE, ADDR_SIGNCODE),  # 'psh'
    19 : 0,  # 'pop'
    20 : 0,  # 'pop2'
    21 : (UNSIGNED_SIGNCODE),  # 'popn'
    22 : (ADDR_SIGNCODE, UNSIGNED_SIGNCODE),  # 'pshfr'
    23 : (ADDR_SIGNCODE, UNSIGNED_SIGNCODE),  # 'poptr'
    24 : (ADDR_SIGNCODE, UNSIGNED_SIGNCODE),  # 'movtr'
    25 : ((ADDR_SIGNCODE, UNSIGNED_SIGNCODE), (ADDR_SIGNCODE, UNSIGNED_SIGNCODE)),  # 'stktr'
    26 : ((ADDR_SIGNCODE, UNSIGNED_SIGNCODE), (ADDR_SIGNCODE, UNSIGNED_SIGNCODE)),  # 'cpyr'
    27 : ((ADDR_SIGNCODE, UNSIGNED_SIGNCODE), (UNSIGNED_SIGNCODE, SIGNED_SIGNCODE, ADDR_SIGNCODE)),  # 'setr'
    28 : (ADDR_SIGNCODE, UNSIGNED_SIGNCODE),  # 'pshfrr'
    29 : (ADDR_SIGNCODE, UNSIGNED_SIGNCODE),  # 'pshfrs'
    30 : 0,  # 'inc'
    31 : 0,  # 'dec'
    32 : 0,  # 'add'
    33 : 0,  # 'sub'
    34 : 0,  # 'mul'
    35 : 0,  # 'div'
    36 : 0,  # 'mod'
    37 : 0,  # 'incs'
    38 : 0,  # 'decs'
    39 : 0,  # 'adds'
    40 : 0,  # 'subs'
    41 : 0,  # 'muls'
    42 : 0,  # 'divs'
    43 : 0,  # 'mods'
    44 : 0,  # 'and'
    45 : 0,  # 'not'
    46 : 0,  # 'xor'
    47 : 0,  # 'or'
    48 : 0,  # 'lshft'
    49 : 0,  # 'rshft'
    50 : 0,  # 'lrot'
    51 : 0,  # 'rrot'
    52 : 0,  # 'ands'
    53 : 0,  # 'nots'
    54 : 0,  # 'xors'
    55 : 0,  # 'ors'
    56 : 0,  # 'lshfts'
    57 : 0,  # 'rshfts'
    58 : 0,  # 'lrots'
    59 : 0   # 'rrots'
}

def opcode_map_test():
    # test that opargc_tbl and oprtype_tbl match up.
    for k, v in opargc_tbl.items():

        if v == 0 and oprtype_tbl[k] != 0:
            print("MISMATCH\n opargc_tbl[%d] = 0 but oprtype_tbl[%d] is not 0 when it should be!" % (k, k))
            print("oprtype_tbl[%d] = %s" % (k, str(oprtype_tbl[k])))
            return 0
        
        if not isinstance(oprtype_tbl[k], tuple):
            print("MISMATCH\noprtype_tbl[%d] is not a tuple when it should be!" % k)
            print("oprtype_tbl[%d] = %s" % (k, str(oprtype_tbl[k])))
            return 0
        
        if len(oprtype_tbl[k]) != v:
            print("MISMATCH\noprtype_tbl[%d] is a tuple but has the wrong length!" % k)
            print("len(oprtype_tbl[%d]) = %d\n actual value: %s" % (k, len(oprtype_tbl[k], str(oprtype_tbl[k]))))
            return 0
        
        print("opargc_tbl matches oprtype_tbl! no errors present.")
        
    # confirm that opsize_tbl matches  oprargc_tbl.
    for k, v in opargc_tbl:
        x = opsize_tbl[k]

      #  if x != ( v * WORDSIZE )
   # opsize_tbl
