class ExpresionNumero:
    def __init__(self, valor): self.valor = valor

class ExpresionIdentificador:
    def __init__(self, nombre): self.nombre = nombre

class ExpresionBinaria:
    def __init__(self, izq, der, op): self.izq = izq; self.der = der; self.op = op

class ExpresionNegativo:
    def __init__(self, expr): self.expr = expr

class ExpresionCadenaNumerico:
    def __init__(self, expr): self.expr = expr

class ExpresionDobleComilla:
    def __init__(self, valor): self.valor = valor

class ExpresionConcatenar:
    def __init__(self, izq, der): self.izq = izq; self.der = der

class ExpresionLogica:
    def __init__(self, izq, der, op): self.izq = izq; self.der = der; self.op = op

class OPERACION_ARITMETICA:
    MAS = "+"
    MENOS = "-"
    POR = "*"
    DIVIDIDO = "/"

class OPERACION_LOGICA:
    MAYOR_QUE = ">"
    MENOR_QUE = "<"
    IGUAL = "=="
    DIFERENTE = "!="
