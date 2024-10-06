from collections import *

import pickle
import assembler

def pickle_token_list(token_list):
    TEMP_TOKEN_DUMPFILE = 'temp_token_dump.b'
    # dump token list to temp file.
    try:
        with open(TEMP_TOKEN_DUMPFILE, 'wb') as file:
            # Write the list to file.
            pickle.dump(token_list, file)
    except FileNotFoundError:
        print("Error: The file was not found.")
    except PermissionError:
        print("Error: You do not have permission to access this file.")
    except IsADirectoryError:
        print("Error: The specified path is a directory, not a file.")
    except OSError as e:
        print(f"Error: An I/O error occurred. {e}")
    except Exception as e:
        print(f"Error building program list: \n {e}")

# parent token type code list.
token_type_list = {
    'KEYWORD'    :  500,
    'IDENTIFIER' :  501,
    'INTEGER'    :  502,
    'OPERATOR'   :  503,
    'TOKENS_EOF' :  999
}

# keyword type code list.
# codes match their respective entries in mnemonic list.
keyword_list = {
    'const'      :  100,
    'var'        :  1,
    'sub'        :  2,
    'if'         :  3,
    'elif'       :  4,
    'else'       :  5,
    'while'      :  6,
    'return'     :  7,
    'print'      :  8,
    'fileopen'   :  9,
    'fileclose'  : 10,
    'continue'   : 38,
    'break'      : 39
 }

# token mnemonic list.
# codes match their respective entries in mnemonic list.
token_mnemonic = {
    999 : "TOKEN_STREAM_END",
    100 : "CONST_DEC",
    1   : "VAR_DEC",
    2   : "SUB_DEC",
    3   : "IF_STMT",
    4   : "ELIF_STMT",
    5   : "ELSE_STMT",
    6   : "WHILE_STMT",
    7   : "RETURN_STMT",
    8   : "PRINT_KEYWORD",
    9   : "FILEOPEN_KEYWORD",
    10  : "FILECLOSE_KEYWORD",
    11  : "L_PAREN",
    12  : "R_PAREN",
    13  : "L_CBRACE",
    14  : "R_CBRACE",
    15  : "L_BRACKET",
    16  : "R_BRACKET",
    17  : "NOT_OP",
    18  : "ADDR_OP",
    19  : "ADD_OP",
    20  : "SUB_OP",
    21  : "MUL_OP",
    22  : "DIV_OP",
    23  : "MOD_OP",
    24  : "ASSIGN_OP",
    501 : "IDENTIFIER",
    502 : "INTEGER",
    27  : "LT_OP",
    28  : "GT_OP",
    29  : "COMMA",
    30  : "EQ_OP",
    31  : "NOT_EQ_OP",
    32  : "LE_OP",
    33  : "GE_OP",
    34  : "INC_OP",
    35  : "DEC_OP",
    36  : "UNARY_ADD",
    37  : "UNARY_SUB",
    38  : "CONTINUE_STMT",
    39  : "BREAK_STMT"
}

# operator type code list.
# NOTE: unary-sub&add use 36+37 type codes. new operator codes must start from 38.
operator_list = {
    '('  : 11,
    ')'  : 12,
    '{'  : 13,
    '}'  : 14,
    '['  : 15,
    ']'  : 16,
    '!'  : 17,
    '&'  : 18,
    '+'  : 19,
    '-'  : 20,
    '*'  : 21,
    '/'  : 22,
    '%'  : 23,
    '='  : 24,
    '<'  : 27,
    '>'  : 28,
    ','  : 29,
    '==' : 30,
    '!=' : 31,
    '<=' : 32,
    '>=' : 33,
    '++' : 34,
    '--' : 35,
    '$+' : 36,
    '$-' : 37,
} # codes 36 & 37 are reserved!!!!!! start from 38

operand_count_map = {
        11 : 0,
        12 : 0,
        13 : 0,
        14 : 0,
        16 : 0,
        15 : 1,
        17 : 1,
        18 : 1,
        19 : 2,
        20 : 2, 
        21 : 2,
        22 : 2,
        23 : 2,
        24 : 2,
        27 : 2, 
        28 : 2, 
        30 : 2,
        31 : 2,
        32 : 2,
        33 : 2,
        36 : 2,
        37 : 2,
} # codes 36 & 37 are reserved!!!!!! start from 38

# Reversed version of the operator & keyword type code list, give it the code and
# returns a string of the operator/keyword, used for error messages and what not.
rev_op_list = {v: k for k, v in operator_list.items()}
rev_kw_list = {v: k for k, v in keyword_list.items()}

