import numpy as np
from scipy.optimize import minimize

# func objetivo (f = x^2 + y^2)
func = lambda x: x[0]**2 + x[1]**2

# ex 1: igualdade (x + y - 1 = 0)
cons1 = {'type': 'eq', 'fun': lambda x: x[0] + x[1] - 1}
res1 = minimize(func, [1, 0], constraints=cons1) # chute inicial random

print(f"Ex 1: {res1.x}")

# ex 2: desigualdade (x + y - 1 <= 0)
# scipy 'ineq' assume func >= 0, então invertemos para 1 - x - y >= 0
cons2 = {'type': 'ineq', 'fun': lambda x: 1 - x[0] - x[1]}
res2 = minimize(func, [2, 2], constraints=cons2)

print(f"Ex 2: {res2.x}")

# ex 3: misto
# igualdade: x + y - 1 = 0
# desigualdade: x - y - 1 <= 0  ->  1 - x + y >= 0
cons3 = [
    {'type': 'eq', 'fun': lambda x: x[0] + x[1] - 1},
    {'type': 'ineq', 'fun': lambda x: 1 - x[0] + x[1]}
]
res3 = minimize(func, [0.5, 0.5], constraints=cons3)

print(f"Ex 3: {res3.x}")