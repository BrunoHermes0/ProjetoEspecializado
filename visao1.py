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
    
    # Encontrando o maior contorno
    maior_contorno = max(contours, key=cv2.contourArea)
    
    # Criando uma máscara contendo apenas o maior componente
    mask_maior_componente = np.zeros_like(mask)
    cv2.drawContours(mask_maior_componente, [maior_contorno], -1, 255, -1)
    
    # Aplicando a máscara à imagem original
    maior_componente = cv2.bitwise_and(image, image, mask=mask_maior_componente)
    
    # Encontrando o centroide do maior componente
    momento_maior = cv2.moments(maior_contorno)
    centroide_maior = (int(momento_maior["m10"] / momento_maior["m00"]), int(momento_maior["m01"] / momento_maior["m00"])) if momento_maior["m00"] != 0 else None
    
    return mask_maior_componente, maior_componente, centroide_maior

# Carregando a imagem
image = cv2.imread("testeee.jpg")

# Encontrando o maior componente vermelho na imagem
mask_maior_vermelho, maior_componente_vermelho, centroide_maior_vermelho = encontrar_maior_componente(image, 'vermelho')

# Encontrando o maior componente azul na imagem
mask_maior_azul, maior_componente_azul, centroide_maior_azul = encontrar_maior_componente(image, 'azul')

# Combinando as máscaras dos maiores componentes
mask_combined = cv2.bitwise_or(mask_maior_vermelho, mask_maior_azul)

# Aplicando a máscara combinada à imagem original
maior_componente_combined = cv2.bitwise_and(image, image, mask=mask_combined)

# Exibindo o maior componente vermelho
cv2.imshow("Maior Componente Vermelho", maior_componente_vermelho)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Exibindo o maior componente azul
cv2.imshow("Maior Componente Azul", maior_componente_azul)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Exibindo o maior componente combinado
cv2.imshow("Maior Componente Combinado", maior_componente_combined)
cv2.waitKey(0)
cv2.destroyAllWindows()
