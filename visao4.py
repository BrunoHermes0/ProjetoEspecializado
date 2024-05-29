import cv2
import numpy as np

def get_hsv_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        color = hsv[y, x]
        print("Cor HSV:", color)

# Carregar a imagem
image = cv2.imread('test34.jpg')

# Mostrar a imagem
cv2.imshow('Imagem', image)

# Definir a função de callback para capturar o clique do mouse
cv2.setMouseCallback('Imagem', get_hsv_color)

# Aguardar por uma tecla ser pressionada e depois fechar a janela
cv2.waitKey(0)
cv2.destroyAllWindows()
