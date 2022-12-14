from formula import *


def presimplify(formula: GLFormula) -> GLFormula:
    if formula.head == HeadSymbol.NOT and formula.f.head == HeadSymbol.NOT:
        return formula.f.f
    if formula.head == HeadSymbol.AND:
        if formula.left == GLFalse or formula.right == GLFalse:
            return GLFalse
        if formula.left == GLTrue:
            return formula.right
        if formula.right == GLTrue:
            return formula.left
    if formula.head == HeadSymbol.OR:
        if formula.left == GLFalse:
            return formula.right
        if formula.right == GLFalse:
            return formula.left
        if formula.left == GLTrue or formula.right == GLTrue:
            return GLTrue
    if formula.head == HeadSymbol.IMPLIES:
        if formula.left == GLFalse or formula.right == GLTrue:
            return GLTrue
        if formula.left == GLTrue:
            return formula.right
        if formula.right == GLFalse:
            return Not(formula.left)
    return formula


def simplify(formula):
    if formula.head == HeadSymbol.NOT:
        return presimplify(Not(simplify(formula.f)))
    if formula.head == HeadSymbol.AND:
        return presimplify(And(simplify(formula.left), simplify(formula.right)))
    if formula.head == HeadSymbol.OR:
        return presimplify(Or(simplify(formula.left), simplify(formula.right)))
    if formula.head == HeadSymbol.IMPLIES:
        return presimplify(Implies(simplify(formula.left), simplify(formula.right)))
    if formula.head == HeadSymbol.BOX:
        return presimplify(Box(simplify(formula.f)))
    if formula.head == HeadSymbol.DIAMOND:
        return presimplify(Diamond(simplify(formula.f)))
    return formula

def prennf(formula):
    if formula.head == HeadSymbol.AND:
        return And(prennf(formula.left), prennf(formula.right))
    if formula.head == HeadSymbol.OR:
        return Or(prennf(formula.left), prennf(formula.right))
    if formula.head == HeadSymbol.IMPLIES:
        return Or(prennf(Not(formula.left)), prennf(formula.right))
    if formula.head == HeadSymbol.BOX:
        return Box(prennf(formula.f))
    if formula.head == HeadSymbol.DIAMOND:
        return Diamond(prennf(formula.f))
    if formula.head == HeadSymbol.NOT:
        if formula.f.head == HeadSymbol.NOT:
            return prennf(formula.f.f)
        if formula.f.head == HeadSymbol.AND:
            return Or(prennf(Not(formula.f.left)), prennf(Not(formula.f.right)))
        if formula.f.head == HeadSymbol.OR:
            return And(prennf(Not(formula.f.left)), prennf(Not(formula.f.right)))
        if formula.f.head == HeadSymbol.IMPLIES:
            return And(prennf(formula.f.left), prennf(Not(formula.f.right)))
        if formula.f.head == HeadSymbol.BOX:
            return Diamond(prennf(Not(formula.f.f)))
        if formula.f.head == HeadSymbol.DIAMOND:
            return Box(prennf(Not(formula.f.f)))
    return formula


def nnf(formula: GLFormula) -> GLFormula:
    return prennf(simplify(formula))


if __name__ == "__main__":
    print(nnf(Implies(Atom("A"), Atom("B"))))
