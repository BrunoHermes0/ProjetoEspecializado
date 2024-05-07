import cv2

# Definir o tamanho dos quadrados e as letras para cada coluna
square_width = 91
square_height = 95
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
rows = range(1, 6)

# Função para desenhar uma grade de quadrados 7x5 na imagem e adicionar letras para identificar as colunas e números para identificar as linhas
def draw_square_grid(image):
    for i in range(len(rows)):
        for j in range(len(columns)):
            start_x = j * square_width
            start_y = i * square_height
            end_x = start_x + square_width
            end_y = start_y + square_height
            cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), thickness=2)
            # Adicionar letras para identificar as colunas
            cv2.putText(image, columns[j], (start_x + 25, start_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 1, 1), 2)
            # Adicionar números para identificar as linhas
            cv2.putText(image, str(rows[i]), (start_x + 45, start_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 1, 1), 2)

# Carregar a imagem
image = cv2.imread('teste14.jpg')

# Verificar se a imagem foi carregada corretamente
if image is None:
    print("Erro ao carregar a imagem.")
    exit()

# Desenhar a grade de quadrados na imagem e adicionar letras e números
draw_square_grid(image)

# Exibir a imagem
cv2.imshow('Rotulamento de coordenadas', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
