import cv2

# Numero de linhas e colunas
num_cols = 6
num_rows = 9

# Carregar uma imagem
img = cv2.imread('c:/Users/UFSC/Desktop/ProjetoPeBrunao/calibracao/teste2.jpg')

# Converter para escala de cinza
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Experimente diferentes métodos de detecção de cantos
methods = [cv2.CALIB_CB_ADAPTIVE_THRESH, cv2.CALIB_CB_FAST_CHECK]

for method in methods:
    # Encontrar cantos do tabuleiro de calibração
    ret, corners = cv2.findChessboardCorners(gray, (num_cols, num_rows), None, flags=method)

    # Se encontrou, desenhe os cantos
    if ret == True:
        # Refinar os cantos detectados
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1))
        
        img_with_corners = cv2.drawChessboardCorners(img.copy(), (num_cols, num_rows), corners, ret)
        cv2.imshow('Cantos Detectados', img_with_corners)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        break
else:
    print("Cantos não detectados nesta imagem.")
