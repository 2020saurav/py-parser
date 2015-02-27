import yacc
import lexer # our lexer
tokens = lexer.tokens
from subprocess import call
import sys


# file_input: (NEWLINE | stmt)* ENDMARKER
def p_file_input(p):
	"""file_input :	single_stmt ENDMARKER
	"""
# Our temporary symbol
def p_single_stmt(p):
	"""single_stmt	:	single_stmt NEWLINE
					|	single_stmt stmt
					|
	"""
# funcdef: [decorators] 'def' NAME parameters ':' suite
def p_funcdef(p):
    "funcdef : DEF NAME parameters COLON suite"


# parameters: '(' [varargslist] ')'
def p_parameters(p):
    """parameters : LPAREN RPAREN
                  | LPAREN varargslist RPAREN"""

#varargslist: ( | fpdef ['=' test] (',' fpdef ['=' test])* [',']) 

def p_varargslist(p):
    """varargslist 	:
    				| fpdef EQUAL test fpdeflist COMMA
    				| fpdef EQUAL test fpdeflist
    				| fpdef fpdeflist COMMA
    				| fpdef fpdeflist
    """

def p_fpdeflist(p):
	"""fpdeflist 	:
					| fpdeflist COMMA fpdef
					| fpdeflist COMMA fpdef EQUAL test
	"""

# fpdef: NAME | '(' fplist ')'
def p_fpdef(p):
	"""fpdef 	: NAME 
				| LPAREN fplist RPAREN
	"""

# fplist: fpdef (',' fpdef)* [',']
def p_fplist(p):
	"""fplist 	: fpdef fplist1 COMMA
				| fpdef fplist1	
	"""
# our temp symbol
def p_fplist1(p):
	"""fplist1 	:
				| fplist1 COMMA fpdef
	"""

# stmt: simple_stmt | compound_stmt
def p_stmt(p):
	"""stmt 	: simple_stmt
				| compound_stmt
	"""

# simple_stmt: small_stmt (';' small_stmt)* [';'] NEWLINE
def p_simple_stmt(p):
	"""simple_stmt 	: small_stmts NEWLINE
					| small_stmts SEMI NEWLINE
	"""

# our temp symbol
def p_small_stmts(p):
	"""small_stmts 	: small_stmts SEMI small_stmt
					| small_stmt
	"""

# small_stmt: 	expr_stmt 	| print_stmt   	| 
#			  	pass_stmt 	| flow_stmt 	|assert_stmt|
#    			import_stmt | global_stmt 	

def p_small_stmt(p):
	"""small_stmt 	: flow_stmt
					| expr_stmt
					| print_stmt
					| pass_stmt
					| import_stmt
					| global_stmt
					| assert_stmt
					"""

# expr_stmt: testlist (augassign testlist | ('=' testlist)*)
def p_expr_stmt(p):
	"""expr_stmt 	: testlist augassign testlist
					| testlist eqtestlist
	"""
# our new symbol
def p_eqtestlist(p):
	"""eqtestlist 	:
					| eqtestlist EQUAL testlist
	"""

# augassign: ('+=' | '-=' | '*=' | '/=' | '%=' | '**=' | '//=')
def p_augassign(p):
	"""augassign 	: PLUSEQUAL 
					| MINEQUAL 
					| STAREQUAL 
					| SLASHEQUAL 
					| PERCENTEQUAL 
					| STARSTAREQUAL 
					| SLASHSLASHEQUAL 
	"""

# print_stmt: 'print' [ test (',' test)* [','] ]
def p_print_stmt(p):
	"""print_stmt 	:	PRINT
					|	PRINT testlist
	"""

# pass_stmt: 'pass'
def p_pass_stmt(p):
	"pass_stmt : PASS"

# flow_stmt: break_stmt | continue_stmt | return_stmt 
def p_flow_stmt(p):
	"""flow_stmt 	: break_stmt
					| continue_stmt
					| return_stmt
	"""

# break_stmt: 'break'
def p_break_stmt(p):
	"""break_stmt 	: BREAK
	"""

# continue_stmt: 'continue'
def p_continue_stmt(p):
	"""continue_stmt 	: CONTINUE
	"""

# return_stmt: 'return' [testlist]
def p_return_stmt(p):
	"""return_stmt 	:	RETURN 
					|	RETURN testlist
	"""
# import_stmt: 'import' NAME ['as' NAME]
def p_import_stmt(p): 
	"""import_stmt 	:	IMPORT NAME
					|	IMPORT NAME AS NAME
	"""

# global_stmt: 'global' NAME (',' NAME)*
def p_global_stmt(p):
	"""global_stmt 	: GLOBAL NAME namelist
	"""
