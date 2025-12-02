import numpy as np
import pygad

# --- Classe Enxuta da Rede (Baseada na Fig 5) ---
class Grid:
    def __init__(self):
        # Dados do PDF (Pág 5 e 9)
        self.parents = {1:0, 2:1, 3:1, 4:2, 5:4, 6:3} # Mapeamento filho:pai
        self.lens = {1:0.5, 2:0.3, 3:0.8, 4:0.4, 5:0.6, 6:1.2} # km
        self.loads = {1:100, 2:150, 3:80, 4:120, 5:60, 6:200} # kW
        
        # Constante M (eq. 2): r=0.2, V0=13.8, cos=0.92
        self.M = 0.2 / (13.8**2 * 0.92**2) 
        
        # Cache de jusante (calculado uma vez só)
        self.downstream = {b: self._get_down(b) for b in self.loads}

    def _get_down(self, node):
        # DFS recursiva simples para achar barras filhas
        kids = [k for k, v in self.parents.items() if v == node]
        group = {node}
        for k in kids: group.update(self._get_down(k))
        return group

    def calc_loss(self, gens={}):
        total_loss = 0
        current_loads = self.loads.copy()
        
        # Abate geração da carga (Carga Negativa - Pág 8)
        for bus, pwr in gens.items():
            if bus in current_loads: current_loads[bus] -= pwr

        # Eq. 1 e 3: Soma perdas dos trechos
        for i in range(1, 7):
            sum_load = sum(current_loads[b] for b in self.downstream[i])
            total_loss += self.M * self.lens[i] * (sum_load**2)
            
        return total_loss

# --- Setup do AG com PyGAD ---
net = Grid()
GEN_POWER = 50 # kW por gerador

def fitness_func(ga_instance, solution, solution_idx):
    # Transforma genótipo [barra_a, barra_b] em dict {barra: 50}
    gens = {int(b): GEN_POWER for b in solution}
    loss = net.calc_loss(gens)
    # Inverte o valor pq o PyGAD quer maximizar fitness
    return 1.0 / (loss + 0.0001)

# Configuração concisa
ga_instance = pygad.GA(
    num_generations=20,
    num_parents_mating=5,
    fitness_func=fitness_func,
    sol_per_pop=10,
    num_genes=2,              # Queremos alocar 2 geradores
    gene_space=range(1, 7),   # Barras 1 a 6
    gene_type=int,
    allow_duplicate_genes=False, # Restrição do exercício: não repetir barra
    mutation_percent_genes=20
)

print("Rodando otimização...")
ga_instance.run()

# Resultados
best_sol, best_fit, _ = ga_instance.best_solution()
loss_base = net.calc_loss()
loss_otim = 1.0 / best_fit

print(f"\n--- Resultado ---")
print(f"Melhor alocação: Barras {best_sol}")
print(f"Perda Base: {loss_base:.2f} kW")
print(f"Perda Otimizada: {loss_otim:.2f} kW")
print(f"Redução: {100*(loss_base - loss_otim)/loss_base:.1f}%")