class Token:
    def __init__(self, 
                 _type, 
                 subtype, 
                 line, 
                 col, 
                 rawstr, 
                 ndx, 
                 value=None):
        
        self.type      = _type # master token type code.
        self.subtype   = subtype # specifies what op, keyword ect token is.
        self.type_set  = ((_type, subtype))
        self.line      = line # line token is on source file.
        self.col       = col # col token is on source file.
        self.rawstr    = rawstr # raw string from source file, '+', 'sub', 'var_name' ect.
        self.value     = value # used by integer tokens.
        self.mnemonic  = token_mnemonic[subtype]
        self.ndx       = ndx # position within token list.
        self.print_str = self.build_print_str()
        #self.oprcount  = operand_count_map[subtype] if _type == 503 else None

    def modify(self, 
               _type, 
               subtype, 
               value=None):
        
        self.mnemonic  = token_mnemonic[subtype]
        self.type      = _type
        self.subtype   = subtype
        self.oprcount  = operand_count_map[subtype]
        self.print_str = self.build_print_str()

    def build_print_str(self):
        if self.type == 502: # 502 = integer token code.
            vs = 'value: <%d>' % self.value
        else:
            vs = ''

        return '<%s> @ col %d line %d raw-string: [%s] %s index: %d | TC: %d STC: %d' % (self.mnemonic, self.col, self.line, self.rawstr, vs, self.ndx, self.type, self.subtype)

    def __str__(self):
        return self.print_str

class TokenList:
    def __init__(self):
        self.list = []
        self.code_list = [] # list of tuples pairs of each token's type and subtype.
        self.tokcount = 0

    def print_token(self, ndx):
        print(self.list[ndx])

    def create(self, _type, subtype, line, col, rawstr, value=None):
        self.list.append(Token(_type, subtype, line, col, rawstr, len(self.list), value))
        self.code_list.append((_type, subtype))
        self.tokcount += 1

    def __str__(self):
        string = ''

        for token in self.list:
            string += '\n\n'
            string += token.__str__()

        return string
    
    def __len__(self):
        # check if last token is end of stream token, if so chop it off the len.
        if self.list[self.tokcount - 1].type == 999:
            return self.tokcount - 1
        else:
            return self.tokcount

class BlockChecker:
    # Keeps a stack that is used to check curly braces, if/elif/else 
    # stmts are correct, handles nested stmts and blocks.

    def __init__(self):
        self.stack = deque()
        self.can_elif_else = False

    def assert_top_tok(self, mnemonic):
        try:
            if self.stack[-1].mnemonic == mnemonic:
                return True
        except Exception:
            return False

    def check(self, tok):
        # if tok is if-stmt or { just push onto stack.
        if tok.mnemonic == 'IF_STMT' or tok.mnemonic == 'L_CBRACE':
            self.stack.append(tok)
            return

        elif tok.mnemonic == 'R_CBRACE':
            # is tok the closing brace of an opening brace on stack?

            if self.assert_top_tok("L_CBRACE"):
                self.stack.pop()

            else:
                raise Exception('misplaced r-cbrace')

            # is tok an if-stmt meaning we can take subsequent elif/else stmts?
            if self.assert_top_tok("IF_STMT") or self.assert_top_tok("ELIF_STMT"):
                self.stack.pop()
                self.can_elif_else = True
                return

            elif self.assert_top_tok("ELSE_STMT"):
                self.stack.pop()
                self.can_elif_else = False
                return

        # if tok is else check can_elif_else is true push onto stack, if not raise exception.
        elif tok.mnemonic == 'ELSE_STMT' or tok.mnemonic == 'ELIF_STMT':
            
            if self.can_elif_else:
                self.stack.append(tok)

            else:
                raise Exception('misplaced elif-stmt, no parent if-stmt')

    def __str__(self):
        # used for debugging purposes.
        string = ''

        for tok in self.stack:
            string += 'can-elif-else: %s' % str(self.can_elif_else)
            string += '\n%s\n\n' % tok.__str__()

        return string

