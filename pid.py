
P = 0 
I = 0
D = 0   
# Parâmetros do sistema 
Kp = 2.2  # Ganho proporcional 1.2
Ki = 0.0  # Ganho integral0.00002
Kd = 0.5 # Ganho derivativo 0.9
aux = 0
lastError = 0 
beta = 0
posicao_anterior = 0
basespeeda = 170
basespeedb = 170
maxspeeda = 230  # Máxima velocidade roda a
maxspeedb = 230  # Máxima velocidade roda b   
pid = []
error = []

def f_PID(erro_input):
    
    global I, lastError, aux
    #erro2 = beta*posicao_anterior + (1 - beta)*erro_input
    erro2 = erro_input
    P = erro2
    I += erro2
    D = erro2 - lastError
    lastError = erro2
    #posicao_anterior = erro2
        
    motorspeed = (P * Kp + I * Ki + D * Kd) 
    #print(f"PID: {motorspeed}")
    """
    print(f"P: {P}")
    print(f"I: {I}")
    print(f"D: {D}")
    print(f"erro: {erro}")
    """
    pid.append(motorspeed)
    error.append(erro_input)
    np.savetxt('controle.txt', pid)
    np.savetxt('Saida.txt', error)
        
    #aux += 1
    #print(f"aux: {aux}")
    motorspeeda = basespeeda + motorspeed
    motorspeedb = basespeedb - motorspeed

    if motorspeeda > maxspeeda:
        motorspeeda = maxspeeda
    if motorspeedb > maxspeedb:
        motorspeedb = maxspeedb
    if motorspeeda < 0:
        motorspeeda = 0
    if motorspeedb < 0:
        motorspeedb = 0
        
    velocidade1 = motorspeeda
    velocidade2 = motorspeedb
    
    return velocidade1, velocidade2













import cv2
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import requests
import math
import matplotlib.pyplot as plt

show_animation = True

P = 0 
I = 0
D = 0   
# Parâmetros do sistema 
Kp = 2.2  # Ganho proporcional 1.2
Ki = 0.0  # Ganho integral0.00002
Kd = 0.5 # Ganho derivativo 0.9
aux = 0
lastError = 0 
beta = 0
posicao_anterior = 0
basespeeda = 170
basespeedb = 170
maxspeeda = 230  # Máxima velocidade roda a
maxspeedb = 230  # Máxima velocidade roda b   
pid = []
error = []

def f_PID(erro_input):
    
    global I, lastError, aux
    #erro2 = beta*posicao_anterior + (1 - beta)*erro_input
    erro2 = erro_input
    P = erro2
    I += erro2
    D = erro2 - lastError
    lastError = erro2
    #posicao_anterior = erro2
        
    motorspeed = (P * Kp + I * Ki + D * Kd) 
    #print(f"PID: {motorspeed}")
    """
    print(f"P: {P}")
    print(f"I: {I}")
    print(f"D: {D}")
    print(f"erro: {erro}")
    """
    pid.append(motorspeed)
    error.append(erro_input)
    np.savetxt('controle.txt', pid)
    np.savetxt('Saida.txt', error)
        
    #aux += 1
    #print(f"aux: {aux}")
    motorspeeda = basespeeda + motorspeed
    motorspeedb = basespeedb - motorspeed

    if motorspeeda > maxspeeda:
        motorspeeda = maxspeeda
    if motorspeedb > maxspeedb:
        motorspeedb = maxspeedb
    if motorspeeda < 0:
        motorspeeda = 0
    if motorspeedb < 0:
        motorspeedb = 0
        
    velocidade1 = motorspeeda
    velocidade2 = motorspeedb
    
    return velocidade1, velocidade2



