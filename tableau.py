from formula import *
from typing import *


class TableauNode:
    def __init__(self, formulas: Set[GLFormula]):
        self.formulas = formulas



    def expand_conjunctions(self):
        """Expand non-branching patterns i.e. conjunctions"""
        pass

    def expand_disjunctions(self):
        """Expand disjunctions"""


    def expand_diamond(self):
        """Expand diamonds"""
        pass
