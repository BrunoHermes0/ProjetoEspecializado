from flask import Flask, request, jsonify
import heapq
import json
from flask_cors import CORS  # Importe o módulo CORS

app = Flask(_name_)
CORS(app)  # Adicione esta linha para habilitar o CORS
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


P = 0 
I = 0
D = 0   
# Parâmetros do sistema 
Kp = 2.2  # Ganho proporcional 1.2
Ki = 0.0  # Ganho integral0.00002
Kd = 0.5 # Ganho derivativo 0.9
aux = 0
lastError = 0 
beta = 0
posicao_anterior = 0
basespeeda = 170
basespeedb = 170
maxspeeda = 230  # Máxima velocidade roda a
maxspeedb = 230  # Máxima velocidade roda b   
pid = []
error = []

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
caminho_proximo_emp2 = 'z'
caminho_proximo_emp1 = 'z'
dist_1 = 10
dist_2 = 10
prioridade1 = 0
prioridade2 = 0
angulo_atual = 0

dados_json2 = [
    {
        "atual": "A1",
        "intermed": "B1",
        "proxima": "B2"
    },
    {
        "atual": "A1",
        "intermed": "B1",
        "proxima": "C1"
    },
    {
        "atual": "B1",
        "intermed": "A1",
        "proxima": "A1"
    },
    {
        "atual": "B1",
        "intermed": "B2",
        "proxima": "B2"
    },
    {
        "atual": "B1",
        "intermed": "C1",
        "proxima": "C1"
    },
    {
        "atual": "C1",
        "intermed": "B1",
        "proxima": "A1"
    },
    {
        "atual": "C1",
        "intermed": "B1",
        "proxima": "B2"
    },
    {
        "atual": "C1",
        "intermed": "D1",
        "proxima": "E1"
    },
    {
        "atual": "C1",
        "intermed": "D1",
        "proxima": "D2"
    },
    {
        "atual": "D1",
        "intermed": "C1",
        "proxima": "C1"
    },
    {
        "atual": "D1",
        "intermed": "D2",
        "proxima": "D2"
    },
    {
        "atual": "D1",
        "intermed": "E1",
        "proxima": "E1"
    },
    {
        "atual": "E1",
        "intermed": "D1",
        "proxima": "C1"
    },
    {
        "atual": "E1",
        "intermed": "D1",
        "proxima": "D2"
    },
    {
        "atual": "E1",
        "intermed": "F1",
        "proxima": "G1"
    },
    {
        "atual": "E1",
        "intermed": "F1",
        "proxima": "F2"
    },
    {
        "atual": "F1",
        "intermed": "E1",
        "proxima": "E1"
    },
    {
        "atual": "F1",
        "intermed": "F2",
        "proxima": "F2"
    },
    {
        "atual": "F1",
        "intermed": "G1",
        "proxima": "G1"
    },
    {
        "atual": "G1",
        "intermed": "F1",
        "proxima": "E1"
    },
    {
        "atual": "G1",
        "intermed": "F1",
        "proxima": "F2"
    },
    {
        "atual": "B2",
        "intermed": "B1",
        "proxima": "A1"
    },
    {
        "atual": "B2",
        "intermed": "B1",
        "proxima": "C1"
    },
    {
        "atual": "B2",
        "intermed": "B3",
        "proxima": "C3"
    },
    {
        "atual": "B2",
        "intermed": "B3",
        "proxima": "B4"
    },
    {
        "atual": "D2",
        "intermed": "D1",
        "proxima": "C1"
    },
    {
        "atual": "D2",
        "intermed": "D1",
        "proxima": "E1"
    },
    {
        "atual": "D2",
        "intermed": "D3",
        "proxima": "C3"
    },
    {
        "atual": "D2",
        "intermed": "D3",
        "proxima": "D4"
    },
    {
        "atual": "D2",
        "intermed": "D3",
        "proxima": "E3"
    },
    {
        "atual": "F2",
        "intermed": "F1",
        "proxima": "E1"
    },
    {
        "atual": "F2",
        "intermed": "F1",
        "proxima": "G1"
    },
    {
        "atual": "F2",
        "intermed": "F3",
        "proxima": "E3"
    },
    {
        "atual": "F2",
        "intermed": "F3",
        "proxima": "F4"
    },
    {
        "atual": "B3",
        "intermed": "B2",
        "proxima": "B2"
    },
    {
        "atual": "B3",
        "intermed": "C3",
        "proxima": "C3"
    },
    {
        "atual": "B3",
        "intermed": "B4",
        "proxima": "B4"
    },
    {
        "atual": "C3",
        "intermed": "B3",
        "proxima": "B2"
    },
    {
        "atual": "C3",
        "intermed": "B3",
        "proxima": "B4"
    },
    {
        "atual": "C3",
        "intermed": "D3",
        "proxima": "D2"
    },
    {
        "atual": "C3",
        "intermed": "D3",
        "proxima": "E3"
    },
    {
        "atual": "C3",
        "intermed": "D3",
        "proxima": "D4"
    },
    {
        "atual": "D3",
        "intermed": "C3",
        "proxima": "C3"
    },
    {
        "atual": "D3",
        "intermed": "D2",
        "proxima": "D2"
    },
    {
        "atual": "D3",
        "intermed": "E3",
        "proxima": "E3"
    },
    {
        "atual": "D3",
        "intermed": "D4",
        "proxima": "D4"
    },
    {
        "atual": "E3",
        "intermed": "D3",
        "proxima": "D2"
    },
    {
        "atual": "E3",
        "intermed": "D3",
        "proxima": "C3"
    },
    {
        "atual": "E3",
        "intermed": "D3",
        "proxima": "D4"
    },
    {
        "atual": "E3",
        "intermed": "F3",
        "proxima": "F2"
    },
    {
        "atual": "E3",
        "intermed": "F3",
        "proxima": "F4"
    },
    {
        "atual": "F3",
        "intermed": "F2",
        "proxima": "F2"
    },
    {
        "atual": "F3",
        "intermed": "E3",
        "proxima": "E3"
    },
    {
        "atual": "F3",
        "intermed": "F4",
        "proxima": "F4"
    },
    {
        "atual": "B4",
        "intermed": "B3",
        "proxima": "B2"
    },
    {
        "atual": "B4",
        "intermed": "B3",
        "proxima": "C3"
    },
    {
        "atual": "B4",
        "intermed": "B5",
        "proxima": "A5"
    },
    {
        "atual": "B4",
        "intermed": "B5",
        "proxima": "C5"
    },
    {
        "atual": "D4",
        "intermed": "D3",
        "proxima": "C3"
    },
    {
        "atual": "D4",
        "intermed": "D3",
        "proxima": "D2"
    },
    {
        "atual": "D4",
        "intermed": "D3",
        "proxima": "E3"
    },
    {
        "atual": "D4",
        "intermed": "D5",
        "proxima": "C5"
    },
    {
        "atual": "D4",
        "intermed": "D5",
        "proxima": "E5"
    },
    {
        "atual": "F4",
        "intermed": "F3",
        "proxima": "E3"
    },
    {
        "atual": "F4",
        "intermed": "F3",
        "proxima": "F2"
    },
    {
        "atual": "F4",
        "intermed": "F5",
        "proxima": "E5"
    },
    {
        "atual": "F4",
        "intermed": "F5",
        "proxima": "G5"
    },
    {
        "atual": "A5",
        "intermed": "B5",
        "proxima": "B4"
    },
    {
        "atual": "A5",
        "intermed": "B5",
        "proxima": "C5"
    },
    {
        "atual": "B5",
        "intermed": "A5",
        "proxima": "A5"
    },
    {
        "atual": "B5",
        "intermed": "B4",
        "proxima": "B4"
    },
    {
        "atual": "B5",
        "intermed": "C5",
        "proxima": "C5"
    },
    {
        "atual": "C5",
        "intermed": "B5",
        "proxima": "A5"
    },
    {
        "atual": "C5",
        "intermed": "B5",
        "proxima": "B4"
    },
    {
        "atual": "C5",
        "intermed": "D5",
        "proxima": "D4"
    },
    {
        "atual": "C5",
        "intermed": "D5",
        "proxima": "E5"
    },
    {
        "atual": "D5",
        "intermed": "C5",
        "proxima": "C5"
    },
    {
        "atual": "D5",
        "intermed": "D4",
        "proxima": "D4"
    },
    {
        "atual": "D5",
        "intermed": "E5",
        "proxima": "E5"
    },
    {
        "atual": "E5",
        "intermed": "D5",
        "proxima": "C5"
    },
    {
        "atual": "E5",
        "intermed": "D5",
        "proxima": "D4"
    },
    {
        "atual": "E5",
        "intermed": "F5",
        "proxima": "F4"
    },
    {
        "atual": "E5",
        "intermed": "F5",
        "proxima": "G5"
    },
    {
        "atual": "F5",
        "intermed": "E5",
        "proxima": "E5"
    },
    {
        "atual": "F5",
        "intermed": "F4",
        "proxima": "F4"
    },
    {
        "atual": "F5",
        "intermed": "G5",
        "proxima": "G5"
    },
    {
        "atual": "G5",
        "intermed": "F5",
        "proxima": "E5"
    },
    {
        "atual": "G5",
        "intermed": "F5",
        "proxima": "F4"
    }
]

