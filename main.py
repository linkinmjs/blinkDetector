import cv2
import numpy as np
import dlib
from board.board import show_board
from util.debug_helper import show_helper, reset_max_values
from math import hypot
import time

# constants and vars
font = cv2.FONT_HERSHEY_PLAIN
umbral = 4.8    # this is a configurable param
rows = 4
columns = 10
velocity = 0.8 # velocity for select letters
last_update_time = time.time()

# board vars
characters = [
"A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
"K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
"U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3",
"4", "5", "6", "7", "8", "9", " ", " ", " ", " "
]
phrase = ""  # Phrase string
selecting_column = False
current_row = 0
current_column = 0

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


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


while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    for face in faces:
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        
        # Uncomment next line to show face rectangle
        # cv2.rectangle(frame, (x,y), (x1, y1), (0, 255, 0), 2)

        landmarks = predictor(gray, face)

        right_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        left_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

        # check second after second
        if time.time() - last_update_time > velocity:
            if not selecting_column:
                current_row = (current_row + 1) % rows
            else:
                current_column = (current_column + 1) % columns
            last_update_time = time.time()

        if blinking_ratio > umbral:
            # Blinking message
            cv2.putText(frame, "BLINK", (50, 150), font, 7, (255, 0, 0))
            
            if not selecting_column:
                # freeze row and start with column
                selecting_column = True
                time.sleep(1)
            else:
                # select letter
                selected_letter = characters[current_row * columns + current_column]
                phrase += selected_letter
                print(phrase)
                
                # reset
                selecting_column = False
                current_row = 0
                current_column = 0
                time.sleep(1)
        
        
        show_board(characters, rows, columns, current_row, current_column, selecting_column)
        show_helper(left_eye_ratio, right_eye_ratio, blinking_ratio)
        
        
    cv2.imshow("Frame", frame)

    # actions by keys
    key = cv2.waitKey(1)
    if key == ord('r') or key == ord('R'):
        reset_max_values()
    elif key == 27:  # ESC key for close app
        break

cap.release()