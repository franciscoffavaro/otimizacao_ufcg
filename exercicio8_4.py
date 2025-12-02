import numpy as np
import pyswarms as ps

# Vamos fingir que calcular a tensão de uma barra é MUITO custoso computacionalmente
# Então usamos o PSO para "caçar" a barra com menor tensão sem varrer tudo (teoricamente)
def check_criticality(x):
    # x é apenas o INDICE da barra (dimensão 1)
    results = []
    
    # Perfil de tensão fixo da rede (Barra 15 é a crítica propositalmente)
    grid_voltages = np.linspace(1.0, 0.85, 33) 
    grid_voltages[14] = 0.80 # A barra crítica escondida (índice 14 = barra 15)
    
    for particle in x:
        idx = int(particle[0])
        # Proteção pra indice fora do array (erro comum)
        if idx >= 33: idx = 32
        if idx < 0: idx = 0
            
        # O objetivo é MINIMIZAR a tensão (achar o vale)
        val = grid_voltages[idx]
        results.append(val)
    return np.array(results)

# Procura apenas 1 variável (índice da barra)
bounds_ex4 = (np.array([0]), np.array([32])) 

opt = ps.single.GlobalBestPSO(n_particles=10, dimensions=1, bounds=bounds_ex4,
                              options={'c1': 0.5, 'c2': 0.5, 'w': 0.9})

val, pos = opt.optimize(check_criticality, iters=20)

print(f"Ex 4 - Barra Crítica Encontrada: Índice {int(pos[0])} com tensão {val:.4f}")