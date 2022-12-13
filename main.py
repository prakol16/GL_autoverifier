from formula import *
from nnf import *


if __name__ == "__main__":
    F = Conjunction(Connectives.AND, Atom("A"), Atom("B"))
    G = Conjunction(Connectives.AND, Atom("A"), Atom("B"))
    # Get the head symbol of F
    print(F.head)
    print(F == G)
