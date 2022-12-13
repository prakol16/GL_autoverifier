from unittest import TestCase
from formula import *
from tableau import is_valid, is_unsat, is_sat


A = Atom("A")
B = Atom("B")
C = Atom("C")
is_consistent = Diamond(GLTrue)


class Test(TestCase):
    def test_implies_godel(self):
        assert is_valid([is_consistent], Not(Box(is_consistent)))

    def test_implies_basic(self):
        assert is_valid([Box(Implies(A, B)), Box(A)], Box(B))

    def test_implies_trans(self):
        assert is_valid([Box(A)], Box(Box(A)))

    def test_sat(self):
        assert is_unsat([Or(A, B, C), Not(A), Not(B), Not(C)])

    def test_msat(self):
        assert is_unsat([is_consistent, Box(Or(A, B, C)),
                Box(Not(A)), Box(Not(B)), Box(Not(C))])

    def test_false(self):
        assert is_unsat([GLFalse])

    def test_lob(self):
        assert is_valid([Box(Implies(Box(A), A))], Box(A))

    def test_self_hating_consistent(self):
        assert is_sat([Not(is_consistent)])

    def test_contingent(self):
        assert not is_valid([A], Box(A))

    def test_loop(self):
        f = Diamond(Box(A))
        assert is_unsat([f, Diamond(Not(A)), A, Box(f), Box(Diamond(Not(A))), Box(A)])


