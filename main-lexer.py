from lexer import lexer
import sys

def obtener_columna(input_text, token):
    ultima_linea = input_text.rfind('\n', 0, token.lexpos)
    if ultima_linea < 0:
        ultima_linea = -1
    return token.lexpos - ultima_linea

def analizar_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo '{nombre_archivo}'")
        return

    lexer.lineno = 1  
    lexer.input(codigo)
    lexer.lexdata = codigo  
    
    print("=== TOKENS ENCONTRADOS ===")
    
    while True:
        token = lexer.token()
        if not token:
            break
        columna = obtener_columna(codigo, token)
        print(f"{token.type} -> '{token.value}' (línea {token.lineno}, columna {columna})")

    from lexer import verificar_delimitadores_final
    verificar_delimitadores_final()
    
    print("\n✅ Análisis léxico completado.")

if __name__ == "__main__":
    analizar_archivo(r"compilador-ply\entrada.txt")
