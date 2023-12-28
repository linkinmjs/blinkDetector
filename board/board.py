import numpy as np
import cv2

# constants
font = cv2.FONT_HERSHEY_PLAIN

def show_board(rows, columns, current_row):

    characters = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3",
    "4", "5", "6", "7", "8", "9", " "
    ]

    board = np.zeros((400, 600, 3), np.uint8)  # Crea una imagen negra
    paso_y = board.shape[0] // rows
    paso_x = board.shape[1] // columns

    for i, char in enumerate(characters):
        y = i // columns * paso_y
        x = i % columns * paso_x
        cv2.putText(board, char, (x + 10, y + paso_y - 10), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Dibuja un rectángulo alrededor de la fila actual
    y_start = current_row * paso_y
    cv2.rectangle(board, (0, y_start), (board.shape[1], y_start + paso_y), (0, 255, 0), 2)


    cv2.imshow("board de Letras", board)
