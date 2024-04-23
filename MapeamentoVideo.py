import cv2
import numpy as np

# Definir o tamanho dos quadrados e as letras para cada coluna
square_width = 91
square_height = 95
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
rows = range(1, 6)

# Definir a função para converter coordenadas (x, y) em nome de região
def coordenadas_para_regiao(x, y):
    coluna = columns[x // square_width]
    linha = rows[y // square_height]
    return f"Região {coluna}{linha}"

# Função para detectar a cor azul no frame
def detectar_azul(frame):
    # Converter o frame para o espaço de cores HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h = 105
    tolerance = 10
    blue_mask1 = np.array([90, 50, 50])
    blue_mask2 = np.array([130, 255, 255])

    # Criar uma máscara para a cor azul
    mask = cv2.inRange(hsv, blue_mask1, blue_mask2)

    return mask

# Iniciar a captura de vídeo da câmera
cap = cv2.VideoCapture(0)

# Verificar se a captura de vídeo foi aberta corretamente
if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

while True:
    # Capturar um frame do vídeo
    ret, frame = cap.read()
    if not ret:
        break

    # Detectar a cor azul no frame
    blue_mask = detectar_azul(frame)

    # Percorrer cada quadrado na grade
    for y in range(0, frame.shape[0], square_height):
        for x in range(0, frame.shape[1], square_width):
            # Extrair a região do quadrado
            quadrado = frame[y:y+square_height, x:x+square_width]
            
            # Verificar se há um pixel branco na região do quadrado
            has_white_pixel = cv2.countNonZero(cv2.cvtColor(quadrado, cv2.COLOR_BGR2GRAY)) > 0
            
            # Se houver um pixel branco, determinar e imprimir a região
            if has_white_pixel:
                # Verificar se o quadrado está na região azul
                if cv2.countNonZero(blue_mask[y:y+square_height, x:x+square_width]) > 0:
                    regiao = coordenadas_para_regiao(x, y)
                    print(f"O pixel branco está na {regiao}, que está na região azul")

    # Exibir o frame
    cv2.imshow('Frame', frame)

    # Verificar se o usuário pressionou a tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

