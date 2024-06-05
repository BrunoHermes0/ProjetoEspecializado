import heapq

# Definir um grafo ponderado das posições no estoque
grafo = {
    'A': {'B', 'D'},
    'B': {'A', 'C', 'D', 'E'},
    'C': {'B', 'E', 'F', 'O'},
    'D': {'A', 'B', 'G', 'I'},
    'E': {'B', 'C', 'G', 'H', 'J'},
    'F': {'C', 'H', 'K', 'O'},
    'G': {'D', 'E', 'H', 'I', 'J'},
    'H': {'E', 'F', 'G', 'J', 'K'},
    'I': {'D', 'G', 'L', 'P'},
    'J': {'E', 'G', 'H', 'L', 'M'},
    'K': {'F', 'H', 'M', 'N'},
    'L': {'I', 'J', 'M', 'P'},
    'M': {'J', 'K', 'L', 'N'},
    'N': {'K', 'M'},
    'O': {'C', 'F'},
    'P': {'I', 'L'}
}

# Variáveis para instruções de movimento
a = "Siga reto"
b = "Vire a direita"
c = "Vire a esquerda"

# Dicionário de mapeamento de instruções de movimento
instrucoes_movimento = {
    ('A', 'B'): a, ('A', 'D'): b,
    ('B', 'A'): a, ('B', 'D'): c, ('B', 'C'): a, ('B', 'E'): b,
    ('C', 'B'): a, ('C', 'E'): c, ('C', 'F'): b, ('C', 'O'): a,
    ('D', 'A'): c, ('D', 'B'): b, ('D', 'G'): c, ('D', 'I'): a,
    ('E', 'B'): c, ('E', 'C'): b, ('E', 'G'): b, ('E', 'H'): c, ('E', 'J'): a,
    ('F', 'C'): c, ('F', 'H'): b, ('F', 'K'): a, ('F', 'O'): b,
    ('G', 'D'): b, ('G', 'E'): c, ('G', 'H'): a, ('G', 'I'): c, ('G', 'J'): b,
    ('H', 'E'): b, ('H', 'F'): c, ('H', 'G'): a, ('H', 'J'): c, ('H', 'K'): b,
    ('I', 'D'): a, ('I', 'G'): b, ('I', 'L'): c, ('I', 'P'): b,
    ('J', 'E'): a, ('J', 'G'): c, ('J', 'H'): b, ('J', 'L'): b, ('J', 'M'): c,
    ('K', 'F'): a, ('K', 'H'): c, ('K', 'M'): b, ('K', 'N'): c,
    ('L', 'I'): b, ('L', 'J'): c, ('L', 'M'): a, ('L', 'P'): a,
    ('M', 'L'): a, ('M', 'J'): b, ('M', 'K'): c, ('M', 'N'): a,
    ('N', 'K'): b, ('N', 'M'): a,
    ('O', 'C'): a, ('O', 'F'): c,
    ('P', 'I'): c, ('P', 'L'): a

}