dados_json3 = [
    {
        "coord": "A1",
        "caminho": "A"  
    },
    {
        "coord": "C1",
        "caminho": "B"  
    },
    {
        "coord": "E1",
        "caminho": "C"  
    },
    {
        "coord": "G1",
        "caminho": "O"  
    },
    {
        "coord": "B2",
        "caminho": "D"  
    },
    {
        "coord": "D2",
        "caminho": "E"  
    },
    {
        "coord": "F2",
        "caminho": "F"  
    },
    {
        "coord": "C3",
        "caminho": "G"  
    },
    {
        "coord": "E3",
        "caminho": "H"  
    },
    {
        "coord": "B4",
        "caminho": "I"  
    },
    {
        "coord": "D4",
        "caminho": "J"  
    },
    {
        "coord": "F4",
        "caminho": "K"  
    },
    {
        "coord": "A5",
        "caminho": "P"  
    },
    {
        "coord": "C5",
        "caminho": "L"  
    },
    {
        "coord": "E5",
        "caminho": "M"  
    },
    {
        "coord": "G5",
        "caminho": "N"  
    }
]



dados_json = [
    {
        "origem": "A1",
        "destino": "B1",
        "angulo": 0
    },
    {
        "origem": "A5",
        "destino": "B5",
        "angulo": 0
    },
    {
        "origem": "B1",
        "destino": "A1",
        "angulo": 180
    },
    {
        "origem": "B1",
        "destino": "B2",
        "angulo": 90
    },
    {
        "origem": "B1",
        "destino": "C1",
        "angulo": 0
    },
    {
        "origem": "B2",
        "destino": "B1",
        "angulo": 270
    },
    {
        "origem": "B2",
        "destino": "B3",
        "angulo": 90
    },
    {
        "origem": "B3",
        "destino": "B2",
        "angulo": 270
    },
    {
        "origem": "B3",
        "destino": "B4",
        "angulo": 90
    },
    {
        "origem": "B3",
        "destino": "C3",
        "angulo": 0
    },
    {
        "origem": "B4",
        "destino": "B3",
        "angulo": 270
    },
    {
        "origem": "B4",
        "destino": "B5",
        "angulo": 90
    },
    {
        "origem": "B5",
        "destino": "A5",
        "angulo": 180
    },
    {
        "origem": "B5",
        "destino": "C5",
        "angulo": 0
    },
    {
        "origem": "B5",
        "destino": "B4",
        "angulo": 270
    },
    {
        "origem": "C1",
        "destino": "B1",
        "angulo": 180
    },
    {
        "origem": "C1",
        "destino": "D1",
        "angulo": 0
    },
    {
        "origem": "C3",
        "destino": "B3",
        "angulo": 180
    },
    {
        "origem": "C3",
        "destino": "D3",
        "angulo": 0
    },
    {
        "origem": "C5",
        "destino": "B5",
        "angulo": 180
    },
    {
        "origem": "C5",
        "destino": "D5",
        "angulo": 0
    },
    {
        "origem": "D1",
        "destino": "C1",
        "angulo": 180
    },
    {
        "origem": "D1",
        "destino": "D2",
        "angulo": 90
    },
    {
        "origem": "D1",
        "destino": "E1",
        "angulo": 0
    },
    {
        "origem": "D2",
        "destino": "D1",
        "angulo": 270
    },
    {
        "origem": "D2",
        "destino": "D3",
        "angulo": 90
    },
    {
        "origem": "D3",
        "destino": "D2",
        "angulo": 270
    },
    {
        "origem": "D3",
        "destino": "E3",
        "angulo": 0
    },
    {
        "origem": "D3",
        "destino": "D4",
        "angulo": 90
    },
    {
        "origem": "D3",
        "destino": "C3",
        "angulo": 180
    },
    {
        "origem": "D4",
        "destino": "D3",
        "angulo": 270
    },
    {
        "origem": "D4",
        "destino": "D5",
        "angulo": 90
    },
    {
        "origem": "D5",
        "destino": "C5",
        "angulo": 180
    },
    {
        "origem": "D5",
        "destino": "E5",
        "angulo": 0
    },
    {
        "origem": "E1",
        "destino": "D1",
        "angulo": 180
    },
    {
        "origem": "E1",
        "destino": "F1",
        "angulo": 0
    },
    {
        "origem": "E3",
        "destino": "D3",
        "angulo": 180
    },
    {
        "origem": "E3",
        "destino": "F3",
        "angulo": 0
    },
    {
        "origem": "E5",
        "destino": "D5",
        "angulo": 180
    },
    {
        "origem": "E5",
        "destino": "F5",
        "angulo": 0
    },
    {
        "origem": "F1",
        "destino": "E1",
        "angulo": 180
    },
    {
        "origem": "F1",
        "destino": "F2",
        "angulo": 90
    },
    {
        "origem": "F1",
        "destino": "G1",
        "angulo": 0
    },
    {
        "origem": "F2",
        "destino": "F1",
        "angulo": 270
    },
    {
        "origem": "F2",
        "destino": "F3",
        "angulo": 90
    },
    {
        "origem": "F3",
        "destino": "F2",
        "angulo": 270
    },
    {
        "origem": "F3",
        "destino": "F4",
        "angulo": 90
    },
    {
        "origem": "F3",
        "destino": "E3",
        "angulo": 180
    },
    {
        "origem": "F4",
        "destino": "F3",
        "angulo": 270
    },
    {
        "origem": "F4",
        "destino": "F5",
        "angulo": 90
    },
    {
        "origem": "F5",
        "destino": "E5",
        "angulo": 180
    },
    {
        "origem": "F5",
        "destino": "G5",
        "angulo": 0
    },
    {
        "origem": "F5",
        "destino": "F4",
        "angulo": 270
    },
    {
        "origem": "G1",
        "destino": "F1",
        "angulo": 180
    },
    {
        "origem": "G5",
        "destino": "F5",
        "angulo": 180
    }
]


