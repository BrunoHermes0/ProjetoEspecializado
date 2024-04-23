import cv2

# Função para desenhar uma grade de quadrados 7x5 na imagem
def draw_square_grid(image):
    largura_size = 91
    altura_size = 95
    num_rows = 5
    num_cols = 7
    for i in range(num_rows):
        for j in range(num_cols):
            start_x = j * largura_size
            start_y = i * altura_size
            end_x = start_x + largura_size
            end_y = start_y + altura_size
            cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), thickness=2)

# Carregar a imagem
image = cv2.imread('testeMapa2.jpg')

# Verificar se a imagem foi carregada corretamente
if image is None:
    print("Erro ao carregar a imagem.")
    exit()

# Desenhar a grade de quadrados na imagem
draw_square_grid(image)

# Exibir a imagem
cv2.imshow('Imagem', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
