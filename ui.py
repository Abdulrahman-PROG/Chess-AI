import pygame
import chess

class ChessUI:
    def __init__(self, game, engine):
        pygame.init()
        self.game = game
        self.engine = engine
        self.square_size = 80
        self.screen = pygame.display.set_mode((8 * self.square_size, 8 * self.square_size))
        pygame.display.set_caption("AI Chess")
        self.colors = [(240, 217, 181), (181, 136, 99)]

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = self.colors[(row + col) % 2]
                pygame.draw.rect(self.screen, color, 
                               (col * self.square_size, row * self.square_size, 
                                self.square_size, self.square_size))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_board()
            pygame.display.flip()
        pygame.quit()