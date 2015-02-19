import ourAST as ast
import yacc
import lexer # our lexer
tokens = lexer.tokens
	
def p_program(p):
	"""
		program  :  file_input_star ENDMARKER
	"""
	p[0] = p[1]

def p_file_input_star_1(p):
	"""
		file_input_star : NEWLINE
	"""
	pass

def p_file_input_star_2(p):
	"""
		file_input_star : stmt
	"""
	p[0] = ast.Program(stmts=p[1])

def p_file_input_star_3(p):
	"""
		file_input_star : file_input_star stmt
	"""
	p[0] = p[1].add(p[2])


def p_stmt_3(p):
	"""
		stmt : single_stmt 
	"""
	p[0] = ast.StmtList(p[1])

def p_stmt_4(p):
	"""
		stmt : compound_stmt
	"""
	p[0] = ast.StmtList(p[1])

def p_stmt_1(p):
	"""
		stmt	: stmt single_stmt
	"""
	p[0] = p[1].add(p[2])

def p_stmt_2(p):
	"""
		stmt	: stmt compound_stmt 
	"""
	p[0] = p[1].add(p[2])


def p_single_stmt_1(p):
	"""
		single_stmt	 : complex_stmt
	"""
	p[0] = p[1]

def p_single_stmt_2(p):
	"""
		single_stmt :	small_stmt NEWLINE
	"""
	p[0] = p[1]

def p_small_stmt_1(p):
	"""
		small_stmt : small_assign_stmt
	"""
	p[0] = p[1]

def p_small_stmt_2(p):
	"""
		small_stmt : trailer_item
	"""
	if not (p[1].v2 is not None and p[1].v2.ts[-1].op == '('):
		p_error("small_stmt is not func_call")
	else:
		p[0] = ast.Stmt('fcall',p[1])

def p_small_stmt_3(p):
	"""
		small_stmt : return_stmt
	"""
	p[0] = p[1]

def p_small_stmt_4(p):
	"""
		small_stmt : print_stmt
	"""
	p[0] = p[1]

def p_small_stmt_5(p):
	"""
		small_stmt : break_stmt
	"""
	p[0] = p[1]

def p_small_stmt_6(p):
	"""
		small_stmt : continue_stmt
	"""
	p[0] = p[1]

def p_return_stmt(p):
	"""
		return_stmt : RETURN small_expression
	"""
	p[0] = ast.Stmt('return',p[2])

def p_break_stmt(p):
	"""
		 break_stmt : BREAK
	"""
	p[0] = ast.Stmt('break')

def p_continue_stmt(p):
	"""
		continue_stmt : CONTINUE
	"""
	p[0] = ast.Stmt('continue')

def p_paramlist(p):
	"""
		paramlist : paramlist COMMA  param
	"""
	p[0] = p[1].add(p[3])

def p_paramlist_2(p):
	"""
		paramlist :  param
	"""
	p[0] = ast.ParamList(p[1])

def p_param_1(p):
	"""
		param   : NAME EQUAL constants
	"""
	p[0] = ast.Param('value',p[1],p[3])

def p_param_2(p):
	"""
		param : NAME 
	"""
	p[0] = ast.Param('default',p[1])

def p_param_3(p):
	"""
		param : constants
	"""
	p[0] = ast.Param('direct',p[1])

def p_callparamlist_1(p):
	"""
		callparamlist : callparamlist COMMA callparam
	"""
	p[0] = p[1].add(p[3])

def p_callparamlist_2(p):
	"""
		callparamlist :  callparam
	"""
	p[0] = ast.ParamList(p[1])

def p_callparam_1(p):
	"""
		callparam   : NAME EQUAL arith_expression
	"""
	p[0] = ast.Param('value',p[1],p[3])

def p_callparam_2(p):
	"""
		callparam : arith_expression
	"""
	p[0] = ast.Param('default',p[1])

def p_small_assign_stmt(p):
	"""
		small_assign_stmt : trailer_item EQUAL small_expression
	"""
	p[0] = ast.Stmt('assign',[p[1],p[3]])

def p_small_expression(p):
	"""
		small_expression : arith_expression 
	"""
	p[0] = p[1]

def p_complex_stmt(p):
	"""
		complex_stmt : trailer_item EQUAL complex_expression
	"""
	p[0] = ast.Stmt('classFunc',[p[1],p[3]])
	_scope_stack[-1]['type'] = p[3].type

def p_complex_expression_1(p):
	"""
		complex_expression : CLASS
							| DEF
	"""
	p[0] = p[1]

def p_namelist_1(p):
	"""
		namelist : namelist COMMA NAME
	"""
	p[0] = p[1].add(p[3])

def p_namelist_2(p):
	"""
		namelist : NAME
	"""
	p[0] = ast.NameList(p[1])

def p_arith_expression(p):
	"""
		arith_expression	: term PLUS term 
							| term MINUS term
							| term
	"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = ast.Arith(p[2],p[1],p[3])

def p_term(p):
	"""
		term : factor STAR factor
				| factor SLASH factor
				| factor
	"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = ast.Arith(p[2],p[1],p[3])

