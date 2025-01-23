import cv2
import mediapipe as mp
# boca

# Inicializamos Mediapipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Configuramos Mediapipe Hands
hands = mp_hands.Hands(static_image_mode=False,               # Para video, debe ser False
                       max_num_hands=2,                      # Número máximo de manos a detectar
                       min_detection_confidence=0.5,         # Confianza mínima para detectar manos
                       min_tracking_confidence=0.5)          # Confianza mínima para rastrear manos

# Capturamos video desde la webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("No se pudo acceder a la cámara.")
        break

    # Convertimos la imagen a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesamos la imagen para detectar manos
    result = hands.process(frame_rgb)

    # Dibujamos las manos detectadas, si existen
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Mostramos el video con las detecciones
    cv2.imshow('Detección de Manos', frame)

    # Salimos si presionamos 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberamos recursos
cap.release()
cv2.destroyAllWindows()
hands.close()


