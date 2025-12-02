from ortools.sat.python import cp_model

def resolver_mochila_atualizada():
    # --- 1. Dados do Problema ---
    # Capacidade assumida (baseada no exemplo anterior)
    capacidade_mochila = 8 
    
    # Dados fornecidos:
    # Artigos: A, B, C, D, E
    nomes =   ['A', 'B', 'C', 'D', 'E']
    pesos =   [ 2,   1,   4,   5,   3 ]
    valores = [79,  17, 187, 245, 140 ]
    
    qtd_itens = len(nomes)

    # --- 2. Modelagem ---
    print(f"Otimizando para capacidade máxima de: {capacidade_mochila} kg...")
    model = cp_model.CpModel()

    # Variáveis de Decisão
    variaveis_qtd = []
    
    for i in range(qtd_itens):
        # Limite teórico: Quantas vezes o item cabe sozinho na mochila
        limite_superior = capacidade_mochila // pesos[i]
        
        # Cria variável inteira: qtd_item_A, qtd_item_B, etc.
        var = model.NewIntVar(0, limite_superior, f'qtd_{nomes[i]}')
        variaveis_qtd.append(var)

    # --- 3. Restrições ---
    # Soma dos pesos <= Capacidade
    expressao_peso = sum(variaveis_qtd[i] * pesos[i] for i in range(qtd_itens))
    model.Add(expressao_peso <= capacidade_mochila)

    # --- 4. Objetivo ---
    # Maximizar lucro total
    expressao_lucro = sum(variaveis_qtd[i] * valores[i] for i in range(qtd_itens))
    model.Maximize(expressao_lucro)

    # --- 5. Resolvendo ---
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # --- 6. Relatório ---
    if status == cp_model.OPTIMAL:
        lucro_maximo = solver.ObjectiveValue()
        print("-" * 40)
        print(f"SOLUÇÃO ÓTIMA ENCONTRADA")
        print(f"Lucro Máximo: {lucro_maximo}")
        print("-" * 40)
        
        peso_usado = 0
        print("Composição da Mochila:")
        for i in range(qtd_itens):
            qtd = solver.Value(variaveis_qtd[i])
            
            if qtd > 0:
                print(f"  > {qtd} unid. de {nomes[i]} (Peso: {pesos[i]}kg | Lucro: {valores[i]})")
                peso_usado += qtd * pesos[i]
        
        print("-" * 40)
        print(f"Peso Total: {peso_usado} / {capacidade_mochila} kg")
        print("-" * 40)
    else:
        print("Não foi possível encontrar a solução ótima.")

if __name__ == "__main__":
    resolver_mochila_atualizada()