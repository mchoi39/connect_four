import pygame
from board import Board
import sys
import math
import random
import copy

# color of pieces
EMPTY = 0
PLAYER = 1
AI = 2
# counts the number of turns
TURN_NUMBER = 0
# change mode for AI/RNG (1 for AI, anything else for RNG)
MODE = 1


def connect_four():
    global screen
    global TURN_NUMBER
    b = Board()
    pygame.init()
    screen = pygame.display.set_mode((75 * b.columns, 75 * (b.rows + 1)))
    square = 75
    draw(b, square)

    pygame.display.update()
    # radius = round(square / 2)
    # board.drop_piece(2, PLAYER)
    # board.drop_piece(4, AI)
    # board.display()

    game_in_progress = True
    while game_in_progress:

        for e in pygame.event.get():
            if e.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, (0, 0, 0), (0, 0, 75 * b.columns, 75))
                if TURN_NUMBER % 2 == 0:
                    pygame.draw.circle(screen, (255, 0, 0), (e.pos[0], 75 / 2), 75 / 2)
            pygame.display.update()

            if e.type == pygame.MOUSEBUTTONDOWN:
                # insert_position = e.pos[0]
                column = int(math.floor(e.pos[0] / square))
                print("column is ", column)
                if TURN_NUMBER % 2 == 0:
                    b.drop_piece(column, 1)
                    if b.check_win_conditions():
                        print("PLAYER WON")
                        sys.exit()  # display win screen
                    TURN_NUMBER += 1

                draw(b, square)
                draw_player_pieces(b, square)
                draw_ai_pieces(b, square)
            if e.type == pygame.QUIT:
                pygame.time.wait(5000)
                sys.exit()
            pygame.display.update()

        if TURN_NUMBER % 2 == 1:
            if MODE == 1:
                col, val = minimax(b, 6, float('-inf'), float('+inf'), True)
                b.drop_piece(col, AI)
            else:
                rng(b, AI)
            draw(b, square)
            draw_player_pieces(b, square)
            draw_ai_pieces(b, square)
            pygame.display.update()
            if b.check_win_conditions():
                print("AI WON")
                sys.exit()
            TURN_NUMBER += 1

        # do AI inserting a piece part. Needa do algorithm and drop piece and check win condition


def score_by_count(four_pieces, piece):
    counter_ai = 0
    counter_player = 0
    counter_none = 0
    for i in four_pieces:
        if i == piece:
            counter_ai += 1
        elif i == PLAYER:
            counter_player += 1
        else:
            counter_none += 1
    score = 0
    if counter_ai == 2 and counter_none == 2:
        score += 2
    elif counter_ai == 3 and counter_none == 1:
        score += 5
    elif counter_ai == 4:
        score += 10000000000000000000000
    if counter_player == 3 and counter_none == 1:
        score -= 100
    elif counter_player == 2 and counter_none == 2:
        score -= 4
    return score


def score_four_pieces(four_pieces, piece):
    score = 0
    counter = 0
    for i in range(len(four_pieces)):
        if four_pieces[i] == piece:
            counter += 1
            if i == len(four_pieces) - 1:
                if counter == 1:
                    score += 1
                elif counter == 2:
                    score += 3
                elif counter == 3:
                    score += 9
                else:
                    score += 10000000000000000  # win condition
        else:
            if counter == 1:
                score += 1
            elif counter == 2:
                score += 3
            elif counter == 3:
                score += 9
            counter = 0

        num_opp = 0
        for value in four_pieces:
            if value != 0 and value != piece:
                num_opp += 1
        if num_opp == 3 and score == 0:
            score -= 4
    return score


