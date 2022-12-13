import random
import timeit
from formula import *
from tableau import is_valid, is_sat

def rand_formula(depth):
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
    return is_valid(rand_formula(4))

#print(timeit.timeit(is_valid_rand))

for i in range(100000):
    formula = rand_formula(4)
    try:
        is_valid(formula)
    except:
        print(formula)
        break
