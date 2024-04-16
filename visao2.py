import numpy as np

# Carregar o arquivo de calibração
calibration_data = np.load('calibration_results.npz')

# Verificar as chaves presentes no arquivo
print(calibration_data.keys())