def encontrar_menor_caminho_com_instrucoes(grafo, inicio, fim, lugares_bloqueados, posicao_anterior):
    distancia = {posicao: float('inf') for posicao in grafo}
    distancia[inicio] = 0
    fila = [(0, inicio, [], posicao_anterior)]  # (distância, posição, caminho)

    menor_caminho = None

    while fila:
        dist_atual, posicao_atual, caminho_atual, posicao_anterior = heapq.heappop(fila)
        if posicao_atual == fim:
            if menor_caminho is None or dist_atual < menor_caminho[0]:
                menor_caminho = (dist_atual, caminho_atual + [posicao_atual])
                
            continue

        for vizinha in sorted(grafo[posicao_atual]):
            print('to no for')
            print(posicao_anterior, posicao_atual, vizinha)
            if (posicao_anterior == 'A' and posicao_atual == 'B' and (vizinha == 'A' or vizinha == 'D')):
                dist_total = 5000
            elif (posicao_anterior == 'A' and posicao_atual == 'D' and (vizinha == 'A' or vizinha == 'B')):
                dist_total = 5000
            elif (posicao_anterior == 'B' and posicao_atual == 'D' and (vizinha == 'B' or vizinha == 'A')):
                dist_total = 5000
            elif (posicao_anterior == 'B' and posicao_atual == 'C' and (vizinha == 'B' or vizinha =='E')):
                dist_total = 5000
            elif (posicao_anterior == 'B' and posicao_atual == 'E' and (vizinha == 'B' or vizinha =='C')):
                dist_total = 5000
            elif (posicao_anterior == 'C' and posicao_atual == 'B' and (vizinha == 'C' or vizinha =='E')):
                dist_total = 5000
            elif (posicao_anterior == 'C' and posicao_atual == 'E' and (vizinha == 'C' or vizinha =='B')):
                dist_total = 5000
            elif (posicao_anterior == 'C' and posicao_atual == 'F' and (vizinha == 'C' or vizinha == 'O')):
                dist_total = 5000
            elif (posicao_anterior == 'D' and posicao_atual == 'B' and (vizinha == 'D' or vizinha == 'A')):
                dist_total = 5000
            elif (posicao_anterior == 'D' and posicao_atual == 'G' and (vizinha == 'D' or vizinha == 'I')):
                dist_total = 5000
            elif (posicao_anterior == 'D' and posicao_atual == 'I' and (vizinha == 'D' or vizinha == 'G')):
                dist_total = 5000
            elif (posicao_anterior == 'E' and posicao_atual == 'B' and (vizinha == 'E' or vizinha == 'C')):
                dist_total = 5000
            elif (posicao_anterior == 'E' and posicao_atual == 'C' and (vizinha == 'E' or vizinha == 'B')):
                dist_total = 5000
            elif (posicao_anterior == 'E' and posicao_atual == 'G' and (vizinha == 'E' or vizinha == 'H' or vizinha == 'J')):
                dist_total = 5000
            elif (posicao_anterior == 'E' and posicao_atual == 'H' and (vizinha == 'E' or vizinha == 'G' or vizinha == 'J')):
                dist_total = 5000
            elif (posicao_anterior == 'E' and posicao_atual == 'J' and (vizinha == 'E' or vizinha == 'G' or vizinha == 'H')):
                dist_total = 5000
            elif (posicao_anterior == 'F' and posicao_atual == 'C' and (vizinha == 'F' or vizinha == 'O')):
                dist_total = 5000
            elif (posicao_anterior == 'F' and posicao_atual == 'H' and (vizinha == 'F' or vizinha == 'K')):
                dist_total = 5000
            elif (posicao_anterior == 'F' and posicao_atual == 'K' and (vizinha == 'F' or vizinha == 'H')):
                dist_total = 5000
            elif (posicao_anterior == 'G' and posicao_atual == 'D' and (vizinha == 'G' or vizinha == 'I')):
                dist_total = 5000
            elif (posicao_anterior == 'G' and posicao_atual == 'E' and (vizinha == 'G' or vizinha == 'H' or vizinha == 'J')):
                dist_total = 5000
            elif (posicao_anterior == 'G' and posicao_atual == 'H' and (vizinha == 'G' or vizinha == 'E' or vizinha == 'J')):
                dist_total = 5000
            elif (posicao_anterior == 'G' and posicao_atual == 'I' and (vizinha == 'G' or vizinha == 'D')):
                dist_total = 5000
            elif (posicao_anterior == 'G' and posicao_atual == 'J' and (vizinha == 'G' or vizinha == 'E' or vizinha == 'H')):
                dist_total = 5000
            elif (posicao_anterior == 'H' and posicao_atual == 'E' and (vizinha == 'H' or vizinha == 'G' or vizinha == 'J')):
                dist_total = 5000
            elif (posicao_anterior == 'H' and posicao_atual == 'F' and (vizinha == 'H' or vizinha == 'K')):
                dist_total = 5000
            elif (posicao_anterior == 'H' and posicao_atual == 'G' and (vizinha == 'H' or vizinha == 'E' or vizinha == 'J')):
                dist_total = 5000
            elif (posicao_anterior == 'H' and posicao_atual == 'J' and (vizinha == 'H' or vizinha == 'E' or vizinha == 'G')):
                dist_total = 5000
            elif (posicao_anterior == 'H' and posicao_atual == 'K' and (vizinha == 'H' or vizinha == 'F')):
                dist_total = 5000
            elif (posicao_anterior == 'I' and posicao_atual == 'D' and (vizinha == 'I' or vizinha == 'G')):
                dist_total = 5000
            elif (posicao_anterior == 'I' and posicao_atual == 'G' and (vizinha == 'I' or vizinha == 'D')):
                dist_total = 5000
            elif (posicao_anterior == 'I' and posicao_atual == 'L' and (vizinha == 'I' or vizinha == 'P')):
                dist_total = 5000
            elif (posicao_anterior == 'J' and posicao_atual == 'E' and (vizinha == 'J' or vizinha == 'G' or vizinha == 'H')):
                dist_total = 5000
            elif (posicao_anterior == 'J' and posicao_atual == 'G' and (vizinha == 'J' or vizinha == 'H' or vizinha == 'E')):
                dist_total = 5000
            elif (posicao_anterior == 'J' and posicao_atual == 'H' and (vizinha == 'J' or vizinha == 'G' or vizinha == 'E')):
                dist_total = 5000
            elif (posicao_anterior == 'J' and posicao_atual == 'L' and (vizinha == 'J' or vizinha == 'M')):
                dist_total = 5000
            elif (posicao_anterior == 'J' and posicao_atual == 'M' and (vizinha == 'J' or vizinha == 'L')):
                dist_total = 5000
            elif (posicao_anterior == 'K' and posicao_atual == 'F' and (vizinha == 'K' or vizinha == 'H')):
                dist_total = 5000
            elif (posicao_anterior == 'K' and posicao_atual == 'H' and (vizinha == 'K' or vizinha == 'F')):
                dist_total = 5000
            elif (posicao_anterior == 'K' and posicao_atual == 'M' and (vizinha == 'K' or vizinha == 'N')):
                dist_total = 5000
            elif (posicao_anterior == 'L' and posicao_atual == 'I' and (vizinha == 'L' or vizinha == 'P')):
                dist_total = 5000
            elif (posicao_anterior == 'L' and posicao_atual == 'J' and (vizinha == 'L' or vizinha == 'M')):
                dist_total = 5000
            elif (posicao_anterior == 'L' and posicao_atual == 'M' and (vizinha == 'L' or vizinha == 'J')):
                dist_total = 5000
            elif (posicao_anterior == 'M' and posicao_atual == 'L' and (vizinha == 'M' or vizinha == 'J')):
                dist_total = 5000
            elif (posicao_anterior == 'M' and posicao_atual == 'J' and (vizinha == 'M' or vizinha == 'L')):
                dist_total = 5000
            elif (posicao_anterior == 'M' and posicao_atual == 'K' and (vizinha == 'M' or vizinha == 'N')):
                dist_total = 5000
            elif (posicao_anterior == 'N' and posicao_atual == 'K' and (vizinha == 'N' or vizinha == 'M')):
                dist_total = 5000
            elif (posicao_anterior == 'N' and posicao_atual == 'M' and (vizinha == 'N' or vizinha == 'K')):
                dist_total = 5000
            elif (posicao_anterior == 'O' and posicao_atual == 'C' and (vizinha == 'O' or vizinha == 'F')):
                dist_total = 5000
            elif (posicao_anterior == 'O' and posicao_atual == 'F' and (vizinha == 'O' or vizinha == 'C')):
                dist_total = 5000
            elif (posicao_anterior == 'P' and posicao_atual == 'I' and (vizinha == 'P' or vizinha == 'L')):
                dist_total = 5000
            elif (posicao_anterior == 'P' and posicao_atual == 'L' and (vizinha == 'P' or vizinha == 'I')):
                dist_total = 5000
            else:
                if vizinha in lugares_bloqueados:
                    dist_total = dist_atual + 1000  # Um peso muito alto para caminhos bloqueados
                    if dist_total == 1000:
                        dist_total = 3000

                else:
                    dist_total = dist_atual + 1  # Peso das arestas é 1
            
                if dist_total < distancia[vizinha]:
                    distancia[vizinha] = dist_total
                    heapq.heappush(fila, (dist_total, vizinha, caminho_atual + [posicao_atual],posicao_atual))
                    print(fila)

        

    return menor_caminho

