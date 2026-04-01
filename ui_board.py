import pygame
from board import Square


        
    
class UIBoard:
    def __init__(self) -> None:
        pass
        
        
    def draw(self, squares: list[Square]) -> None:
        screen = pygame.display.get_surface()
        for square in squares:
            pygame.draw.rect(screen, square.color(), square.square())
            
