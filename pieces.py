import numpy as np

class Piece:
    def __init__(self, color: str, start_pos: tuple[int, int]):
        self._color = color
        self._start_pos = start_pos
        self._pos = start_pos
        
    def color(self) -> str:
        return self._color
    
    def y(self) -> int:
        return self._pos[0]
    
    def x(self) -> int:
        return self._pos[1]
    
    def offset(self, y_offset: int, x_offset: int) -> tuple[int, int]:
        return (self.y() + y_offset, self.x() + x_offset)
    
    def movement(self, current_layout: np.ndarray) -> list[tuple[int, int]]:
        raise NotImplementedError
    
    def start_pos(self) -> tuple[int, int]:
        return self._start_pos
    
    def current_pos(self) -> tuple[int, int]:
        return self._pos
    
    def remove_off_board_moves(self, moves: list[tuple[int, int]]) -> list[tuple[int, int]]:
        current_pos = self.current_pos()
        return [move for move in moves if (0 <= move[0] <= 7 and 0 <= move[1] <= 7 and move != current_pos)]

    def linear_moves(self, current_layout: np.ndarray, y_step: int, x_step: int) -> list[tuple[int, int]]:
        possible_moves: list[tuple[int, int]] = []
        x, y = self.x(), self.y()
        x += x_step
        y += y_step

        while 0 <= x < 8 and 0 <= y < 8:
            square = current_layout[y, x]
            if square is None:
                possible_moves.append((y, x))
            elif square.color() != self.color():
                possible_moves.append((y, x))
                break
            else:
                break

            x += x_step
            y += y_step

        return possible_moves
    
class Pawn(Piece):
    def __init__(self, color: str, start_pos: tuple[int, int]) -> None:
        super().__init__(color, start_pos)
        self._dy = 1 if self.color() == "black" else -1
        
    def dy(self) -> int:
        return self._dy
        
    def movement(self, current_layout: np.ndarray) -> list[tuple[int, int]]:
        possible_moves = []
        x, y = self.x(), self.y()
        above = y + self.dy()
        check_above = current_layout[above, x]
        if check_above is None:
            possible_moves.append((above, x))
            check_above_two = current_layout[above + self.dy(), x]
            if check_above_two is None and self.start_pos() == self.current_pos():
                possible_moves.append((above + self.dy(), x))

        left = x - 1
        if left >= 0:
            check_capture = current_layout[above, left]
            if check_capture is not None and check_capture.color() != self.color():
                possible_moves.append((above, left))
        
        right = x + 1
        if right <= 7:
            check_capture = current_layout[above, right]
            if check_capture is not None and check_capture.color() != self.color():
                possible_moves.append((above, right))
            
        return self.remove_off_board_moves(possible_moves)
    
    def __repr__(self) -> str:
        return f"{self.color()} Pawn"
    
    
class Rook(Piece):
    def __init__(self, color: str, start_pos: tuple[int, int]) -> None:
        super().__init__(color, start_pos)
        
    def movement(self, current_layout: np.ndarray) -> list[tuple[int, int]]:
        possible_moves: list[tuple[int, int]] = []
        directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0)
        ]

        for y_step, x_step in directions:
            possible_moves.extend(self.linear_moves(current_layout, y_step, x_step))

        return possible_moves
    
             
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
        
        on_board_moves = self.remove_off_board_moves(possible_moves) 
        return self.filter_moves(on_board_moves, current_layout)
    
    def filter_moves(self, possible_moves: list[tuple[int, int]], current_layout: np.ndarray) -> list[tuple[int, int]]:
        valid_moves = []
        for move in possible_moves:
            y, x = move
            if current_layout[y, x] is None:
                valid_moves.append(move)
                continue
            
            piece = current_layout[y, x]
            if piece.color() != self.color():
                valid_moves.append(move)
       
        return valid_moves
            
    
    def __repr__(self):
        return f"{self.color()} Knight"
    
class Bishop(Piece):
    def __init__(self, color: str, start_pos: tuple[int, int]) -> None:
        super().__init__(color, start_pos)
        
    def movement(self, current_layout: np.ndarray):
        possible_moves: list[tuple[int, int]] = []
        directions = [
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1)
        ]

        for y_step, x_step in directions:
            possible_moves.extend(self.linear_moves(current_layout, y_step, x_step))

        return possible_moves
    
    def __repr__(self) -> str:
        return f"{self.color()} Bishop"
    
class Queen(Bishop):
    def __init__(self, color: str, start_pos: tuple[int, int]) -> None:
        super().__init__(color, start_pos)
        
    def movement(self, current_layout: np.ndarray):
        possible_moves = super().movement(current_layout)
        rook_directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0)
        ]

        for y_step, x_step in rook_directions:
            possible_moves.extend(self.linear_moves(current_layout, y_step, x_step))

        return possible_moves
    
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
        
        on_board_moves = self.remove_off_board_moves(possible_moves)

        return self.filter_moves(on_board_moves, current_layout)
    
    def filter_moves(self, possible_moves: list[tuple[int, int]], current_layout: np.ndarray):
        valid_moves = []
        for move in possible_moves:
            y, x = move
            if current_layout[y, x] is None:
                valid_moves.append(move)
                continue
            
            piece = current_layout[y, x]
            if piece.color() != self.color():
                valid_moves.append(move)
                
        return valid_moves
    
    def __repr__(self) -> str:
        return f"{self.color()} King"
