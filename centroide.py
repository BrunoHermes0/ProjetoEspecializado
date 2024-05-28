import cv2
import numpy as np

def select_color(event, x, y, flags, param):
    global hsv_color
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_color = cv2.cvtColor(np.uint8([[frame[y, x]]]), cv2.COLOR_BGR2HSV)
        detect_centroid(frame)

def detect_centroid(image):
    # Definir uma margem de tolerância para a cor selecionada
    tolerance = 10
    
    # Extrair os valores HSV da cor selecionada
    h, s, v = hsv_color[0][0]

    # Definir o intervalo de cor com base na cor selecionada e na tolerância
    lower_color = np.array([h - tolerance, 100, 100])
    upper_color = np.array([h + tolerance, 255, 255])

    # Converter a imagem para o espaço de cor HSV
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Criar uma máscara binária usando o intervalo de cor definido
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)

    # Encontrar contornos na máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Inicializar variável para o centroide
    centroid = None

    # Encontrar o centroide da região correspondente à cor selecionada
    if contours:
        contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centroid = (cx, cy)

    # Desenhar o centroide na imagem
    if centroid is not None:
        cv2.circle(image, centroid, 5, (255, 0, 0), -1)

    # Exibir a imagem com o centroide
    cv2.imshow('Centroid Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Carregar a imagem
frame = cv2.imread('teste123.jpg')

# Exibir a imagem
cv2.imshow('Frame', frame)

# Definir uma função de retorno de chamada do mouse para capturar cliques do mouse
cv2.setMouseCallback('Frame', select_color)

# Aguardar até que uma tecla seja pressionada
cv2.waitKey(0)
