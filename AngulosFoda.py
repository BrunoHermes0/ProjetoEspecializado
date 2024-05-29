import cv2
import numpy as np

def encontrar_maior_componente(image, cor):
    # Convertendo a imagem para o espaço de cores HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
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
    
    # Aplicando a máscara à imagem original
    maior_componente = cv2.bitwise_and(image, image, mask=mask_maior_componente)
    
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

# Carregando a imagem
image = cv2.imread("testeee.jpg")

# Encontrando o maior componente vermelho na imagem
mask_maior_vermelho, maior_componente_vermelho, centroides_vermelhos = encontrar_maior_componente(image, 'vermelho')

# Encontrando o maior componente azul na imagem
mask_maior_azul, maior_componente_azul, centroides_azuis = encontrar_maior_componente(image, 'azul')

# Calculando o ângulo entre os centroides vermelhos
angulo_vermelho = calcular_angulo(centroides_vermelhos[1], centroides_vermelhos[0])

# Calculando o ângulo entre os centroides azuis
angulo_azul = calcular_angulo(centroides_azuis[1], centroides_azuis[0])

# Desenhando os centroides e os vetores na imagem original
cv2.arrowedLine(image, centroides_vermelhos[1], centroides_vermelhos[0], (0, 0, 255), 2)
cv2.putText(image, f"Vermelho: {angulo_vermelho:.2f} ", (centroides_vermelhos[0][0], centroides_vermelhos[0][1] - 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (1, 1, 1), 2)
cv2.arrowedLine(image, centroides_azuis[1], centroides_azuis[0], (255, 0, 0), 2)
cv2.putText(image, f"Azul: {angulo_azul:.2f} ", (centroides_azuis[0][0], centroides_azuis[0][1] - 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (1, 1, 1), 2)

# Exibindo a imagem com os ângulos e os vetores
cv2.imshow("Imagem com Angulos e Vetores", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
