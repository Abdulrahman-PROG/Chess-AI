import pygame
import chess

class ChessUI:
    def __init__(self, game, engine):
        # Initialize Pygame for the graphical interface
        pygame.init()
        self.game = game  # Reference to the ChessGame instance
        self.engine = engine  # Reference to the ChessEngine instance
        self.square_size = 80  # Size of each square on the board (80x80 pixels)
        self.screen = pygame.display.set_mode((8 * self.square_size, 8 * self.square_size))  # Create an 8x8 board window
        pygame.display.set_caption("AI Chess")  # Set the window title
        self.colors = [(240, 217, 181), (181, 136, 99)]  # Colors for light and dark squares
        self.selected_square = None  # Track the currently selected square (for moving pieces)
        self.font = pygame.font.SysFont(None, 40)  # Font for rendering piece symbols as text (temporary)

    def square_to_pos(self, square):
        # Convert a chess square (e.g., chess.A1) to pixel coordinates on the screen
        file = chess.square_file(square)  # Get the file (column, 0-7)
        rank = 7 - chess.square_rank(square)  # Get the rank (row, 0-7, inverted for Pygame's coordinate system)
        return (file * self.square_size, rank * self.square_size)  # Return (x, y) position

    def pos_to_square(self, pos):
        # Convert mouse click coordinates (x, y) to a chess square (e.g., chess.A1)
        x, y = pos
        file = x // self.square_size  # Calculate the file (column) from x-coordinate
        rank = 7 - (y // self.square_size)  # Calculate the rank (row) from y-coordinate, inverted
        return chess.square(file, rank)  # Return the corresponding chess square

    def draw_board(self):
        # Draw the 8x8 chessboard with alternating colors
        for row in range(8):
            for col in range(8):
                color = self.colors[(row + col) % 2]  # Alternate between light and dark colors
                pygame.draw.rect(self.screen, color,
                               (col * self.square_size, row * self.square_size,
                                self.square_size, self.square_size))  # Draw each square

        # Draw the pieces on the board (as text for now, e.g., "P" for pawn, "K" for king)
        board = self.game.get_board()  # Get the current board state
        for square in chess.SQUARES:
            piece = board.piece_at(square)  # Check if there's a piece on this square
            if piece:
                pos = self.square_to_pos(square)  # Get the pixel position of the square
                piece_text = self.font.render(piece.symbol(), True, (0, 0, 0))  # Render the piece symbol as text
                self.screen.blit(piece_text, (pos[0] + 20, pos[1] + 20))  # Draw the text on the board

        # Highlight the selected square with a red border (if a square is selected)
        if self.selected_square is not None:
            pos = self.square_to_pos(self.selected_square)
            pygame.draw.rect(self.screen, (255, 0, 0), (pos[0], pos[1], self.square_size, self.square_size), 3)

    def run(self):
        # Main game loop to handle user input and game flow
        running = True
        player_turn = True  # Start with the player's turn (player plays as White)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Exit the game if the window is closed
                elif event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                    # Handle mouse clicks during the player's turn
                    pos = pygame.mouse.get_pos()  # Get the mouse click position
                    square = self.pos_to_square(pos)  # Convert the position to a chess square
                    if self.selected_square is None:
                        # If no square is selected, try to select a piece
                        if self.game.get_board().piece_at(square) and self.game.get_board().piece_at(square).color == chess.WHITE:
                            self.selected_square = square  # Select the square if it has a White piece
                    else:
                        # If a square is already selected, try to move the piece to the new square
                        move = chess.Move(self.selected_square, square)  # Create a move from selected to target square
                        if self.game.make_move(move):  # If the move is legal, apply it
                            player_turn = False  # Switch to AI's turn
                        self.selected_square = None  # Reset the selected square

            if not player_turn and not self.game.is_game_over():
                # AI's turn: calculate and make the best move
                move = self.engine.get_best_move(self.game.get_board())  # Get the AI's best move
                self.game.make_move(move)  # Apply the AI's move
                player_turn = True  # Switch back to the player's turn

            self.draw_board()  # Redraw the board after each action
            pygame.display.flip()  # Update the display
        pygame.quit()  # Clean up Pygame when the game ends