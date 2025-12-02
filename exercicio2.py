from scipy.optimize import linprog

# 1. Função Objetivo: Maximize y = 1*x1 - 2*x2
# No scipy, convertemos para Minimizar: -1*x1 + 2*x2
c = [-1, 2] 

# 2. Restrições (Lado Esquerdo - Matriz A)
# x1 + x2 >= 3   -> Multiplica por -1 -> -1*x1 - 1*x2 <= -3
# x1 + 3x2 >= 4  -> Multiplica por -1 -> -1*x1 - 3*x2 <= -4
# 3x1 + x2 <= 8  -> Já está em <=    ->  3*x1 + 1*x2 <=  8
A = [
    [-1, -1],
    [-1, -3],
    [3,  1]
]

# 3. Restrições (Lado Direito - Vetor b)
b = [-3, -4, 8]

# 4. Limites das variáveis (x1 >= 0, x2 >= 0)
x_bounds = (0, None) # 0 até infinito
bounds = [x_bounds, x_bounds]

# 5. Resolver
res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

# 6. Resultados
print(f"Status: {res.message}")
print(f"Valor de x1: {res.x[0]}")
print(f"Valor de x2: {res.x[1]}")
# Multiplicamos por -1 novamente para obter o valor original de Maximização
print(f"Valor Máximo (y): {-res.fun}")