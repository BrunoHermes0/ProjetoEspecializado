import cv2
import numpy as np

def select_color(event, x, y, flags, param):
    global hsv_color
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_color = cv2.cvtColor(np.uint8([[frame[y, x]]]), cv2.COLOR_BGR2HSV)

def detect_front_and_rear(image):
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

    # Inicializar variáveis para a parte frontal e traseira do robô
    front_area = None
    rear_area = None

    # Encontrar a maior área correspondente à parte frontal e traseira do robô
    max_front_area = 0
    max_rear_area = 0
    if contours:
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1:  # Filtro de área mínima para evitar ruídos
                rect = cv2.minAreaRect(contour)
                center, size, angle = rect
                width, height = size
                if width < height:
                    if area > max_rear_area:
                        max_rear_area = area
                        rear_area = contour
                else:
                    if area > max_front_area:
                        max_front_area = area
                        front_area = contour

    # Desenhar contornos na imagem original para a parte frontal e traseira do robô
    if front_area is not None:
        cv2.drawContours(image, [front_area], -1, (0, 255, 0), 2)
    if rear_area is not None:
        cv2.drawContours(image, [rear_area], -1, (0, 0, 255), 2)

    # Exibir a imagem com os contornos identificados
    cv2.imshow('Front and Rear Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Carregar a imagem
frame = cv2.imread('teste4.jpg')

# Exibir a imagem
cv2.imshow('Frame', frame)

# Definir uma função de retorno de chamada do mouse para capturar cliques do mouse
cv2.setMouseCallback('Frame', select_color)

# Aguardar até que uma tecla seja pressionada
cv2.waitKey(0)

# Chamar a função para detectar a parte frontal e traseira do robô
detect_front_and_rear(frame)