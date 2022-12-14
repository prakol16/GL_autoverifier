from formula import *
from nnf import *


if __name__ == "__main__":
    F = Conjunction(Connectives.AND, Atom("A"), Atom("B"))
    G = Conjunction(Connectives.AND, Atom("A"), Atom("B"))
    # Get the head symbol of F
    print(F.head)
    print(F == G)

    H = Not(Box(Atom("A")))
    print(H)
    print(nnf(H))

    print()

    I = Not(Box(Not(Atom("A"))))
    print(I)
    print(nnf(I))

    print(nnf(Box(Not(Not(Atom("A"))))))

    print(nnf(Not(And(Atom("A"), Atom("B")))))
