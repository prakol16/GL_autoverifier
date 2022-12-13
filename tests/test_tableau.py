from unittest import TestCase
from formula import *
from tableau import implies, inconsistent


A = Atom("A")
B = Atom("B")
C = Atom("C")
is_consistent = Diamond(GLTrue)


class Test(TestCase):
    def test_implies_godel(self):
        assert implies([is_consistent], Not(Box(is_consistent)))

    def test_implies_basic(self):
        assert implies([Box(Implies(A, B)), Box(A)], Box(B))

    def test_implies_trans(self):
        assert implies([Box(A)], Box(Box(A)))

    def test_sat(self):
        assert inconsistent([Or(A, B, C), Not(A), Not(B), Not(C)])

    def test_msat(self):
        assert inconsistent([is_consistent, Box(Or(A, B, C)),
                Box(Not(A)), Box(Not(B)), Box(Not(C))])

    def test_false(self):
        assert inconsistent([GLFalse])

    def test_lob(self):
        assert implies([Box(Implies(Box(A), A))], Box(A))
