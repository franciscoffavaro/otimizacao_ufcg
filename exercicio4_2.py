import numpy as np

# Dados do sistema (Pág. 9)
S_CARGAS = np.array([0.3, 0.8, 1.0, 0.4]) # MVA
R = 5.0      # Ohms
V = 13.8     # kV
C = 0.3      # MVar por banco
COS_PHI = 0.8
SEN_PHI = 0.6
K = R / (V**2)

def calcular_perdas_total(configuracao_capacitores):
    """Calcula perda total em kW para uma lista de capacitores nas 4 barras."""
    # Garante vetor de 4 posições
    caps = np.array(configuracao_capacitores + [0]*(4 - len(configuracao_capacitores)))
    
    P_carga = S_CARGAS * COS_PHI
    Q_carga = S_CARGAS * SEN_PHI
    Q_caps = caps * C
    Q_liquido = Q_carga - Q_caps
    
    P_fluxo = 0
    Q_fluxo = 0
    perda_total = 0
    
    # Backward sweep (da barra 4 para 1)
    for i in range(3, -1, -1):
        P_fluxo += P_carga[i]
        Q_fluxo += Q_liquido[i]
        
        perda_trecho = K * (P_fluxo**2 + Q_fluxo**2)
        perda_total += perda_trecho
        
        P_fluxo += perda_trecho # Atualiza fluxo ativo com perdas
        
    return perda_total * 1000 # Retorna em kW