def encontrar_angulo_referencia(origem, destino):
    for item in dados_json:
        if item['origem'] == origem and item['destino'] == destino:
            return item['angulo']
    return None  # Retorna None se não encontrar correspondência


@app.route('/calcular_caminho', methods=['POST'])
def calcular_caminho():
    global dist_2  # Declare dist_2 como uma variável global
    global dist_1 # Declare dist_2 como uma variável global
    global caminho_proximo_emp1  # Declare dist_2 como uma variável global
    global caminho_proximo_emp2  # Declare dist_2 como uma variável global
    global prioridade1
    global prioridade2
    global angulo_atual
    proxima_posicao = " "
    data = request.json
    print("-------------------DADOS RECEBIDOS DO SERVIDOR NODE JS------------------------")
    
    print(data)
    print("-------------------------------------------")
    # Extrair parâmetros do JSON enviado pelo server.js
    inicio1 = data.get('posicao_atual')
    fim1 = data.get('positionCode')
    lugares_bloqueados = data.get('caminho_bloqueado')
    prioridadeSTR = data.get('priority')
    posicao_anterior = data.get('posicao_anterior')
    IdESTR = data.get('forkliftNumber',0)
    angulo_atual = data.get('angulo_car')
    
    

    #resultado = []
    IdE = int(IdESTR)
    #print("ID:----------------------")
    #print(IdE)
    #print(type(IdE))
    #print(repr(IdE))
    prioridadeR = int(prioridadeSTR)
    #print((prioridadeR))
    #print("LUGARES BLOQUEADOS--------")
    #print(lugares_bloqueados)

    if prioridade1 > prioridade2:
        prioridade = 1
    elif prioridade1 < prioridade2:
        prioridade = 2
    else:
        prioridade = 0
    resultado = {"erro": "não consegui entrar nas condicoes"}

    inicio, fim, checagem = checa_menor_caminho(inicio1, fim1)
    
    if(checagem == 1):
        [dist1, caminho1] = encontrar_menor_caminho(grafo, inicio, fim, posicao_anterior)
        #print("prints da função encontrar_menor_caminho-------------")
        #print(dist1)
        #print(caminho1)
        #print("------------")
        if IdE == 1:
            if len(caminho1)>1:
                caminho_proximo_emp1 = caminho1[1]
                print(caminho_proximo_emp1)

            else:
                caminho_proximo_emp1 = caminho1[0]
                print(caminho_proximo_emp1)

            dist_1 = dist1
            #print("DADOS DA EMPI 1:")
            #print(dist_1)
            #print(dist_2)
            #print(caminho1)
            #print(caminho_proximo_emp2)
            #print(posicao_anterior)
            prioridade1 = prioridadeR

            resultado = encontrar_e_navegar(inicio, fim, lugares_bloqueados, prioridade, dist_1, dist_2, caminho1, caminho_proximo_emp2, IdE, posicao_anterior)
        if IdE == 2:
            if len(caminho1)>1:
                caminho_proximo_emp2 = caminho1[1]
                #print(caminho_proximo_emp2)
            else:
                caminho_proximo_emp2 = caminho1[0]
                #print(caminho_proximo_emp2)

            dist_2 = dist1
            #print("DADOS DA EMPI 2:")
            #print(dist1)
            #print(dist_1)
            #print(caminho1)
            #print(caminho_proximo_emp1)
            #print(posicao_anterior)
            #prioridade2 = prioridadeR

            resultado = encontrar_e_navegar(inicio, fim, lugares_bloqueados, prioridade, dist1, dist_1, caminho1, caminho_proximo_emp1, IdE, posicao_anterior)

        # Retornar resultados como JSON para o server.js
        #print("Resultado------>")
        #resultado["caminho_completo"] = list(resultado["caminho_completo"])

        ################### dest --- falta pegar do resultado ###################
        

        
        string_proxima_posicao = resultado["ordem_caminho"].copy()
        proxima_posicao = string_proxima_posicao.split(" ")[3]
        #print(proxima_posicao)
        atual, prox = posicao_intermed(inicio,proxima_posicao) #pegar
        angulo_referencia = encontrar_angulo_referencia(atual, prox)
        #add função de pegar novo proximo caminho
        ERRO = angulo_atual - angulo_referencia
        vel_roda1, vel_roda2 = f_PID(ERRO)
        print("----------------RESULTADO JSON:---------------------")
        print(resultado)
        print("-------------------------------------")
        return vel_roda1, vel_roda2
    else:
        atual, prox = posicao_intermed(inicio,proxima_posicao) #pegar
        angulo_referencia = encontrar_angulo_referencia(atual, prox)
        #add função de pegar novo proximo caminho
        ERRO = angulo_atual - angulo_referencia
        vel_roda1, vel_roda2 = f_PID(ERRO)
        ################### dest --- falta pegar do resultado ###################
        
        ################### nao sei oq retorna aqui ###################
        return vel_roda1, velc_roda2
    #return jsonify(resultado)
    

    #pegar proxima posição do json e enviar

    #return jsonify(resultado)