def p_factor_1(p):
	"""
		factor : trailer_item
	"""
	p[0] = p[1]

def p_factor_4(p):
	"""
		factor : LPAREN arith_expression RPAREN
	"""
	p[0] = ast.Arith(p[1],p[2])

def p_print_stmt(p):
	"""
		print_stmt : PRINT small_expression
	"""
	p[0] = ast.Stmt('print',p[2])

def p_constants(p):
	"""
		constants : NUMBER
					| STRING
	"""
	p[0] = ast.Const(p[1])

def p_compound_stmt(p):
	"""
		compound_stmt   : if_stmt
						| for_stmt
						| while_stmt
	"""
	p[0] = p[1]

def p_if_stmt_1(p):
	"""
		if_stmt : IF test COLON suite
	"""
	p[0] = ast.Stmt('if',[p[2],p[4]])

def p_if_stmt_2(p):
	""" 
		if_stmt : IF test COLON suite NEWLINE ELSE suite
	"""
	p[0] = ast.Stmt('ifelse',[p[2],p[4],p[7]])

def p_while_stmt(p):
	"""
		while_stmt : WHILE test COLON suite
	"""
	p[0] = ast.Stmt('while',[p[2],p[4]])

def p_for_stmt(p):
	""" 
		for_stmt : FOR NAME IN small_expression COLON suite
	"""
	p[0] = ast.Stmt('for',[p[2],p[4],p[6]])

def p_suite(p):
	"""
		suite : NEWLINE INDENT stmt DEDENT
	"""
	p[0] = ast.Suite(p[3])

def p_test(p):
	"""
		test : test_add AND test_add
				| test_add
	"""
	if len(p) == 2:
		p[0] = p[1]			
	else:
		p[0] = ast.Test('and',p[1],p[3])

def p_test_add(p):
	"""
		test_add : test_or OR test_or
				| test_or
	"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = ast.Test('or',p[1],p[3])

def p_test_or(p):
	"""
		test_or : test_not
				| test_factor
	"""
	p[0] = p[1]

def p_test_not(p):
	"""
		test_not : NOT test_factor
	"""
	p[0] = ast.Test('not',p[2])

def p_test_factor_1(p):
	"""
		test_factor : arith_expression cmp_op arith_expression
	"""
	p[0] = ast.Test(p[2],p[1],p[3])

def p_test_factor_2(p):
	"""
		test_factor : arith_expression
	"""
	p[0] = ast.Test('direct',p[1])

def p_cmp_op(p):
	"""
		cmp_op  : EQEQUAL 
				| NOTEQUAL 
				| LESSEQUAL 
				| GREATEREQUAL 
				| LESS 
				| GREATER
	"""
	p[0] = p[1]

def p_trailer_0(p):
	"""
		trailer : DOT NAME 
	"""
	p[0] = ast.Trailer('.',p[2])

def p_trailer_1(p):
	"""
		trailer : LSQB subscript RSQB
	"""
	p[0] = ast.Trailer('[',p[2])

def p_trailer_2(p):
	"""
		trailer : LPAREN RPAREN
	"""
	p[0] = ast.Trailer('(',None)

def p_trailer_3(p):
	"""
		trailer : LPAREN callparamlist RPAREN
	"""
	p[0] = ast.Trailer('(',p[2])

def p_trailer_star_1(p):
	"""
		trailer_star : trailer
	"""
	p[0] = ast.TrailerList(p[1])

def p_trailer_star_2(p):
	"""
		trailer_star : trailer_star trailer
	"""
	p[0] = p[1].add(p[2])

def p_trailer_item_1(p):
	"""
		trailer_item : atom
	"""
	p[0] = ast.Item('direct',p[1])

def p_trailer_item_2(p):
	"""
		trailer_item : atom trailer_star
	"""
	p[0] = ast.Item('trailer',p[1],p[2])

def p_atom_0(p):
	"""
		atom : AT NAME
	"""
	p[0] = ast.Atom('@',p[2])

def p_atom_1(p):
	"""
		atom : NAME
	"""
	p[0] = ast.Atom('name',p[1])

def p_atom_2(p):
	"""
		atom : constants
	"""
	p[0] = ast.Atom('constants',p[1])

def p_subscript(p):
	"""
		subscript : NUMBER 
	"""
	p[0] = ast.Const(p[1])

def p_empty(p):
	"""
		empty : 
	"""

def p_error(p):
	if p:
		print p
		# parse_error(
		# 	'before: %s' % p.value,
		# 	'')
	else:
		print p
		# parse_error('At end of input', '')
class G1Parser(object):
	def __init__(self, mlexer=None):
		if mlexer is None:
			mlexer = lexer.G1Lexer()
		self.mlexer = mlexer
		self.parser = yacc.yacc(start="program")
	def parse(self, code):
		self.mlexer.input(code)
		result = self.parser.parse(lexer = self.mlexer)
		return result

z = G1Parser()
data = open('../test/test1.py')
# I dont know how to print content from this AST
t =  z.parse(data.read())
# print dir(t)
p = (t.__class__.__name__)
print p
# print dir(t.stmts)
# print z.parse("a=4")
# print z.mlexer.input("a=4")

