import cv2

# Função para desenhar uma grade de quadrados 7x5 na imagem
def draw_square_grid(image):
    largura_size = 91
    altura_size = 95
    num_rows = 5
    num_cols = 7
    central_size = 20
    
    for i in range(num_rows):
        for j in range(num_cols):
            start_x = j * largura_size
            start_y = i * altura_size
            end_x = start_x + largura_size
            end_y = start_y + altura_size
            
            # Desenhar região maior em verde
            cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), thickness=2)
            
            # Calcular coordenadas para a região central
            center_start_x = start_x + (largura_size - central_size) // 2
            center_start_y = start_y + (altura_size - central_size) // 2
            center_end_x = center_start_x + central_size
            center_end_y = center_start_y + central_size
            
            # Desenhar contorno da região central em preto
            cv2.rectangle(image, (center_start_x, center_start_y), (center_end_x, center_end_y), (0, 0, 0), thickness=2)
            
            # Calcular e desenhar o ponto central da região central em preto
            centro_x = center_start_x + central_size // 2
            centro_y = center_start_y + central_size // 2
            cv2.circle(image, (centro_x, centro_y), 1, (0, 0, 0), thickness=cv2.FILLED)

# Capturar vídeo da câmera
cap = cv2.VideoCapture(0)

# Verificar se a câmera está aberta corretamente
if not cap.isOpened():
    print("Erro ao acessar a câmera.")
    exit()

while True:
    # Capturar quadro a quadro
    ret, frame = cap.read()
    if not ret:
        print("Não foi possível capturar o quadro.")
        break
    
    # Desenhar a grade de quadrados no quadro
    draw_square_grid(frame)
    
    # Exibir o quadro
    cv2.imshow('Quadro da Câmera', frame)
    
    # Parar o loop se 'q' for pressionado
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a captura e fechar todas as janelas
cap.release()
cv2.destroyAllWindows()
