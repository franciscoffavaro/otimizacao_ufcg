from exercicio4_2 import calcular_perdas_total
from exercicio4_3 import perdasPorEstagio

def reducaoPerdasIncrementaisPorEstagio(solucao, estagio):
    perda_atual = perdasPorEstagio(solucao, estagio)
    
    if estagio == 1:
        # Estágio anterior é 0 (sem capacitores)
        perda_anterior = calcular_perdas_total([0, 0, 0, 0])
    else:
        perda_anterior = perdasPorEstagio(solucao, estagio - 1)
        
    return perda_anterior - perda_atual

# Exemplo de uso
red = reducaoPerdasIncrementaisPorEstagio([0, 1, 2, 0], 2)
print(f"Redução Incremental no Estágio 2: {red:.2f} kW")