from exercicio4_2 import calcular_perdas_total

def perdasPorEstagio(solucao, estagio):
    # Considera apenas os capacitores até o estágio informado (índice 1 a 4)
    # Zera os capacitores das barras posteriores ao estágio
    configuracao_parcial = solucao[:estagio] + [0]*(4 - estagio)
    
    return calcular_perdas_total(configuracao_parcial)

# Testes solicitados no PDF (Pág. 14):
sol = [0, 1, 2, 0]
print(f"Solução {sol}, Estágio 2: {perdasPorEstagio(sol, 2):.2f} kW")
print(f"Solução [0,1,0,2], Estágio 2: {perdasPorEstagio([0,1,0,2], 2):.2f} kW")