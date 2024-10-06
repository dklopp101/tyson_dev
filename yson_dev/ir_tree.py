from collections import deque
from copy import deepcopy, copy
from parser import *

# NOTE: within this file 'cnfrm' is used as an abbreviation for 'confirm'.

# Source file is parsed into token objects which are turned into an ast.
# Ast is a list stmt & expr node objects with their own children nodes,
# which in turn can have their own children, and so on.

# expr nodes are operations, identifiers & integers. unary operations
# have the left node as operand, binary have left and right expr nodes.
# expr l/r nodes can be any expr, subcalls l_operand is subid, args are
# in exprnode args.

# operator precedence dict used by ast generator.
# key: operator-code, value: precedence number, lower the number: higher the precedence.
op_precedence2 = {
    11 :   1, # '('  
    12 :   1, # ')'  
    13 : 100, # '{'
    14 : 100, # '}'  
    15 :   1, # '['
    16 :   1, # ']'
    17 :   2, # '!'  
    18 :   2, # '&' 
    19 :   4, # '+'
    20 :   4, # '-'
    21 :   3, # '*'
    22 :   3, # '/'
    23 :   3, # '%'
    24 :  50, # '='
    27 :   6, # '<'
    28 :   6, # '>'
    29 :  55, # ','
    30 :   7, # '==' 
    31 :   7, # '!=' 
    32 :   6, # '<='
    33 :   6, # '>=' 
}

op_precedence = {
    11 :   1000, # '('  
    12 :   1000, # ')'  
    15 :   1000, # '['
    16 :   1000, # ']'
    17 :    900, # '!'  
    18 :    900, # '&' 
    19 :    700, # '+'
    20 :    700, # '-'
    21 :    800, # '*'
    22 :    800, # '/'
    23 :    800, # '%'
    24 :     20, # '='
    27 :    600, # '<'
    28 :    600, # '>'
    29 :     20, # ','
    30 :    500, # '==' 
    31 :    500, # '!=' 
    32 :    600, # '<='
    33 :    600, # '>=' 
}


