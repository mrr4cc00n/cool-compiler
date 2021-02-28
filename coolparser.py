import coolex
from cooltrees import *
from ply import *

tokens = coolex.tokens
a=" "
start = 'program'

def p_empty(p):
    '''empty : '''
def p_constant(p):
	'''constant : INTEGER
			 | STRING
			 | ID
			 | TRUE
			 | FALSE'''
	p[0]=p[1]


def p_letc(p):
	'''letc : let params in expression'''
	p[0] = Tree("letc",(p[2],p[4]))

def p_ifc(p):
	'''ifc : if expression then expression elsec fi'''
	p[0] = Tree("ifc",(p[2],p[4],p[5]))

def p_whilec(p):
	'''whilec : while expression loop expression pool'''
	p[0] = Tree("whilec",(p[2],p[4]))

def p_elsec(p):
	'''elsec : else expression
			 | empty'''
	if len(p)==2:
		p[0]=None
	else:
		p[0]=p[1]

def p_newc(p):
	'''newc : new ID'''
	p[0]=Tree("NEW",leaf = p[2])

def p_callmethods(p):
	'''callmethods : whocalls POINT ID LPAREN paramsexpr RPAREN
				   | ID LPAREN paramsexpr RPAREN'''
	if len(p) == 5:
		p[0] = Tree("CALL",(p[3]),p[1])
	else:
		p[0] = Tree("CALL",(p[1],p[5]),p[3])

def p_paramsexpr(p):
	'''paramsexpr : expression nextparamexpr
				  | empty'''
	if len(p) == 2:
		p[0] = None
	else:
		p[0] = []
		p[0].append(p[1])
		p[0].append(p[2])

def p_nextparamexpr(p):
	'''nextparamexpr : COMMA paramsexpr 
	    			 | empty'''
	if len(p) == 2:
		p[0] = None
	else:
		p[0] = p[2]

def p_whocalls(p):
	'''whocalls : LPAREN expression RPAREN
				| father'''#revisar con el pinki a ver sto bien q se me olvido como funcionaba
	if len(p) == 2:
		p[0] = Tree("WHOCALLS",(p[1]))
	else:
		p[0]=Tree("WHOCALLS",(p[2]))

def p_father(p):
	'''father : ARROBA ID
			  | empty'''#aqui falta revisar si el @ es obligatorio

	if len(p) == 2:
		p[0]=None
	else:
		p[0] = Tree("IM YOUR FATHER",p[2])

def p_isvoidc(p):
	'''isvoidc : isvoid expression'''
	p[0] = p[2]

def p_casec(p):
	'''casec : case expression of caseparams esac'''
	p[0] = Tree("CASE",(p[2],p[4]))

def p_caseparams(p):
	'''caseparams : casebranch NEWLINE nextcasebranch'''
	p[0] = Tree("CASEPARAMS",(p[1],p[3]))

def p_casebranch(p):
	'''casebranch : ID TWOPOINTS ID ASS expression
				  | empty'''
	if len(p) == 2:
		p[0] = None
	else:
		p[0]= (p[1],p[3],p[5])

def p_nextcasebranch(p):
	'''nextcasebranch : caseparams
					  | empty'''
	if len(p) == 2:
		p[0] = None
	else:
		p[0] = p[1]

def p_aritmethicexp(p):
	'''aritmethicexp : highpriority PLUS aritmethicexp
					 | highpriority MINUS aritmethicexp
					 | COMPADOS aritmethicexp
					 | highpriority'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = Tree("binop",(p[1],p[3]),p[2])

def p_endpriority(p):
	'''endpriority : constant
				   | callmethods'''
	p[0] = p[1]

def p_highpriority(p):
	'''highpriority : endpriority TIMES highpriority
					| endpriority DIVIDE highpriority
					| endpriority
					| LPAREN expression RPAREN'''
	if len(p) == 2:
		p[0] = p[1]
	elif (p[2] == 'TIMES' | p[2] == 'DIVIDE'):
		p[0]=Tree("binop",(p[1],p[3]),p[2])
	else:
		p[0] = p[2]

def p_logicalexp(p):
	'''logicalexp : aritmethicexp LT logicalexp
				  | aritmethicexp LE logicalexp
				  | aritmethicexp GT logicalexp
				  | aritmethicexp GE logicalexp
				  | aritmethicexp EQUALS logicalexp
				  | aritmethicexp ISNE logicalexp
				  | aritmethicexp'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = Tree("LOGIC",(p[1],p[3]),p[2])
				

def p_expression(p):
	'''expression : letc
                  | ifc
                  | whilec
                  | newc
                  | isvoidc
                  | casec
                  | logicalexp
                  | block'''
	p[0]=Tree("EXP",(p[1]))

def p_block(p):
	'''block : LKEY nextexpression RKEY'''
	p[0] = p[2]
	
def p_nextexpression(p):
	'''nextexpression : expression SEMI nextexpression 
					  | empty'''
	if len(p) == 2:
		p[0]=None
	else:
		p[0] = []
		p[0].append(p[1])
		p[0].append(p[3])

def p_nextparam(p):
	'''nextparam : COMMA params 
				 | empty'''
	if len(p) == 2:
		p[0]=None
	else:
		p[0] = p[2]

def p_params(p):
	'''params : assignement nextparam 
			  | empty'''
	if len(p)==2:
		p[0]=None
	else:
		p[0]=[]
		p[0].append(p[1])
		p[0].append(p[2])

def p_method(p):
	'''method : ID LPAREN params RPAREN TWOPOINTS ID block'''
	p[0]=Tree("METHOD",(p[3],p[7]),(p[1],p[6]))

def p_value(p):
	'''value : ASS expression
			 | empty'''
	if len(p) == 2:
		p[0]=None
	else:
		p[0]=p[2]

def p_assignement(p):
	'''assignement : ID TWOPOINTS ID value 
				   | ID ASS expression'''
	if len(p)==5:		
		p[0] = Tree("ASSIGNEMENT",(p[4]),(p[1],p[3]))
	else:
		p[0] = Tree("ASSIGNEMENT",(p[3]),p[1])

def p_body(p):
	'''body : assignement SEMI body 
			| method body 
			| empty'''
	if len(p) == 3:
		p[0] = Tree("BODY",(p[1],p[2]))
	elif len(p) == 4:
		p[0] = Tree("BODY",(p[1],p[3]))
	elif len(p)==2:
		p[0]=None

def p_inheritc(p):
	'''inheritc : inherits ID 
			   | empty'''
	if len(p)==2:
		p[0]=None
	else:
		p[0] = Tree("INHERITS",p[2])

def p_claxes(p):
	'''claxes : clax claxes 
			  | empty'''
	if len(p) == 2:
		p[0]=None
	else:
		p[0]=Tree("LIST",(p[1],p[2]))

def p_clax(p):
	'''clax : class ID inheritc LKEY body RKEY '''
	p[0] = Tree("CLASS",(p[5]),(p[2],p[3]))

def p_program(p):
	'''program : clax claxes'''
	p[0] = Tree("PROGRAM",(p[1],p[2]))

def p_error(p):
    if not p:
        print("SYNTAX ERROR AT EOF")

cparser = yacc.yacc(start='program')

def parse(data, debug=0):
    cparser.error = 0
    p = cparser.parse(data, debug=1)
    if cparser.error:
        return None
    return p

b=parse("class main{a : MANUEL; H(a:MA,b:N):YI { let X:N,f:T in O-F; } } class A inherits B{}")