def posicao_intermed(inic, fin):
    for item in dados_json2:
        if item['atual'] == inic and item['proxima'] == fin:
            return item['atual'], item['intermed']
    return None # Retorna None se não encontrar correspondência

def checa_menor_caminho(inicio, fim):
    caminho_inicio = None
    caminho_fim = None

    for item in dados_json3:
        if item['coord'] == inicio:
            caminho_inicio = item['caminho']
        if item['coord'] == fim:
            caminho_fim = item['caminho']

    if caminho_inicio is not None and caminho_fim is not None:
        return caminho_inicio, caminho_fim, 1
    else:
        return inicio, fim, 0


def f_PID(erro_input):
    
    global I, lastError, aux
    #erro2 = beta*posicao_anterior + (1 - beta)*erro_input
    erro2 = erro_input
    P = erro2
    I += erro2
    D = erro2 - lastError
    lastError = erro2
    #posicao_anterior = erro2
        
    motorspeed = (P * Kp + I * Ki + D * Kd) 
    #print(f"PID: {motorspeed}")
    """
    print(f"P: {P}")
    print(f"I: {I}")
    print(f"D: {D}")
    print(f"erro: {erro}")
    """
    #pid.append(motorspeed)
    #error.append(erro_input)
    #np.savetxt('controle.txt', pid)
    #np.savetxt('Saida.txt', error)
        
    #aux += 1
    #print(f"aux: {aux}")
    motorspeeda = basespeeda + motorspeed
    motorspeedb = basespeedb - motorspeed

    if motorspeeda > maxspeeda:
        motorspeeda = maxspeeda
    if motorspeedb > maxspeedb:
        motorspeedb = maxspeedb
    if motorspeeda < 0:
        motorspeeda = 0
    if motorspeedb < 0:
        motorspeedb = 0
        
    velocidade1 = motorspeeda
    velocidade2 = motorspeedb
    
    return velocidade1, velocidade2

