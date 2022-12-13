from __future__ import annotations
import copy
from formula import *
from typing import *
from nnf import nnf
from and_or_tree import Tree
import itertools

DEBUG = False


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
        for f in self.formulas[HeadSymbol.DIAMOND]:
            new_node = TableauNode(set())
            new_node.formulas[HeadSymbol.BOX] = self.formulas[HeadSymbol.BOX].copy()
            for g in self.formulas[HeadSymbol.BOX]:
                new_node.add_formula(g.f)
            new_node.add_formula(f.f)
            new_node.add_formula(nnf(Box(Not(f.f))))
            yield new_node

    def is_contradiction(self) -> bool:
        # Checks if there is an atom whose negation is also in the formula
        for f in self.formulas[HeadSymbol.ATOM]:
            if f.is_false() or Not(f) in self.formulas[HeadSymbol.NOT]:
                return True
        return False

    def is_closed(self, debug=DEBUG) -> bool:
        tree: Tree[TableauNode] = Tree(self,
            expand_and=lambda n: copy.copy(n).expand_proposition(),
            expand_or=lambda n: list(n.expand_diamonds()))
        return tree.search(debug)

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

    # ♢(♢♢A ⋁ ☐♢A)
    # (♢♢A ⋁ ☐♢A), ☐(¬♢♢A AND ¬☐♢A),
    # ♢♢A, ☐(☐☐¬A AND ♢☐¬A)
    #  - ♢A, ☐☐¬A, ♢☐¬A, ☐(☐☐¬A AND ♢☐¬A)
    #     - A,  ☐☐¬A, ☐¬A, (☐☐¬A AND ♢☐¬A),  ☐(☐☐¬A AND ♢☐¬A)
    #     - ☐¬A, ☐♢A, ☐☐¬A, ☐¬A, ☐(☐☐¬A AND ♢☐¬A), (☐☐¬A AND ♢☐¬A)
    # ☐♢A
    #  - ☐♢A, ☐(☐☐¬A AND ♢☐¬A)
    A = Atom("A")
    B = Atom("B")
    C = Atom("C")
    is_consistent = Diamond(GLTrue)
    f = Diamond(Or(Diamond(Diamond(Not(A))), Box(Diamond(Not(A)))))
    print(is_unsat([f]))

# diamond(box(R)), box(diamond(box(R)))
