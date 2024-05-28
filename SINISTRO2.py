import cv2
import numpy as np
import requests

posicao_aux = None

# Função para enviar os dados via POST para o web service
def enviar_dados_para_webservice(posicao_carrinhoA, anguloA, posicao_carrinhoV, anguloV):
    url = "http://150.162.206.197:8080/resumo"  # Substitua pela URL do seu web service
    dados = {"pos_carA": posicao_carrinhoA, "ang_carA": anguloA, "pos_carV": posicao_carrinhoV, "ang_carV": anguloV}
    resposta = requests.post(url, json=dados)
    if resposta.status_code == 200:
        print("Dados enviados com sucesso para o web service!")
    else:
        print("Falha ao enviar os dados para o web service:", resposta.status_code)
        
def encontrar_maior_componente(frame, cor):
    # Convertendo o frame para o espaço de cores HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Definindo os intervalos de cor para a cor especificada em HSV
    if cor == 'vermelho':
        lower_color = np.array([1, 100, 100])
        upper_color = np.array([11, 255, 255])
    elif cor == 'azul':
        lower_color = np.array([90, 100, 100])
        upper_color = np.array([130, 255, 255])
    else:
        raise ValueError("Cor inválida")
    
    # Criando a máscara para a cor especificada
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.erode(mask, kernel, iterations=1)
    
    # Encontrando os contornos na máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Encontrando o maior e o segundo maior contorno
    maiores_contornos = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
    
    # Criando uma máscara contendo apenas o maior componente
    mask_maior_componente = np.zeros_like(mask)
    cv2.drawContours(mask_maior_componente, maiores_contornos[0:1], -1, 255, -1)
    
    # Aplicando a máscara ao frame original
    maior_componente = cv2.bitwise_and(frame, frame, mask=mask_maior_componente)
    
    # Encontrando os centroides do maior e do segundo maior componentes
    centroides = []
    for c in maiores_contornos:
        M = cv2.moments(c)
        if M["m00"] != 0:
            centroide = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            centroides.append(centroide)
    
    return mask_maior_componente, maior_componente, centroides

def calcular_angulo(centroide_menor, centroide_maior):
    # Calcula o vetor entre os centroides
    vetor = np.array(centroide_maior) - np.array(centroide_menor)
    
    # Calcula o ângulo entre o vetor e o eixo horizontal
    angulo_rad = np.arctan2(vetor[1], vetor[0])
    angulo_deg = np.degrees(angulo_rad)
    
    # Ajusta o ângulo para estar entre 0 e 360 graus
    if angulo_deg < 0:
        angulo_deg += 360
    
    return angulo_deg

# Definir a função para converter coordenadas (x, y) em nome de região
def coordenadas_para_regiao(x, y):
    global posicao_aux
    coluna = columns[x // square_width]
    linha = rows[y // square_height]

    # Calcular as coordenadas do centro da região
    centro_x = (x // square_width) * square_width + square_width // 2
    centro_y = (y // square_height) * square_height + square_height // 2

    # Verificar se o ponto está dentro da região central de 20x20 pixels
    if (centro_x - 10 <= x <= centro_x + 10) and (centro_y - 10 <= y <= centro_y + 10):
        posicao_aux = f"{coluna}{linha}"
        return posicao_aux
    else:
        return posicao_aux
    
def calcular_ponto_medio(ponto1, ponto2):
    return ((ponto1[0] + ponto2[0]) // 2, (ponto1[1] + ponto2[1]) // 2)
    
# Definir o tamanho dos quadrados e as letras para cada coluna
square_width = 91
square_height = 95
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
rows = range(1, 6)

# Inicializando a captura de vídeo da câmera
cap = cv2.VideoCapture(0)

angulo_vermelho = 0
angulo_azul = 0
frame_count = 0

while True:
    # Lendo o próximo frame da câmera
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1

    if frame_count == 10:  # A cada segundo (considerando 30 frames por segundo)
        frame_count = 0

        # Encontrando o maior componente vermelho no frame
        mask_maior_vermelho, maior_componente_vermelho, centroides_vermelhos = encontrar_maior_componente(frame, 'vermelho')

        # Encontrando o maior componente azul no frame
        mask_maior_azul, maior_componente_azul, centroides_azuis = encontrar_maior_componente(frame, 'azul')

        # Calculando o ângulo entre os centroides vermelhos
        angulo_vermelho = calcular_angulo(centroides_vermelhos[1], centroides_vermelhos[0])
        
        # Calculando o ângulo entre os centroides azuis
        angulo_azul = calcular_angulo(centroides_azuis[1], centroides_azuis[0])

        # Desenhando os centroides e os vetores na imagem original
        cv2.arrowedLine(frame, centroides_vermelhos[1], centroides_vermelhos[0], (0, 0, 255), 2)
        cv2.putText(frame, f"Vermelho: {angulo_vermelho:.2f} ", (centroides_vermelhos[0][0], centroides_vermelhos[0][1] - 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (1, 1, 1), 2)
        cv2.arrowedLine(frame, centroides_azuis[1], centroides_azuis[0], (255, 0, 0), 2)
        cv2.putText(frame, f"Azul: {angulo_azul:.2f} ", (centroides_azuis[0][0], centroides_azuis[0][1] - 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (1, 1, 1), 2)

        # Exibindo o frame com os ângulos e os vetores
        cv2.imshow("Frame com Angulos e Vetores", frame)

        # Imprimindo os ângulos no terminal
        print("Angulo do Vermelho:", angulo_vermelho)
        print("Angulo do Azul:", angulo_azul)

        x_azul1 = centroides_azuis[1][0]
        y_azul1 = centroides_azuis[1][1]
        x_azul2 = centroides_azuis[0][0]
        y_azul2 = centroides_azuis[0][1]
        
        x_vermelho1 = centroides_vermelhos[1][0]
        y_vermelho1 = centroides_vermelhos[1][1]
        x_vermelho2 = centroides_vermelhos[0][0]
        y_vermelho2 = centroides_vermelhos[0][1]
        
        ponto_medio_azul = calcular_ponto_medio(centroides_azuis[1], centroides_azuis[0])
        ponto_medio_vermelho = calcular_ponto_medio(centroides_vermelhos[1], centroides_vermelhos[0])

        # Converter as coordenadas dos centroides para as regiões correspondentes
        coordenadas_centroide_azul = coordenadas_para_regiao(ponto_medio_azul[0], ponto_medio_azul[1])
       
             
        coordenadas_centroide_vermelho = coordenadas_para_regiao(ponto_medio_vermelho[0], ponto_medio_vermelho[1])
        
        # Imprimir as coordenadas dos centroides
        if coordenadas_centroide_vermelho:
            print(f"Marcador Vermelho: {coordenadas_centroide_vermelho}")
        else:
            print("Nenhum marcador vermelho detectado")
        
        if coordenadas_centroide_azul:
            print(f"Marcador Azul: {coordenadas_centroide_azul}")
        else:
            print("Nenhum marcador azul detectado")  
    
    #REVER 
    #enviar_dados_para_webservice(coordenadas_centroide_azul, angulo_azul, coordenadas_centroide_vermelho, angulo_vermelho)
    
    # Esperando por 33 milissegundos (aproximadamente 30 frames por segundo) e verificando se a tecla 'q' foi pressionada para sair
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

# Liberando os recursos e fechando todas as janelas
cap.release()
cv2.destroyAllWindows()