def encontrar_menor_caminho_com_instrucoes(grafo, inicio, fim, lugares_bloqueados, posicao_anterior):
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

        for vizinha in sorted(grafo[posicao_atual]):
            if (posicao_anterior == 'A' and posicao_atual == 'B' and (vizinha == 'A' or vizinha == 'D')):
                continue
            elif (posicao_anterior == 'A' and posicao_atual == 'D' and (vizinha == 'A' or vizinha == 'B')):
                continue
            elif (posicao_anterior == 'B' and posicao_atual == 'D' and (vizinha == 'B' or vizinha == 'A')):
                continue
            elif (posicao_anterior == 'B' and posicao_atual == 'C' and (vizinha == 'B' or vizinha == 'E')):
                continue
            elif (posicao_anterior == 'B' and posicao_atual == 'E' and (vizinha == 'B' or vizinha == 'C')):
                continue
            elif (posicao_anterior == 'C' and posicao_atual == 'B' and (vizinha == 'C' or vizinha == 'E')):
                continue
            elif (posicao_anterior == 'C' and posicao_atual == 'E' and (vizinha == 'C' or vizinha == 'B')):
                continue
            elif (posicao_anterior == 'C' and posicao_atual == 'F' and (vizinha == 'C' or vizinha == 'O')):
                continue
            elif (posicao_anterior == 'D' and posicao_atual == 'B' and (vizinha == 'D' or vizinha == 'A')):
                continue
            elif (posicao_anterior == 'D' and posicao_atual == 'G' and (vizinha == 'D' or vizinha == 'I')):
                continue
            elif (posicao_anterior == 'D' and posicao_atual == 'I' and (vizinha == 'D' or vizinha == 'G')):
                continue
            elif (posicao_anterior == 'E' and posicao_atual == 'B' and (vizinha == 'E' or vizinha == 'C')):
                continue
            elif (posicao_anterior == 'E' and posicao_atual == 'C' and (vizinha == 'E' or vizinha == 'B')):
                continue
            elif (posicao_anterior == 'E' and posicao_atual == 'G' and (
                    vizinha == 'E' or vizinha == 'H' or vizinha == 'J')):
                continue
            elif (posicao_anterior == 'E' and posicao_atual == 'H' and (
                    vizinha == 'E' or vizinha == 'G' or vizinha == 'J')):
                continue
            elif (posicao_anterior == 'E' and posicao_atual == 'J' and (
                    vizinha == 'E' or vizinha == 'G' or vizinha == 'H')):
                continue
            elif (posicao_anterior == 'F' and posicao_atual == 'C' and (vizinha == 'F' or vizinha == 'O')):
                continue
            elif (posicao_anterior == 'F' and posicao_atual == 'H' and (vizinha == 'F' or vizinha == 'K')):
                continue
            elif (posicao_anterior == 'F' and posicao_atual == 'K' and (vizinha == 'F' or vizinha == 'H')):
                continue
            elif (posicao_anterior == 'G' and posicao_atual == 'D' and (vizinha == 'G' or vizinha == 'I')):
                continue
            elif (posicao_anterior == 'G' and posicao_atual == 'E' and (
                    vizinha == 'G' or vizinha == 'H' or vizinha == 'J')):
                continue
            elif (posicao_anterior == 'G' and posicao_atual == 'H' and (
                    vizinha == 'G' or vizinha == 'E' or vizinha == 'J')):
                continue
            elif (posicao_anterior == 'G' and posicao_atual == 'I' and (vizinha == 'G' or vizinha == 'D')):
                continue
            elif (posicao_anterior == 'G' and posicao_atual == 'J' and (
                    vizinha == 'G' or vizinha == 'E' or vizinha == 'H')):
                continue
            elif (posicao_anterior == 'H' and posicao_atual == 'E' and (
                    vizinha == 'H' or vizinha == 'G' or vizinha == 'J')):
                continue
            elif (posicao_anterior == 'H' and posicao_atual == 'F' and (vizinha == 'H' or vizinha == 'K')):
                continue
            elif (posicao_anterior == 'H' and posicao_atual == 'G' and (
                    vizinha == 'H' or vizinha == 'E' or vizinha == 'J')):
                continue
            elif (posicao_anterior == 'H' and posicao_atual == 'J' and (
                    vizinha == 'H' or vizinha == 'E' or vizinha == 'G')):
                continue
            elif (posicao_anterior == 'H' and posicao_atual == 'K' and (vizinha == 'H' or vizinha == 'F')):
                continue
            elif (posicao_anterior == 'I' and posicao_atual == 'D' and (vizinha == 'I' or vizinha == 'G')):
                continue
            elif (posicao_anterior == 'I' and posicao_atual == 'G' and (vizinha == 'I' or vizinha == 'D')):
                continue
            elif (posicao_anterior == 'I' and posicao_atual == 'L' and (vizinha == 'I' or vizinha == 'P')):
                continue
            elif (posicao_anterior == 'J' and posicao_atual == 'E' and (
                    vizinha == 'J' or vizinha == 'G' or vizinha == 'H')):
                continue
            elif (posicao_anterior == 'J' and posicao_atual == 'G' and (
                    vizinha == 'J' or vizinha == 'H' or vizinha == 'E')):
                continue
            elif (posicao_anterior == 'J' and posicao_atual == 'H' and (
                    vizinha == 'J' or vizinha == 'G' or vizinha == 'E')):
                continue
            elif (posicao_anterior == 'J' and posicao_atual == 'L' and (vizinha == 'J' or vizinha == 'M')):
                continue
            elif (posicao_anterior == 'J' and posicao_atual == 'M' and (vizinha == 'J' or vizinha == 'L')):
                continue
            elif (posicao_anterior == 'K' and posicao_atual == 'F' and (vizinha == 'K' or vizinha == 'H')):
                continue
            elif (posicao_anterior == 'K' and posicao_atual == 'H' and (vizinha == 'K' or vizinha == 'F')):
                continue
            elif (posicao_anterior == 'K' and posicao_atual == 'M' and (vizinha == 'K' or vizinha == 'N')):
                continue
            elif (posicao_anterior == 'L' and posicao_atual == 'I' and (vizinha == 'L' or vizinha == 'P')):
                continue
            elif (posicao_anterior == 'L' and posicao_atual == 'J' and (vizinha == 'L' or vizinha == 'M')):
                continue
            elif (posicao_anterior == 'L' and posicao_atual == 'M' and (vizinha == 'L' or vizinha == 'J')):
                continue
            elif (posicao_anterior == 'M' and posicao_atual == 'L' and (vizinha == 'M' or vizinha == 'J')):
                continue
            elif (posicao_anterior == 'M' and posicao_atual == 'J' and (vizinha == 'M' or vizinha == 'L')):
                continue
            elif (posicao_anterior == 'M' and posicao_atual == 'K' and (vizinha == 'M' or vizinha == 'N')):
                continue
            elif (posicao_anterior == 'N' and posicao_atual == 'K' and (vizinha == 'N' or vizinha == 'M')):
                continue
            elif (posicao_anterior == 'N' and posicao_atual == 'M' and (vizinha == 'N' or vizinha == 'K')):
                continue
            elif (posicao_anterior == 'O' and posicao_atual == 'C' and (vizinha == 'O' or vizinha == 'F')):
                continue
            elif (posicao_anterior == 'O' and posicao_atual == 'F' and (vizinha == 'O' or vizinha == 'C')):
                continue
            elif (posicao_anterior == 'P' and posicao_atual == 'I' and (vizinha == 'P' or vizinha == 'L')):
                continue
            elif (posicao_anterior == 'P' and posicao_atual == 'L' and (vizinha == 'P' or vizinha == 'I')):
                continue

            else:

                if vizinha in lugares_bloqueados:
                    dist_total = dist_atual + 1000  # Um peso muito alto para caminhos bloqueados
                    if dist_total == 1000:
                        dist_total = 3000

                else:
                    dist_total = dist_atual + 1  # Peso das arestas é 1

                if dist_total < distancia[vizinha]:
                    if dist_total > 1:
                        posicao_anterior = posicao_atual
                        distancia[vizinha] = dist_total
                        heapq.heappush(fila, (dist_total, vizinha, caminho_atual + [posicao_atual]))
                    else:
                        distancia[vizinha] = dist_total
                        heapq.heappush(fila, (dist_total, vizinha, caminho_atual + [posicao_atual]))

    return menor_caminho