def main():
    # Configuração da comunicação com a ESP
    esp32_ip = "192.168.4.1"
    url = f"http://{esp32_ip}/receber_info"
    
    # Configuração de entrada do algoritmo A*    
    grid_size = 10.0  
    robot_radius = 55.0
    
    # Início da Câmera
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    
    # Análise da imagem e operações morfológicas
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    kernel = np.ones((3, 3), np.uint8)
    edges_closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(edges_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Matriz lógica dos obstáculos
    height, width = gray.shape
    object_matrix = np.ones((height, width), dtype=np.uint8)    
    
    # Laço dos objetos    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 4000: # Obstáculos
            cv2.drawContours(object_matrix, [contour], -1, 0, thickness=cv2.FILLED)
        if 1100 < area < 1300: # Chegada
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centroid_chegada = (cX, cY)
        if 550 < area < 750: #Centroide dianteiro
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centroid_dianteira = (cX, cY)
    
    # Reconhecimento dos obstáculos    
    oy, ox = np.where(object_matrix == 0)
    oy = height - oy
    ox = ox.tolist()
    oy = oy.tolist()            

    obstacle_border = [(x, 0) for x in range(width)] + \
                      [(x, height - 1) for x in range(width)] + \
                      [(0, y) for y in range(height)] + \
                      [(width - 1, y) for y in range(height)]

    all_obstacles = obstacle_border + list(zip(ox, oy))

    ox, oy = zip(*all_obstacles)

    # Ponto de partida e chegada    
    sx = centroid_dianteira[0]
    sy = height - centroid_dianteira[1]
    gx = centroid_chegada[0]
    gy = height - centroid_chegada[1]  
    
    # Parâmetros de obstáculo partida e chegada para simulação
    if show_animation:
        plt.plot(ox, oy, ".k")
        plt.plot(sx, sy, "og")
        plt.plot(gx, gy, "xb")
        plt.grid(True)
        plt.axis("equal")
        
    # Chamada da função de planejamento A*
    a_star = AStarPlanner(ox, oy, grid_size, robot_radius)    
    rx, ry = a_star.planning(sx, sy, gx, gy)
    
    # Discretização da trajetória
    rx = [rx[i] for i in range(5, len(rx), 4)]
    ry = [ry[i] for i in range(5, len(ry), 4)]
    
    # Garantia que o último ponto é a chegada
    rx.insert(0, centroid_chegada[0])
    ry.insert(0, height - centroid_chegada[1]) 
    
    # Parâmetros de trajetória para simulação    
    if show_animation:  
        plt.plot(rx, ry, "-r")
        plt.pause(0.001)
        plt.show()
    
    # Tratamento da trajetória para orientação da imagem e para inteiros
    rx = [x  for x in rx]
    ry = [height - y  for y in ry]
    
    rx = [round(valor) for valor in rx]
    ry = [round(valor) for valor in ry]
    
    # Inversão da lista e índice 
    rx.reverse()
    ry.reverse()
    
    indice_atual = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Análise da imagem e operações morfológicas
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        kernel = np.ones((3, 3), np.uint8)
        edges_closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(edges_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        # Laço dos objetos    
        contour_image = frame.copy()
        for contour in contours:
            area = cv2.contourArea(contour)   
            if 550 < area < 750: # Centroide dianteiro
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    centroid_dianteira = (cX, cY)
            if 350 < area < 550: # Centroide traseiro
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    centroid_traseira = (cX, cY)
            
        # Calcular a diferença entre os centroides do carrinho
        dx_theta = centroid_dianteira[0] - centroid_traseira[0]
        dy_theta = centroid_dianteira[1] - centroid_traseira[1]            
        
        # Calcular a diferença do ponto atual e centroide traseiro    
        ponto_atual = (rx[indice_atual], ry[indice_atual])

        # Calcular a diferença do ponto atual e centroide traseiro
        dx_phi = ponto_atual[0] - centroid_traseira[0]
        dy_phi = ponto_atual[1] - centroid_traseira[1]

        # Distância euclidiana para ajuste do índice
        if math.sqrt((dx_phi)*2 + (dy_phi)*2) < 50:
            indice_atual += 1
            if indice_atual >= len(rx):
                indice_atual = len(rx) - 1
            
        # Calcular o ângulo theta entre os dois centroides
        angle_rad_theta = np.arctan2(dy_theta, dx_theta)
        angle_deg_theta = np.degrees(angle_rad_theta)
            
        # Calcular o ângulo phi entre os dois centroides
        angle_rad_phi = np.arctan2(dy_phi, dx_phi)
        angle_deg_phi = np.degrees(angle_rad_phi)

        # Calcular o erro entre os ângulos phi e theta
        erro = angle_deg_phi - angle_deg_theta
        
        erro1 = angle_deg_phi - angle_deg_theta
        erro2 = angle_deg_phi + angle_deg_theta
        
        if((abs(erro1) < abs(erro2))):
        # Utilize o ângulo como entrada para o sistema de controle fuzzy
            velocidade1, velocidade2 = fuzzy_control(erro)
        else:
            velocidade1, velocidade2 = fuzzy_control(erro)
            
        # Arredonda os valores para ESP
        velocidade1 = round(velocidade1)
        velocidade2 = round(velocidade2)
            
        # Verifica a distância euclidiana entre o carrinho e a chegada (Condição de parada)
        if math.sqrt((centroid_traseira[0] - centroid_chegada[0])*2 + (centroid_traseira[1] - centroid_chegada[1])*2 ) < 30:
            velocidade1 = 0
            velocidade2 = 0
            
            print(f"Você Chegou!") 
                       
            params = {"motor1SpeedValue": velocidade1, "motor2SpeedValue": velocidade2}  

            try:                
                requests.get(url, params=params)

            except requests.exceptions.RequestException as e:
                print(f"Erro de conexão: {e}")
                
            break
        
        params = {"motor1SpeedValue": velocidade1, "motor2SpeedValue": velocidade2}

        try:            
            requests.get(url, params=params)

        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão: {e}")
        
        # Desenhar uma linha indicando a direção do ângulo theta
        length_theta = 50
        x1_line_theta = int(centroid_dianteira[0] + length_theta * np.cos(angle_rad_theta))
        y1_line_theta = int(centroid_dianteira[1] + length_theta * np.sin(angle_rad_theta))
        
        cv2.line(contour_image, centroid_traseira, (x1_line_theta, y1_line_theta), (0, 0, 255), 1)
        cv2.line(contour_image, centroid_traseira, ponto_atual, (0, 255, 0), 1)
            
        # Exibir ângulos e velocidades
        cv2.putText(contour_image, f"theta: {angle_deg_theta:.2f} degrees", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1, cv2.LINE_AA)
        cv2.putText(contour_image, f"phi: {angle_deg_phi:.2f} degrees", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1, cv2.LINE_AA)
        cv2.putText(contour_image, f"erro: {erro:.2f} degrees", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1, cv2.LINE_AA)
        cv2.putText(contour_image, f"motor_1: {velocidade1} PWM", (200, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1, cv2.LINE_AA)
        cv2.putText(contour_image, f"motor_2: {velocidade2} PWM", (200, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1, cv2.LINE_AA)

        # Exiba o frame
        cv2.imshow("live", contour_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
        
if _name_ == '_main_':
    main()