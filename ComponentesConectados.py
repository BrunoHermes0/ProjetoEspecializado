import cv2
import numpy as np

# Carregar a imagem
image = cv2.imread('teste10.jpg')

# Definir o tamanho dos quadrados e as letras para cada coluna
square_width = 91
square_height = 95
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
rows = range(1, 5)

# Definir a função para converter coordenadas (x, y) em nome de região
def coordenadas_para_regiao(x, y):
    coluna = columns[x // square_width]
    linha = rows[y // square_height]
    return f"Região {coluna}{linha}"

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

# Função para rotular componentes na imagem binária
def rotular_componentes(bin_image):
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bin_image, connectivity=8)
    return num_labels, labels, stats, centroids

# Função para eliminar ruído usando dilatação e erosão
def limpar_ruido(bin_image):
    kernel = np.ones((3, 3), np.uint8)
    dilated_image = cv2.dilate(bin_image, kernel, iterations=1)
    eroded_image = cv2.erode(dilated_image, kernel, iterations=1)
    return eroded_image

# Detectar a cor azul e vermelha na imagem
red_mask = detectar_vermelho(image)
blue_mask = detectar_azul(image)

# Aplicar as máscaras na imagem original
masked_image_red = cv2.bitwise_and(image, image, mask=red_mask)
masked_image_blue = cv2.bitwise_and(image, image, mask=blue_mask)

# Combinar as máscaras para formar uma única máscara
combined_mask = cv2.bitwise_or(red_mask, blue_mask)
cv2.imshow('coyuiui', combined_mask)

# Limpar ruído na imagem binária
cleaned_image = limpar_ruido(combined_mask)

# Rotular os componentes na imagem binária limpa
num_labels, labels, stats, centroids = rotular_componentes(cleaned_image)

# Criar uma imagem de saída com os componentes rotulados
output_image = np.zeros_like(image)

# Para os componentes
for i in range(1, num_labels):
    output_image[labels == i] = np.random.randint(0, 255, size=(3,))
    # Desenhar o número do componente no centro
    centroide_x = int(centroids[i][0])
    centroide_y = int(centroids[i][1])
    cv2.putText(output_image, str(i), (centroide_x, centroide_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Mostrar a imagem com os componentes rotulados
cv2.imshow('Componentes Azuis e Vermelhos', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Imprimir a quantidade de componentes encontrados
print(f"Quantidade de componentes encontrados: {num_labels - 1}")
