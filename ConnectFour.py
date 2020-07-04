import numpy as np
import pygame
import sys

# RGB values
GREEN = (76, 153, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # Player A
ORANGE = (255, 165, 0)  # Player B

# grid/matrix size
ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    # initialize our matrix board of 6x7 to all zeros
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def insert_piece(board, row, columnChoice, piece):
    # insert piece to chosen location
    board[row][columnChoice] = piece


def is_valid_location(board, columnChoice):
    # Check if the very top of a column is occupied
    return board[0][columnChoice] == 0


def get_next_open_row(board, columnChoice):
    # check for the next available spot for insertion of piece
    for i in range(ROW_COUNT - 1, -1, -1):
        if board[i][columnChoice] == 0:
            return i


def winning_move(board, piece):
    # check horizontal
    for row in range(ROW_COUNT):
        for column in range(COLUMN_COUNT-3):
            if board[row][column] == piece and board[row][column + 1] == piece and board[row][column + 2] == piece and \
                    board[row][column + 3] == piece:
                return True

    # check vertical
    for row in range(ROW_COUNT-3):
        for column in range(COLUMN_COUNT):
            if board[row][column] == piece and board[row + 1][column] == piece and board[row + 2][column] == piece and \
                    board[row + 3][column] == piece:
                return True

    # check positive sloped diagonals
    for column in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT - 3):
            if board[row][column] == piece and board[row + 1][column + 1] == piece and board[row + 2][
                column + 2] == piece and board[row + 3][column + 3] == piece:
                return True

    # check negative sloped diagonals
    for column in range(COLUMN_COUNT - 3):
        for row in range(3, ROW_COUNT):
            if board[row][column] == piece and board[row - 1][column + 1] == piece and board[row - 2][
                column + 2] == piece and board[row - 3][column + 3] == piece:
                return True


def draw_board(board):
    for row in range(ROW_COUNT):
        for column in range(COLUMN_COUNT):
            pygame.draw.rect(screen, GREEN,
                             (column * squaresize, (row * squaresize) + squaresize, squaresize, squaresize))
            if board[row][column] == 0:
                pygame.draw.circle(screen, BLACK, (
                    int(column * squaresize + squaresize / 2), int(row * squaresize + squaresize + squaresize / 2)), radius)
            elif board[row][column] == 1:
                pygame.draw.circle(screen, YELLOW, (
                    int(column * squaresize + squaresize / 2), int(row * squaresize + squaresize + squaresize / 2)),
                                   radius)
            else:
                pygame.draw.circle(screen, ORANGE, (
                    int(column * squaresize + squaresize / 2), int(row * squaresize + squaresize + squaresize / 2)),
                                   radius)
    pygame.display.update()


board = create_board()
print(board)

game_over = False
turn = 0

pygame.init()

squaresize = 80
width = COLUMN_COUNT * squaresize
height = (ROW_COUNT + 1) * squaresize
size = (width, height)
radius = int(squaresize / 2 - 5)

screen = pygame.display.set_mode(size)

draw_board(board)
pygame.display.update()
font = pygame.font.SysFont("courier new", 70)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, squaresize))
            pos_x = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, YELLOW, (pos_x, int(squaresize / 2)), radius)
            else:
                pygame.draw.circle(screen, ORANGE, (pos_x, int(squaresize / 2)), radius)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, squaresize))
            # print(event.pos) --> tells us the position of the screen in pixel values
            # ask input from Player 1
            if turn == 0:
                pox_x = event.pos[0]
                columnChoice = int(pox_x // squaresize)  # gives us a range from 0-7

                if is_valid_location(board, columnChoice):
                    row = get_next_open_row(board, columnChoice)
                    insert_piece(board, row, columnChoice, 1)
                    if winning_move(board, 1):
                        label = font.render("Player A wins!", 1, YELLOW)
                        screen.blit(label, (0, 15))
                        game_over = True

            # ask input from Player 2
            else:
                pox_x = event.pos[0]
                columnChoice = int(pox_x // squaresize)

                if is_valid_location(board, columnChoice):
                    row = get_next_open_row(board, columnChoice)
                    insert_piece(board, row, columnChoice, 2)
                    if winning_move(board, 2):
                        label = font.render("Player B wins:)", 1, ORANGE)
                        screen.blit(label, (0, 15))
                        game_over = True

            print(board)
            draw_board(board)

            # alternate selection between player A and B
            turn += 1
            turn %= 2

            if game_over: # to prevent the program from escaping immediately after a player won
                pygame.time.wait(3000)
