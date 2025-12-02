import numpy as np
import pyswarms as ps

# Mock do fluxo de potência (simula a física da rede)
def calculate_losses(x):
    # x = [barra1, barra2, barra3, pot1, pot2, pot3]
    losses_batch = []
    for particle in x:
        # Decodifica (3 primeiros sao locais, 3 ultimos potencias)
        locs = np.rint(particle[:3]) # cast pra int
        pots = particle[3:]
        
        # Restrição: Geradores em barras diferentes
        if len(np.unique(locs)) != len(locs):
            losses_batch.append(1e6) # Penalidade absurda
            continue
            
        # Função simples: quanto mais potencia bem distribuida, menos perda
        # O 0.5 é a perda base do sistema sem GD
        loss = 0.5 - (np.sum(pots) * 0.08) 
        losses_batch.append(max(0, loss))
    return np.array(losses_batch)

# Limites: Barras (1-33), Potencia (0.1-2.0 MW)
max_bound = 33 * np.ones(6)
max_bound[3:] = 2.0 
min_bound = np.ones(6)
min_bound[3:] = 0.1
bounds = (min_bound, max_bound)

# Roda PSO
opt = ps.single.GlobalBestPSO(n_particles=20, dimensions=6, bounds=bounds, 
                              options={'c1': 1.5, 'c2': 1.5, 'w': 0.7})
cost, pos = opt.optimize(calculate_losses, iters=50)

print(f"Ex 1 - Melhor Perda: {cost:.4f} MW")
print(f"Barras: {np.rint(pos[:3])}, Potências: {np.round(pos[3:], 2)}")