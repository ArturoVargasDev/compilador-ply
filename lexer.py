import sys

variables_declaradas = set()
_last_token_was_numero = False

error_lexico_ocurrido = False 
pila_delimitadores = []  

reservadas = {
    'numero' : 'NUMERO',
    'imprimir' : 'IMPRIMIR',
    'mientras' : 'MIENTRAS',
    'if' : 'IF',
    'else' : 'ELSE'
}

tokens  = [
    'PTCOMA',
    'LLAVIZQ',
    'LLAVDER',
    'PARIZQ',
    'PARDER',
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'CONCAT',
    'MENQUE',
    'MAYQUE',
    'IGUALQUE',
    'NIGUALQUE',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID',
] + list(reservadas.values())

t_PTCOMA    = r';'
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_CONCAT    = r'&'
t_IGUAL     = r'='
t_MAYQUE    = r'>'
t_MENQUE    = r'<'
t_IGUALQUE  = r'=='
t_NIGUALQUE = r'!='

def t_PARIZQ(t):
    r'\('
    col = t.lexpos - t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    pila_delimitadores.append(('(', t.lineno, col))
    return t

def t_PARDER(t):
    r'\)'
    col = t.lexpos - t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    if pila_delimitadores and pila_delimitadores[-1][0] == '(':
        pila_delimitadores.pop()
        return t
    else:
        print(f"❌ Error léxico: paréntesis de cierre sin apertura en la línea {t.lineno}, columna {col}")
        sys.exit(1)

def t_LLAVIZQ(t):
    r'\{'
    col = t.lexpos - t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    pila_delimitadores.append(('{', t.lineno, col))
    return t

def t_LLAVDER(t):
    r'\}'
    col = t.lexpos - t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    if pila_delimitadores and pila_delimitadores[-1][0] == '{':
        pila_delimitadores.pop()
        return t
    else:
        print(f"❌ Error léxico: llave de cierre sin apertura en la línea {t.lineno}, columna {col}")
        sys.exit(1)

def t_OPERADOR_INVALIDO(t):
    r'(=>|=<|==<|!=<|=>=|=<==?)'
    col = t.lexpos - t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    print(f"❌ Error léxico: operador no válido '{t.value}' en la línea {t.lineno}, columna {col}")
    t.lexer.skip(len(t.value))

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    global _last_token_was_numero, variables_declaradas
    col = t.lexpos - t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    valor_minuscula = t.value.lower()

    if valor_minuscula in reservadas:
        t.type = reservadas[valor_minuscula]
        _last_token_was_numero = (valor_minuscula == 'numero')
        return t

    elif _last_token_was_numero:
        variables_declaradas.add(t.value)
        _last_token_was_numero = False
        return t

    elif t.value in variables_declaradas:
        return t

    else:
        posibles = [pal for pal in reservadas if sum(a == b for a, b in zip(pal, valor_minuscula)) >= 3]
        if posibles:
            print(f"❌ Error léxico: palabra clave inválida '{t.value}' en la línea {t.lineno}, columna {col}")
        else:
            print(f"❌ Error léxico: identificador no declarado '{t.value}' en la línea {t.lineno}, columna {col}")
        return None

def t_CADENA(t):
    r'"([^"\n])*"?'
    if t.value.endswith('"'):
        t.value = t.value[1:-1]
        return t
    else:
        col = t.lexpos - t.lexer.lexdata.rfind('\n', 0, t.lexpos)
        print(f"❌ Error léxico: cadena sin cerrar en la línea {t.lineno}, columna {col}")
        sys.exit(1)


def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_COMENTARIO_SIMPLE(t):
    r'//.*\n'
    t.lexer.lineno += 1

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    col = t.lexpos - t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    print(f"❌ Error léxico: carácter ilegal '{t.value[0]}' en la línea {t.lineno}, columna {col}")
    sys.exit(1)


import ply.lex as lex
lexer = lex.lex()

def verificar_delimitadores_final():
    if pila_delimitadores:
        simbolo, linea, col = pila_delimitadores[0]
        tipo = "paréntesis" if simbolo == '(' else "llave"
        print(f"❌ Error léxico: falta cierre de {tipo} abierto en línea {linea}, columna {col}")
        sys.exit(1)
