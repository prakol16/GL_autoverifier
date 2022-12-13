import random
import timeit
from formula import *
from tableau import is_valid, is_sat, TableauNode
from tqdm import tqdm
from nnf import nnf

def rand_formula(depth: int) -> GLFormula:
    if depth == 0:
        atom = Atom(chr(random.randint(ord('A'), ord('Z'))))
        if random.choice([True, False]):
            return atom
        else:
            return Not(atom)

    rand_head = random.choice([0,1,2,4,5]) # Exclude NOT

    if rand_head <= 2: # AND, OR, IMPLIES
        if random.choice([True, False]):
            return Conjunction(Connectives(rand_head), rand_formula(depth-1), rand_formula(depth-1))
        else:
            return Not(Conjunction(Connectives(rand_head), rand_formula(depth-1), rand_formula(depth-1)))
    elif rand_head == 4:
        if random.choice([True, False]):
            return Box(rand_formula(depth-1))
        else:
            return Not(Box(rand_formula(depth-1)))
    else:
        if random.choice([True, False]):
            return Diamond(rand_formula(depth-1))
        else:
            return Not(Diamond(rand_formula(depth-1)))


def is_valid_rand():
    return is_valid([], rand_formula(4))

#print(timeit.timeit(is_valid_rand))
if __name__ == "__main__":
    # ¬(¬(¬((S ⋀ ¬G) ⭢ ¬(¬G ⭢ J)) ⭢ ¬♢¬(¬C ⋀ P)) ⋀ ¬♢☐♢R)
    # formula = Not(Not(Not()))
    # ☐¬(☐(¬J ⋀ ¬B) ⭢ ¬♢☐R)
    # formula = Box(Not(Implies(Box(And(Not(Atom("J")), Not(Atom("B")))), Not(Diamond(Box(Atom("R")))))))
    # print(formula)
    # # print(nnf(Not(formula)))
    #
    # (¬☐¬☐(¬A ⋁ A) ⭢ ♢☐¬☐A)
    # random.seed(11)
    # A = Atom("A")
    # formula = Diamond(And(Box(Box(Not(A))), Diamond(Diamond(A))))
    # print(is_sat([formula]))
    for i in tqdm(range(1000)):
        formula = rand_formula(5)
        try:
            # print(formula)
            is_sat([formula])
        except Exception as e:
            print("Exception", e)
            print(formula)
            print(nnf(formula))
            # TableauNode({nnf(formula)}).is_closed(debug=True)
            break
