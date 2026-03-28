from typing import Union
import pygame
import numpy as np
from settings import SquareSettings, Colors, UIBoardSettings

from pieces import Piece


class Square:
    def __init__(self, left: float, top: float, color: str, row: int, col: int, piece: Piece):
        self._square = pygame.FRect(left, top, SquareSettings.SQUARE_WIDTH, SquareSettings.SQUARE_HEIGHT)
        self._color = color
        self._original_color = color
        self._row = row
        self._col = col
        self._piece = piece
        
    def square(self) -> pygame.FRect:
        return self._square
    
    def row(self) -> int:
        return self._row
    
    def col(self) -> int:
        return self._col
    
    def piece(self) -> Union[Piece, None]:
        return self._piece
    
    def x(self) -> float:
        return self.square().x
    
    def y(self) -> float:
        return self.square().y
    
    def color(self) -> str:
        return self._color
    
    def was_clicked(self, click_point: tuple[int, int]) -> bool:
        clicked_x, clicked_y = click_point
        
        width = self.x() + SquareSettings.SQUARE_WIDTH
        height = self.y() + SquareSettings.SQUARE_HEIGHT
        
        return (self.x() <= clicked_x <= width and self.y() <= clicked_y <= height)
    
    def set_selected(self) -> None:
        self._color = Colors.SELECTED
        
    def set_possible_move(self) -> None:
        self._color = Colors.POSSIBLE_MOVE
        
    def set_capturable(self) -> None:
        self._color = Colors.CAN_CAPTURE
        
    def unselect(self) -> None:
        self._color = self._original_color
        
    
class UIBoard:
    def __init__(self, squares: list[Square]) -> None:
        self._squares = squares
        
    @classmethod
    def populate(cls, pieces: np.ndarray) -> "UIBoard":
        squares = []
        color = Colors.WHITE
        for row, y in enumerate(range(UIBoardSettings.START_Y, UIBoardSettings.END_Y, UIBoardSettings.STEP)):
            for col, x in enumerate(range(UIBoardSettings.START_X, UIBoardSettings.END_X, UIBoardSettings.STEP)):
                squares.append(Square(x, y, color, row, col, pieces[row, col]))
                color = Colors.BLACK if color == Colors.WHITE else Colors.WHITE
            color = Colors.BLACK if color == Colors.WHITE else Colors.WHITE
            
        return cls(squares)
        
    def squares(self) -> list[Square]:
        return self._squares
        
    def draw(self) -> None:
        screen = pygame.display.get_surface()
        for square in self.squares():
            pygame.draw.rect(screen, square.color(), square.square())
            
    def select_square(self, click_point: tuple[int, int]) -> Union[Square, None]:
        squares = self.squares()
        selected = [square for square in squares if square.was_clicked(click_point)]
        
        if not selected:
            return
        
        selected_square = selected[0]
        selected_square.set_selected()
        
        for square in squares:
            if square != selected_square:
                square.unselect()
        
        return selected_square

    def set_possible_moves(self, selected_square: Square, current_layout: np.ndarray) -> None:
        possible_moves = selected_square.piece().movement(current_layout)
        piece_color = selected_square.piece().color()
        for square in self.squares():

            square_coordinates = (square.row(), square.col())
            if square_coordinates not in possible_moves:
                continue

            if square.piece() is not None and square.piece().color() != piece_color:
                square.set_capturable()
                continue
            
            square.set_possible_move()
            