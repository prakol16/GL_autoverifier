import random
import timeit
from formula import *
from tableau import is_valid, is_sat, is_unsat
from tqdm import tqdm
from nnf import nnf
from benchmark_data import hard_sat_formulas, hard_unsat_formulas

def rand_formula(depth: int) -> GLFormula:
    if depth == 0:
        atom = Atom(chr(random.randint(ord('A'), ord('E'))))
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
    for f in hard_sat_formulas:
        assert is_sat([f])
    for f in hard_unsat_formulas:
        assert is_unsat([f])


if __name__ == "__main__":
    random.seed(21730)
    # print(rand_formula(6))
    formulas = [rand_formula(6) for _ in range(100)]
    for f in tqdm(formulas):
        is_unsat([f])