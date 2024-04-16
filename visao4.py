import numpy as np
import cv2

# Carregar parâmetros da câmera
calibration_data = np.load('camera_calibration.npz')
mtx, dist = calibration_data['mtx'], calibration_data['dist']

# Função para mapear pontos do mundo real para pixels na imagem
def map_world_to_pixels(world_points):
    # Converter os pontos do mundo real para coordenadas da imagem
    image_points, _ = cv2.projectPoints(world_points, np.zeros((3,1)), np.zeros((3,1)), mtx, dist)
    return np.squeeze(image_points)

# Definir os pontos no mundo real que você deseja mapear para pixels na imagem
# Por exemplo, um quadrado de 10x10 cm
world_square_points = np.array([[0, 0, 0], [0.1, 0, 0], [0.1, 0.1, 0], [0, 0.1, 0]], dtype=np.float32)

# Mapear os pontos do mundo real para pixels na imagem
pixel_coordinates = map_world_to_pixels(world_square_points)

# Arredondar as coordenadas dos pixels
pixel_coordinates = np.round(pixel_coordinates).astype(np.int)

print("Coordenadas dos pixels na imagem:")
print(pixel_coordinates)
