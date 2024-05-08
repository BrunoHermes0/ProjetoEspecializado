import cv2
import numpy as np

def encontrar_maior_componente(frame, cor):
    # Convertendo o frame para o espaço de cores HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Definindo os intervalos de cor para a cor especificada em HSV
    if cor == 'vermelho':
        lower_color = np.array([0, 100, 100])
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

def detectar_vermelho(frame):
    # Converter o frame para o espaço de cores HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Definir a faixa de cor vermelha em HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    
    # Criar uma máscara para a cor vermelha
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    return mask

def detectar_azul(frame):
    # Converter o frame para o espaço de cores HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Definir a faixa de cor azul em HSV
    lower_blue = np.array([110, 100, 100])
    upper_blue = np.array([130, 255, 255])
    
    # Criar uma máscara para a cor azul
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    return mask

def encontrar_maior_regiao(mask):
    # Encontrar contornos na máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Inicializar a maior área e o maior contorno
    maior_area = 0
    maior_contorno = None
    
    # Percorrer todos os contornos encontrados
    for contour in contours:
        # Calcular a área do contorno
        area = cv2.contourArea(contour)
        # Se a área for maior que a maior área atual
        if area > maior_area:
            maior_area = area
            maior_contorno = contour
    
    # Retornar a máscara da maior região
    mask_maior_regiao = np.zeros_like(mask)
    cv2.drawContours(mask_maior_regiao, [maior_contorno], -1, (255), thickness=cv2.FILLED)
    
    return mask_maior_regiao

def encontrar_menor_regiao(mask):
    # Encontrar contornos na máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Inicializar a menor área e o menor contorno
    menor_area = float('inf')
    menor_contorno = None
    
    # Percorrer todos os contornos encontrados
    for contour in contours:
        # Calcular a área do contorno
        area = cv2.contourArea(contour)
        # Se a área for menor que a menor área atual
        if area < menor_area:
            menor_area = area
            menor_contorno = contour
    
    # Retornar a máscara da menor região
    mask_menor_regiao = np.zeros_like(mask)
    cv2.drawContours(mask_menor_regiao, [menor_contorno], -1, (255), thickness=cv2.FILLED)
    
    return mask_menor_regiao

def calcular_centroide(mask):
    # Encontrar contornos na máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Inicializar o centroide
    centroide = None
    
    # Se houver contornos encontrados
    if contours:
        # Calcular o momento do contorno
        M = cv2.moments(contours[0])
        
        # Calcular o centroide
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        
        centroide = (cx, cy)
    
    return centroide

# Definir a função para converter coordenadas (x, y) em nome de região
def coordenadas_para_regiao(x1, y1, x2, y2):
    coluna1 = columns[x1 // square_width]
    linha1 = rows[y1 // square_height]
    coluna2 = columns[x2 // square_width]
    linha2 = rows[y2 // square_height]
    if coluna1 == coluna2 and linha1 == linha2:              
        return f"{coluna1}{linha1}"
    else:
        return f"Em movimento"

# Função para aferir a posição dos marcadores vermelho e azul
def aferir_posicao(frame):
    # Detectar a cor vermelha na imagem
    red_mask = detectar_vermelho(frame)
    # Detectar a cor azul na imagem
    blue_mask = detectar_azul(frame)
    
    # Encontrar a maior região vermelha
    maior_regiao_vermelha = encontrar_maior_regiao(red_mask)
    # Encontrar a maior região azul
    maior_regiao_azul = encontrar_maior_regiao(blue_mask)
    
    # Encontrar a menor região azul
    menor_regiao_azul = encontrar_menor_regiao (blue_mask)
    # Encontrar a menor região azul
    menor_regiao_vermelha = encontrar_menor_regiao (red_mask)

    # Calcular os centroides da maior região vermelha e azul
    centroide_vermelho = calcular_centroide(maior_regiao_vermelha)
    centroide_azul = calcular_centroide(maior_regiao_azul)
    
    # Calcular os centroides da menor região azul e vermelha
    centroide_azul_2 = calcular_centroide(menor_regiao_azul)
    centroide_vermelho_2 = calcular_centroide(menor_regiao_vermelha)

   # Converter as coordenadas dos centroides para as regiões correspondentes
    coordenadas_centroide_azul = coordenadas_para_regiao(centroide_azul[0], centroide_azul[1],centroide_azul_2[0],centroide_azul_2[1])
    coordenadas_centroide_vermelho = coordenadas_para_regiao(centroide_vermelho[0], centroide_vermelho[1],centroide_vermelho_2[0],centroide_vermelho_2[1])

    # Imprimir as coordenadas dos centroides
    if coordenadas_centroide_vermelho:
        print(f"Marcador Vermelho: {coordenadas_centroide_vermelho}")
    else:
        print("Nenhum marcador vermelho detectado")
        
    if coordenadas_centroide_azul:
        print(f"Marcador Azul: {coordenadas_centroide_azul}")
    else:
        print("Nenhum marcador azul detectado")


# Definir o tamanho dos quadrados e as letras para cada coluna
square_width = 91
square_height = 95
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
rows = range(1, 5)

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

        # Aferindo a posição dos marcadores vermelho e azul
        aferir_posicao(frame)
    
    # Esperando por 33 milissegundos (aproximadamente 30 frames por segundo) e verificando se a tecla 'q' foi pressionada para sair
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

# Liberando os recursos e fechando todas as janelas
cap.release()
cv2.destroyAllWindows()
