import numpy as np
from scipy.optimize import minimize
from dados_carga import get_dados_ordenados

# --- Exercício 1: Função de Cálculo de Erro e Níveis ---
def calcular_segmentacao(tempos_corte, dados_demanda_ordenados):
    """
    Realiza a segmentação baseada nos tempos de corte fornecidos.
    
    Args:
        tempos_corte (list): Lista de tempos (em horas) onde ocorrem as mudanças de patamar.
        dados_demanda_ordenados (array): Curva de duração de carga.
    
    Returns:
        tuple: (erro_total, niveis_calculados)
    """
    # Adiciona 0 e 24h para facilitar o fatiamento
    tempos_completos = np.concatenate(([0], sorted(tempos_corte), [24]))
    
    # Converte horas para índices do array (assumindo passo de 15 min = 0.25h)
    indices = (tempos_completos * 4).astype(int)
    
    # Garante que indices não estourem o array
    indices = np.clip(indices, 0, len(dados_demanda_ordenados))
    
    erro_total = 0
    niveis = []

    for i in range(len(indices) - 1):
        inicio, fim = indices[i], indices[i+1]
        
        # Se o segmento for vazio (ex: cortes sobrepostos), ignora
        if inicio == fim:
            continue
            
        segmento = dados_demanda_ordenados[inicio:fim]
        
        # i) Calcule a demanda média na duração do patamar [cite: 346]
        nivel_medio = np.mean(segmento)
        niveis.append(nivel_medio)
        
        # ii) Calcule a soma de todos os desvios a maior [cite: 347]
        # Interpretação: Somar (Valor - Média) apenas quando Valor > Média
        desvios = segmento - nivel_medio
        desvios_a_maior = np.sum(desvios[desvios > 0])
        
        erro_total += desvios_a_maior
        
    return erro_total, niveis

# --- Exercício 2: Código de Otimização Nelder-Mead ---
def funcao_objetivo(tempos_corte, dados_demanda):
    """
    Função wrapper para o Scipy. O Nelder-Mead precisa minimizar um escalar.
    Inclui penalização para restrições (tempos devem ser ordenados e entre 0-24).
    """
    # Restrições "Soft": Penalizar se os tempos não estiverem em ordem ou fora dos limites
    if not np.all(np.diff(tempos_corte) > 0) or np.any(tempos_corte <= 0) or np.any(tempos_corte >= 24):
        return 1e9 # Retorna um erro gigante para o algoritmo "fugir" dessa região
    
    erro, _ = calcular_segmentacao(tempos_corte, dados_demanda)
    return erro

def otimizar_segmentacao(n_patamares, dados_demanda):
    """
    Executa o Nelder-Mead para encontrar os tempos ótimos.
    O número de variáveis (cortes) é n_patamares - 1[cite: 266].
    """
    n_cortes = n_patamares - 1
    
    # Chute inicial: espaçar os cortes igualmente ao longo das 24h
    x0 = np.linspace(0, 24, n_patamares + 1)[1:-1]
    
    # Uso do 'minimize' do Scipy conforme sugerido na página 8 [cite: 199]
    res = minimize(
        funcao_objetivo, 
        x0, 
        args=(dados_demanda,), 
        method='Nelder-Mead',
        tol=1e-4
    )
    
    return res