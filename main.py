from game import ChessGame
from chess_engine import ChessEngine
from ui import ChessUI

def main():
    game = ChessGame()
    engine = ChessEngine(depth=3)
    ui = ChessUI(game, engine)
    ui.run()

if __name__ == "__main__":
    main()