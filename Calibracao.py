import cv2
import os
import numpy as np
import json

# Numero de linhas e colunas
num_cols = 6
num_rows = 6

# Criar a pasta \resultadosCalibracao se ela não existir
if not os.path.exists('c:/Users/UFSC/Desktop/ProjetoPeBrunao/resultadosCalibracao'):
    os.makedirs('c:/Users/UFSC/Desktop/ProjetoPeBrunao/resultadosCalibracao')

# Definindo a lista de letras de "a" a "n"
letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']

# Arrays para armazenar pontos de objeto e pontos de imagem de todas as imagens
objpoints = [] # Pontos 3D no espaço do mundo real
imgpoints = [] # Pontos 2D no plano da imagem
extrinsic_params = []  # Parâmetros extrínsecos (rvecs, tvecs) de cada imagem

for letra in letras:
    img = cv2.imread('c:/Users/UFSC/Desktop/ProjetoPeBrunao/calibracao/{}.jpg'.format(letra))
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
            
            # Adicionar pontos de objeto e pontos de imagem
            objp = np.zeros((num_rows*num_cols, 3), np.float32)
            objp[:, :2] = np.mgrid[0:num_cols, 0:num_rows].T.reshape(-1, 2)
            objpoints.append(objp)
            imgpoints.append(corners)

            img_with_corners = cv2.drawChessboardCorners(img.copy(), (num_cols, num_rows), corners, ret)
            cv2.imshow('Cantos Detectados', img_with_corners)
            cv2.waitKey(500)
            break
else:
    print("Cantos não detectados nesta imagem.")

cv2.destroyAllWindows()

# Calibrar a câmera
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Calcular parâmetros extrínsecos para cada imagem
for objp, corners in zip(objpoints, imgpoints):
    ret, rvec, tvec = cv2.solvePnP(objp, corners, mtx, dist)
    extrinsic_params.append((rvec, tvec))

# Convertendo os arrays NumPy em listas Python
mtx_list = mtx.tolist()
dist_list = dist.tolist()
extrinsic_params_list = [(rvec.tolist(), tvec.tolist()) for rvec, tvec in extrinsic_params]

# Criar um dicionário para armazenar os resultados
calibration_results = {
    "intrinsics": {"mtx": mtx_list, "dist": dist_list},
    "extrinsics": extrinsic_params_list
}

# Salvar os resultados em um arquivo JSON
with open('calibration_results.json', 'w') as json_file:
    json.dump(calibration_results, json_file)

print("Parâmetros intrínsecos (Matriz da câmera):")
print(mtx)
print("\nCoeficientes de distorção:")
print(dist)

print("\nParâmetros extrínsecos (rvecs, tvecs) para cada imagem:")
for i, (rvec, tvec) in enumerate(extrinsic_params, 1):
    print(f"Imagem {i}:")
    print("Vetor de rotação:")
    print(rvec)
    print("Vetor de translação:")
    print(tvec)
    print("")
