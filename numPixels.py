import cv2

# Iniciar a captura de vídeo da câmera
cap = cv2.VideoCapture(0)

# Definir a resolução desejada (960x720 pixels)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Verificar se a câmera está aberta corretamente
if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

while True:
    # Capturar um quadro da câmera
    ret, frame = cap.read()
    if not ret:
        break

    # Obter a altura e largura do quadro capturado
    height, width, _ = frame.shape

    # Exibir a altura e largura do quadro em tempo real
    print(f"Altura: {height} pixels, Largura: {width} pixels")

    # Exibir o quadro
    cv2.imshow('Frame', frame)

    # Verificar se o usuário pressionou a tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

