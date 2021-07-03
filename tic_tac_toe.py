from MCTS import MCTS, State
import numpy as np

NOUGHT = 1
CROSS = 4

class Board(State):
    def __init__(self, stone):
        """
        self.board is represented by a 3x3 numpy array.
            1 for nought, 4 for crosse.
        self.stone is the player's identity
        """
        self.board = np.zeros([3,3])
        self.id = stone              # The next stone which is going to be put on the board
        self.result = {NOUGHT: 0, CROSS: 0}

    def is_terminal(self):
        for i in range(3):
            if self.board[i, :].sum() == 3 \
                or self.board[:, i].sum() == 3 \
                or self.board[0, 0] + self.board[1, 1] + self.board[2, 2] == 3 \
                or self.board[0, 2] + self.board[1, 1] + self.board[2, 0] == 3:

                self.result[CROSS] = float(self.id == NOUGHT)
                self.result[NOUGHT] = float(self.id == CROSS)
                return True
            if self.board[:, i].sum() == 12 \
                or self.board[i, :].sum() == 12 \
                or self.board[0, 0] + self.board[1, 1] + self.board[2, 2] == 12 \
                or self.board[0, 2] + self.board[1, 1] + self.board[2, 0] == 12:

                self.result[CROSS] = float(self.id == NOUGHT)
                self.result[NOUGHT] = float(self.id == CROSS)
                return True
        if 0 not in self.board:
            return True
        return False

    def possible_moves(self):
        """
        return: [pos1, pos2, ..., posn]
        """
        moves = np.where(self.board == 0)
        return list(zip(moves[0], moves[1]))

    def update(self, move):
        """
        move = (x, y)
        """
        new_board = Board(NOUGHT if self.id==CROSS else CROSS)
        new_board.board = self.board.copy()
        new_board.board[move[0], move[1]] = self.id
        return new_board

    def get_score(self):
        if not self.is_terminal:
            # draw
            pass
        return self.result


if __name__=="__main__":
    pass