from unittest import TestCase
from nnf import nnf
from formula import *

# nnf(Box(Not(Not(GLFalse))))

A = Atom("A")
B = Atom("B")


class Test(TestCase):

    def test_nnf_box_not_false(self):
        f = Box(Not(GLTrue))
        assert nnf(f) == Box(GLFalse)

    def test_nnf_not_not(self):
        assert nnf(Not(Not(A))) == A

    def test_nnf_not_and(self):
        f = Not(And(Not(A), Not(B)))
        assert nnf(f) == Or(A, B)

    def test_nnf_implies(self):
        assert nnf(Implies(A, B)) == Or(Not(A), B)
        assert nnf(Not(Implies(A, B))) == And(A, Not(B))

    def test_nnf_diamond(self):
        assert nnf(Not(Diamond(Diamond(A)))) == Box(Box(Not(A)))