def encontrar_menor_caminho(grafo, inicio, fim,posicao_anterior):
    distancia = {posicao: float('inf') for posicao in grafo}
    distancia[inicio] = 0
    fila = [(0, inicio, [])]  # (distância, posição, caminho)

    menor_caminho = None

    while fila:
        dist_atual, posicao_atual, caminho_atual = heapq.heappop(fila)

        if posicao_atual == fim:
            if menor_caminho is None or dist_atual < menor_caminho[0]:
                menor_caminho = (dist_atual, caminho_atual + [posicao_atual])
            continue

        for vizinha in grafo[posicao_atual]:
            dist_total = dist_atual + 1  # Peso das arestas é 1
            if dist_total < distancia[vizinha]:
                distancia[vizinha] = dist_total
                heapq.heappush(fila, (dist_total, vizinha,caminho_atual + [posicao_atual]))
                
    return menor_caminho


def encontrar_e_navegar(inicio, fim, lugares_bloqueados, prioridade, dist1, dist2, caminho_aux,caminho_outro, IdE, posicao_anterior):

    if inicio == fim:
        print("Empilhadeira chegou no destino.")
    else:
        prox_outro = caminho_outro[1] if len(caminho_outro) > 1 else caminho_outro[0]
        prox = caminho_aux[1]
        if prox == lugares_bloqueados:
            if (prioridade == 1 and IdE == 1) or (prioridade == 2 and IdE == 2) or (prioridade == 0 and IdE == 2 and (dist1 > dist2)) or (prioridade == 0 and IdE == 1 and (dist2 > dist1)):
                print("Espere pela outra empilhadeira para continuar")
            if (prioridade == 1 and IdE == 2) or (prioridade == 2 and IdE == 1) or (prioridade == 0 and IdE == 2 and (dist2 > dist1)) or (prioridade == 0 and IdE == 1 and (dist1 > dist2)):
                if inicio == 'D' and prox == 'B':
                    print(f'De D para A: Vire a esquerda')
                elif inicio == 'B' and prox == 'D':
                    print(f'De B para A: Siga reto')
                elif inicio == 'I' and prox == 'L':
                    print(f'De I para P: Vire a direita')
                elif inicio == 'L' and prox == 'I':
                    print(f'De L para P: Siga reto')
                elif inicio == 'K' and prox == 'M':
                    print(f'De K para N: Vire a esquerda')
                elif inicio == 'M' and prox == 'K':
                    print(f'De M para N: Siga reto')
                elif inicio == 'F' and prox == 'C':
                    print(f'De F para O: Vire a direita')
                elif inicio == 'C' and prox == 'F':
                    print(f'De C para O: Siga reto')
                else:

                    melhor_caminho = encontrar_menor_caminho_com_instrucoes(grafo, inicio, fim, lugares_bloqueados, posicao_anterior)

                    if melhor_caminho:
                        dist, caminho = melhor_caminho
                        print(f"Melhor caminho entre {inicio} e {fim}: ")
                        print(
                            f"Caminho: {' -> '.join(caminho)}, Distância: {dist}")

                        # Obter instruções de movimento
                        # for i in range(len(caminho) - 1):
                        # origem, destino = caminho[i], caminho[i + 1]
                        # instrucao = instrucoes_movimento.get((origem, destino))
                        origem, destino = caminho[0], caminho[1]
                        instrucao = instrucoes_movimento.get((origem, destino))
                        print(f'De {origem} para {destino}: {instrucao}')

                        
                    
                    else:
                        print(f"Não há caminho possível entre {inicio} e {fim}.")
                        
        else:
            if prox == prox_outro:
                if (prioridade == 1 and IdE == 2) or (prioridade == 2 and IdE == 1) or (prioridade == 0 and IdE == 2 and (dist2 > dist1)) or (prioridade == 0 and IdE == 1 and (dist1 > dist2)):
                    print("Espere pela outra empilhadeira para continuar")
                else:
                    melhor_caminho = encontrar_menor_caminho_com_instrucoes(grafo, inicio, fim, lugares_bloqueados, posicao_anterior)

                    if melhor_caminho:
                        dist, caminho = melhor_caminho
                        print(f"Melhor caminho entre {inicio} e {fim}: ")
                        print(f"Caminho: {' -> '.join(caminho)}, Distância: {dist}")

                        # Obter instruções de movimento
                        # for i in range(len(caminho) - 1):
                        # origem, destino = caminho[i], caminho[i + 1]
                        # instrucao = instrucoes_movimento.get((origem, destino))
                        origem, destino = caminho[0], caminho[1]
                        instrucao = instrucoes_movimento.get((origem, destino))
                        print(f'De {origem} para {destino}: {instrucao}')
            else:
                if (
    (inicio == 'E' and prox == 'J' and lugares_bloqueados == 'G' and prox_outro == 'H' and IdE == 1 and prioridade == 2) or
    (inicio == 'E' and prox == 'J' and lugares_bloqueados == 'H' and prox_outro == 'G' and IdE == 1 and prioridade == 2) or
    (inicio == 'E' and prox == 'G' and lugares_bloqueados == 'J' and prox_outro == 'H' and IdE == 1 and prioridade == 2) or
    (inicio == 'E' and prox == 'G' and lugares_bloqueados == 'H' and prox_outro == 'J' and IdE == 1 and prioridade == 2) or
    (inicio == 'E' and prox == 'H' and lugares_bloqueados == 'G' and prox_outro == 'J' and IdE == 1 and prioridade == 2) or
    (inicio == 'E' and prox == 'H' and lugares_bloqueados == 'J' and prox_outro == 'G' and IdE == 1 and prioridade == 2) or
    (inicio == 'J' and prox == 'E' and lugares_bloqueados == 'G' and prox_outro == 'H' and IdE == 1 and prioridade == 2) or
    (inicio == 'J' and prox == 'E' and lugares_bloqueados == 'H' and prox_outro == 'G' and IdE == 1 and prioridade == 2) or
    (inicio == 'J' and prox == 'G' and lugares_bloqueados == 'E' and prox_outro == 'H' and IdE == 1 and prioridade == 2) or
    (inicio == 'J' and prox == 'G' and lugares_bloqueados == 'H' and prox_outro == 'E' and IdE == 1 and prioridade == 2) or
    (inicio == 'J' and prox == 'H' and lugares_bloqueados == 'E' and prox_outro == 'G' and IdE == 1 and prioridade == 2) or
    (inicio == 'J' and prox == 'H' and lugares_bloqueados == 'G' and prox_outro == 'E' and IdE == 1 and prioridade == 2) or
    (inicio == 'G' and prox == 'E' and lugares_bloqueados == 'H' and prox_outro == 'J' and IdE == 1 and prioridade == 2) or
    (inicio == 'G' and prox == 'E' and lugares_bloqueados == 'J' and prox_outro == 'H' and IdE == 1 and prioridade == 2) or
    (inicio == 'G' and prox == 'H' and lugares_bloqueados == 'J' and prox_outro == 'E' and IdE == 1 and prioridade == 2) or
    (inicio == 'G' and prox == 'H' and lugares_bloqueados == 'E' and prox_outro == 'J' and IdE == 1 and prioridade == 2) or
    (inicio == 'G' and prox == 'J' and lugares_bloqueados == 'E' and prox_outro == 'H' and IdE == 1 and prioridade == 2) or
    (inicio == 'G' and prox == 'J' and lugares_bloqueados == 'H' and prox_outro == 'E' and IdE == 1 and prioridade == 2) or
    (inicio == 'H' and prox == 'J' and lugares_bloqueados == 'G' and prox_outro == 'E' and IdE == 1 and prioridade == 2) or
    (inicio == 'H' and prox == 'J' and lugares_bloqueados == 'E' and prox_outro == 'G' and IdE == 1 and prioridade == 2) or
    (inicio == 'H' and prox == 'E' and lugares_bloqueados == 'J' and prox_outro == 'G' and IdE == 1 and prioridade == 2) or
    (inicio == 'H' and prox == 'E' and lugares_bloqueados == 'G' and prox_outro == 'J' and IdE == 1 and prioridade == 2) or
    (inicio == 'H' and prox == 'G' and lugares_bloqueados == 'E' and prox_outro == 'J' and IdE == 1 and prioridade == 2) or
    (inicio == 'H' and prox == 'G' and lugares_bloqueados == 'J' and prox_outro == 'E' and IdE == 1 and prioridade == 2) or
    (inicio == 'E' and prox == 'J' and lugares_bloqueados == 'G' and prox_outro == 'H' and IdE == 2 and prioridade == 1) or
    (inicio == 'E' and prox == 'J' and lugares_bloqueados == 'H' and prox_outro == 'G' and IdE == 2 and prioridade == 1) or
    (inicio == 'E' and prox == 'G' and lugares_bloqueados == 'J' and prox_outro == 'H' and IdE == 2 and prioridade == 1) or
    (inicio == 'E' and prox == 'G' and lugares_bloqueados == 'H' and prox_outro == 'J' and IdE == 2 and prioridade == 1) or
    (inicio == 'E' and prox == 'H' and lugares_bloqueados == 'G' and prox_outro == 'J' and IdE == 2 and prioridade == 1) or
    (inicio == 'E' and prox == 'H' and lugares_bloqueados == 'J' and prox_outro == 'G' and IdE == 2 and prioridade == 1) or
    (inicio == 'J' and prox == 'E' and lugares_bloqueados == 'G' and prox_outro == 'H' and IdE == 2 and prioridade == 1) or
    (inicio == 'J' and prox == 'E' and lugares_bloqueados == 'H' and prox_outro == 'G' and IdE == 2 and prioridade == 1) or
    (inicio == 'J' and prox == 'G' and lugares_bloqueados == 'E' and prox_outro == 'H' and IdE == 2 and prioridade == 1) or
    (inicio == 'J' and prox == 'G' and lugares_bloqueados == 'H' and prox_outro == 'E' and IdE == 2 and prioridade == 1) or
    (inicio == 'J' and prox == 'H' and lugares_bloqueados == 'E' and prox_outro == 'G' and IdE == 2 and prioridade == 1) or
    (inicio == 'J' and prox == 'H' and lugares_bloqueados == 'G' and prox_outro == 'E' and IdE == 2 and prioridade == 1) or
    (inicio == 'G' and prox == 'E' and lugares_bloqueados == 'H' and prox_outro == 'J' and IdE == 2 and prioridade == 1) or
    (inicio == 'G' and prox == 'E' and lugares_bloqueados == 'J' and prox_outro == 'H' and IdE == 2 and prioridade == 1) or
    (inicio == 'G' and prox == 'H' and lugares_bloqueados == 'J' and prox_outro == 'E' and IdE == 2 and prioridade == 1) or
    (inicio == 'G' and prox == 'H' and lugares_bloqueados == 'E' and prox_outro == 'J' and IdE == 2 and prioridade == 1) or
    (inicio == 'G' and prox == 'J' and lugares_bloqueados == 'E' and prox_outro == 'H' and IdE == 2 and prioridade == 1) or
    (inicio == 'G' and prox == 'J' and lugares_bloqueados == 'H' and prox_outro == 'E' and IdE == 2 and prioridade == 1) or
    (inicio == 'H' and prox == 'J' and lugares_bloqueados == 'G' and prox_outro == 'E' and IdE == 2 and prioridade == 1) or
    (inicio == 'H' and prox == 'J' and lugares_bloqueados == 'E' and prox_outro == 'G' and IdE == 2 and prioridade == 1) or
    (inicio == 'H' and prox == 'E' and lugares_bloqueados == 'J' and prox_outro == 'G' and IdE == 2 and prioridade == 1) or
    (inicio == 'H' and prox == 'E' and lugares_bloqueados == 'G' and prox_outro == 'J' and IdE == 2 and prioridade == 1) or
    (inicio == 'H' and prox == 'G' and lugares_bloqueados == 'E' and prox_outro == 'J' and IdE == 2 and prioridade == 1) or
    (inicio == 'H' and prox == 'G' and lugares_bloqueados == 'J' and prox_outro == 'E' and IdE == 2 and prioridade == 1) 
):
                    print("Espere pela outra empilhadeira para continuar")
                else:
                    melhor_caminho = encontrar_menor_caminho_com_instrucoes(grafo, inicio, fim, lugares_bloqueados, posicao_anterior)
                    if melhor_caminho:
                        dist, caminho = melhor_caminho
                        print(f"Melhor caminho entre {inicio} e {fim}: ")
                        print(f"Caminho: {' -> '.join(caminho)}, Distância: {dist}")

                        # Obter instruções de movimento
                        # for i in range(len(caminho) - 1):
                        # origem, destino = caminho[i], caminho[i + 1]
                        # instrucao = instrucoes_movimento.get((origem, destino))
                        origem, destino = caminho[0], caminho[1]
                        instrucao = instrucoes_movimento.get((origem, destino))
                        print(f'De {origem} para {destino}: {instrucao}')
    
            

