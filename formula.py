from enum import Enum
from typing import *

class GLFormula:
    pass


class Connectives(Enum):
    AND = 0
    OR = 1
    IMPLIES = 2

    def __str__(self):
        return ["⋀", "⋁", "⭢"][self.value]


class Atom(GLFormula):
    def __init__(self, ident: str):
        self.ident = ident

    def __str__(self):
        return self.ident

    def is_false(self) -> bool:
        return self.ident == "⊥"

class Conjunction(GLFormula):
    def __init__(self, conj: Connectives, left: GLFormula, right: GLFormula):
        self.conj = conj
        self.left = left
        self.right = right

    def __str__(self):
        return f'({self.left} {self.conj} {self.right})'


def And(left: GLFormula, right: GLFormula): return Conjunction(Connectives.AND, left, right)
def Or(left: GLFormula, right: GLFormula): return Conjunction(Connectives.OR, left, right)
def Implies(left: GLFormula, right: GLFormula): return Conjunction(Connectives.IMPLIES, left, right)


class Not(GLFormula):
    def __init__(self, f: GLFormula):
        self.f = f

    def __str__(self):
        return "¬" + str(self.f)


class Box(GLFormula):
    def __init__(self, f: GLFormula):
        self.f = f

    def __str__(self):
        return "☐" + str(self.f)


class Diamond(GLFormula):
    def __init__(self, f: GLFormula):
        self.f = f

    def __str__(self):
        return "♢" + str(self.f)


GLFalse: GLFormula = Atom("⊥")
GLTrue: GLFormula = Not(Atom("⊥"))
