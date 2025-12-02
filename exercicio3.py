from scipy.optimize import linprog

# --- Dados do Problema ---
# Preços por tonelada
preco_A = 1500
preco_B = 1800
venda_padrao = 5000
venda_especial = 7000

# Cálculo dos custos de produção (R$/ton)
# Padrão: 3 partes A + 5 partes B = 8 partes no total
custo_padrao = (3/8 * preco_A) + (5/8 * preco_B)

# Especial: 5 partes A + 2 partes B = 7 partes no total
custo_especial = (5/7 * preco_A) + (2/7 * preco_B)

# Margem de contribuição (Lucro por unidade)
lucro_padrao = venda_padrao - custo_padrao
lucro_especial = venda_especial - custo_especial

print(f"Lucro Padrão: R$ {lucro_padrao:.2f}/ton")
print(f"Lucro Especial: R$ {lucro_especial:.2f}/ton")

# --- Montagem do Modelo ---

# Função Objetivo: Maximizar lucro
# Como o linprog faz minimização, invertemos o sinal dos lucros
c = [-lucro_padrao, -lucro_especial]

# Restrições de disponibilidade (Inequações <=)
# A matriz representa o quanto cada produto consome de A e B
A = [
    [3/8, 5/7],  # Consumo de ingrediente A
    [5/8, 2/7]   # Consumo de ingrediente B
]

# Disponibilidade total diária (lado direito das inequações)
b = [15, 10]  # 15 ton de A e 10 ton de B

# Limites de produção baseados na Demanda Média
# Calculando a média da distribuição uniforme: (min + max) / 2
demanda_media_padrao = (8 + 10) / 2
demanda_media_especial = (15 + 18) / 2

# Tuplas (minimo, maximo) para cada variável
# x0 (padrão) vai de 0 até a demanda média
# x1 (especial) vai de 0 até a demanda média
bounds = [
    (0, demanda_media_padrao), 
    (0, demanda_media_especial)
]

# --- Solução ---
res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

# --- Resultado ---
if res.success:
    qtd_padrao = res.x[0]
    qtd_especial = res.x[1]
    lucro_total = -res.fun # Inverte o sinal de volta para positivo

    print("\n--- Resultado da Otimização ---")
    print(f"Produzir Adubo Padrão:   {qtd_padrao:.2f} toneladas")
    print(f"Produzir Adubo Especial: {qtd_especial:.2f} toneladas")
    print(f"Lucro Total Esperado:    R$ {lucro_total:.2f}")
else:
    print("Não foi possível encontrar uma solução ótima.")