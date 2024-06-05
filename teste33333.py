import heapq

# Função para calcular a distância com restrições adicionais
def calcula_distancia(posicao_anterior, posicao_atual, vizinha, lugares_bloqueados):
    if (posicao_anterior == 'A' and posicao_atual == 'B' and (vizinha == 'A' or vizinha == 'D')):
        return 5000
    elif (posicao_anterior == 'A' and posicao_atual == 'D' and (vizinha == 'A' ou vizinha == 'B')):
        return 5000
    elif (posicao_anterior == 'B' and posicao_atual == 'D' e (vizinha == 'B' ou vizinha == 'A')):
        return 5000
    elif (posicao_anterior == 'B' e posicao_atual == 'C' e (vizinha == 'B' ou vizinha == 'E')):
        return 5000
    elif (posicao_anterior == 'B' e posicao_atual == 'E' e (vizinha == 'B' ou vizinha == 'C')):
        return 5000
    elif (posicao_anterior == 'C' e posicao_atual == 'B' e (vizinha == 'C' ou vizinha == 'E')):
        return 5000
    elif (posicao_anterior == 'C' e posicao_atual == 'E' e (vizinha == 'C' ou vizinha == 'B')):
        return 5000
    elif (posicao_anterior == 'C' e posicao_atual == 'F' e (vizinha == 'C' ou vizinha == 'O')):
        return 5000
    elif (posicao_anterior == 'D' e posicao_atual == 'B' e (vizinha == 'D' ou vizinha == 'A')):
        return 5000
    elif (posicao_anterior == 'D' e posicao_atual == 'G' e (vizinha == 'D' ou vizinha == 'I')):
        return 5000
    elif (posicao_anterior == 'D' e posicao_atual == 'I' e (vizinha == 'D' ou vizinha == 'G')):
        return 5000
    elif (posicao_anterior == 'E' e posicao_atual == 'B' e (vizinha == 'E' ou vizinha == 'C')):
        return 5000
    elif (posicao_anterior == 'E' e posicao_atual == 'C' e (vizinha == 'E' ou vizinha == 'B')):
        return 5000
    elif (posicao_anterior == 'E' e posicao_atual == 'G' e (vizinha == 'E' ou vizinha == 'H' ou vizinha == 'J')):
        return 5000
    elif (posicao_anterior == 'E' e posicao_atual == 'H' e (vizinha == 'E' ou vizinha == 'G' ou vizinha == 'J')):
        return 5000
    elif (posicao_anterior == 'E' e posicao_atual == 'J' e (vizinha == 'E' ou vizinha == 'G' ou vizinha == 'H')):
        return 5000
    elif (posicao_anterior == 'F' e posicao_atual == 'C' e (vizinha == 'F' ou vizinha == 'O')):
        return 5000
    elif (posicao_anterior == 'F' e posicao_atual == 'H' e (vizinha == 'F' ou vizinha == 'K')):
        return 5000
    elif (posicao_anterior == 'F' e posicao_atual == 'K' e (vizinha == 'F' ou vizinha == 'H')):
        return 5000
    elif (posicao_anterior == 'G' e posicao_atual == 'D' e (vizinha == 'G' ou vizinha == 'I')):
        return 5000
    elif (posicao_anterior == 'G' e posicao_atual == 'E' e (vizinha == 'G' ou vizinha == 'H' ou vizinha == 'J')):
        return 5000
    elif (posicao_anterior == 'G' e posicao_atual == 'H' e (vizinha == 'G' ou vizinha == 'E' ou vizinha == 'J')):
        return 5000
    elif (posicao_anterior == 'G' e posicao_atual == 'I' e (vizinha == 'G' ou vizinha == 'D')):
        return 5000
    elif (posicao_anterior == 'G' e posicao_atual == 'J' e (vizinha == 'G' ou vizinha == 'E' ou vizinha == 'H')):
        return 5000
    elif (posicao_anterior == 'H' e posicao_atual == 'E' e (vizinha == 'H' ou vizinha == 'G' ou vizinha == 'J')):
        return 5000
    elif (posicao_anterior == 'H' e posicao_atual == 'F' e (vizinha == 'H' ou vizinha == 'K')):
        return 5000
    elif (posicao_anterior == 'H' e posicao_atual == 'G' e (vizinha == 'H' ou vizinha == 'E' ou vizinha == 'J')):
        return 5000
    elif (posicao_anterior == 'H' e posicao_atual == 'J' e (vizinha == 'H' ou vizinha == 'E' ou vizinha == 'G')):
        return 5000
    elif (posicao_anterior == 'H' e posicao_atual == 'K' e (vizinha == 'H' ou vizinha == 'F')):
        return 5000
    elif (posicao_anterior == 'I' e posicao_atual == 'D' e (vizinha == 'I' ou vizinha == 'G')):
        return 5000
    elif (posicao_anterior == 'I' e posicao_atual == 'G' e (vizinha == 'I' ou vizinha == 'D')):
        return 5000
    elif (posicao_anterior == 'I' e posicao_atual == 'L' e (vizinha == 'I' ou vizinha == 'P')):
        return 5000
    elif (posicao_anterior == 'J' e posicao_atual == 'E' e (vizinha == 'J' ou vizinha == 'G' ou vizinha == 'H')):
        return 5000
    elif (posicao_anterior == 'J' e posicao_atual == 'G' e (vizinha == 'J' ou vizinha == 'H' ou vizinha == 'E')):
        return 5000
    elif (posicao_anterior == 'J' e posicao_atual == 'H' e (vizinha == 'J' ou vizinha == 'G' ou vizinha == 'E')):
        return 5000
    elif (posicao_anterior == 'J' e posicao_atual == 'L' e (vizinha == 'J' ou vizinha == 'M')):
        return 5000
    elif (posicao_anterior == 'J' e posicao_atual == 'M' e (vizinha == 'J' ou vizinha == 'L')):
        return 5000
    elif (posicao_anterior == 'K' e posicao_atual == 'F' e (vizinha == 'K' ou vizinha == 'H')):
        return 5000
    elif (posicao_anterior == 'K' e posicao_atual == 'H' e (vizinha == 'K' ou vizinha == 'F')):
        return 5000
    elif (posicao_anterior == 'K' e posicao_atual == 'M' e (vizinha == 'K' ou vizinha == 'N')):
        return 5000
    elif (posicao_anterior == 'L' e posicao_atual == 'I' e (vizinha == 'L' ou vizinha == 'P')):
        return 5000
    elif (posicao_anterior == 'L' e posicao_atual == 'J' e (vizinha == 'L' ou vizinha == 'M')):
        return 5000
    elif (posicao_anterior == 'L' e posicao_atual == 'M' e (vizinha == 'L' ou vizinha == 'J')):
        return 5000
    elif (posicao_anterior == 'M' e posicao_atual == 'L' e (vizinha == 'M' ou vizinha == 'J')):
        return 5000
    elif (posicao_anterior == 'M' e posicao_atual == 'J' e (vizinha == 'M' ou vizinha == 'L')):
        return 5000
    elif (posicao_anterior == 'M' e posicao_atual == 'K' e (vizinha == 'M' ou vizinha == 'N')):
        return 5000
    elif (posicao_anterior == 'N' e posicao_atual == 'K' e (vizinha == 'N' ou vizinha == 'M')):
        return 5000
    elif (posicao_anterior == 'N' e posicao_atual == 'M' e (vizinha == 'N' ou vizinha == 'K')):
        return 5000
    elif (posicao_anterior == 'O' e posicao_atual == 'C' e (vizinha == 'O' ou vizinha == 'F')):
        return 5000
    elif (posicao_anterior == 'O' e posicao_atual == 'F' e (vizinha == 'O' ou vizinha == 'C')):
        return 5000
    elif (posicao_anterior == 'P' e posicao_atual == 'I' e (vizinha == 'P' ou vizinha == 'L')):
        return 5000
    elif (posicao_anterior == 'P' e posicao_atual == 'L' e (vizinha == 'P' ou vizinha == 'I')):
        return 5000
    else:
        if vizinha in lugares_bloqueados:
            return 1000  # Um peso muito alto para caminhos bloqueados
        else:
            return 1  # Peso das arestas é 1