# gets the value of each win condition given the piece
def get_heuristic_val(b, piece):
    board = b.board
    score = 0
    for row in range(b.rows):
        for col in range(b.columns - 3):
            pc1 = board[row][col]
            pc2 = board[row][col + 1]
            pc3 = board[row][col + 2]
            pc4 = board[row][col + 3]
            four_pieces = [pc1, pc2, pc3, pc4]
            score += score_by_count(four_pieces, piece)
            # score += score_four_pieces(four_pieces, piece)
    # vertical
    for row in range(b.rows - 3):
        for col in range(b.columns):
            pc1 = board[row][col]
            pc2 = board[row + 1][col]
            pc3 = board[row + 2][col]
            pc4 = board[row + 3][col]

            four_pieces = [pc1, pc2, pc3, pc4]
            score += score_by_count(four_pieces, piece)
            # score += score_four_pieces(four_pieces, piece)
    # pos diagonal
    for row in range(3, 6):  # points to test: (3,0) (3,1) (3,2) (3,3) (4,0) (4,1) (4,2) (4,3) (5,0) (5,1) (5,2) (5,3)
        for col in range(4):
            pc1 = board[row][col]
            pc2 = board[row - 1][col + 1]
            pc3 = board[row - 2][col + 2]
            pc4 = board[row - 3][col + 3]

            four_pieces = [pc1, pc2, pc3, pc4]
            # score += score_four_pieces(four_pieces, piece)
            score += score_by_count(four_pieces, piece)
    # neg diagonal
    for row in range(3):
        for col in range(4):
            pc1 = board[row][col]
            pc2 = board[row + 1][col + 1]
            pc3 = board[row + 2][col + 2]
            pc4 = board[row + 3][col + 3]

            four_pieces = [pc1, pc2, pc3, pc4]
            # score += score_four_pieces(four_pieces, piece)
            score += score_by_count(four_pieces, piece)
    return score


# if you need the link, https://towardsdatascience.com/creating-the-perfect-connect-four-ai-bot-c165115557b0
# https://en.wikipedia.org/wiki/Minimax # source for Minimax pseudocode
def minimax(b, depth, alpha, beta, maximizing_player):
    if depth == 0 or b.check_win_conditions() or len(
            b.get_valid_columns()) == 0:  # if depth = 0 or node is a terminal node then
        return None, get_heuristic_val(b, AI)  # return the heuristic value of node
    if maximizing_player:  # if maximizingPlayer then
        value = float('-inf')  # value := −∞
        column = -1
        for col in b.get_valid_columns():  # for each child of node do
            b_copy = copy.deepcopy(b)
            b_copy.drop_piece(col, AI)
            new_value = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_value > value:
                value = new_value
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:  # (* minimizing player *)
        value = float('+inf')  # value := +∞
        column = -1
        for col in b.get_valid_columns():  # for each child of node do
            b_copy = copy.deepcopy(b)
            b_copy.drop_piece(col, PLAYER)
            new_value = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_value < value:
                value = new_value
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value  # u dont need parenthesis


def rng(b, player):  # random number generator
    flag = 0
    col = -1
    # b.drop_piece(0, player)
    while flag != 1:
        if col in b.get_valid_columns():
            flag = 1
            b.drop_piece(col, player)
            b.display()
        else:
            col = random.randint(0, 6)


# draw board on pygame
def draw(b, square):
    global screen
    for row_b in b.board:
        print(row_b)
    cols = len(b.board[0])
    # print("cols ", cols)
    rows = len(b.board)
    # print("rows", rows)
    for col in range(cols):
        for row in range(rows):
            rect_pos = (col * square, row * square + square, square, square)
            pygame.draw.rect(screen, (50, 50, 255), rect_pos)
            circle_pos = (col * square + square / 2, row * square + square + square / 2)
            radius = square / 2
            pygame.draw.circle(screen, (0, 0, 0), circle_pos, radius)
    pygame.display.update()


def draw_player_pieces(board, square):
    global screen
    # print(board.board)
    cols = len(board.board[0])
    rows = len(board.board)

    for col in range(cols):
        for row in range(rows):
            if board.board[row][col] == PLAYER:
                circle_pos = (col * square + square / 2, row * square + square + square / 2)
                radius = square / 2
                pygame.draw.circle(screen, (255, 0, 0), circle_pos, radius)
    pygame.display.update()


def draw_ai_pieces(board, square):
    global screen
    cols = len(board.board[0])
    rows = len(board.board)

    for col in range(cols):
        for row in range(rows):
            if board.board[row][col] == AI:
                circle_pos = (col * square + square / 2, row * square + square + square / 2)
                radius = square / 2
                pygame.draw.circle(screen, (255, 192, 203), circle_pos, radius)
    pygame.display.update()


if __name__ == '__main__':
    TURN_NUMBER = int(input("Enter 0 or 1. 0 for Player starts, 1 for AI starts: "))
    MODE = int(input("Enter 1 for MINIMAX and 0 for RNG: "))
    connect_four()
