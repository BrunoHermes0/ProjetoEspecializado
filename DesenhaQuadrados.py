import cv2

# Função para desenhar uma grade de quadrados 7x5 na tela
def draw_square_grid(frame):
    largura_size = 91
    altura_size = 95
    num_rows = 5
    num_cols = 7
    for i in range(num_rows):
        for j in range(num_cols):
            start_x = j *largura_size
            start_y = i * altura_size
            end_x = start_x + largura_size
            end_y = start_y + altura_size
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), thickness=2)

# Iniciar a captura de vídeo da câmera
cap = cv2.VideoCapture(0)

# Definir a resolução desejada (960x720 pixels)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Definir a taxa de quadros desejada (30 FPS)
cap.set(cv2.CAP_PROP_FPS, 30)

# Verificar se a câmera está aberta corretamente
if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

while True:
    # Capturar um quadro da câmera
    ret, frame = cap.read()
    if not ret:
        break

    # Desenhar a grade de quadrados no quadro capturado
    draw_square_grid(frame)

    # Exibir o quadro
    cv2.imshow('Frame', frame)

    # Verificar se o usuário pressionou a tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
