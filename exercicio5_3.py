import numpy as np
from dados_carga import get_dados_ordenados
from core_otimizacao import otimizar_segmentacao, calcular_segmentacao

def main():
    dados_ordenados = get_dados_ordenados()
    
    print("=== Otimização de Curva de Carga via Nelder-Mead ===\n")

    # --- Exercício 3a: 5 Patamares ---
    print("--> Processando caso A: 5 Patamares (4 cortes)")
    res_5 = otimizar_segmentacao(5, dados_ordenados)
    erro_5, niveis_5 = calcular_segmentacao(res_5.x, dados_ordenados)
    
    print(f"Status Convergência: {res_5.success}")
    print(f"Tempos de corte ótimos (h): {np.round(res_5.x, 2)}")
    print(f"Níveis de Carga (kW): {[round(n, 2) for n in niveis_5]}")
    print(f"Erro de segmentação (Função Objetivo): {erro_5:.4f}")
    print("-" * 40)

    # --- Exercício 3b: 3 Patamares ---
    print("--> Processando caso B: 3 Patamares (2 cortes)")
    res_3 = otimizar_segmentacao(3, dados_ordenados)
    erro_3, niveis_3 = calcular_segmentacao(res_3.x, dados_ordenados)
    
    print(f"Status Convergência: {res_3.success}")
    print(f"Tempos de corte ótimos (h): {np.round(res_3.x, 2)}")
    print(f"Níveis de Carga (kW): {[round(n, 2) for n in niveis_3]}")
    print(f"Erro de segmentação (Função Objetivo): {erro_3:.4f}")
    print("-" * 40)

if __name__ == "__main__":
    main()