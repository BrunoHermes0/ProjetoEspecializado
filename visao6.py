import cv2
import numpy as np

def detect_front_and_rear(image):
    # Definir uma margem de tolerância para a cor selecionada
    tolerance = 10
    
    # Extrair os valores HSV da cor selecionada
    hsv_color = [115,171,249]
    h = 105
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

    # Encontrar a menor área correspondente à parte frontal e traseira do robô
    min_front_area = float('inf')
    min_rear_area = float('inf')
    if contours:
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Filtro de área mínima para evitar ruídos
                rect = cv2.minAreaRect(contour)
                center, size, angle = rect
                width, height = size
                if width < height:
                    if area < min_rear_area:
                        min_rear_area = area
                        rear_area = contour
                else:
                    if area < min_front_area:
                        min_front_area = area
                        front_area = contour

    # Desenhar contornos na imagem original para a parte frontal e traseira do robô
    if front_area is not None:
        cv2.drawContours(image, [front_area], -1, (0, 255, 0), 2)
    if rear_area is not None:
        cv2.drawContours(image, [rear_area], -1, (0, 0, 255), 2)

    # Calcular o ângulo de orientação da parte frontal do robô
    if front_area is not None:
        rect = cv2.minAreaRect(front_area)
        angle = rect[2]
        angle_text = f'Angle: {angle:.2f} degrees'
        cv2.putText(image, angle_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Exibir a imagem com os contornos identificados e o ângulo calculado
    cv2.imshow('Front and Rear Detection', image)
    

# Iniciar a captura de vídeo da câmera
cap = cv2.VideoCapture(0)

while True:
    # Capturar um quadro da câmera
    ret, frame = cap.read()
    if not ret:
        break

    # Chamar a função para detectar a parte frontal e traseira do robô
    detect_front_and_rear(frame)

    # Verificar se o usuário pressionou a tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
