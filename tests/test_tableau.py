import random
from unittest import TestCase
from formula import *
from tableau import is_valid, is_unsat, is_sat
from random_formula import rand_formula

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

    def test_rand1(self):
        assert is_unsat(
            [Not(Or(Not(And(And(Not(Diamond(Implies(C, A))), Not(Diamond(Box(Not(B))))), Diamond(Not(Or(Diamond(A), Diamond(Not(B))))))), Implies(Not(Box(Not(Box(Diamond(C))))), Not(Or(Not(Or(Diamond(Not(A)), Or(Not(A), B))), Not(Diamond(And(B, Not(B)))))))))]
        )

    def test_rand2(self):
        random.seed(314159)
        # Ensure random algorithm hasn't changed; note variables were generated A-C
        assert rand_formula(3, 'C') == Not(Or(Implies(Not(And(Not(C), C)), Or(A, Not(A))), And(Not(Implies(Not(B), Not(B))), Or(Not(A), B))))
        # Precomputed set of values
        assert {i for i in range(100) if is_unsat([rand_formula(5, 'C')])} == {1, 66, 98, 68, 10, 11, 13, 84, 21, 56, 25}
