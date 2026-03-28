import numpy as np

class Piece:
    def __init__(self, color: str, start_pos: tuple[int, int]):
        self._color = color
        self._start_pos = start_pos
        self._pos = start_pos
        
    def color(self) -> str:
        return self._color
    
    def x(self) -> int:
        return self._pos[0]
    
    def y(self) -> int:
        return self._pos[1]
    
    def offset(self, x_offset, y_offset) -> tuple[int, int]:
        return (self.x() + x_offset, self.y() + y_offset)
    
    def movement(self, current_layout: np.ndarray) -> list[tuple[int, int]]:
        raise NotImplementedError
    
    def start_pos(self) -> tuple[int, int]:
        return self._start_pos
    
    def current_pos(self) -> tuple[int, int]:
        return self._pos
    
    def filter_moves(self, moves: list[tuple[int, int]]) -> list[tuple[int, int]]:
        current_pos = self.current_pos()
        return [move for move in moves if (0 <= move[0] <= 7 and 0 <= move[1] <= 7 and move != current_pos)]
    
class Pawn(Piece):
    def __init__(self, color: str, start_pos: tuple[int, int]) -> None:
        super().__init__(color, start_pos)
        self._dy = 1 if self.color() == "black" else -1
        
    def dy(self) -> int:
        return self._dy
        
    def movement(self, current_layout: np.ndarray) -> list[tuple[int, int]]:
        possible_moves = [
            self.offset(self.dy(), 0),
            self.offset(self.dy() * 2, 1),
            self.offset(self.dy() * 2, -1)
        ]
        
        if self.start_pos() == self.current_pos():
            possible_moves.append(self.offset(self.dy() * 2, 0))
        
        on_board_moves = super().filter_moves(possible_moves)   
            
        return on_board_moves
    
    def __repr__(self) -> str:
        return f"{self.color()} Pawn"
    
    
class Rook(Piece):
    def __init__(self, color: str, start_pos: tuple[int, int]) -> None:
        super().__init__(color, start_pos)
        
    def movement(self, current_layout: np.ndarray) -> list[tuple[int, int]]:
        possible_x = [self.offset(offset, 0) for offset in range(-8, 9, 1)]
        possible_y = [self.offset(0, offset) for offset in range(-8, 9, 1)]
        
        possible_moves = possible_x + possible_y
        on_board_moves = super().filter_moves(possible_moves)
        self.filter_moves(on_board_moves, current_layout)
        return on_board_moves
    
    def __repr__(self) -> str:
        return f"{self.color()} Rook"
    
    
class Knight(Piece):
    def __init__(self, color: str, start_pos: tuple[int, int]) -> None:
        super().__init__(color, start_pos)
        
    def movement(self, current_layout: np.ndarray) -> list[tuple[int, int]]:
        possible_moves = [
            self.offset(-1, 2),
            self.offset(-2, 1),
            self.offset(-2, -1),
            self.offset(-1, -2),
            self.offset(1, -2),
            self.offset(2, -1),
            self.offset(2, 1),
            self.offset(1, 2)
        ]
        
        on_board_moves = super().filter_moves(possible_moves) 
        return on_board_moves
    
    def __repr__(self):
        return f"{self.color()} Knight"
    
class Bishop(Piece):
    def __init__(self, color: str, start_pos: tuple[int, int]) -> None:
        super().__init__(color, start_pos)
        
    def movement(self, current_layout: np.ndarray):
        possible_1 = [self.offset(offset, offset) for offset in range(-8, 9, 1)]
        possible_2 = [self.offset(offset, -offset) for offset in range(-8, 9, 1)]
        possible_moves = possible_1 + possible_2
        
        on_board_moves = super().filter_moves(possible_moves) 
        return on_board_moves
    
    def __repr__(self) -> str:
        return f"{self.color()} Bishop"
    
class Queen(Bishop):
    def __init__(self, color: str, start_pos: tuple[int, int]) -> None:
        super().__init__(color, start_pos)
        
    def movement(self, current_layout: np.ndarray):
        possible_x = [self.offset(offset, 0) for offset in range(-8, 9, 1)]
        possible_y = [self.offset(0, offset) for offset in range(-8, 9, 1)]
        possible_moves = possible_x + possible_y
        on_board_moves = super().filter_moves(possible_moves)

        return super().movement(current_layout) + on_board_moves 
    
    def __repr__(self) -> str:
        return f"{self.color()} Queen"
    
class King(Piece):
    def __init__(self, color: str, start_pos: tuple[int, int]) -> None:
        super().__init__(color, start_pos)
        
    def movement(self, current_layout: np.ndarray):
        possible_moves = [
            self.offset(1, 0),
            self.offset(1, 1),
            self.offset(0, 1),
            self.offset(-1, 1),
            self.offset(-1, 0),
            self.offset(-1, -1),
            self.offset(0, -1),
            self.offset(1, -1)
        ]
        
        on_board_moves = super().filter_moves(possible_moves)

        return  on_board_moves
    
    def __repr__(self) -> str:
        return f"{self.color()} King"
