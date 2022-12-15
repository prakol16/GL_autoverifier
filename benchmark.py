import timeit

from tableau import is_unsat
import random


def benchmark_formulas(formulas):
    for f in formulas:
        is_unsat([f])

def bench_depth5():
    tms = timeit.repeat(stmt="benchmark_formulas(formulas)",
                        setup="from __main__ import benchmark_formulas; import random; from random_formula import rand_formula; random.seed(21730);"
                              "formulas = [rand_formula(5) for _ in range(100)]",
                        number=10,
                        repeat=5)
    print("Timing is_unsat depth 5 on 100 formulas, 10 times, best of 5", tms)  # Benchmark: 1.4s


def bench_depth6():
    tms = timeit.repeat(stmt="benchmark_formulas(formulas)",
                  setup="from __main__ import benchmark_formulas; import random; from random_formula import rand_formula; random.seed(21730);"
                        "formulas = [rand_formula(6) for _ in range(100)]",
                  number=10,
                  repeat=5)
    print("Timing is_unsat depth 6 on 100 formulas, 10 times, best of 5", tms) # Benchmark: 17.2s


def bench_hard():
    tms = timeit.repeat(stmt="benchmark_formulas(hard_unsat_formulas)",
                  setup="from __main__ import benchmark_formulas; from benchmark_data import hard_unsat_formulas, hard_sat_formulas;",
                  number=1,
                  repeat=1)
    print("Timing is_unsat on hard unsat formulas, 1 times, best of 1", tms)  # Benchmark: 14.5


if __name__ == "__main__":
    bench_hard()