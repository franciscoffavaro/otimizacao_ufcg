import numpy as np
import pyswarms as ps

def cost_with_voltage_constraint(x):
    results = []
    for p in x:
        # ... (lógica de decodificação igual ao anterior)
        locs = np.rint(p[:3])
        pots = p[3:]
        
        # Simula tensões aleatórias nas 33 barras para essa partícula
        # Num caso real, aqui entraria o OpenDSS ou Newton-Raphson
        v_profile = np.random.uniform(0.93, 1.06, 33) # Gera algumas violações propositais
        
        # Calcula perda base
        loss = 0.5 - (np.sum(pots) * 0.08)
        
        # Verifica violações (Penalidade)
        violation_count = np.sum((v_profile < 0.95) | (v_profile > 1.05))
        penalty = violation_count * 100 # Peso alto pra forçar a restrição
        
        results.append(loss + penalty)
    return np.array(results)

# Config igual ao Ex 1
# ... bounds definidos anteriormente ... 
opt = ps.single.GlobalBestPSO(n_particles=30, dimensions=6, bounds=bounds,
                              options={'c1': 1.49, 'c2': 1.49, 'w': 0.729})
cost, pos = opt.optimize(cost_with_voltage_constraint, iters=50)

print(f"Ex 2 - Custo Final (com penalidades): {cost:.4f}")