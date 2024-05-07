import cv2
import numpy as np

# Carregar a imagem
image = cv2.imread('teste11.jpg')

# Definir o tamanho dos quadrados e as letras para cada coluna
square_width = 91
square_height = 95
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
rows = range(1, 6)

def draw_square_grid(image):
    for i in range(len(rows)):
        for j in range(len(columns)):
            start_x = j * square_width
            start_y = i * square_height
            end_x = start_x + square_width
            end_y = start_y + square_height
            cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), thickness=2)
            # Adicionar letras para identificar as colunas
            cv2.putText(image, columns[j], (start_x + 25, start_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 1, 1), 2)
            # Adicionar números para identificar as linhas
            cv2.putText(image, str(rows[i]), (start_x + 45, start_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 1, 1), 2)


# Definir a função para converter coordenadas (x, y) em nome de região
def coordenadas_para_regiao(x, y):
    coluna = columns[x // square_width]
    linha = rows[y // square_height]
    return f"{coluna}{linha}"

def detectar_vermelho(frame):
    # Converter o frame para o espaço de cores HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h = 1
    tolerance = 10
    red_mask1 = np.array([h - tolerance, 100, 100])
    red_mask2 = np.array([h + tolerance, 255, 255])

    # Criar uma máscara para a cor vermelha
    mask_vermelho = cv2.inRange(hsv, red_mask1, red_mask2)

    return mask_vermelho

# Função para detectar a cor azul na imagem
def detectar_azul(image):
    # Converter a imagem para o espaço de cores HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h = 110
    tolerance = 20
    blue_mask1 = np.array([h - tolerance, 100, 100])
    blue_mask2 = np.array([h + tolerance, 255, 255])
    
    # Criar uma máscara para a cor azul
    mask_azul = cv2.inRange(hsv, blue_mask1, blue_mask2)

    return mask_azul

# Função para encontrar a maior região
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

# Função para calcular o centróide
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

# Detectar a cor azul e vermelha na imagem
red_mask = detectar_vermelho(image)
blue_mask = detectar_azul(image)

# Encontrar a maior região azul
maior_regiao_azul = encontrar_maior_regiao(blue_mask)
# Encontrar a maior região vermelha
maior_regiao_vermelha = encontrar_maior_regiao(red_mask)

# Calcular os centroides da maior região azul e vermelha
centroide_azul = calcular_centroide(maior_regiao_azul)
centroide_vermelho = calcular_centroide(maior_regiao_vermelha)

# Converter as coordenadas dos centroides para as regiões correspondentes
coordenadas_centroide_azul = coordenadas_para_regiao(centroide_azul[0], centroide_azul[1])
coordenadas_centroide_vermelho = coordenadas_para_regiao(centroide_vermelho[0], centroide_vermelho[1])

# Desenhar a grade de coordenadas
for y in range(0, image.shape[0], square_height):
    cv2.line(image, (0, y), (image.shape[1], y), (0, 255, 0), 1)
for x in range(0, image.shape[1], square_width):
    cv2.line(image, (x, 0), (x, image.shape[0]), (0, 255, 0), 1)

# Desenhar os marcadores dos centroides
if centroide_azul:
    cv2.circle(image, centroide_azul, 5, (1, 1, 1), -1)
if centroide_vermelho:
    cv2.circle(image, centroide_vermelho, 5, (1, 1, 1), -1)

# Imprimir as coordenadas dos centroides
if centroide_azul:
    print(f"AZUL: {coordenadas_centroide_azul}")
if centroide_vermelho:
    print(f"VERMELHO: {coordenadas_centroide_vermelho}")

#draw_square_grid(image)

# Mostrar a imagem com os centroides e a grade de coordenadas
cv2.imshow('Centroides e Grade de Coordenadas', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
