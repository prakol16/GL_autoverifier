from __future__ import annotations
import copy
from formula import *
from typing import *
from nnf import nnf
import itertools

DEBUG = False
DEBUG_DEPTH = 0

def any_none(ls: Iterable[Optional[bool]]) -> Optional[bool]:
    """Returns true if any of inputs are true, and none if any are none"""
    for x in ls:
        if x is None:
            return None
        if x:
            return True
    return False


def all_none(ls: Iterable[Optional[bool]]) -> Optional[bool]:
    """Returns true if all values are true, none if any are none"""
    for x in ls:
        if x is None:
            return None
        if not x:
            return False
    return True


class TableauNode:
    formulas: Dict[HeadSymbol, Set[GLFormula]]

    def add_formula(self, f: GLFormula):
        self.formulas[f.head].add(f)

    def contains_formula(self, f: GLFormula) -> bool:
        return f in self.formulas[f.head]

    def add_formulas(self, formulas: Set[GLFormula]):
        """Add a set of formulas by sorting by head symbol"""
        for f in formulas:
            self.add_formula(f)

    def __init__(self, formulas: Set[GLFormula]):
        self.formulas = {h: set() for h in HeadSymbol}
        # Get the formulas sorted by head node
        self.add_formulas(formulas)

    def expand_conjunctions(self):
        """Expand non-branching patterns i.e. conjunctions"""
        new_formulas = {}
        while self.formulas[HeadSymbol.AND]:
            f: Conjunction = self.formulas[HeadSymbol.AND].pop()
            self.add_formula(f.left)
            self.add_formula(f.right)

    def __str__(self):
        return ", ".join(str(f) for fs in self.formulas.values() for f in fs)

    def __copy__(self):
        node = TableauNode(set())
        node.formulas = {k: {f for f in v} for k, v in self.formulas.items()}
        return node

    def expand_disjunction(self) -> (TableauNode, TableauNode):
        """Expand a single disjunction"""
        disj: Conjunction = self.formulas[HeadSymbol.OR].pop()
        left = copy.copy(self)
        right = copy.copy(self)
        left.add_formula(disj.left)
        right.add_formula(disj.right)
        return left, right

    def expand_proposition(self) -> List[TableauNode]:
        """Apply all possible propositional rules;
        automatically close any that result in contradiction"""
        self.expand_conjunctions()
        if self.is_contradiction():
            return []
        if self.formulas[HeadSymbol.OR]:
            left, right = self.expand_disjunction()
            return left.expand_proposition() + right.expand_proposition()
        else:
            return [self]

    def expand_diamonds(self) -> Iterable[TableauNode]:
        """Expand diamonds"""
        if DEBUG:
            print("\t" * DEBUG_DEPTH + "Expanding diamonds in ", self)
        for f in self.formulas[HeadSymbol.DIAMOND]:
            new_node = TableauNode(set())
            new_node.formulas[HeadSymbol.BOX] = self.formulas[HeadSymbol.BOX].copy()
            for g in self.formulas[HeadSymbol.BOX]:
                new_node.add_formula(g.f)
            new_node.add_formula(f.f)
            new_node.add_formula(nnf(Box(Not(f.f))))
            if new_node.formulas != self.formulas:
                yield new_node

    def is_contradiction(self) -> bool:
        # Checks if there is an atom whose negation is also in the formula
        for f in self.formulas[HeadSymbol.ATOM]:
            if f.is_false() or Not(f) in self.formulas[HeadSymbol.NOT]:
                return True
        return False

    def is_closed(self, max_depth=2**32) -> Optional[bool]:
        global DEBUG_DEPTH
        if DEBUG:
            print("\t" * DEBUG_DEPTH + "Determining if", self, "is closed, depth", max_depth)
            DEBUG_DEPTH += 1
        children = self.expand_proposition()
        if DEBUG:
            print("\t" * DEBUG_DEPTH + "Num Children", len(children))

        res = None
        for depth in range(max_depth):
            res = all_none(any_none(c.is_closed(depth) for c in child.expand_diamonds()) for child in children)
            if res is not None:
                break

        DEBUG_DEPTH -= 1
        return res


def is_unsat(formulas: Iterable[GLFormula]) -> bool:
    """Decides whether a collection of formulas is inconsistent"""
    return TableauNode({nnf(f) for f in formulas}).is_closed()


def is_valid(hyp: Iterable[GLFormula], tgt: GLFormula) -> bool:
    """Decides whether hyp |- tgt"""
    fs: Iterable[GLFormula] = itertools.chain(hyp, [Not(tgt)])
    return is_unsat(fs)

def is_sat(formulas: Iterable[GLFormula]):
    """Decides whether a collection of formulas is satisfiable"""
    return not is_unsat(formulas)


if __name__ == "__main__":
    # ♢☐R, ♢¬R, R, ☐♢☐R, ☐♢¬R, ☐R
    # ♢(☐R or ☐R), ♢¬R, R, ☐♢☐R, ☐♢¬R, (☐R or ☐R)
    # (¬☐¬☐(¬A ⋁ A) ⭢ ♢☐¬☐A)

    # ☐(♢♢A ⋁ ☐☐¬A), ♢♢A, ♢A
    # ☐(♢♢A ⋁ ☐☐¬A), ♢A, ☐¬♢A, ♢♢A
    A = Atom("A")
    B = Atom("B")
    print(is_valid([Box(Implies(A, B)), Box(A)], Box(B)))
    # print(is_valid([], F))

# diamond(box(R)), box(diamond(box(R)))
