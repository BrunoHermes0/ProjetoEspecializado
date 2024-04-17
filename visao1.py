import cv2
import json
import numpy as np

# Carregar parâmetros da câmera a partir de um arquivo JSON
with open('calibration_results.json', 'r') as json_file:
    calibration_data = json.load(json_file)

mtx = np.array(calibration_data['intrinsics']['mtx'], dtype=np.float32)
dist = np.array(calibration_data['intrinsics']['dist'], dtype=np.float32)

# Função para detectar posição do objeto
def detect_object_position(image):
    # Corrigir distorção na imagem
    undistorted_img = cv2.undistort(image, mtx, dist, None, mtx)

    # Converter imagem para tons de cinza
    gray = cv2.cvtColor(undistorted_img, cv2.COLOR_BGR2GRAY)

    # Converter imagem para a escala de cores RGB
    rgb = cv2.cvtColor(undistorted_img, cv2.COLOR_BGR2RGB)

    # Definir intervalo de cor verde na escala RGB
    lower_green = np.array([0, 100, 0])
    upper_green = np.array([100, 255, 100])

    # Criar máscara para a cor verde
    mask = cv2.inRange(rgb, lower_green, upper_green)

    # Aplicar operações morfológicas para remover ruídos na máscara
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Encontrar contornos na máscara
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encontrar o contorno com a maior área (presumindo que seja o objeto de interesse)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        # Calcule o centro do contorno
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return (cx, cy)
    return None

# Capturar vídeo da câmera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detectar posição do objeto
    object_position = detect_object_position(frame)

    # Desenhar uma marca na posição do objeto, se detectado
    if object_position:
        cv2.circle(frame, object_position, 5, (0, 255, 0), -1)

    # Exibir o frame
    cv2.imshow('Object Position Detection', frame)

    # Verifique se o usuário pressionou 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