class TokenListVerifier:
# Takes a TokenList() object verifies that the tokens are all where they
# should be. Verifies the source code in .pys file is all correct.
# Once TokenListVerifier() has verified the TokenList() it can then be used
# to construct an AST. AstGenerator() object performs no token verification.

    def __init__(self, toklist):
        self.block_checker = BlockChecker()
        self.tokndx = -1
        self.toklist = toklist
        self.tok = None
        self.in_subdef = False
        self.tokens_verified = 0
        lparen_count = 0
        rparen_count = 0

    def advance_tok(self):
        self.tokndx += 1
        self.tok = self.toklist.list[self.tokndx]
        self.tokens_verified += 1

    def recede_tok(self):
        self.tokndx -= 1
        if (self.tokndx - 1) == -1:
            self.tok = None
        else:
            self.tok = self.toklist.list[self.tokndx]
        self.tokens_verified -= 1

    def linecol_str(self):
        return 'line: %d col:%d' % (self.tok.line, self.tok.col)

    def assert_next_tok(self, 
                        toktype, 
                        subtype=None):
        
        # takes a toktype code and optional subtype and returns True or False
        # depending on if the next token(based on tokndx) matches.

        # check if we're at last token meaning next token cannot be of toktype.
        if (self.tokndx + 1) == len(self.toklist.list):
            return False

        return self.assert_tok(self.toklist.list[self.tokndx + 1], toktype, subtype)
    
    def assert_curr_tok(self, 
                        toktype, 
                        subtype=None):
        
        return self.assert_tok(self.tok, toktype, subtype)

    def assert_last_tok(self, 
                        toktype, 
                        subtype=None):
        
        if self.tokndx == 0:
            return False
        
        return self.assert_tok(self.toklist.list[self.tokndx - 1], toktype, subtype)

    def assert_tok(self, 
                   tok, 
                   toktype, 
                   subtype=None):
        
        if tok.type != toktype:
            return False
        if subtype:
            if tok.subtype != subtype:
                return False

        return True
    
    def verify_expr(self, 
                    expr_line, 
                    is_test_expr=False):
        
        # expr_line: line number that expr is on in source file.
        # is_test_expr: tells this method if the expr being verified is a test expr or not.

        # when this method is called self.tok is the first token of the expr.
        lparen_count = rparen_count = assign_count = 0
        lbracket_count = rbracket_count = 0
        print("first tok in expr-> %s" % self.tok)
        # test_expr_errmsg is used when raising exceptions.
        if is_test_expr: 
            if not self.assert_curr_tok(503, 11): # 11: lparen op type code.
                raise Exception('%s left paren expected to start test expr' % (self.linecol_str()))
            test_expr_errmsg = 'test'
        else:
            test_expr_errmsg = ''

        # recede token because top of loop below advances tok.
        self.recede_tok()
        
        while True:
            if (self.tokndx - 1) == -1:
                last_tok = None
            else:
                last_tok = self.tok

            self.advance_tok()

            # check if end of expr reached, first by checking if EOL reached, 
            # otherwise check for l-curly brace, lastly check for last token in toklist.
            # for l-curlyb & tok on different line we must recede_tok() so this
            # method only eats the tokens within the expr nothing more.
            if self.tok.line != expr_line: # eol check.
                self.recede_tok()
                break

            if self.assert_curr_tok(503, 13): # left curly brace check.
                break

            if self.assert_curr_tok(999): # check for last token.
                break

            if self.assert_curr_tok(503, 24):
                assign_count += 1

                if assign_count > 1:
                    raise Exception("misplaced assignment operator")
                
                continue

            # process parens here, they will never be caught by the
            # operator processing code below this.
            # if l parent just increment the counter
            if self.assert_curr_tok(503, 11):
                lparen_count += 1
                continue

            if self.assert_curr_tok(503, 15):
                lbracket_count += 1
                continue

            # if r paren ensure it's a closing paren for counted l parens.
            # if r_paren count is more than l_paren count we have a problem.
            elif self.assert_curr_tok(503, 12):

                rparen_count += 1
                if rparen_count == lparen_count:
                    # open parens have been closed so reset paren 
                    # counts and continue validating expr
                    lparen_count, rparen_count = 0, 0
                    continue

                elif lparen_count == 0:
                    raise Exception('%s r paren misplaced in %s expr.' % (self.linecol_str(), test_expr_errmsg))

            # OPERATOR VALIDATING CODE
            # Catches all cases of invalid operator use within all exprs and raises exception.
            # If operator use is valid then expr validation continues.
            # Also detects unary operators add/sub turning the tokens into them. The lexer
            # only detects add/sub op tokens here is where they're modified into being unary op tokens.
            # this is the only case of token modification within the entire token validating system.
            if self.assert_curr_tok(503): # 503: operator token type code.

                        # DELETE FROM HERE DOWN IF  NEW BUG
                if self.assert_curr_tok(503, 16):

                    rbracket_count += 1

                    if rbracket_count == lbracket_count:
                        # open parens have been closed so reset paren 
                        # counts and continue validating expr
                        lbracket_count, rbracket_count = 0, 0
                        continue

                    if lbracket_count == 0:
                        raise Exception('%s r bracket misplaced in %s expr.' % (self.linecol_str(), test_expr_errmsg))

                    lasttok  = self.toklist.list[self.tokndx - 1]
                    lasttok2 = self.toklist.list[self.tokndx - 2]

                            # check if last tok was int or id, then check if tok before that was l-bracket.
                            # if no id/int and no l-bracket then we have misplaced r-bracket.
                    if self.assert_tok(lasttok, 501, 501) or self.assert_tok(lasttok, 502, 502):

                        if self.assert_tok(lasttok2, 503, 15):
                            lbracket_count += 1
                            continue
                            
                        raise Exception("misplaced 1r-bracket")

                        # DELETE FROM HERE UP IF NEW BUG

                # check if curr op is ! operator being used incorrectly.
                if self.assert_curr_tok(503, 17):
                    if not is_test_expr:
                        raise Exception('%s misplaced %s oper3ator in %s expr.' % (self.linecol_str(), rev_op_list[self.tok.subtype], test_expr_errmsg))

                    # check if last op was anything except l paren.
                    if not self.assert_last_tok(503, 11):
                        raise Exception('%s misplaced %s ope2rator in %s expr.' % (self.linecol_str(), rev_op_list[self.tok.subtype], test_expr_errmsg))

                    # check if next op is any operator.
                    if self.assert_next_tok(503):
                        raise Exception('%s misplaced %s o1perator in %s expr.' % (self.linecol_str(), rev_op_list[self.tok.subtype], test_expr_errmsg))
                    
                    # ! op is valid so continue validating expr.
                    continue

                # check for any cases of invalidation where last tok was also an operator that is
                # caught in the above if blocks.
                if self.assert_last_tok(503):
                    print(last_tok)

                    # check for last op being = and curr being [, which is valid.
                    if self.assert_last_tok(503, 24) and self.assert_curr_tok(503, 15):
                            
                        # # IF BUG DELETE BELOW
                        # # confirm that l-bracket has corresponding r-bracket for array.
                        # if self.toklist.list[self.tokndx  + 2].subtype != 16:
                        #     raise Exception("missing r-bracket")

                        # # IF BUG DELETE ABOVE

                        # l-bracket has corresponding r-bracket.
                        continue

                    # check for last op being ) and next op being =, ,, &, [ ,] or ! al are invalid.
                    # unary add/sub op also get caught in this if block but fall thru it being caught below.
                    # in their processing code.
                    if self.assert_last_tok(503, 11):
                        if self.tok.subtype in [15, 16, 17, 18, 24, 29]:
                            raise Exception('%s misplaced %s oper4ator in %s expr.' % (self.linecol_str(), rev_op_list[self.tok.subtype], test_expr_errmsg))

                    # catch cases of non +/-/ ops to the right of ) ops.
                    if self.assert_last_tok(503, 12):
                        if self.tok.subtype not in [19, 20]:
                            continue

                    # process unary add operator.
                    if self.assert_curr_tok(503, 19):
                        # confirm next token is int or identifier.
                        # 501: id code., 502: int code
                        if self.assert_next_tok(501) or self.assert_next_tok(502):
                            # current token is unary-add operator, update the token.
                            self.tok.modify(503, 36) # 36: unary add
                            continue

                    # process unary sub operator.
                    elif self.assert_curr_tok(503, 20):

                        # confirm next token is int or identifier.
                        if self.assert_next_tok(501) or self.assert_next_tok(502):

                            # current token is unary-sub operator, update the token.
                            self.tok.modify(503, 37) # 36: unary sub
                            continue

                    # check if last op was (.
                    if self.assert_last_tok(503, 11):

                        # check if is ! op used in test expr otherwise its invalid.
                        if self.assert_curr_tok(503, 17):
                            if is_test_expr: 
                                continue
                            else:
                                raise Exception('%s misplaced %s oper9ator in %s expr.' % (self.linecol_str(), rev_op_list[self.tok.subtype], test_expr_errmsg))
                        
                        # check if curr op is & which is valid when not in test expr.
                        elif self.assert_curr_tok(503, 18):
                            if is_test_expr:
                                raise Exception('%s misplaced %s opera99tor in %s expr.' % (self.linecol_str(), rev_op_list[self.tok.subtype], test_expr_errmsg))
                            else:
                                continue
                    
                    print("DANIEL")

                    # two operators next to each other in invalid fasion.
                    raise Exception('%s misplaced %s oper66ator in %s expr.' % (self.linecol_str(), rev_op_list[self.tok.subtype], test_expr_errmsg))
            
                # last tok wasnt an operator, no error here.
                continue

            # check if current tok is int, if so check if last tok was int.
            # cannot have two consequtive ints or identifiers.
            if self.assert_curr_tok(502): # 502: int code

                if self.assert_last_tok(502):
                    # check if the two ints were on same line otherwise no error.
                    if last_tok.line == self.tok.line:
                        raise Exception('%s integer misplaced in %s expr.' % (self.linecol_str(), test_expr_errmsg))
                
                continue

            # if token is an identifier just confirm the next token isnt an identifier.
            if self.assert_curr_tok(501): # 501: identifier code
    
                if self.assert_last_tok(501):
                    # check if the two identifiers were on same line otherwise no error.
                    if last_tok.line == self.tok.line:
                        raise Exception('%s identifier misplaced in %s expr.' % (self.linecol_str(), test_expr_errmsg))
                
                continue

        if lparen_count:   raise Exception("misplaced l-paren or missing r-paren")
        if rparen_count:   raise Exception("misplaced r-paren or missing l-paren")
        if lbracket_count: raise Exception("misplaced l-bracket or missing r-bracket")
        if rbracket_count: raise Exception("misplaced r-bracket or missing l-bracket")

    def verify_block(self, 
                     confirm_cbraces=True, 
                     is_while_block=False, 
                     at_global_lvl=False,
                     in_subdef=False,
                     is_first_call=False):
        
        # confirm_cbraces: tells method to check for code-block curly braces.
        # is_while_block: tells method to accept continue/break stmt as valid.
        # at_global_lvl: tells method whether or not to accept subdef+const stmt as valid, 
        # since they can only be declared at global level.

        # when this method is called, the current tok is the first tok of the block, 
        # which is opening/left cbrace if confirm_cbraces is true.
        # NOTE: blocks can contain all stmt's, keywords, blocks.

        if is_first_call:
            self.advance_tok()

            # check that first tok isnt any of the tokens covered below.
            first_tok = self.toklist.list[0]

            # all operators are invalid as the first token.
            if self.assert_tok(first_tok, 503):
                raise Exception('Line: %d Col: %d misplaced %s operator' % (first_tok.line, first_tok.col))
            
            # identifiers cannot be first token.
            elif self.assert_tok(first_tok, 501):
                raise Exception('Line: %d Col: %d misplaced identifier' % (first_tok.line, first_tok.col))
            
            # integers cannot be first token.
            elif self.assert_tok(first_tok, 502):
                raise Exception('Line: %d Col: %d misplaced integer' % (first_tok.line, first_tok.col))


        # deal with opening l-cbrace.
        if self.assert_curr_tok(503, 13):

            if confirm_cbraces:
                
                try:
                    self.block_checker.check(self.tok)
                except Exception as e:
                    raise '%s %s' % (self.linecol_str(), e)

        # if we dont have an l-cbrace, check if we one was required.
        # if it was required then raise exception.
        else:
            
            if confirm_cbraces:
                raise Exception('%s left curly brace expected to start block' % (self.linecol_str()))

        if is_first_call:
            self.recede_tok()
        
        # loop for processing tokens within the block.
        while True:
            self.advance_tok()

            if self.assert_curr_tok(999): # check for stream end token.
                
                if confirm_cbraces:
                    raise Exception('%s right curly brace expected to end block' % (self.linecol_str()))
                
                break

            elif self.assert_curr_tok(503, 14): # 14: r-cbrace op token type code.
                
                try:
                    self.block_checker.check(self.tok)
                except Exception as e:
                    raise Exception('%s %s' % (self.linecol_str(), e))
                
                if confirm_cbraces: 
                    break

                raise Exception('%s right curly brace misplaced within block' % (self.linecol_str()))
                
            elif self.assert_curr_tok(500, 3): # check for if stmt.
                self.verify_if_elif_stmt(is_elif=False)
                
            elif self.assert_curr_tok(500, 4): # check for elif stmt.
                self.verify_if_elif_stmt(is_elif=True)

            elif self.assert_curr_tok(500, 5): # check for else stmt.
                self.verify_else_stmt()

            elif self.assert_curr_tok(500, 6): # check for while stmt.
                self.verify_while_stmt()

            elif self.assert_curr_tok(500, 7): # check for return stmt.
                # confirm we're actually in a subdef stmt.
                if not in_subdef:
                    raise Exception('%s return stmt must be within subroutine.' % (self.linecol_str()))
                
                rettok_line = self.tok.line
                self.advance_tok()
                self.verify_expr(rettok_line)

            elif self.assert_curr_tok(500, 8): # check for print tok.
                printtok_line = self.tok.line
                self.advance_tok()
                self.verify_expr(printtok_line)

            elif self.assert_curr_tok(500, 37) or self.assert_curr_tok(500, 38): # 37/38: cont/break kw codes.
                # if not a while block these keywords are misplaced.
                if not is_while_block:
                    raise Exception('%s %s stmt misplaced' % (self.linecol_str(), rev_kw_list[self.tok.subtype]))
                
            elif self.assert_curr_tok(500, 2): # 2: sub kw code.
                # check if we're at global level, if not then sub stmt is misplaced.
                if not at_global_lvl:
                    raise Exception('%s sub stmt misplaced' % (self.linecol_str()))
                self.verify_subdef_stmt()

            elif self.assert_curr_tok(500, 100): # 0: const kw code.
                # check if we're at global level, if not then const stmt is misplaced.
                if not at_global_lvl:
                    raise Exception('%s const stmt misplaced' % (self.linecol_str()))
                self.verify_const_dec()

            elif self.assert_curr_tok(500, 1): # 1: var kw code.
                # check if we're at global level, if not then var stmt is misplaced.
                if not at_global_lvl:
                    raise Exception('%s var stmt misplaced' % (self.linecol_str()))
                self.verify_var_dec()

            else:
                # if no matches for keywords or stmt only exprs are left.
                try:
                    self.verify_expr(self.tok.line)
                except Exception as e:
                    raise Exception('%s' % e)

    def verify_const_dec(self):  # WORKS
        # const token was found, next token must be identifier.
        self.advance_tok()
        if not self.assert_curr_tok(501): # 501: id tok type code.
            raise Exception('%s identifier required after const dec' % (self.linecol_str()))

        # next token must be assignment operator.
        self.advance_tok()
        if not self.assert_curr_tok(503, 24): # 503: op tok, 24: assignment op.
            raise Exception('%s assignment operator required after identifier for const declaration.' % (self.linecol_str()))

        # next token must be integer literal.
        self.advance_tok()
        if not self.assert_curr_tok(502): # 502: int token type code.
            raise Exception('%s integer required after identifier for const declaration.' % (self.linecol_str()))

    def verify_var_dec(self): # WORKS
        # var token was found, next token must be identifier.
        self.advance_tok()
        if not self.assert_curr_tok(501): # 501: id tok type code.
            raise Exception('%s identifier required after const dec' % (self.linecol_str()))

        # next token must be assignment operator.
        self.advance_tok()
        if not self.assert_curr_tok(503, 24): # 503: op tok, 24: assignment op.
            raise Exception('%s assignment operator required after identifier for const declaration.' % (self.linecol_str()))

        self.recede_tok()

        # next token must be valid expr.
        try:
            self.verify_expr(self.tok.line)
        except Exception as e:
            raise Exception('%s within var declaration.' % e)
        
    def verify_if_elif_stmt(self, is_elif=False):
        # NOTE: this method handles if AND elif stmts, not else stmts.
        # is_elif: when passed as True then method is verifying an elif stmt, otherwise if stmt.
        # when this method is called self.tok is the if or elif token.

        errstr = 'elif' if is_elif else 'if'

        # send last tok to block-checker because self.tok is token proceeding if-stmt tok.
        try:
            self.block_checker.check(self.tok)
        except Exception as e:
            raise Exception('%s in %s stmt.' % (e, errstr))

        self.advance_tok()

        # check for l-paren of if stmt test expr.
        if not self.assert_curr_tok(503, 11):
            raise Exception('l-paren operator must proceed %s stmt.' % errstr)

        # verify if/elif stmt test expr.
        try:
            self.verify_expr(self.tok.line, is_test_expr=True)
        except Exception as e:
            raise Exception('%s in %s stmt.' % (e, errstr))

        # verify if/elif stmt block.
        try:
            self.verify_block()
        except Exception as e:
            raise Exception('%s in %s stmt.' % (e, errstr))

    def verify_else_stmt(self):
        # when this method is called self.tok is the else token.
        # so we send the last tok to block-checker which is the else tok.

        # catch if else stmt is the first token and therefore misplaced.
        if self.tokndx == 0:
            raise Exception('%s else stmt must have parent if or elif stmt.' % self.linecol_str())

        try:
            self.block_checker.check(self.tok)
        except Exception as e:
             raise Exception('%s %s in else stmt.' % (self.linecol_str(), e))

        self.advance_tok()

        try:
            self.verify_block()
        except Exception as e:
            raise Exception('%s %s in else stmt' % (self.linecol_str(), e))

    def verify_while_stmt(self):
        # verify while stmt test expr.
        self.advance_tok()

        if not self.assert_curr_tok(503, 11):
            raise Exception('l-paren operator must proceed while stmt.')
        
        try:
            self.verify_expr(self.tok.line, is_test_expr=True)
        except Exception as e:
            raise Exception('%s in while stmt.' % e)

        try:
            self.verify_block(is_while_block=True)
        except Exception as e:
            raise Exception('%s in while stmt block' % (self.linecol_str()))
        
    def verify_subdef_stmt(self):
        # verify the subroutine's args expr.
        self.advance_tok()

        # confirm we have an identifier for the subroutine def.
        if not self.assert_curr_tok(501, 501):
            raise Exception('%s subroutine is missing identifier' % self.linecol_str())

        self.advance_tok()

        # process arg expr, first confirm current tok is a l-paren.
        if not self.assert_curr_tok(503, 11):
            raise Exception('%s subroutine has invalid arg expr, missing l-paren' % self.linecol_str())

        try:
            self.verify_expr(self.tok.line)
        except Exception as e:
            raise Exception('%s %s in subroutine arg expr' % (self.linecol_str(), e))
        
        # verify subroutine's block.
        self.verify_block(confirm_cbraces=True, is_while_block=False, at_global_lvl=True, in_subdef=True)
        

    def verify_tokens(self, do_silent=False):
        result = True

        try:
            self.verify_block(confirm_cbraces=False, at_global_lvl=True, is_first_call=True)
        except Exception as e: # verification failed.
            result = False
            if not do_silent:
                print('TokenListVerifier test FAILED!\ndetails:\n\n%s\n\n' % (e))
        else: # verification passed.
            if not do_silent:
                print('\nTokenListVerifier test PASSED!')
        
        return result

