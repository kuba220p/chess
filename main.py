import pygame
from board import ChessBoard
from ui_board import UIBoard

class Game:
    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode((1280, 720))
        self._clock = pygame.time.Clock()
        self._running = True
        self._dt = 0
        self._board = ChessBoard.populate()
        self._ui_board = UIBoard.populate(self._board.board())

    def stop(self) -> None:
        self._running = False
        
    def screen(self) -> pygame.Surface:
        return self._screen
        
    def running(self) -> bool:
        return self._running
    
    def set_dt(self, dt: float) -> None:
        self._dt = dt 
        
    def clock(self) -> pygame.time.Clock:
        return self._clock
    
    def screen_size(self) -> tuple[int, int]:
        return self.screen().width, self.screen().height
        
    def play(self) -> None:
        
        while self.running():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    positions = pygame.mouse.get_pos()
                    selected_square = self._ui_board.select_square(positions)
                    if selected_square is not None and selected_square.piece() is not None:
                        self._ui_board.set_possible_moves(selected_square, self._board.board())

                    
            self.screen().fill("blue")
            self._ui_board.draw()
            
            pygame.display.flip()
            
            
            self.set_dt(self.clock().tick(60) / 1000)
            
        pygame.quit()
        
if __name__ == "__main__":
    game = Game()
    game.play()