from abc import abstractmethod
from enum import Enum
from dataclasses import dataclass
from functools import reduce, cached_property
from typing import List


class HeadSymbol(Enum):
    AND = 0
    OR = 1
    IMPLIES = 2
    NOT = 3
    BOX = 4
    DIAMOND = 5
    ATOM = 6


class GLFormula:
    _cached_nested_diamonds = None

    @property
    def head(self) -> HeadSymbol:
        pass

    @cached_property
    def nested_diamonds(self):
        """Determines how many times Diamons are nested in `f`"""
        if self.head == HeadSymbol.DIAMOND:
            return self.f.nested_diamonds + 1
        elif self.head == HeadSymbol.BOX or self.head == HeadSymbol.NOT:
            return self.f.nested_diamonds
        elif isinstance(self, Conjunction):
            return max(self.left.nested_diamonds, self.right.nested_diamonds)
        else:
            return 0


class Connectives(Enum):
    AND = 0
    OR = 1
    IMPLIES = 2

    def __str__(self):
        return ["⋀", "⋁", "⭢"][self.value]

    def to_head(self) -> HeadSymbol:
        return [HeadSymbol.AND, HeadSymbol.OR, HeadSymbol.IMPLIES][self.value]


@dataclass(frozen=True)
class Atom(GLFormula):
    ident: str

    def __str__(self):
        return self.ident

    def __repr__(self):
        return self.ident

    def is_false(self) -> bool:
        return self.ident == "⊥"

    @property
    def head(self) -> HeadSymbol:
        return HeadSymbol.ATOM


@dataclass(frozen=True)
class Conjunction(GLFormula):
    conj: Connectives
    left: GLFormula
    right: GLFormula

    def __str__(self):
        return f'({self.left} {self.conj} {self.right})'

    def __repr__(self):
        return f'{self.conj.name.title()}({repr(self.left)}, {repr(self.right)})'

    @property
    def head(self) -> HeadSymbol:
        return self.conj.to_head()


@dataclass(frozen=True)
class Not(GLFormula):
    f: GLFormula

    def __str__(self):
        return "¬" + str(self.f)

    def __repr__(self):
        return f'Not({repr(self.f)})'

    @property
    def head(self) -> HeadSymbol:
        return HeadSymbol.NOT


@dataclass(frozen=True)
class Box(GLFormula):
    f: GLFormula

    def __str__(self):
        return "☐" + str(self.f)

    def __repr__(self):
        return f'Box({repr(self.f)})'

    @property
    def head(self) -> HeadSymbol:
        return HeadSymbol.BOX


@dataclass(frozen=True)
class Diamond(GLFormula):
    f: GLFormula

    def __str__(self):
        return "♢" + str(self.f)

    def __repr__(self):
        return f'Diamond({repr(self.f)})'

    @property
    def head(self) -> HeadSymbol:
        return HeadSymbol.DIAMOND


GLFalse: GLFormula = Atom("⊥")
GLTrue: GLFormula = Not(Atom("⊥"))


def connect(conj: Connectives, fs: List[GLFormula]) -> GLFormula:
    return reduce(lambda x, y: Conjunction(conj, x, y), fs)
def And(*fs) -> GLFormula: return connect(Connectives.AND, fs)
def Or(*fs) -> GLFormula: return connect(Connectives.OR, fs)
def Implies(left: GLFormula, right: GLFormula): return Conjunction(Connectives.IMPLIES, left, right)
