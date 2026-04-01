import pygame
from board import ChessBoard
from ui_board import UIBoard, Square

class Game:
    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode((1280, 720))
        self._clock = pygame.time.Clock()
        self._running = True
        self._dt = 0
        self._board = ChessBoard.populate()
        self._ui_board = UIBoard()

    def stop(self) -> None:
        self._running = False
        
    def board(self) -> ChessBoard:
        return self._board
        
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
    
    def select_square(self) -> Square:
        position = pygame.mouse.get_pos()
        square = self.board().get_selected_square(position)
        return square
        
    def play(self) -> None:
        square_selected = None
        move_complete = False
        player_turn = "white"
        while self.running():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if move_complete:
                        player_turn = "white" if player_turn == "black" else "black"
                        move_complete = False
                    
                    if square_selected:
                        target_square = self.select_square()
                        if target_square is not None:
                            target_square_pos = (target_square.row(), target_square.col())
                            valid = target_square_pos in self.board().possible_moves()
                            if valid and square_selected.piece() is not None:
                                self.board().move_piece(square_selected, target_square)
                                self.board().set_possible_moves(None)
                                move_complete = True
                                continue
                                
                        square_selected = None
                    
                    if not square_selected:
                        square_selected = self.select_square()
                    
                    if square_selected is not None and square_selected.piece() is not None and square_selected.piece().color() == player_turn:
                        self.board().set_selected_square(square_selected)
                        self.board().set_possible_moves(square_selected)
                       
                    
            self.screen().fill("blue")
            self._ui_board.draw(self.board().squares())
            
            pygame.display.flip()
            
            
            self.set_dt(self.clock().tick(60) / 1000)
            
        pygame.quit()
        
if __name__ == "__main__":
    game = Game()
    game.play()