class Lexer:
    def __init__(self):
        self.toklist   = TokenList()
        self.col_num   = 0
        self.line_num  = 0
        self.line_len  = 0
        self.line_ndx  = -1
        self.ID_MAXLEN = 30

    def is_operator(self, char):
        # list of operators 1st chars, used by is_operator() for detecting operators.
        op1stchars = ['(', 
                      ')', 
                    '{', 
                    '}', 
                    '[', 
                    ']', 
                    '!', 
                    '&', 
                    '+', 
                    '-', 
                    '*', 
                    '/', 
                    '%', 
                    '=', 
                    '<', 
                    '>', 
                    ',']
        return char in op1stchars

    # Determines if the passed char is an identifier or integer string delimiter.
    def delimiter_reached(self, char):
        if self.line_ndx > self.line_len: return 1 # EOL.
        if char == '\n':                  return 1 # EOL.
        if char == ' ':                   return 2 # whitespace.
        if char == '#':                   return 3 # comment.
        if self.is_operator(char):        return 4 # operator.
        return 0 # no delimiter.

    def next_char_is_delim(self):
        # check if current char is last char of the line.
        if (self.line_ndx + 1) == self.line_len: 
            return 1 # EOL or EOF.

        next_char = self.line[self.line_ndx + 1]

        if next_char == '\n':            return 1 # EOL.
        if next_char == ' ':             return 2 # whitespace.
        if next_char == '#':             return 3 # comment.
        if self.is_operator(next_char):  return 4 # operator.

        return 0 # no delimiter.

    def valid_id_char(self, char):
        return char.isalnum() or char == '_'

    def tokenize(self, pys_file_path):
        str_start_col = 0
        skip_line = False

        try:
            file = open(pys_file_path, 'r')
        except FileNotFoundError:
            print("The file \"%s\" does not exist." % pys_file_path)

        # iterate through source file lines one by one.
        for self.line in file:
            # skip empty lines.
            if len(self.line) == 0: continue

            self.line_len = len(self.line)
            self.line_num += 1
            self.line_ndx = -1

            # skip empty lines.
            #if self.line_len == 0: continue

            # char processing loop.
            # iterate through line's chars one by one, using while stmt because at times we must
            # look one or more chars ahead ect. to process next char just continue this while stmt.
            # when we are done with the line we just break from this while loop and the next cycle
            # of <for line in file> executes.
            while True:
                self.line_ndx += 1

                # for some mysterious reason this is how we must detect
                # the EOL of the last line in the file.
                # print(self.line_len)
                if self.line_ndx == self.line_len: 
                    break

                # assign char we're processing to char variable.
                char = self.line[self.line_ndx]

                # deal with end of line, no idea why sometimes it's dealt with by the code below
                # yet sometimes dealt with <if col_num > line_len: break> code above.
                if char == '\n': break

                # handle our whitespace and comments. if char is whitespace process next char.
                if char == ' ': continue

                # if char is comment the entire line is just skipped.
                if char == '#': break

                # are we dealing with an integer value?
                if char.isdigit():
                    num_str = char # buffer used to build multi-digit numbers(integers).
                    str_start_col = self.line_ndx + 1 # hold the col of mumber.

                    # is it a single digit number? check if next char is a delimiter.
                    # check if we've reached end of the integer by finding a
                    # delimiter at the next char after this current one being processed.
                    if self.next_char_is_delim():
                        # we have single digit int, create token then continue to next char.
                        self.toklist.create(502, 502, self.line_num, str_start_col, char, int(num_str))
                        continue

                    # no delimiter found so we have multi-digit number, build it's string.
                    while True:
                        self.line_ndx += 1
                        char = self.line[self.line_ndx]

                        # check if we have an invalid char for an integer value.
                        if not char.isdigit():
                            raise Exception('invalid integer [%s] on line: %d col: %d' % (num_str + char, self.line_num, self.line_ndx + 1))

                        # append to num string and continue building.
                        num_str += char

                        # check if we've reached end of the integer by finding a delimiter at the next 
                        # char after this current one.
                        if self.next_char_is_delim():
                            # integer complete, tokenize that slut.
                            self.toklist.create(502, 502, self.line_num, str_start_col, num_str, int(num_str))
                            break

                    # finished processing integer, so continue next iteration of char processing loop.
                    continue

                # check for all possible single char tokens before processing identifers & keywords.
                # if found, create token and continue processing next char.
                if char == '(':
                    self.toklist.create(503, 11, self.line_num, self.line_ndx + 1, char)
                    continue

                elif char == ')':
                    self.toklist.create(503, 12, self.line_num, self.line_ndx + 1, char)
                    continue

                elif char == '{':
                    self.toklist.create(503, 13, self.line_num, self.line_ndx + 1, char)
                    continue

                elif char == '}':
                    self.toklist.create(503, 14, self.line_num, self.line_ndx + 1, char)
                    continue

                # '!' char could be not operator or first char of not-equal operator.
                # so we look ahead at next char to determine.
                elif char == '!':
                    # determine if we have not-equal operator by looking ahead to next char
                    # and checking if it is a '=' character.
                    if self.line[self.line_ndx + 1] == '=':
                        self.toklist.create(503, 31, self.line_num, self.line_ndx + 1, '!=')
                        # advance col_num past 2nd char of '!=' operator. so that next iteration of char 
                        # processing loop is looking at the correct char.
                        self.line_ndx += 1
                        continue
                    else:
                        self.toklist.create(503, 17, self.line_num, self.line_ndx + 1, char)
                        continue

                elif char == '&':
                    self.toklist.create(503, 18, self.line_num, self.line_ndx + 1, char)
                    continue

                elif char == '*':
                    self.toklist.create(503, 21, self.line_num, self.line_ndx + 1, char)
                    continue

                elif char == '-':
                    self.toklist.create(503, 20, self.line_num, self.line_ndx + 1, char)
                    continue

                elif char == '+':
                    self.toklist.create(503, 19, self.line_num, self.line_ndx + 1, char)
                    continue

                elif char == '%':
                    self.toklist.create(503, 23, self.line_num, self.line_ndx + 1, char)
                    continue

                elif char == "/":
                    self.toklist.create(503, 22, self.line_num, self.line_ndx + 1, char)
                    continue

                elif char == '=':
                    # determine if we have equal operator by looking ahead to next char
                    # and checking if it is a '=' character.
                    if self.line[self.line_ndx + 1] == '=':
                        self.toklist.create(503, 30, self.line_num, self.line_ndx + 1, '==')
                        # advance col_num past 2nd char of '==' operator. so that next iteration of char 
                        # processing loop is looking at the correct char.
                        self.line_ndx += 1
                        continue
                    else:
                        self.toklist.create(503, 24, self.line_num, self.line_ndx + 1, char)
                        continue

                elif char == '<':
                    # determine if we have less-than-or-equal operator by looking ahead to next char
                    # and checking if it is a '=' character.
                    if self.line[self.line_ndx + 1] == '=':
                        self.toklist.create(503, 32, self.line_num, self.line_ndx + 1, '<=')
                        # advance col_num past 2nd char of '<=' operator. so that next iteration of char 
                        # processing loop is looking at the correct char.
                        self.line_ndx += 1
                        continue
                    else:
                        self.toklist.create(503, 27, self.line_num, self.line_ndx + 1, char)
                        continue

                elif char == '>':
                    # determine if we have greater-than-or-equal operator by looking ahead to next char
                    # and checking if it is a '=' character.
                    if self.line[self.line_ndx + 1] == '=':
                        self.toklist.create(503, 33, self.line_num, self.line_ndx + 1, '>=')
                        # advance col_num past 2nd char of '>=' operator. so that next iteration of char 
                        # processing loop is looking at the correct char.
                        self.line_ndx += 1
                        continue
                    else:
                        self.toklist.create(503, 28, self.line_num, self.line_ndx + 1, char)
                        continue

                elif char == '[':
                    self.toklist.create(503, 15, self.line_num, self.line_ndx + 1, char)
                    continue

                elif char == ']':
                    self.toklist.create(503, 16, self.line_num, self.line_ndx + 1, char)
                    continue

                elif char == ',':
                    self.toklist.create(503, 29, self.line_num, self.line_ndx + 1, char)
                    continue

                # handle identifiers & keywords, check if char is valid starting character.
                if self.valid_id_char(char):
                    # we have valid start to our identifier or keyword so lets build the string.
                    str_start_col = self.line_ndx + 1
                    string = char

                    # check if string is only one char long, no need to enter string building loop below.
                    if self.next_char_is_delim():
                        self.toklist.create(501, 501, self.line_num, str_start_col, string)
                        continue # continue next iteration of char processing loop.
                    
                    # string building loop.
                    while True:
                        self.line_ndx += 1
                        char = self.line[self.line_ndx]

                        # check if char is identifier delimiter of some kind.
                        # if so break out of string building loop and tokenize it.
                        if self.next_char_is_delim():
                            string += char
                            break

                        # check if char is valid identifer char then add to string
                        if self.valid_id_char(char):
                            string += char
                        else:
                            print('invalid identifier char [%s] on line: %d col: %d' % (char, self.line_num, self.line_ndx + 1))
                            #raise Exception(s)

                    # confirm the string is valid identifier or keyword before tokenization.
                    # check if it exceeds the maximum identifier length.
                    if len(string) > self.ID_MAXLEN:
                        raise Exception('invalid identifier [%s] exceeds maximum length on line: %d col: %d' % (string, self.line_num, self.line_ndx + 1))

                    # is the string a keyword?
                    if string in keyword_list.keys():
                        self.toklist.create(500, keyword_list[string], self.line_num, str_start_col, string)
                        continue

                    # string is valid identifier, tokenize it. then
                    # continue processing next char in line
                    self.toklist.create(501, 501, self.line_num, str_start_col, string)
                    continue

        file.close() # close .pys file we just tokenized.

        # append TOKEN_STREAM_END token to signify the end of the stream.
        # we add two of these tokens due to weirdness in the verifier design....
        self.toklist.create(999, 999, 0, 0, '') # 999: tokstream end type+subtype code.
        self.toklist.create(999, 999, 0, 0, '')

        # Tokenization complete.