# our new symbol
def p_namelist(p):
	"""namelist 	: 
					| COMMA NAME namelist
	"""
# assert_stmt: 'assert' test [',' test]
def p_assert_stmt(p):
	"""assert_stmt 	: ASSERT testlist
	"""

# compound_stmt: if_stmt | while_stmt | for_stmt | funcdef | classdef 
def p_compound_stmt(p):
	"""compound_stmt 	: if_stmt
						| for_stmt
						| while_stmt
						| funcdef
						| classdef
	"""

# if_stmt: 'if' test ':' suite ('elif' test ':' suite)* ['else' ':' suite]
def p_if_stmt(p):
	"""if_stmt 	:	IF test COLON suite elif_list
				|	IF test COLON suite elif_list ELSE COLON suite
	"""
# our new symbol
def p_elif_list(p):
	"""elif_list 	:
					| ELIF test COLON suite elif_list
	"""

# while_stmt: 'while' test ':' suite ['else' ':' suite]
def p_while_stmt(p):
	"""while_stmt 	:	WHILE test COLON suite 
					|	WHILE test COLON suite ELSE COLON suite
	"""
# for_stmt: 'for' exprlist 'in' testlist ':' suite ['else' ':' suite]
def p_for_stmt(p): 
	"""for_stmt 	:	FOR exprlist IN testlist COLON suite
					|	FOR exprlist IN testlist COLON suite ELSE COLON suite
	"""

# suite: simple_stmt | NEWLINE INDENT stmt+ DEDENT
def p_suite(p):
	"""suite 	: simple_stmt
				| NEWLINE INDENT stmts DEDENT"""

# test: or_test ['if' or_test 'else' test]
def p_test(p):
	"""test 	: or_test
				| or_test IF or_test ELSE test
	"""

# or_test: and_test ('or' and_test)*
def p_or_test(p):
	"""or_test 	: and_test ortestlist
	"""

# our new symbol
def p_ortestlist(p):
	"""ortestlist 	:
					| OR and_test ortestlist
	"""

# and_test: not_test ('and' not_test)*
def p_and_test(p):
	"""and_test 	: not_test andtestlist
	"""

#our new symbol
def p_andtestlist(p):
	"""andtestlist 	:
					| AND not_test andtestlist
	"""

# not_test: 'not' not_test | comparison
def p_not_test(p):
	"""not_test 	: NOT not_test
					| comparison
	"""

# comparison: expr (comp_op expr)*
def p_comparision(p):
	"""comparison 	: expr compexprlist
	"""

# our new symbol
def p_compexprlist(p):
	"""compexprlist 	:
						| comp_op expr compexprlist
	"""

# comp_op: '<'|'>'|'=='|'>='|'<='|'!='|'in'|'not' 'in'|'is'|'is' 'not'
def p_comp_op(p):
	"""comp_op 	: LESS
				| GREATER
				| EQEQUAL
				| GREATEREQUAL
				| LESSEQUAL
				| NOTEQUAL
				| IN
				| NOT IN
				| IS
				| IS NOT
	"""

# expr: xor_expr ('|' xor_expr)*
def p_expr(p):
	"""expr 	: xor_expr xorexprlist
	"""

# our new symbol
def p_xorexprlist(p):
	"""xorexprlist 	:
					|	VBAR xor_expr xorexprlist
	"""

# xor_expr: and_expr ('^' and_expr)*
def p_xor_expr(p):
	"""xor_expr 	: and_expr andexprlist
	"""

# our new symbol
def p_andexprlist(p):
	"""andexprlist 	:
					| CIRCUMFLEX and_expr andexprlist
	"""

# and_expr: shift_expr ('&' shift_expr)*
def p_and_expr(p):
	"""and_expr 	: shift_expr shiftexprlist
	"""

# our new symbol
def p_shiftexprlist(p):
	"""shiftexprlist 	:
						| AMPER shift_expr shiftexprlist
	"""

# shift_expr: arith_expr (('<<'|'>>') arith_expr)*
def p_shift_expr(p):
	"""shift_expr 	: arith_expr arithexprlist
	"""

# our new symbol
def p_arithexprlist(p):
	"""arithexprlist 	:
						| LEFTSHIFT arith_expr arithexprlist
						| RIGHTSHIFT arith_expr arithexprlist
	"""

# arith_expr: term (('+'|'-') term)*
def p_arith_expr(p):
	"""arith_expr 	:	term termlist
	"""

# our new symbol
def p_termlist(p):
	"""termlist 	:
					| PLUS term termlist
					| MINUS term termlist
	"""

# term: factor (('*'|'/'|'%'|'//') factor)*
def p_term(p):
	"""term :	factor factorlist
	"""

