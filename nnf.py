from formula import *

def presimplify(formula):
    if formula.head == HeadSymbol.NOT and formula.f.head == HeadSymbol.NOT:
        return formula.f.f
    if formula.head == HeadSymbol.AND and formula.left == GLFalse:
        return GLFalse
    if formula.head == HeadSymbol.AND and formula.right == GLFalse:
        return GLFalse
    if formula.head == HeadSymbol.AND and formula.left == GLTrue:
        return formula.right
    if formula.head == HeadSymbol.AND and formula.right == GLTrue:
        return formula.left
    if formula.head == HeadSymbol.OR and formula.left == GLFalse:
        return formula.right
    if formula.head == HeadSymbol.OR and formula.right == GLFalse:
        return formula.left
    if formula.head == HeadSymbol.OR and formula.left == GLTrue:
        return GLTrue
    if formula.head == HeadSymbol.OR and formula.right == GLTrue:
        return GLTrue
    if formula.head == HeadSymbol.IMPLIES and formula.left == GLFalse:
        return GLTrue
    if formula.head == HeadSymbol.IMPLIES and formula.right == GLTrue:
        return GLTrue
    if formula.head == HeadSymbol.IMPLIES and formula.left == GLTrue:
        return formula.right
    if formula.head == HeadSymbol.IMPLIES and formula.right == GLFalse:
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
    return formula

def prennf(formula):
    if formula.head == HeadSymbol.AND:
        return And(prennf(formula.left), prennf(formula.right))
    if formula.head == HeadSymbol.OR:
        return Or(prennf(formula.left), prennf(formula.right))
    if formula.head == HeadSymbol.IMPLIES:
        return Or(prennf(Not(formula.left)), prennf(formula.right))
    if formula.head == HeadSymbol.NOT and formula.f.head == HeadSymbol.NOT:
        return prennf(formula.f.f)
    if formula.head == HeadSymbol.NOT and formula.f.head == HeadSymbol.AND:
        return Or(prennf(Not(formula.f.left)), prennf(Not(formula.f.right)))
    if formula.head == HeadSymbol.NOT and formula.f.head == HeadSymbol.OR:
        return And(prennf(Not(formula.f.left)), prennf(Not(formula.f.right)))
    if formula.head == HeadSymbol.NOT and formula.f.head == HeadSymbol.IMPLIES:
        return And(prennf(formula.f.left), prennf(Not(formula.f.right)))
    return formula

def nnf(formula):
    return prennf(simplify(formula))


