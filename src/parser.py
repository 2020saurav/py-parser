from compiler import ast
import yacc
import lexer # our lexer
tokens = lexer.tokens


# Helper function
def Assign(left, right):
    names = []
    if isinstance(left, ast.Name):
        # Single assignment on left
        return ast.Assign([ast.AssName(left.name, 'EQUAL')], right)
    elif isinstance(left, ast.Tuple):
        # List of things - make sure they are Name nodes
        names = []
        for child in left.getChildren():
            if not isinstance(child, ast.Name):
                raise SyntaxError("that assignment not supported")
            names.append(child.name)
        ass_list = [ast.AssName(name, 'EQUAL') for name in names]
        return ast.Assign([ast.AssTuple(ass_list)], right)
    else:
        raise SyntaxError("Can't do that yet")

# The grammar comments come from Python's Grammar/Grammar file

## NB: compound_stmt in single_input is followed by extra NEWLINE!
# file_input: (NEWLINE | stmt)* ENDMARKER
def p_program(p):
    """program : file_input ENDMARKER"""
    p[0] = ast.Stmt(p[1])
def p_file_input(p):
    """file_input : file_input NEWLINE
                  | file_input stmt
                  | NEWLINE
                  | stmt"""
    if isinstance(p[len(p)-1], basestring):
        if len(p) == 3:
            p[0] = p[1]
        else:
            p[0] = [] # p == 2 --> only a blank line
    else:
        if len(p) == 3:
            p[0] = p[1] + p[2]
        else:
            p[0] = p[1]
            


# stmt: simple_stmt | compound_stmt
def p_stmt_simple(p):
    """stmt : simple_stmt"""
    # simple_stmt is a list
    p[0] = p[1]
    
def p_stmt_compound(p):
    """stmt : compound_stmt"""
    p[0] = [p[1]]

# simple_stmt: small_stmt (';' small_stmt)* [';'] NEWLINE
def p_simple_stmt(p):
    """simple_stmt : small_stmts NEWLINE
                   | small_stmts SEMI NEWLINE"""
    p[0] = p[1]

def p_small_stmts(p):
    """small_stmts : small_stmts SEMI small_stmt
                   | small_stmt"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

# small_stmt: expr_stmt | print_stmt  | del_stmt | 
#			  pass_stmt | flow_stmt |assert_stmt |
#    import_stmt | global_stmt | exec_stmt 
def p_small_stmt(p):
    """small_stmt : flow_stmt
                  | expr_stmt
                  | print_stmt
                  | pass_stmt
                  | import_stmt
                 """
    p[0] = p[1]

# expr_stmt: testlist (augassign (yield_expr|testlist) |
#                      ('=' (yield_expr|testlist))*)
# augassign: ('+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=' |
#             '<<=' | '>>=' | '**=' | '//=')
def p_expr_stmt(p):
    """expr_stmt : testlist EQUAL testlist
                 | testlist """
    if len(p) == 2:
        # a list of expressions
        p[0] = ast.Discard(p[1])
    else:
        p[0] = Assign(p[1], p[3])

def p_flow_stmt(p):
    "flow_stmt : return_stmt"
    p[0] = p[1]

def p_print_stmt(p):
	"print_stmt : PRINT test"
	p[0] = ast.Printnl(p[2], None)

# return_stmt: 'return' [testlist]
def p_return_stmt(p):
    "return_stmt : RETURN testlist"
    p[0] = ast.Return(p[2])

def p_pass_stmt(p):
	"pass_stmt : PASS"
	p[0] = ast.Pass()

def p_import_stmt(p): # extremely oversimplified. "from","dots","as" to be done
	"""import_stmt 	:	IMPORT NAME
	"""
	p[0] = ast.Import(p[2])

def p_compound_stmt(p):
    """compound_stmt : if_stmt
    				 | for_stmt
    				 | while_stmt
                     | funcdef"""
    p[0] = p[1]

# def p_if_stmt(p):
#     'if_stmt : IF test COLON suite'
#     p[0] = ast.If([(p[2], p[4])], None)

def p_if_stmt(p):
	"""if_stmt 	:	IF test COLON suite elif_expr
				|	IF test COLON suite elif_expr ELSE COLON suite
	"""
	if len(p) == 6:
		p[0] = ast.IfExp(p[2], p[4], p[5])
	else:
		p[0] = ast.IfExp(p[2], p[4], [(p[5],p[8])])
def p_elif_expr(p):
	"""elif_expr 	:
					| ELIF test COLON suite elif_expr
	"""
	if(len(p)>2):
		p[0] = ast.IfExp(p[2], p[4], p[5])


def p_for_stmt(p): # not very sure if 'test' is correct TODO
	"""for_stmt :	FOR NAME IN test COLON suite
	"""
	p[0] = ast.For(p[2],p[4],p[6],None)

def p_while_stmt(p):
	"""while_stmt 	:	WHILE test COLON suite 
					|	WHILE test COLON suite ELSE COLON suite
	"""
	if(len(p)==5):
		p[0] = ast.While(p[2],p[4], None)
	else:
		p[0] = ast.While(p[2],p[4],p[7])


def p_suite(p):
    """suite : simple_stmt
             | NEWLINE INDENT stmts DEDENT"""
    if len(p) == 2:
        p[0] = ast.Stmt(p[1])
    else:
        p[0] = ast.Stmt(p[3])
    

def p_stmts(p):
    """stmts : stmts stmt
             | stmt"""
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]
# funcdef: [decorators] 'def' NAME parameters ':' suite
# ignoring decorators
def p_funcdef(p):
    "funcdef : DEF NAME parameters COLON suite"
    p[0] = ast.Function(None, p[2], tuple(p[3]), (), 0, None, p[5])
    
# parameters: '(' [varargslist] ')'
def p_parameters(p):
    """parameters : LPAREN RPAREN
                  | LPAREN varargslist RPAREN"""
    if len(p) == 3:
        p[0] = []
    else:
        p[0] = p[2]
    

# varargslist: (fpdef ['=' test] ',')* ('*' NAME [',' '**' NAME] | '**' NAME) | 
# highly simplified
def p_varargslist(p):
    """varargslist : varargslist COMMA NAME
                   | NAME"""
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = [p[1]]

## No using Python's approach because Ply supports precedence

# comparison: expr (comp_op expr)*
# arith_expr: term (('+'|'-') term)*
# term: factor (('*'|'/'|'%'|'//') factor)*
# factor: ('+'|'-'|'~') factor | power
# comp_op: '<'|'>'|'=='|'>='|'<='|'<>'|'!='|'in'|'not' 'in'|'is'|'is' 'not'

def make_lt_compare((left, right)):
    return ast.Compare(left, [('<', right),])
def make_gt_compare((left, right)):
    return ast.Compare(left, [('>', right),])
def make_eq_compare((left, right)):
    return ast.Compare(left, [('==', right),])


binary_ops = {
    "+": ast.Add,
    "-": ast.Sub,
    "*": ast.Mul,
    "/": ast.Div,
    "<": make_lt_compare,
    ">": make_gt_compare,
    "==": make_eq_compare,
}
unary_ops = {
    "+": ast.UnaryAdd,
    "-": ast.UnarySub,
    }
precedence = (
    ("left", "EQEQUAL", "GREATER", "LESS"),
    ("left", "PLUS", "MINUS"),
    ("left", "STAR", "SLASH"),
    )

def p_comparison(p):
    """comparison : comparison PLUS comparison
                  | comparison MINUS comparison
                  | comparison STAR comparison
                  | comparison SLASH comparison
                  | comparison LESS comparison
                  | comparison EQEQUAL comparison
                  | comparison GREATER comparison
                  | PLUS comparison
                  | MINUS comparison
                  | power"""
    if len(p) == 4:
        p[0] = binary_ops[p[2]]((p[1], p[3]))
    elif len(p) == 3:
        p[0] = unary_ops[p[1]](p[2])
    else:
        p[0] = p[1]
                  
# power: atom trailer* ['**' factor]
# trailers enables function calls.  I only allow one level of calls
# so this is 'trailer'
def p_power(p):
    """power : atom
             | atom trailer"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2][0] == "CALL":
            p[0] = ast.CallFunc(p[1], p[2][1], None, None)
        else:
            raise AssertionError("not implemented")

