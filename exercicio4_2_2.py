from exercicio4_2 import calcular_perdas_total
from exercicio4_3 import perdasPorEstagio
from exercicio4_4 import reducaoPerdasIncrementaisPorEstagio

def gerar_dados_quadro_5(solucao):
    print(f"\nDados para Quadro 5 - Solução: {solucao}")
    perda_base = calcular_perdas_total([0,0,0,0])
    print(f"Perda Inicial (Estágio 0): {perda_base:.2f} kW")
    
    for i in range(1, 5):
        delta = reducaoPerdasIncrementaisPorEstagio(solucao, i)
        print(f"Estágio {i} (Barra {i}, Qtd {solucao[i-1]}): Delta^2 P = {delta:.2f} kW")
    
    print(f"Perda Final: {perdasPorEstagio(solucao, 4):.2f} kW")

# Gerando para a solução ótima citada no PDF [0, 1, 2, 0]
gerar_dados_quadro_5([0, 1, 2, 0])