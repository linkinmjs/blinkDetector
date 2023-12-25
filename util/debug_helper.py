import numpy as np
import cv2

# constants
font = cv2.FONT_HERSHEY_PLAIN
max_left_eye = 0
max_right_eye = 0
max_blinking_ratio = 0

def show_helper(left_eye, right_eye, blinking_ratio):
    global max_left_eye, max_right_eye, max_blinking_ratio

    # Actualizar los máximos si los nuevos valores son mayores
    max_left_eye = max(max_left_eye, left_eye)
    max_right_eye = max(max_right_eye, right_eye)
    max_blinking_ratio = max(max_blinking_ratio, blinking_ratio)

    board = np.zeros((400, 600, 3), np.uint8)  # Crea una imagen negra

    # Configuración del texto
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1
    color = (255, 255, 255)  # Blanco
    thickness = 2

    # Posiciones para el texto
    pos_left_eye = (10, 30)  # Parte superior izquierda del tablero
    pos_right_eye = (10, 60)  # Parte superior, un poco a la derecha
    pos_ratio = (10, 380)  # Parte inferior del tablero

    # Dibujando el texto con los valores máximos
    cv2.putText(board, f"Left Eye: {left_eye:.2f} (Max: {max_left_eye:.2f})", pos_left_eye, font, scale, color, thickness)
    cv2.putText(board, f"Right Eye: {right_eye:.2f} (Max: {max_right_eye:.2f})", pos_right_eye, font, scale, color, thickness)
    cv2.putText(board, f"Blinking Ratio: {blinking_ratio:.2f} (Max: {max_blinking_ratio:.2f})", pos_ratio, font, scale, color, thickness)

    cv2.imshow("Debugger", board)

def reset_max_values():
    global max_left_eye, max_right_eye, max_blinking_ratio
    max_left_eye = 0
    max_right_eye = 0
    max_blinking_ratio = 0