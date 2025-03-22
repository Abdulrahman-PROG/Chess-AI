import chess

class ChessGame:
    def __init__(self):
        self.board = chess.Board()

    def make_move(self, move):
        if move in self.board.legal_moves:
            self.board.push(move)
            return True
        return False

    def get_board(self):
        return self.board

    def is_game_over(self):
        return self.board.is_game_over()

    def reset(self):
        self.board.reset()