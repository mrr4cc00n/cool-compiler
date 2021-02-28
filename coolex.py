from ply import *

keywords = ('class','inherits','let','if','while',
			'new', 'in', 'else', 'loop', 'then','fi',
			'pool', 'case','isvoid','of','esac',)
tokens = keywords+('EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LT', 'LE', 'GT', 'GE','ISNE',
    'COMMA', 'SEMI', 'INTEGER', 'STRING',
    'ID', 'NEWLINE','TRUE','FALSE','LKEY','RKEY','TWOPOINTS','ASS','POINT','COMPADOS','ARROBA')
t_ARROBA = r'@'
t_COMPADOS = r'~'
t_POINT=r'\.'#revisar si el punto se pone asi en las expr regulares
t_ASS=r'<-'
t_TWOPOINTS=r':'
t_LKEY=r'\{'
t_RKEY=r'\}'
t_EQUALS = r'='
t_PLUS=r'\+'
t_MINUS=r'\-'
t_TIMES=r'\*'
t_DIVIDE=r'/'
t_COMMA=r'\,'
t_SEMI=r';'
t_INTEGER = r'\d+'
t_STRING=r'\".*?\"'
t_TRUE=r'true'
t_FALSE=r'false'
t_LPAREN=r'\('
t_RPAREN=r'\)'
t_LT=r'<'
t_LE=r'<='
t_GT=r'>'
t_GE=r'>='
t_ISNE=r'!='
t_ignore = ' \t'

def t_ID(t):
	r'[a-zA-Z][a-zA-Z0-9]*'
	if t.value in keywords:
		t.type = t.value
	return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

lex.lex(debug=0)
		