stmt_list = {
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

expr_list = {
    'operation'  :  2000,
    'integer'    :  2001,
    'identifier' :  2002,
    'subcall'    :  2003
}

class ExprNode:
    def __init__(self, _type):
        self.type     = _type
        self.op       = None
        self.oprcount = None
        self.l_oprnd  = None
        self.r_oprnd  = None
        self.val      = None # used by int & id exprs.
        self.args     = None

    def __str__(self):
        if self.type == 2000:
            s = 'OpNode<%s>' % token_mnemonic[self.op]

            if self.l_oprnd:
                s += self.l_oprnd.__str__()

            if self.r_oprnd:
                s += self.r_oprnd.__str__()

        elif self.type == 2001:
            s = 'IntNode\nValue: <%d>' % self.val

        elif self.type == 2002:
            s = 'IDNode\nValue: <%s>' % self.val

        elif self.type == 2003:
            s = 'SubCNode<%s>' % self.val

            for arg in self.args:
                s += arg.__str__()

        return s

class StmtNode:
    def __init__(self, _type):
        self.type     = _type
        self.id       = None
        self.expr     = None # used for if/elif/else/while test.
        self.args     = deque() # used by subdef stmt nodes.
        self.body     = deque()
        self.children = deque() # used for elif/else

    def __str__(self):
        s = ''

        if self.type == 100:
            s += 'ConstDefStmtNode\nID: <%s>' % self.id.__str__()
            s += 'Expr: \n%s' % self.expr.__str__()

        elif self.type == 1:
            s += 'VarStmtNode\nID: <%s>' % self.id.__str__()
            s += 'Expr: \n%s' % self.expr.__str__()

        elif self.type == 2:
            s += 'SubDefNode\nID: <%s>' % self.id.__str__()
            s += 'Args: \n'

            for arg in self.args:
                s += arg.__str__()

            for node in self.body:
                s += node.__str__()

        elif self.type == 3:
            s += 'IfStmtNode\n'
            s += 'TestExpr: %s' % self.expr.__str__()

            for node in self.body:
                s += node.__str__()

            if self.children:

                for child in self.children:
                    s += child.__str__()

        elif self.type == 4:
            s += 'ElifStmtNode\n'
            s += 'TestExpr: %s' % self.expr.__str__()

            for node in self.body:
                s += node.__str__()

            if self.children:

                for child in self.children:
                    s += child.__str__()

        elif self.type == 5:
            s += 'ElseStmtNode\n'

            for node in self.body:
                s += node.__str__()

        elif self.type == 6:
            s += 'WhileStmtNode\n'
            s += 'TestExpr: %s' % self.expr.__str__()

            for node in self.body:
                s += node.__str__()

        elif self.type == 7:
            s += 'ReturnStmtNode\n'
            s += 'Expr: %s' % self.expr.__str__()

        elif self.type == 8:
            s += 'PrintStmtNode\n'
            s += 'Expr: %s' % self.expr.__str__()

        elif self.type == 9:
            s += 'ContinueStmtNode\n'
            s += 'Expr: %s' % self.expr.__str__()

        elif self.type == 10:
            s += 'BreakStmtNode\n'
            s += 'Expr: %s' % self.expr.__str__()

        return s

class AstGenerator:
# self.globlist = deque() = main list of global node objects.
# self.op_stack = deque() = operator stack used for processing exprs.
# self.opr_stack = deque() = operand stack used for processing exprs.
# self.curr_globnode_ndx = -1 = index of current global node.
# self.curr_body_ndx = -1 = index of current node inside a body list.
# self.curr_node = None = current node being processed.
# self.curr_node_ndx = -1 = 
# self.in_operation = False
# self.in_subdef = False
# self.tokndx = -1 = index of current token.
# self.toklist = list of token objects returned from parser tokenizer.

    def __init__(self):
        self.globlist = deque()
        self.op_stack = deque()
        self.opr_stack = deque()

        self.curr_globnode_ndx = -1
        self.curr_node_ndx = -1
        self.curr_body_ndx = -1
        self.curr_node = None
        self.curr_parent_node = None
        self.parent_nodes = deque()
        self.expr_node_holder = None

        self.tokndx = -1
        self.toklist = None
        self.tok = None

        self.in_op = False
        self.in_expr = False
        self.in_subdef = False
        self.at_globlvl = False

    def build_toklist(self, input_file_path):
        # parse source file into token list.
        try:
            self.toklist  = lexer.tokenize(input_file_path)
        except Exception:
            print('exception thrown from parser.')

    def build_id_node(self, idstr):
        id_node = ExprNode(2002)
        id_node.val = idstr
        return deepcopy(id_node)

    def build_int_node(self, intval):
        int_node = ExprNode(2001)
        int_node.val = intval
        return deepcopy(int_node)

    def advance_tok(self):
        self.tokndx += 1
        self.tok = self.toklist[self.tokndx]

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
    
    def build_expr_node(self):
    # ARRAYS: arrays are represented by a [ op expr node, left node is identifier, right node is integer.

        expr_node = ExprNode()

        while True:
            self.advance_tok()

            # check for end of expr.
            if self.tok.line != self.toklist.list[self.tokndx - 1].line:
                break

            # left curly brace check &
            elif self.assert_curr_tok(503, 13) or  self.assert_curr_tok(999):
                break

            # if token is left paren, if so push onto operator stack.
            if self.assert_curr_tok(503, 11):
                self.op_stack.append(ExprNode(2000))
                self.op_stack[-1].op = 11
                continue

            # if right paren we will process the operator stack until reaching a l-paren.
            elif self.assert_curr_tok(503, 12):
                
                # until top of op stack isnt l-paren process op stack.
                while True:
                    if self.op_stack[-1].op == 11:
                        break
                
                    op_node_from_stack = self.op_stack.pop()

                    if self.opr_stack:
                        op_node_from_stack.r_oprnd = self.opr_stack.pop()
                    else:
                        raise Exception("operand missing in expr")
                    
                    if op_node_from_stack.opcount == 2:
                        if self.opr_stack:
                            op_node_from_stack.l_oprnd = self.opr_stack.pop()
                        else:
                            raise Exception("operand missing in expr")

                    self.opr_stack.append(copy(op_node_from_stack))
                
                continue                    

            #  Check for r-bracket, should never be one, if so is error.
            # elif self.assert_curr_tok(503, 16):
            #     raise Exception("misplaced r-bracket in expr.")

            # process operators. paren and bracket operators are caught in their above if stmts.s
            elif self.assert_curr_tok(503):
                # compare top of operator stack with tok operator see whos higher prec.

                # check if operator is r-bracket.
                if self.assert_curr_tok(503, 16):

                    # if so check if op on stack is l-bracket. if not we have a misplaced r-bracket.
                    if not self.op_stack or self.op_stack[-1].subtype != 15:
                        raise Exception("misplaced r-bracket")

                # check if operator stack empty, if so push token operator onto stack.
                if not self.op_stack:
                    self.op_stack.append(ExprNode())
                    self.op_stack[-1].op      = self.tok.subtype
                    self.op_stack[-1].opcount = operand_count_map[self.tok.subtype]
                    continue

                # see whos got the higher prec.
                tok_prec = op_precedence[self.tok.subtype]  # token.
                stk_prec = op_precedence[self.op_stack[-1].subtype] # operator on top of operator stack.

                # check if tok_prec is higher if so push tok operator onto operator stack.
                if tok_prec > stk_prec:
                    self.op_stack.append(self.tok)
                    continue

                # higher prec. op on stack so we must pop off the operator, make its node,
                # then we pop operand off stack, put it on right side of op node, pop off
                # the next operand and put on the left, then we push the op node onto opr stack.
                # then we can push the tok onto the operator stack.
 
                op_node_from_stack = self.op_stack.pop()

                if self.opr_stack:
                    op_node_from_stack.r_oprnd = self.opr_stack.pop()
                else:
                    raise Exception("operand missing in expr")
                
                if op_node_from_stack.opcount == 2:
                    if self.opr_stack:
                        op_node_from_stack.l_oprnd = self.opr_stack.pop()
                    else:
                        raise Exception("operand missing in expr")

                # now push op-node-from-stack onto operand stack.
                self.opr_stack.append(copy(op_node_from_stack))

                # make new op-node from token then push onto stack.
                self.op_stack.append(ExprNode(2000))
                self.op_stack[-1].op      = self.tok.subtype
                self.op_stack[-1].opcount = operand_count_map[self.tok.subtype]
                continue

            # check if tok is identifier.
            elif self.assert_curr_tok(501, 501):

                # check if we have a sub call.
                if self.is_subcall():
                    pass

                # no subcall so we push identifier onto operand stack.
                self.opr_stack.append(self.build_id_node(self.tok.rawstr))
                continue

            elif self.assert_curr_tok(502, 502):
                self.op_stack.append(self.build_int_node(self.tok.value))

         # expr tokens have been processed into operator and operand stacks.
         # now we will process them into nodes.
        while True:
            if not self.op_stack: break

            op_node_from_stack = self.op_stack.pop()

            if self.opr_stack:
                op_node_from_stack.r_oprnd = self.opr_stack.pop()
            else:
                raise Exception("operand missing in expr")
                
            if op_node_from_stack.opcount == 2:
                if self.opr_stack:
                    op_node_from_stack.l_oprnd = self.opr_stack.pop()
                else:
                    raise Exception("operand missing in expr")

            self.opr_stack.append(copy(op_node_from_stack))

        # expr node has been built.
        return expr_node   

    def proc_ret_stmt(self):
        # confirm we're within subdef before proceding.
        if not self.in_subdef:
            print('return stmt not in subdef')
            raise Exception

        ret_node = StmtNode(7) # 7: ret stmt type code.
        ret_node.expr = self.build_expr_node()
        self.curr_parent_node.body.append(deepcopy(ret_node))

    def proc_print_stmt(self):
        print_node = StmtNode(8) # 8: print stmt type code.
        print_node.expr = self.build_expr_node()
        self.curr_parent_node.body.append(deepcopy(print_node))

    def proc_var_assign(self, id_node):
        assign_node = ExprNode()
        assign_node.op = 24 # 24: assignment op type code.
        assign_node.l_oprnd = deepcopy(id_node)
        assign_node.r_oprnd = self.build_expr_node()

        if self.at_globlvl:
            self.globlist.append(deepcopy(assign_node))
        else:
            self.curr_parent_node.body.append(deepcopy(assign_node))


    def makenew_parent_node(self, new_parent_node):
        """ Takes reference to new-parent-node.
            Appends current parent node to child nodes stack.
            Sets new parent to self.curr_parent_node.
        """ 

        if self.curr_parent_node: # if no parent node nothing to append to child-nodes-stack.
            self.parent_nodes.append(self.curr_parent_node)
        self.curr_parent_node = new_parent_node

    def proc_if_stmt(self):
        if self.at_globlvl:
            self.globlist[-1].append(StmtNode(3))
            if_node = self.globlist[-1] # create a ref of if-node for convenience.
        else:
            self.curr_parent_node.body.append(StmtNode(3))
            if_node = self.curr_parent_node.body[-1] # create a ref of if-node for convenience.
            self.makenew_parent_node(if_node)

        # process the if stmt test. next token must be left parent token.
        self.advance_tok()
        self.assert_optok(11) # 11: lparen op type code.
        
        # left parent found, but we will take tokndx back one because
        # build_expr_node needs it as it's part of the expr.
        self.tokndx -= 1
        if_node.expr = deepcopy(self.build_expr_node())

        # confirm next tok is left-curly-brace
        self.advance_tok()
        self.assert_optok(13) # 13: lcurly brace op type code.

        # first check for simplest stuff, var assignments, simple stmts ect.
        if self.tok.type == 501: # 501: id tok type code.
            id_node = self.build_id_node(self.tok.rawstr)

            # tok was id, advance tok then check for assignment, inc or dec tokens.
            self.advance_tok()

            if self.tok.type == 503: # operator tok type code.
                # determine if assignment op or inc/dec op.
                if self.tok.subtype == 24: # assignment op type code.
                    self.proc_var_assign(id_node)

                elif self.tok.subtype == 34 or self.tok.subtype == 35: # 34/35: inc/dec type codes.
                    pass

        
    def proc_elif_stmt(self):
        pass

    def proc_else_stmt(self):
        pass

    def proc_while_stmt(self):
        pass

    def proc_const_dec(self):
        """ const dec: const stmt(id-expr, int-expr)
            const decs can only be integer literals.
            as oposed to var decs which can be int
            literals *or* an expression.
        """
        id_node = None
        int_node = None

        # confirm const dec is at global level.
        if not self.at_globlvl:
            print('const dec not at global level.')
            raise Exception         

        # confirm const dec isn't within an operator or expression.
        if self.in_expr:
            print('const dec within expression')
            raise Exception

        # confirm next token is an identifier if so make it's node.
        self.advance_tok()
        self.assert_toktype(501) # 501: identifier token
        
        id_node = self.build_id_node(self.tok.rawstr)

        # confirm next tok is an assignment op if so advance past it.
        self.advance_tok()
        self.assert_optok(24) # 24: assignment op type code.

        # confirm next tok is an integer tok if so make it's node.
        self.advance_tok()
        self.assert_toktype(502) # 501: int token
        int_node = self.build_int_node(self.tok.value)

        # everything's in order so create const node add to globlist.
        # const StmtNode, body has id node and int node in this order.
        self.globlist.append(StmtNode(100)) # 0- const type code.

        # [-1] index is top item of globist stack.
        self.globlist[-1].id = deepcopy(id_node)
        self.globlist[-1].expr = deepcopy(int_node)

        # const declaration complete.

    def proc_var_dec(self):
        """ var dec: var stmt(id-expr, expr)
            var dec's are same as const except they can be
            exprs instead of only int literals.
        """
        id_node = None
        expr_node = None

        # confirm var dec isn't within an operator or expression.
        if self.in_expr:
            print('var dec within expression')
            raise Exception

        # confirm next token is an identifier if so make it's node.
        self.advance_tok()
        self.assert_toktype(501) # 501: identifier token
        
        id_node = self.build_id_node(self.tok.rawstr)

        # confirm next tok is an assignment op if so advance past it.
        self.advance_tok()
        self.assert_optok(24) # 24: assignment op type code.

        # build var dec expr.
        expr_node = self.build_expr_node()

        # since vars can be declared locally, we check where to put the node.
        if self.at_globlvl:
            self.globlist[-1].append(StmtNode(1))
            if_node = self.globlist[-1] # create a ref of if-node for convenience.
        else:
            self.curr_parent_node.body.append(StmtNode(1))
            if_node = self.curr_parent_node.body[-1] # create a ref of if-node for convenience.
            self.makenew_parent_node(if_node)

        # [-1] index is top item of globist stack.
        self.globlist[-1].id = deepcopy(id_node)
        self.globlist[-1].expr = deepcopy(expr_node)
        
        # var declaration complete.



