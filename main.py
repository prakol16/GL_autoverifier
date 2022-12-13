from formula import *


if __name__ == "__main__":
    F = Conjunction(Connectives.AND, Atom("A"), Atom("B"))
    G = Conjunction(Connectives.AND, Atom("A"), Atom("B"))
    print(hash(F), hash(G), id(F), id(G), F == G)