# our new symbol
def p_factorlist(p):
	"""factorlist 	:
					| STAR factor factorlist
					| SLASH factor factorlist
					| PERCENT factor factorlist
					| SLASHSLASH factor factorlist
	"""

# factor: ('+'|'-'|'~') factor | power
def p_factor(p):
	"""factor 	: power
				| PLUS factor
				| MINUS factor
				| TILDE factor
	"""

# without lak:

# power: atom trailer* ['**' factor]
def p_power(p):
	"""power 	: atom trailerlist
				| atom trailerlist STARSTAR factor
	"""

# our new symbol
def p_trailerlist(p):
	"""trailerlist 	: 
					| trailer trailerlist
	"""

# atom: ('(' [testlist_comp] ')' |
#       '[' [listmaker] ']' |
#       '{' [dictorsetmaker] '}' |
#       '`' testlist1 '`' |
#       NAME | NUMBER | STRING+)
def p_atom(p):
	"""atom 	: LPAREN RPAREN
				| LPAREN testlist_comp RPAREN
				| LSQB RSQB
				| LSQB listmaker RSQB
				| LBRACE RBRACE
				| LBRACE dictorsetmaker RBRACE
				| BACKQUOTE testlist1
				| NAME
				| NUMBER
				| FNUMBER
				| stringlist
	"""

# our new symbol
def p_stringlist(p):
	"""stringlist 	: STRING 
					| STRING stringlist
					| TRIPLESTRING
					| TRIPLESTRING stringlist
	"""

# listmaker: test (',' test)* [','] 
def p_listmaker(p):
	"""listmaker 	: testlist
	"""

# testlist_comp: test (',' test)* [','] 
def p_testlist_comp(p):
	"""testlist_comp 	: testlist
	"""

# trailer: '(' [arglist] ')' | '[' subscriptlist ']' | '.' NAME
def p_trailer(p):
	"""trailer 	: LPAREN RPAREN
				| LPAREN arglist RPAREN
				| LSQB RSQB
				| LSQB subscriptlist RSQB
				| DOT NAME
	"""

# subscriptlist: subscript (',' subscript)* [',']
def p_subscriptlist(p):
	"""subscriptlist 	: subscript
						| subscript COMMA
						| subscript COMMA subscriptlist
	"""

# subscript: '.' '.' '.' | test | [test] ':' [test] [sliceop]
def p_subscript(p):
	"""subscript 	: DOT DOT DOT
					| test
					| test COLON test sliceop
					| COLON test sliceop
					| test COLON sliceop
					| test COLON test
					| test COLON
					| COLON test
					| COLON sliceop
					| COLON
	"""

# sliceop: ':' [test]
def p_sliceop(p):
	"""sliceop 	: COLON
				| COLON test
	"""

# exprlist: expr (',' expr)* [',']
def p_exprlist(p):
	"""exprlist 	: expr
					| expr COMMA
					| expr COMMA exprlist
	"""

# testlist: test (',' test)* [',']
def p_testlist(p):
	"""testlist 	: test
					| test COMMA
					| test COMMA testlist
	"""

# dictorsetmaker:  (test ':' test  (',' test ':' test)* [',']) 
#					| (test  (',' test)* [',']) 
def p_dictorsetmaker(p):
	"""dictorsetmaker 	: testcolonlist
						| testlist
	"""

# our new symbol
def p_testcolonlist(p):
	"""testcolonlist 	: test COLON test
						| test COLON test COMMA
						| test COLON test COMMA testcolonlist
	"""

# classdef: 'class' NAME ['(' [testlist] ')'] ':' suite
def p_classdef(p):
	"""classdef 	: CLASS NAME COLON suite
					| CLASS NAME LPAREN testlist RPAREN COLON suite
	"""

# arglist: (argument ',')* argument [',']
def p_arglist(p):
	"""arglist 	: argument
				| argument COMMA
				| argument COMMA arglist
	"""
# argument: test | test '=' test
def p_argument(p):
	"""argument 	: test
					| test EQUAL test
	"""
# testlist1: test (',' test)*
def p_testlist1(p):
	"""testlist1 	: test
					| test COMMA testlist1
	"""





# CORRECT UPTIL HERE ^

# these 2 below are added to run without error for now, replace with exact rules.





def p_stmts(p):
    """stmts : stmts stmt
             | stmt"""



def p_error(p):
    raise SyntaxError(str(p))

class G1Parser(object):
	def __init__(self, mlexer=None):
		if mlexer is None:
			mlexer = lexer.G1Lexer()
		self.mlexer = mlexer
		self.parser = yacc.yacc(start="file_input", debug=True)
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
