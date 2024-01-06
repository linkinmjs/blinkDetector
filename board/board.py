import numpy as np
import cv2

# constants
font = cv2.FONT_HERSHEY_PLAIN

def show_board(characters, rows, columns, current_row, current_column, show_column_rect):

    board = np.zeros((400, 600, 3), np.uint8)  # Crea una imagen negra
    paso_y = board.shape[0] // rows
    paso_x = board.shape[1] // columns

    for i, char in enumerate(characters):
        y = i // columns * paso_y
        x = i % columns * paso_x
        cv2.putText(board, char, (x + 10, y + paso_y - 10), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Dibuja un rectángulo alrededor de la fila seleccionada
    y_start = current_row * paso_y
    cv2.rectangle(board, (0, y_start), (board.shape[1], y_start + paso_y), (0, 255, 0), 2)

    if show_column_rect:
        # Si se está seleccionando una columna, dibuja un rectángulo alrededor de la columna actual
        x_start = current_column * paso_x
        cv2.rectangle(board, (x_start, 0), (x_start + paso_x, board.shape[0]), (0, 0, 255), 2)  # Usar otro color para diferenciar


    cv2.imshow("board de Letras", board)
