# main.py

from gramatica import lexer  
import sys

def analizar_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo '{nombre_archivo}'")
        return

    lexer.input(codigo) 
    errores = False

    print("=== TOKENS ENCONTRADOS ===")
    while True:
        token = lexer.token()
        if not token:
            break
        print(f"{token.type} -> '{token.value}' (línea {token.lineno})")

    if errores:
        print("\n❌ Se encontraron errores léxicos.")
    else:
        print("\n✅ Análisis léxico completado sin errores.")

if __name__ == "__main__":
    analizar_archivo("entrada.txt")