def encontrar_menor_caminho(grafo, inicio, fim, posicao_anterior):
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
                heapq.heappush(fila, (dist_total, vizinha, caminho_atual + [posicao_atual]))

    return menor_caminho


def encontrar_e_navegar(inicio, fim, lugares_bloqueados, prioridade, dist1, dist2, caminho_aux, caminho_outro, IdE,
                        posicao_anterior):
    resultado = {}
    resultado['caminho_completo'] = ''
    if inicio == fim:
        resultado["ordem_caminho"] = "Empilhadeira chegou no destino."
        #talvez por um return aq
    else:
        prox_outro = caminho_outro
        #print("PROXIMO DO OUTRO ------------------------------------")
        #print(prox_outro)
        prox = caminho_aux[1]
        #print("MEU CAMINHO PROXIMO")
        #print(prox)

        if prox == lugares_bloqueados:
            if (prioridade == 1 and IdE == 1) or (prioridade == 2 and IdE == 2) or (
                    prioridade == 0 and IdE == 2 and (dist1 > dist2)) or (
                    prioridade == 0 and IdE == 1 and (dist2 > dist1)):
                    resultado["ordem_caminho"] = "Espere pela outra empilhadeira para continuar"
            if (prioridade == 1 and IdE == 2) or (prioridade == 2 and IdE == 1) or (
                    prioridade == 0 and IdE == 2 and (dist2 > dist1)) or (
                    prioridade == 0 and IdE == 1 and (dist1 > dist2)):
                if inicio == 'D' and prox == 'B':
                    resultado["ordem_caminho"] = "De D para A: Vire a esquerda"
                elif inicio == 'B' and prox == 'D':
                    resultado["ordem_caminho"] ="De B para A: Siga reto"
                elif inicio == 'I' and prox == 'L':
                    resultado["ordem_caminho"] =" De I para P: Vire a direita"
                elif inicio == 'L' and prox == 'I':
                    resultado["ordem_caminho"] = "De L para P: Siga reto"
                elif inicio == 'K' and prox == 'M':
                    resultado["ordem_caminho"] = "De K para N: Vire a esquerda"
                elif inicio == 'M' and prox == 'K':
                    resultado["ordem_caminho"] = "De M para N: Siga reto"
                elif inicio == 'F' and prox == 'C':
                    resultado["ordem_caminho"] = "De F para O: Vire a direita"
                elif inicio == 'C' and prox == 'F':
                    resultado["ordem_caminho"] = "De C para O: Siga reto"
                else:

                    melhor_caminho = encontrar_menor_caminho_com_instrucoes(grafo, inicio, fim, lugares_bloqueados,
                                                                            posicao_anterior)

                    if melhor_caminho:
                        dist, caminho = melhor_caminho
                       # print(f"Melhor caminho entre {inicio} e {fim}: ")
                       # print(f"Caminho: {' -> '.join(caminho)}, Distância: {dist}")

                        resultado["caminho_completo"] = set(caminho)
                        resultado["distancia"] = dist

                        # Obter instruções de movimento
                        # for i in range(len(caminho) - 1):
                        # origem, destino = caminho[i], caminho[i + 1]
                        # instrucao = instrucoes_movimento.get((origem, destino))
                        origem, destino = caminho[0], caminho[1]
                        instrucao = instrucoes_movimento.get((origem, destino))
                        #print(f'De {origem} para {destino}: {instrucao}')
                        resultado["ordem_caminho"] = 'De {} para {}: {}'.format(origem, destino, instrucao)



                    else:
                        print(f"Não há caminho possível entre {inicio} e {fim}.")

        else:
            if prox == prox_outro:
                #print("-----------------------------------")
                #print("ENTREI NO IF DO PROXIMO")
                #print("PRIORIDADE 1")
                #print(prioridade1)
                #print("PRIORIDADE 2")
                #print(prioridade2)
                #print("PRIORIDADE")
                #print(prioridade)
                #print(IdE)
                if (prioridade == 1 and IdE == 2) or (prioridade == 2 and IdE == 1) or (
                        prioridade == 0 and IdE == 2 and (dist2 > dist1)) or (
                        prioridade == 0 and IdE == 1 and (dist1 > dist2)):
                        #print("Identifiquei ordem de espera")
                        resultado["ordem_caminho"] = "Espere pela outra empilhadeira para continuar"
                else:
                    melhor_caminho = encontrar_menor_caminho_com_instrucoes(grafo, inicio, fim, lugares_bloqueados,
                                                                            posicao_anterior)
                    #print("ENTREI NO MELHOR CAMINHO AO INVES DE MANDAR ESPERAR")
                    if melhor_caminho:
                        dist, caminho = melhor_caminho
                        #print(f"Melhor caminho entre {inicio} e {fim}: ")
                        #print(f"Caminho: {' -> '.join(caminho)}, Distância: {dist}")
                        resultado["caminho_completo"] = set(caminho)
                        resultado["distancia"] = dist

                        # Obter instruções de movimento
                        # for i in range(len(caminho) - 1):
                        # origem, destino = caminho[i], caminho[i + 1]
                        # instrucao = instrucoes_movimento.get((origem, destino))
                        origem, destino = caminho[0], caminho[1]
                        instrucao = instrucoes_movimento.get((origem, destino))
                        #print(f'De {origem} para {destino}: {instrucao}')
                        resultado["ordem_caminho"] = 'De {} para {}: {}'.format(origem, destino, instrucao)
            else:
                melhor_caminho = encontrar_menor_caminho_com_instrucoes(grafo, inicio, fim, lugares_bloqueados,
                                                                        posicao_anterior)

                if melhor_caminho:
                    dist, caminho = melhor_caminho
                    #print(f"Melhor caminho entre {inicio} e {fim}: ")
                    #print(f"Caminho: {' -> '.join(caminho)}, Distância: {dist}")

                    resultado["caminho_completo"] = set(caminho)
                    resultado["distancia"] = dist

                    # Obter instruções de movimento
                    # for i in range(len(caminho) - 1):
                    # origem, destino = caminho[i], caminho[i + 1]
                    # instrucao = instrucoes_movimento.get((origem, destino))
                    origem, destino = caminho[0], caminho[1]
                    instrucao = instrucoes_movimento.get((origem, destino))
                    resultado["ordem_caminho"] = 'De {} para {}: {}'.format(origem, destino, instrucao)
    resultado["caminho_completo"] = list(resultado["caminho_completo"])
    print("Este aqui é o resultado da funcao encontrar e navegar: ")
    print(resultado)
    return jsonify(resultado)

# Identificação de empilhadeiras
IdE1 = 1
IdE2 = 2

if _name_ == '_main_':
    app.run(port=5001)  # Porta diferente do Flask para evitar conflitos com o server.js

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

[dist1, caminho1] = encontrar_menor_caminho(grafo, inicio1, fim1, posicao_anterior1)

[dist2, caminho2] = encontrar_menor_caminho(grafo, inicio2, fim2, posicao_anterior2)