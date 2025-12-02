import numpy as np
import pyswarms as ps

def voltage_quality_index(x):
    results = []
    for p in x:
        # Decodifica
        pots = p[3:] # A posição importa menos pro mock, focamos na injeção de potência
        
        # Simula perfil de tensão. 
        # Hipótese: Mais potência = sobe tensão.
        # Base é 0.90 (subtensão). GD ajuda a subir pra 1.0.
        v_base = np.full(33, 0.90) 
        boost = np.sum(pots) * 0.05 # GD melhorando o perfil
        v_profile = v_base + boost 
        
        # Função Objetivo: Desvio quadrático do 1.0 pu (Alvo)
        # Queremos que v_profile seja igual a 1.0
        iq = np.sum((v_profile - 1.0)**2)
        
        results.append(iq)
    return np.array(results)

opt = ps.single.GlobalBestPSO(n_particles=30, dimensions=6, bounds=bounds,
                              options={'c1': 1.5, 'c2': 1.5, 'w': 0.7})
cost, pos = opt.optimize(voltage_quality_index, iters=50)

print(f"Ex 3 - Desvio de Tensão (Zero é perfeito): {cost:.4f}")