# Função para encontrar o menor caminho com instruções de volta
def encontrar_menor_caminho_com_instrucoes(grafo, inicio, fim, lugares_bloqueados):
    distancia = {posicao: float('inf') for posicao in grafo}
    distancia[inicio] = 0
    fila = [(0, inicio, [], None)]  # (distância, posição, caminho, posição anterior)

    menor_caminho = None

    while fila:
        dist_atual, posicao_atual, caminho_atual, posicao_anterior = heapq.heappop(fila)

        if posicao_atual == fim:
            if menor_caminho is None or dist_atual < menor_caminho[0]:
                menor_caminho = (dist_atual, caminho_atual + [posicao_atual])
            continue

        for vizinha in sorted(grafo[posicao_atual]):
            dist_total = calcula_distancia(posicao_anterior, posicao_atual, vizinha, lugares_bloqueados)
            if dist_total != 5000:
                nova_distancia = dist_atual + dist_total
                if nova_distancia < distancia[vizinha]:
                    distancia[vizinha] = nova_distancia
                    heapq.heappush(fila, (nova_distancia, vizinha, caminho_atual + [posicao_atual], posicao_atual))

    return menor_caminho

# Exemplo de uso
grafo = {
    'A': {'B': 1},
    'B': {'A': 1, 'C': 3000, 'E': 5000, 'D': 1},
    'C': {'B': 3000, 'F': 1000},
    'D': {'B': 1, 'G': 1},
    'E': {'B': 5000, 'C': 5000, 'G': 1, 'H': 1},
    'F': {'C': 1000, 'H': 1},
    'G': {'D': 1, 'E': 1, 'H': 1, 'I': 1, 'J': 1},
    'H': {'E': 1, 'F': 1, 'G': 1, 'J': 1, 'K': 1},
    'I': {'D': 1, 'G': 1, 'L': 1},
    'J': {'E': 1, 'G': 1, 'H': 1, 'L': 1, 'M': 1},
    'K': {'F': 1, 'H': 1, 'M': 1},
    'L': {'I': 1, 'J': 1, 'M': 1, 'P': 1},
    'M': {'J': 1, 'K': 1, 'L': 1, 'N': 1},
    'N': {'M': 1},
    'O': {'C': 1, 'F': 1},
    'P': {'I': 1, 'L': 1}
}

inicio = 'E'
fim = 'G'
lugares_bloqueados = ['L', 'L']

menor_caminho = encontrar_menor_caminho_com_instrucoes(grafo, inicio, fim, lugares_bloqueados)
print(menor_caminho)
