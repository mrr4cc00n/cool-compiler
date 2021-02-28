import ply.yacc as yacc

start = 'program'

literals = ['{','}','(',')',';',':','<','-',':',',']

class Tree:
    def __init__(self,type,children=None,leaf = None):
        self.type = type
        self.children=children
        self.leaf = leaf
    def __str__(self):
        if self.children is not None:
            for x in  self.children:
                print(x)
            print(self.leaf)                                        
        return self.type

def p_empty(p):
	"empty :"
	pass



def p_block(p):
	"block : '{' nextexpression '}'"
	p[0] = p[2]
	
def p_nextexpression(p):
	"nextexpression : expression ';' nextexpression | empty"
	if len(p) == 2:
		p[0]=p[1]
	else:
		p[0] = p[1]+" "+p[3]

def p_nextparam(p):
	"nextparam : ',' params | empty"
	if len(p) == 2:
		p[0]=p[1]
	else:
		p[0] = p[2]

def p_params(p):
	"params : assignement nextparam | empty"
	if len(p)==2:
		p[0]=p[1]
	else:
		p[0]=p[1]+" "+p[2]

def p_method(p):
	"method : uppername '(' params ')' ':' type block"
	p[0]=p[1]+ " "+p[3]+" "+p[6]+" "+p[7]

def p_value(p):
	"value : '<' '-' expression"
	p[0]=p[3]

def p_assignement(p):
	"assignement : lowername ':' type value | lowername '<' '-' expression"
	if p[2] == ':':		
		p[0] = p[1] + " " + p[3] + " "+p[4]
	else:
		p[0] = p[1] + " "+p[4]

def p_body(p):
	"body : assignement ; body | method body | empty"
	if p[2]==';':
		p[0] = p[1]+" "+p[3]
	elif p[1]=='method':
		p[0] = p[1]+" "+p[2]
	elif len(p)==2:
		p[0]=p[1]

def p_inherit(p):
	"inherit : inherits classname | empty"
	if len(p)==2:
		p[0]=p[1]
	else:
		p[0] = p[1]+" "+p[2]

def p_clax(p):
	"clax : class classname inherit '{' body '}' "
	p[0] = p[1]+ " " + p[2]+" " + p[3] +" "+ p[5]

def p_program(p):
	"program :clax claxes"
	p[0] = p[1]+" " + p[2]