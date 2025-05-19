from gramatica import lexer
import json
import re  

# Función auxiliar

def calcular_columna(entrada, token):
    ultima_nueva_linea = entrada.rfind('\n', 0, token.lexpos)
    if ultima_nueva_linea < 0:
        ultima_nueva_linea = -1
    return token.lexpos - ultima_nueva_linea

# Función para verificar comentario no cerrado
def VERIFICADOR_COMENTARIO_NO_CERRADO(entrada):
    tokens = list(re.finditer(r'/\*|\*/', entrada))
    pila = []

    for token in tokens:
        tipo = token.group()
        if tipo == '/*':
            pila.append(token.start())
        elif tipo == '*/':
            if pila:
                pila.pop()

    if pila and not lexer.error_detected:
        for pos in pila:
            linea = entrada[:pos].count('\n') + 1
            print(f"❌ Error: comentario multilínea no cerrado detectado desde línea {linea}")
            lexer.error_detected = True  

# Función para detectar basura léxica después del punto y coma
def verificar_basura_despues_de_ptcoma(entrada):
    lineas = entrada.split('\n')
    for i, linea in enumerate(lineas, start=1):
        if ';' in linea:
            partes = linea.split(';')
            for idx in range(len(partes) - 1):
                resto = partes[idx + 1].strip()
                # Ignorar si resto es comentario simple o multilínea válido
                if resto:
                    if resto.startswith('//'):
                        continue
                    if resto.startswith('/*') and resto.endswith('*/'):
                        continue
                    # Si no es comentario, verificar tokens inválidos
                    tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', resto)
                    if tokens:
                        print(f"❌ Error: contenido inesperado después de ';' en línea {i}")
                        lexer.error_detected = True
                        return

# Leer entrada
with open(r"tests/entrada_grande.txt", "r", encoding="utf-8") as archivo:
    entrada = archivo.read()

# Inicializar el lexer
lexer.input(entrada)
lexer.error_detected = False

verificar_basura_despues_de_ptcoma(entrada)

# Lista para guardar tokens
tokens_reconocidos = []

# Escanear tokens
tokens_reconocidos = []

while True:
    if lexer.error_detected:
        break 
    tok = lexer.token()
    if not tok:
        break
    columna = calcular_columna(entrada, tok)
    tokens_reconocidos.append({
        "tipo": tok.type,
        "valor": tok.value,
        "linea": tok.lineno,
        "columna": columna
    })
# Mostrar tokens
for tok in tokens_reconocidos:
    print(f"{tok['tipo']:<12} Valor: {str(tok['valor']):<20} Línea: {tok['linea']} Columna: {tok['columna']}")

# Guardar tokens en JSON
with open("tokens.json", "w") as f:
    json.dump(tokens_reconocidos, f, indent=4)
