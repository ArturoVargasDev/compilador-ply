import sys
from lexer import lexer
from parser import parser, parse

def analizar_codigo(archivo_path):
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            entrada = f.read()
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo '{archivo_path}'")
        return

    print("🔍 Iniciando análisis léxico y sintáctico...\n")
    
    # Análisis léxico
    lexer.input(entrada)
    lexer.lexdata = entrada  # para calcular columnas correctamente

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"{tok.type} -> '{tok.value}' (línea {tok.lineno}, columna {tok.lexpos - entrada.rfind(chr(10), 0, tok.lexpos)})")

    print("\n✅ Análisis léxico finalizado.\n")

    # Análisis sintáctico
    try:
        resultado = parse(entrada)
        if resultado is not None:
            print("✅ Análisis sintáctico finalizado sin errores.")
    except Exception as e:
        print(f"❌ Error sintáctico detectado: {e}")

if __name__ == "__main__":
    archivo = sys.argv[1] if len(sys.argv) > 1 else r"tests\test-1.txt"
    analizar_codigo(archivo)
