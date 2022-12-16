from formula import *

A, B, C, D, E, F = [Atom(x) for x in "ABCDEF"]

hard_unsat_formulas = [
And(Not(Diamond(Not(Or(Not(Box(Not(Or(Not(Box(B)), Not(Or(Not(C), C)))))), And(Not(Diamond(Not(Implies(A, Not(D))))), Diamond(Not(Box(D)))))))), Not(Implies(Implies(Not(Or(Implies(Diamond(Not(D)), Not(Diamond(Not(B)))), Implies(And(Not(C), C), Diamond(Not(A))))), Not(And(Diamond(Box(D)), Not(Box(Box(Not(C))))))), Implies(Not(Box(Not(Diamond(Not(Diamond(A)))))), And(Not(Implies(Not(Or(D, D)), Not(Diamond(Not(B))))), Not(And(And(B, Not(E)), Diamond(Not(E))))))))),
Not(Implies(Not(Diamond(Implies(And(Box(Diamond(Not(E))), Not(Box(Diamond(A)))), Not(Or(Box(Or(A, Not(A))), Or(Not(And(C, D)), Or(C, Not(C)))))))), Implies(Not(And(Box(Box(Not(And(E, Not(B))))), Box(Not(Or(Not(Box(Not(A))), Not(Box(D))))))), Not(And(Not(And(Box(Diamond(D)), Diamond(Not(Or(Not(B), C))))), And(Not(And(Implies(Not(A), D), Not(Implies(Not(C), Not(C))))), Not(Implies(And(Not(C), Not(D)), Box(Not(B)))))))))),
Not(Or(Implies(Diamond(Not(Or(And(Not(And(B, D)), Not(Box(A))), Not(Implies(Implies(Not(E), Not(E)), Not(Or(Not(D), C))))))), Not(Diamond(Not(Box(Or(Diamond(Not(B)), Not(And(Not(D), Not(B))))))))), Not(Box(Diamond(Or(Not(Or(Implies(Not(D), Not(C)), Not(Box(C)))), Not(Or(Box(Not(D)), Not(Diamond(A)))))))))),
Not(Box(Or(Or(Diamond(Not(Diamond(Not(And(E, Not(D)))))), Not(Diamond(Implies(Not(Diamond(B)), Box(D))))), Or(Not(And(Not(Or(Not(Box(D)), Implies(Not(D), D))), Or(Not(Implies(A, Not(C))), Implies(B, Not(A))))), Diamond(Not(Implies(Not(Box(B)), Not(And(D, Not(E)))))))))),
Not(Or(Not(And(Box(Not(And(Not(Box(Diamond(D))), Not(Or(Implies(Not(C), A), Or(Not(D), D)))))), Implies(Implies(Implies(Not(Diamond(Not(D))), Not(Or(D, Not(D)))), Not(And(And(A, Not(B)), Not(And(D, Not(E)))))), Diamond(Diamond(Implies(Not(E), Not(C))))))), Not(Implies(Implies(Diamond(Not(Implies(Not(Implies(C, Not(A))), Box(C)))), Implies(Box(Not(Box(E))), Diamond(Box(Not(D))))), Not(Diamond(Or(Not(Or(Box(D), Box(B))), Not(Implies(Box(A), Not(Box(E))))))))))),
Not(Or(Not(Box(Or(Not(Implies(Or(Implies(B, B), And(Not(B), Not(C))), Not(And(Diamond(D), Not(Box(D)))))), Or(Box(Or(Not(D), Not(B))), Implies(Not(And(A, C)), Not(And(C, Not(B)))))))), Not(And(Not(And(Diamond(Not(And(Not(Box(Not(B))), Not(Diamond(Not(A)))))), Box(Not(Diamond(Not(Or(B, E))))))), And(Box(Not(Box(Not(Diamond(C))))), Diamond(Not(Box(Not(Or(Not(D), Not(B))))))))))),
And(And(Diamond(And(Box(Diamond(Not(C))), Diamond(Box(Not(B))))), Box(Not(Implies(Not(Box(Diamond(B))), And(And(E, E), Or(Not(E), Not(D))))))), Box(Not(Implies(Not(Box(Not(And(Not(Implies(C, Not(A))), Diamond(Not(C)))))), Not(Or(Not(Diamond(Implies(D, Not(A)))), Not(Box(Not(Diamond(Not(C))))))))))),
Not(Box(Not(And(Not(Or(Not(Implies(Diamond(Box(Not(A))), Not(Diamond(Box(Not(C)))))), Not(Diamond(Not(Diamond(Not(Or(B, Not(A))))))))), Not(Implies(Implies(Not(Implies(Not(Diamond(E)), Not(Diamond(Not(B))))), Or(Not(Box(C)), Not(Diamond(Not(A))))), Implies(Box(Implies(B, E)), Not(Or(Not(Box(Not(D))), Not(Implies(Not(E), D))))))))))),
Not(Implies(Not(Implies(Not(Diamond(Not(Implies(Box(Not(Box(Not(B)))), Not(Or(Or(Not(C), Not(E)), Not(Diamond(A)))))))), And(Not(And(Not(And(And(Not(D), Not(E)), Box(A))), And(Diamond(E), Not(Box(Not(D)))))), Box(Not(And(Diamond(C), Implies(D, Not(B)))))))), Or(Not(Implies(And(And(Not(Or(Not(E), E)), Not(Diamond(Not(B)))), Not(Or(Box(E), Diamond(A)))), Not(Or(Diamond(Not(Implies(Not(D), Not(B)))), Implies(Implies(Not(A), A), Diamond(E)))))), Or(Not(Box(Not(And(Not(Implies(Not(A), D)), Diamond(Not(E)))))), Or(Implies(Not(Implies(Not(A), B)), Not(Or(C, Not(D)))), Not(Box(Or(Not(A), Not(D)))))))))
]

hard_sat_formulas = [
Diamond(Not(Implies(Not(And(Not(Or(Not(Implies(Not(Or(Not(C), Not(D))), Box(B))), Not(Box(Or(Not(B), Not(D)))))), Or(Not(Or(Not(Diamond(Not(E))), Box(Not(A)))), Not(Box(Not(Or(C, Not(B)))))))), Or(Not(Or(Not(Box(Box(Not(C)))), Box(Not(Box(C))))), Box(Box(Box(Not(C)))))))),
]