import numpy as np
import cv2
import glob

# Tamanho do tabuleiro de calibração
num_cols = 9
num_rows = 6

print("Versão do OpenCV:", cv2.__version__)

# Preparar pontos de objeto, como (0,0,0), (1,0,0), (2,0,0) ..., (8,5,0)
objp = np.zeros((num_rows*num_cols, 3), np.float32)
objp[:, :2] = np.mgrid[0:num_cols, 0:num_rows].T.reshape(-1, 2)

# Arrays para armazenar pontos de objeto e pontos de imagem de todas as imagens
objpoints = [] # Pontos 3D no espaço do mundo real
imgpoints = [] # Pontos 2D no plano da imagem

# Carregar imagens de calibração
images = glob.glob('c:\Users\UFSC\Desktop\Projeto PE brunao\calibracao/*.jpg') # Coloque suas imagens de calibração aqui
print (images)
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Encontrar cantos do tabuleiro de calibração
    ret, corners = cv2.findChessboardCorners(gray, (num_cols, num_rows), None)

    # Se encontrou, adicione pontos de objeto e pontos de imagem
    if ret == True:
        objpoints.append(objp)
        imgpoints.append(corners)

        # Desenhe e mostre os cantos
        img = cv2.drawChessboardCorners(img, (num_cols, num_rows), corners, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500) # Aguarde meio segundo

cv2.destroyAllWindows()

# Calibrar a câmera
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Salvar os parâmetros da câmera
np.savez('calibracao_camera.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

print("Matriz da câmera (mtx):")
print(mtx)
print("\nCoeficientes de distorção (dist):")
print(dist)

