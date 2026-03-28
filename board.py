import numpy as np
from pieces import Pawn, King, Knight, Queen, Bishop, Rook, Piece



class ChessBoard:
    def __init__(self) -> None:
        self._board = np.empty((8, 8), dtype=object)
        self._initial_positions = {
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

    def board(self) -> np.ndarray:
        return self._board
    
    def set_piece(self, pos: tuple[int, int], piece: Piece) -> None:
        board = self.board()
        board[pos[0], pos[1]] = piece
    
    def initial_positions(self) -> dict:
        return self._initial_positions
    
    def populate(self) -> None:
        for pos, keys in self.initial_positions().items():
            piece_class: Piece = keys["class"]
            color = keys["color"]
            
            piece_object = piece_class(color, pos)
            self.set_piece(pos, piece_object)


if __name__ == "__main__":
    chess_board = ChessBoard()
    chess_board.populate()