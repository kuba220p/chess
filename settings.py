from enum import IntEnum, StrEnum



class SquareSettings(IntEnum):
    SQUARE_WIDTH = 75
    SQUARE_HEIGHT = 75
    
class UIBoardSettings(IntEnum):
    START_X = 330
    START_Y = 50
    END_X = SquareSettings.SQUARE_WIDTH * 8 + START_X
    END_Y = SquareSettings.SQUARE_HEIGHT * 8 + START_Y
    STEP = SquareSettings.SQUARE_WIDTH
                        
class Colors(StrEnum):
    WHITE = "white"
    BLACK = "black"
    SELECTED = "yellow"
    POSSIBLE_MOVE = "green"
    CAN_CAPTURE = "red"