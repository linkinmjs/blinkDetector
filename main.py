import cv2
import numpy as np
import dlib
from math import hypot

# constants
font = cv2.FONT_HERSHEY_PLAIN
umbral = 4.8    # this is a configurable param

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

caracteres = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3",
    "4", "5", "6", "7", "8", "9", " "
]

# obtiene la mitad de 2 puntos
def midpoint(p1, p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

# Esta función retornará el ratio del pestañeo
def get_blinking_ratio(eye_points, facial_landmarks):
        left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
        right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
        center_top = midpoint(facial_landmarks.part(eye_points[1]),facial_landmarks.part(eye_points[2]))
        center_bottom = midpoint(facial_landmarks.part(eye_points[5]),facial_landmarks.part(eye_points[4]))

        hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
        ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

        hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
        ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
        
        ratio = hor_line_lenght/ver_line_lenght
        return ratio

def mostrar_tablero(caracteres, filas, columnas):
    tablero = np.zeros((400, 600, 3), np.uint8)  # Crea una imagen negra
    paso_y = tablero.shape[0] // filas
    paso_x = tablero.shape[1] // columnas

    for i, char in enumerate(caracteres):
        y = i // columnas * paso_y
        x = i % columnas * paso_x
        cv2.putText(tablero, char, (x + 10, y + paso_y - 10), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Tablero de Letras", tablero)


while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)



    for face in faces:
        # x, y = face.left(), face.top()
        # x1, y1 = face.right(), face.bottom()
        
        # cv2.rectangle(frame, (x,y), (x1, y1), (0, 255, 0), 2)
        # print(face)

        landmarks = predictor(gray, face)

        right_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        left_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

        # print(left_eye_ratio)
        mostrar_tablero(caracteres, 4, 10)


        if blinking_ratio > 4.8:
            cv2.putText(frame, "BLINKING", (50, 150), font, 7, (255, 0, 0))


    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()