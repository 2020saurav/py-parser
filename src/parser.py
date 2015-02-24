import yacc
import lexer # our lexer
tokens = lexer.tokens
from subprocess import call
import sys
import time

## NB: compound_stmt in single_input is followed by extra NEWLINE!
# file_input: (NEWLINE | stmt)* ENDMARKER

def p_program(p):
    """program : file_input ENDMARKER"""

def p_file_input(p):
    """file_input : file_input NEWLINE
                  | file_input stmt
                  | NEWLINE
                  | stmt"""

# stmt: simple_stmt | compound_stmt
def p_stmt_simple(p):
    """stmt : simple_stmt"""
    
def p_stmt_compound(p):
    """stmt : compound_stmt"""

# simple_stmt: small_stmt (';' small_stmt)* [';'] NEWLINE
def p_simple_stmt(p):
    """simple_stmt : small_stmts NEWLINE
                   | small_stmts SEMI NEWLINE"""

def p_small_stmts(p):
    """small_stmts : small_stmts SEMI small_stmt
                   | small_stmt"""

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

# expr_stmt: testlist (augassign (yield_expr|testlist) |
#                      ('=' (yield_expr|testlist))*)
# augassign: ('+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=' |
#             '<<=' | '>>=' | '**=' | '//=')
def p_expr_stmt(p):
    """expr_stmt : testlist EQUAL testlist
                 | testlist """

def p_flow_stmt(p):
    "flow_stmt : return_stmt"

def p_print_stmt(p):
	"print_stmt : PRINT test"

# return_stmt: 'return' [testlist]
def p_return_stmt(p):
    "return_stmt : RETURN testlist"

def p_pass_stmt(p):
	"pass_stmt : PASS"

def p_import_stmt(p): # extremely oversimplified. "from","dots","as" to be done
	"""import_stmt 	:	IMPORT NAME
	"""
def p_compound_stmt(p):
    """compound_stmt : if_stmt
    				 | for_stmt
    				 | while_stmt
                     | funcdef"""
def p_if_stmt(p):
	"""if_stmt 	:	IF test COLON suite elif_expr
				|	IF test COLON suite elif_expr ELSE COLON suite
	"""
def p_elif_expr(p):
	"""elif_expr 	:
					| ELIF test COLON suite elif_expr
	"""
def p_for_stmt(p): # not very sure if 'test' is correct TODO
	"""for_stmt :	FOR NAME IN test COLON suite
	"""

def p_while_stmt(p):
	"""while_stmt 	:	WHILE test COLON suite 
					|	WHILE test COLON suite ELSE COLON suite
	"""
def p_suite(p):
    """suite : simple_stmt
             | NEWLINE INDENT stmts DEDENT"""

def p_stmts(p):
    """stmts : stmts stmt
             | stmt"""
# funcdef: [decorators] 'def' NAME parameters ':' suite
# ignoring decorators
def p_funcdef(p):
    "funcdef : DEF NAME parameters COLON suite"
    
# parameters: '(' [varargslist] ')'
def p_parameters(p):
    """parameters : LPAREN RPAREN
                  | LPAREN varargslist RPAREN"""

# varargslist: (fpdef ['=' test] ',')* ('*' NAME [',' '**' NAME] | '**' NAME) | 
# highly simplified
def p_varargslist(p):
    """varargslist : varargslist COMMA NAME
                   | NAME"""

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

# power: atom trailer* ['**' factor]
# trailers enables function calls.  I only allow one level of calls
# so this is 'trailer'
def p_power(p):
    """power : atom
             | atom trailer"""

def p_atom_name(p):
    """atom : NAME"""

def p_atom_number(p):
    """atom : NUMBER
            | STRING"""

def p_atom_tuple(p):
    """atom : LPAREN testlist RPAREN"""

# trailer: '(' [arglist] ')' | '[' subscriptlist ']' | '.' NAME
def p_trailer(p):
    "trailer : LPAREN arglist RPAREN"

# testlist: test (',' test)* [',']
# Contains shift/reduce error
def p_testlist(p):
    """testlist : testlist_multi COMMA
                | testlist_multi """

def p_testlist_multi(p):
    """testlist_multi : testlist_multi COMMA test
                      | test"""

# test: or_test ['if' or_test 'else' test] | lambdef
#  as I don't support 'and', 'or', and 'not' this works down to 'comparison'
def p_test(p):
    "test : comparison"

# arglist: (argument ',')* (argument [',']| '*' test [',' '**' test] | '**' test)
# XXX INCOMPLETE: this doesn't allow the trailing comma
def p_arglist(p):
    """arglist : arglist COMMA argument
               | argument"""

# argument: test [gen_for] | test '=' test  # Really [keyword '='] test
def p_argument(p):
    "argument : test"

def p_error(p):
    raise SyntaxError(str(p))

class G1Parser(object):
	def __init__(self, mlexer=None):
		if mlexer is None:
			mlexer = lexer.G1Lexer()
		self.mlexer = mlexer
		self.parser = yacc.yacc(start="program", debug=True)
	def parse(self, code):
		self.mlexer.input(code)
		result = self.parser.parse(lexer = self.mlexer, debug=True)
		return result

if __name__=="__main__":
	z = G1Parser()
	data = open('../test/test1.py')
	sys.stderr = open('dump','w')
	root =  z.parse(data.read())
	sys.stderr.close()
	call(["python","converter.py"])
	call(["dot","-Tpng","dot.dot","-o","dot.png"])
