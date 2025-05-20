class Imprimir:
    def __init__(self, expr): self.expr = expr

class Definicion:
    def __init__(self, nombre): self.nombre = nombre

class Asignacion:
    def __init__(self, nombre, expr): self.nombre = nombre; self.expr = expr

class Mientras:
    def __init__(self, condicion, cuerpo): self.cond = condicion; self.cuerpo = cuerpo

class If:
    def __init__(self, condicion, cuerpo): self.cond = condicion; self.cuerpo = cuerpo

class IfElse:
    def __init__(self, condicion, cuerpo_if, cuerpo_else):
        self.cond = condicion; self.cuerpo_if = cuerpo_if; self.cuerpo_else = cuerpo_else
