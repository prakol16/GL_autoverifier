from enum import Enum
from dataclasses import dataclass
from typing import *

class GLFormula:
    pass


class Connectives(Enum):
    AND = 0
    OR = 1
    IMPLIES = 2

    def __str__(self):
        return ["⋀", "⋁", "⭢"][self.value]


@dataclass(frozen=True)
class Atom(GLFormula):
    ident: str

    def __str__(self):
        return self.ident

    def is_false(self) -> bool:
        return self.ident == "⊥"


@dataclass(frozen=True)
class Conjunction(GLFormula):
    conj: Connectives
    left: GLFormula
    right: GLFormula

    def __str__(self):
        return f'({self.left} {self.conj} {self.right})'

@dataclass(frozen=True)
class Not(GLFormula):
    f: GLFormula

    def __str__(self):
        return "¬" + str(self.f)

@dataclass(frozen=True)
class Box(GLFormula):
    f: GLFormula

    def __str__(self):
        return "☐" + str(self.f)


@dataclass(frozen=True)
class Diamond(GLFormula):
    f: GLFormula

    def __str__(self):
        return "♢" + str(self.f)


GLFalse: GLFormula = Atom("⊥")
GLTrue: GLFormula = Not(Atom("⊥"))

def And(left: GLFormula, right: GLFormula): return Conjunction(Connectives.AND, left, right)
def Or(left: GLFormula, right: GLFormula): return Conjunction(Connectives.OR, left, right)
def Implies(left: GLFormula, right: GLFormula): return Conjunction(Connectives.IMPLIES, left, right)