def p_atom_name(p):
    """atom : NAME"""
    p[0] = ast.Name(p[1])

def p_atom_number(p):
    """atom : NUMBER
            | STRING"""
    p[0] = ast.Const(p[1])

def p_atom_tuple(p):
    """atom : LPAREN testlist RPAREN"""
    p[0] = p[2]

# trailer: '(' [arglist] ')' | '[' subscriptlist ']' | '.' NAME
def p_trailer(p):
    "trailer : LPAREN arglist RPAREN"
    p[0] = ("CALL", p[2])

# testlist: test (',' test)* [',']
# Contains shift/reduce error
def p_testlist(p):
    """testlist : testlist_multi COMMA
                | testlist_multi """
    if len(p) == 2:
        p[0] = p[1]
    else:
        # May need to promote singleton to tuple
        if isinstance(p[1], list):
            p[0] = p[1]
        else:
            p[0] = [p[1]]
    # Convert into a tuple?
    if isinstance(p[0], list):
        p[0] = ast.Tuple(p[0])

def p_testlist_multi(p):
    """testlist_multi : testlist_multi COMMA test
                      | test"""
    if len(p) == 2:
        # singleton
        p[0] = p[1]
    else:
        if isinstance(p[1], list):
            p[0] = p[1] + [p[3]]
        else:
            # singleton -> tuple
            p[0] = [p[1], p[3]]


# test: or_test ['if' or_test 'else' test] | lambdef
#  as I don't support 'and', 'or', and 'not' this works down to 'comparison'
def p_test(p):
    "test : comparison"
    p[0] = p[1]
    


# arglist: (argument ',')* (argument [',']| '*' test [',' '**' test] | '**' test)
# XXX INCOMPLETE: this doesn't allow the trailing comma
def p_arglist(p):
    """arglist : arglist COMMA argument
               | argument"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

# argument: test [gen_for] | test '=' test  # Really [keyword '='] test
def p_argument(p):
    "argument : test"
    p[0] = p[1]

def p_error(p):
    print "Error",p
    #print "Error!", repr(p)
    # raise SyntaxError(p)


class G1Parser(object):
	def __init__(self, mlexer=None):
		if mlexer is None:
			mlexer = lexer.G1Lexer()
		self.mlexer = mlexer
		self.parser = yacc.yacc(start="program")
	def parse(self, code):
		self.mlexer.input(code)
		result = self.parser.parse(lexer = self.mlexer)
		return ast.Module(None, result)

z = G1Parser()
data = open('../test/test1.py')
# I dont know how to print content from this AST
t =  z.parse(data.read())
# print dir(t)
# print (t)
nodes = t.node.nodes
for node in nodes:
	print node
	print type(node)
	print ""