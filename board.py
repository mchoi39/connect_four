
class Board():
    def __init__(self):
        self.columns = 7
        self.rows = 6
        self.board = []
        for i in range(self.rows):
            self.board.append([0] * self.columns)

    # print the board
    def display(self):
        for i in self.board:
            print(i)

    # get list of valid columns
    def get_valid_columns(self):
        valid = []
        for i in range(self.columns):
            if self.board[0][i] == 0:
                valid.append(i)
        return valid

    # drop a piece
    def drop_piece(self, col, color):
        for i in reversed(range(self.rows)):
            if i is not None and col is not None and color is not None:
                if self.board[i][col] == 0:
                    self.board[i][col] = color
                    break

    # check for winning conditions
    def check_win_conditions(self):
        if self.check_vertical() or self.check_horizontal():
            return True
        if self.check_neg_diag() or self.check_pos_diag():
            return True
        return False

    def check_vertical(self):
        board = self.board
        for row in reversed(range(len(board) - 3)):  # check if column has 4 in a row
            for col in range(len(board[0])):
                if board[row][col] != 0:  # if there is a piece
                    color = board[row][col]
                    if board[row + 1][col] == color:
                        if board[row + 2][col] == color:
                            if board[row + 3][col] == color:
                                return True
        return False

    def check_horizontal(self):
        board = self.board
        for row in range(len(board)):
            for col in range(len(board[0]) - 3):
                if board[row][col] != 0: # if there is a piece
                    color = board[row][col]
                    if board[row][col + 1] == color:
                        if board[row][col + 2] == color:
                            if board[row][col + 3] == color:
                                return True
        return False

    def check_upward(self, row, col, flag):  # row - 1, col + 1
        board = self.board
        color = board[row][col]
        if color == 0:
            return False
        if flag == 1:
            for i in range(4):
                if board[row][col] != color:
                    return False
                row-=1
                col+=1
            return True
        else:  # row - 1, col - 1
            for i in range(4):
                if board[row][col] != color:
                    return False
                row-=1
                col-=1
            return True

    def check_downward(self, row, col, flag):  # row + 1, col - 1
        board = self.board
        color = board[row][col]
        if color == 0:
            return False
        if flag == 1:
            for i in range(4):
                if board[row][col] != color:
                    return False
                row += 1
                col -= 1
            return True
        else:  # + row, + column
            for i in range(4):
                if board[row][col] != color:
                    return False
                row += 1
                col += 1
            return True

    def check_pos_diag(self):
        board = self.board
        for i in range(len(board)):  # traverse rows
            if i == 0:  # check (0, 6), row + 1, col - 1 each iteration
                if self.check_downward(0, 6, 1):
                    return True
            elif i == 1:  # check (1, 6), (1, 5) row + 1, col - 1 each iteration
                if self.check_downward(1, 6, 1) or self.check_downward(1, 5, 1):
                    return True
            elif i == 2:  # check (2,6), (2,5), (2,4) row + 1, col - 1 each iteration
                if self.check_downward(2, 6, 1) or self.check_downward(2, 5, 1):
                    return True
                if self.check_downward(2, 4, 1):
                    return True
            elif i == 3:  # check (3, 0), (3, 1), (3, 2) row - 1, col + 1 each iteration
                if self.check_upward(3, 0, 1) or self.check_upward(3, 1, 1):
                    return True
                if self.check_upward(3, 2, 1):
                    return True
            elif i == 4:  # check (4, 0), (4, 1), row - 1, col + 1 each iteration
                if self.check_upward(4, 0, 1) or self.check_upward(4, 1, 1):
                    return True
            elif i == 5:  # check (5, 0), (5, 1), (5, 2), row - 1, col + 1 each iteration
                if self.check_upward(5, 0, 1) or self.check_upward(5, 1, 1):
                    return True
                if self.check_upward(5, 2, 1):
                    return True
        return False

    def check_neg_diag(self):
        board = self.board
        for i in range(len(board)):  # traverse rows
            if i == 0:  # check (0, 0), (0, 1), (0, 2)
                if self.check_downward(0, 0, -1) or self.check_downward(0, 1, -1):
                    return True
                if self.check_downward(0, 2, -1):
                    return True
            elif i == 1:  # check (1, 0), (1, 1)
                if self.check_downward(1, 0, -1) or self.check_downward(1, 1, -1):
                    return True
            elif i == 2:  # check (2, 0)
                if self.check_downward(2, 0, -1):
                    return True
            elif i == 3:  # check (3, 6)
                if self.check_upward(3, 6, -1):
                    return True
            elif i == 4:  # check (4, 6), (4, 5)
                if self.check_upward(4, 0, -1) or self.check_upward(4, 1, -1):
                    return True
            elif i == 5:  # check (5, 6), (5, 5), (5, 4)
                if self.check_upward(5, 6, -1) or self.check_upward(5, 5, -1):
                    return True
                if self.check_upward(5, 4, -1):
                    return True
        return False


# b = Board()
# b.display()
# print("col " + str(len(b.board[0])))
# print("row " + str(len(b.board)))
# b.drop_piece(0, 1)
# b.drop_piece(1, 2)
# b.drop_piece(2, 2)
# b.drop_piece(3, 2)
# b.drop_piece(1, 1)
# b.drop_piece(2,2)
# b.drop_piece(2,1)
# b.drop_piece(3, 2)
# b.drop_piece(3, 2)
# b.drop_piece(3, 1)
# b.drop_piece(1, 2)
#
#
# b.display()
# print(b.check_neg_diag())