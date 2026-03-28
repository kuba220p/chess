import numpy as np
from pieces import Pawn, King, Knight, Queen, Bishop, Rook, Piece

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

class ChessBoard:
    def __init__(self, board: np.ndarray) -> None:
        self._board = board

    def board(self) -> np.ndarray:
        return self._board
     
    @classmethod
    def populate(cls) -> "ChessBoard":
        board = np.empty((8, 8), dtype=object)
        for pos, keys in _INITIAL_POSITIONS.items():
            piece_class: Piece = keys["class"]
            color = keys["color"]

            board[pos[0], pos[1]] = piece_class(color, pos)
            
        return cls(board)
