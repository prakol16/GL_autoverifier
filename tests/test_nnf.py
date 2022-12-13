from unittest import TestCase
from nnf import nnf
from formula import *


class Test(TestCase):
    def test_nnf_box_not(self):
        f = Box(Not(Not(GLFalse)))
        assert nnf(f) == Box(GLFalse)

    def test_nnf_not_and(self):
        f = Not(And(Not(Atom("A")), Not(Atom("B"))))
        assert nnf(f) == Or(Atom("A"), Atom("B"))