# Identificação de empilhadeiras
IdE1 = 1
IdE2 = 2
# Informações de inicio e fim de movimentações

inicio1 = input(f"Informe posição inicial {IdE1}: ")
posicao_anterior1 = input(f"Informe posição anterior {IdE1}: ")
fim1 = input(f"Informe posição final {IdE1}: ")
inicio2 = input(f"Informe posição inicial {IdE2}: ")
posicao_anterior2 = input(f"Informe posição anterior {IdE2}: ")
fim2 = input(f"Informe posição final {IdE2}: ")
# Prioridade de 0 a 1  -> a maior prioridade é a que espera no lugar e a outra que mude sua rota
# #Se tiverem a mesma prioridade escolha pela menor distancia
prioridade1 = 1
prioridade2 = 0

# Lógica de prioridade

if prioridade1 > prioridade2:
    prioridade = 1
elif prioridade1 < prioridade2:
    prioridade = 2
else:
    prioridade = 0

# Verifique se a posição inicial é igual à posição final
lugares_bloqueados1 = inicio2
lugares_bloqueados2 = inicio1

[dist1, caminho1] = encontrar_menor_caminho(grafo, inicio1, fim1,posicao_anterior1)

      
[dist2, caminho2] = encontrar_menor_caminho(grafo, inicio2, fim2,posicao_anterior2)


encontrar_e_navegar(inicio1, fim1, lugares_bloqueados1,prioridade, dist1, dist2, caminho1,caminho2, IdE1,posicao_anterior1)

encontrar_e_navegar(inicio2, fim2, lugares_bloqueados2,prioridade, dist1, dist2, caminho2,caminho1, IdE2,posicao_anterior2)
