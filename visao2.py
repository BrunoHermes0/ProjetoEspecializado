import cv2
import numpy as np

def select_color(event, x, y, flags, param):
    global hsv_color
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_color = cv2.cvtColor(np.uint8([[frame[y, x]]]), cv2.COLOR_BGR2HSV)
        h, s, v = hsv_color[0][0]
        print(f"Cor selecionada em HSV: H={h}, S={s}, V={v}")
         
# Carregar a imagem
frame = cv2.imread('teste4.jpg')

# Exibir a imagem
cv2.imshow('Frame', frame)

# Definir uma função de retorno de chamada do mouse para capturar cliques do mouse
cv2.setMouseCallback('Frame', select_color)

# Aguardar até que uma tecla seja pressionada
cv2.waitKey(0)

# Extrair os valores HSV da cor selecionada
h, s, v = hsv_color[0][0]
print(h)
# Definir uma margem de tolerância para a cor selecionada
tolerance = 10

# Definir o intervalo de cor com base na cor selecionada e na tolerância
lower_color = np.array([h - tolerance, 100, 100])
upper_color = np.array([h + tolerance, 200, 240])

# Converter a imagem para o espaço de cor HSV
hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Criar uma máscara binária usando o intervalo de cor definido
mask = cv2.inRange(hsv_frame, lower_color, upper_color)

# Exibir a máscara binária
cv2.imshow('Mask', mask)

cv2.waitKey(0)
cv2.destroyAllWindows()

