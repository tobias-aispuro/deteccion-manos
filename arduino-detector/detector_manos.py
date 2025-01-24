import cv2
import mediapipe as mp
from math import dist, acos, degrees
import time
import serial

arduino = serial.Serial('COM3', 9600)  

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

def coord_x(marcador):
    return results.multi_hand_landmarks[0].landmark[marcador].x

def coord_y(marcador):
    return results.multi_hand_landmarks[0].landmark[marcador].y

def calcular_angulo(x1, y1, x2, y2, x3, y3):
    angulo = acos(((x2 - x1) * (x3 - x2) + (y2 - y1) * (y3 - y2)) /
                  (dist([x1, y1], [x2, y2]) * dist([x2, y2], [x3, y3])))
    return degrees(angulo)

    # Coordenada de cada dedo según la imagen
dedos = {
    "pulgar": [2, 4],  
    "indice": [6, 8],
    "anular": [10, 12],
    "mayor": [14, 16],
    "menique": [18, 20]
}

def detectarDedo():
    if results.multi_hand_landmarks:
        try:
            x_palma = coord_x(0)
            y_palma = coord_y(0)
            cerrados = []

            # Para los dedos normales (índice, anular, mayor, meñique)
            for dedo, (medio, punta) in dedos.items():
                x_medio = coord_x(medio)
                y_medio = coord_y(medio)
                x_punta = coord_x(punta)
                y_punta = coord_y(punta)
                
                if dedo != "pulgar":
                    d_medio = dist([x_palma, y_palma], [x_medio, y_medio])
                    d_punta = dist([x_palma, y_palma], [x_punta, y_punta])
                    # Comparar distancias para determinar si el dedo está levantado
                    cerrados.append(1 if d_medio < d_punta else 0)
                else:
                    # Para el pulgar
                    x_punta_base = coord_x(1)  
                    y_punta_base = coord_y(1)
                    angulo_pulgar = calcular_angulo(x_palma, y_palma, x_punta_base, y_punta_base, x_punta, y_punta)
                    # Ajustar el umbral del ángulo para el pulgar
                    umbral_angulo = 60 
                    # Verificar si el pulgar está levantado según el ángulo
                    cerrados.append(1 if angulo_pulgar < umbral_angulo else 0)

            if len(cerrados) > 5:
                cerrados = cerrados[:5]

            return cerrados
        except Exception as e:
            print(f"Error en la detección del dedo: {e}")
            return [0] * 5  # Devolver una lista de 5 ceros si hay un error

# Inicializar la cámara 
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error al abrir la cámara.")
    exit()

while True:
    try:
        ret, frame = cap.read()
        if not ret:
            break

        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

        deteccion = detectarDedo()

        if deteccion is not None:
            # cv2.putText(frame, f"dedos detectados={sum(deteccion)}", (20, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0))
            print(f"Detección: {deteccion}")

            # Crear una cadena de todos los dedos y sus estados
            datos = ''.join([f"{i}{estado}" for i, estado in enumerate(deteccion)])
            arduino.write(bytes(datos + '\n', 'utf-8'))  # Enviar todos los dedos y sus estados en una sola línea

        cv2.imshow('Detección de mano', frame)
        time.sleep(1 / 30)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except Exception as e:
        print(f"Error en el bucle principal: {e}")

cap.release()
cv2.destroyAllWindows()
arduino.close()


