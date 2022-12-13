from __future__ import annotations
import copy
from formula import *
from typing import *
from nnf import nnf
import itertools

DEBUG = False


class TableauNode:
    formulas: Dict[HeadSymbol, Set[GLFormula]]

    def add_formula(self, f: GLFormula):
        self.formulas[f.head].add(f)

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
            print("Expanding diamonds in ", self)
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

    def is_closed(self) -> bool:
        if DEBUG:
            print("Determining if", self, "is closed")
        children = self.expand_proposition()
        return all(any(c.is_closed() for c in child.expand_diamonds()) for child in children)


def inconsistent(formulas: Iterable[GLFormula]) -> bool:
    """Decides whether a collection of formulas is inconsistent"""
    return TableauNode({nnf(f) for f in formulas}).is_closed()


def implies(hyp: Iterable[GLFormula], tgt: GLFormula) -> bool:
    """Decides whether hyp |- tgt"""
    fs: Iterable[GLFormula] = itertools.chain(hyp, [Not(tgt)])
    return inconsistent(fs)


# def test():
    # formulas: Set[GLFormula] = {
    #     Diamond(Not(GLFalse)), # Theory is consistent
    #     Box(Diamond(Not(GLFalse)))  # Theory proves it is consistent
    # }
    # node = TableauNode(formulas)
    # print(node.is_closed())


if __name__ == "__main__":
    is_consistent = Diamond(GLTrue)
    print(implies(
        [is_consistent],
        Not(Box(is_consistent))
    ))


