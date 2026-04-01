from typing import Union
import pygame
import numpy as np
from pieces import Pawn, King, Knight, Queen, Bishop, Rook, Piece
from settings import SquareSettings, Colors, UIBoardSettings

_INITIAL_POSITIONS = {
            (0, 0): {"class": Rook, "color": "black"},
            (0, 1): {"class": Knight, "color": "black"},
            (0, 2): {"class": Bishop, "color": "black"},
            (0, 3): {"class": Queen, "color": "black"},
            (0, 4): {"class": King, "color": "black"},
            (0, 5): {"class": Bishop, "color": "black"},
            (0, 6): {"class": Knight, "color": "black"},
            (0, 7): {"class": Rook, "color": "black"},
            (1, 0): {"class": Pawn, "color": "black"},
            (1, 1): {"class": Pawn, "color": "black"},
            (1, 2): {"class": Pawn, "color": "black"},
            (1, 3): {"class": Pawn, "color": "black"},
            (1, 4): {"class": Pawn, "color": "black"},
            (1, 5): {"class": Pawn, "color": "black"},
            (1, 6): {"class": Pawn, "color": "black"},
            (1, 7): {"class": Pawn, "color": "black"},

            (7, 0): {"class": Rook, "color": "white"},
            (7, 1): {"class": Knight, "color": "white"},
            (7, 2): {"class": Bishop, "color": "white"},
            (7, 3): {"class": Queen, "color": "white"},
            (7, 4): {"class": King, "color": "white"},
            (7, 5): {"class": Bishop, "color": "white"},
            (7, 6): {"class": Knight, "color": "white"},
            (7, 7): {"class": Rook, "color": "white"},
            (6, 0): {"class": Pawn, "color": "white"},
            (6, 1): {"class": Pawn, "color": "white"},
            (6, 2): {"class": Pawn, "color": "white"},
            (6, 3): {"class": Pawn, "color": "white"},
            (6, 4): {"class": Pawn, "color": "white"},
            (6, 5): {"class": Pawn, "color": "white"},
            (6, 6): {"class": Pawn, "color": "white"},
            (6, 7): {"class": Pawn, "color": "white"},
        }

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
        
    def set_piece(self, piece: Piece) -> None:
        self._piece = piece
        self.piece().register_movement((self.row(), self.col()))
        
    def remove_piece(self) -> None:
        self._piece = None

class ChessBoard:
    def __init__(self, board: np.ndarray, squares: list[Square]) -> None:
        self._board = board
        self._squares = squares
        self._possible_moves = []
        
    @classmethod
    def populate(cls) -> "ChessBoard":
        board = np.empty((8, 8), dtype=object)
        for pos, keys in _INITIAL_POSITIONS.items():
            piece_class: Piece = keys["class"]
            color = keys["color"]

            board[pos[0], pos[1]] = piece_class(color, pos)
            
        squares = []
        color = Colors.WHITE
        for row, y in enumerate(range(UIBoardSettings.START_Y, UIBoardSettings.END_Y, UIBoardSettings.STEP)):
            for col, x in enumerate(range(UIBoardSettings.START_X, UIBoardSettings.END_X, UIBoardSettings.STEP)):
                squares.append(Square(x, y, color, row, col, board[row, col]))
                color = Colors.BLACK if color == Colors.WHITE else Colors.WHITE
            color = Colors.BLACK if color == Colors.WHITE else Colors.WHITE
            
        return cls(board, squares)

    def board(self) -> np.ndarray:
        return self._board
    
    def squares(self) -> list[Square]:
        return self._squares
    
    def possible_moves(self) -> list[tuple[int, int]]:
        return self._possible_moves
     
    def get_selected_square(self, position: tuple[int, int]) -> Union[Square, None]:
        squares = self.squares()
        selected = [square for square in squares if square.was_clicked(position)]
        return selected[0] if selected else None
    
    def set_selected_square(self, selected_square: Square) -> None:
        selected_square.set_selected()
        
        for square in self.squares():
            if square != selected_square:
                square.unselect()
    
    def set_possible_moves(self, square: Union[Square, None]) -> list[tuple[int, int]]:
        if not square:
            for square in self.squares():
                square.unselect()
            self._possible_moves = []
            return

        possible_moves = square.piece().movement(self.board())
        piece_color = square.piece().color()

        for square in self.squares():

            square_coordinates = (square.row(), square.col())
            if square_coordinates not in possible_moves:
                continue

            if square.piece() is not None and square.piece().color() != piece_color:
                square.set_capturable()
                continue
            
            square.set_possible_move()
            
        self._possible_moves = possible_moves
    
    def move_piece(self, square: Square, target_square: Square) -> None:
        piece = square.piece()
        original_row, original_col = square.row(), square.col()
        target_row, target_col = target_square.row(), target_square.col()
        
        self._board[original_row, original_col] = None
        self._board[target_row, target_col] = piece
        
        square.remove_piece()
        target_square.set_piece(piece)
