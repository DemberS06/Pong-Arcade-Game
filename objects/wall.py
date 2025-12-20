# wall.py
import pygame
from settings import WALL_THICKNESS, WHITE

class Wall:
    def __init__(
        self,
        orientation: bool,  # True = horizontal, False = vertical
        x,
        y,
        length,
        bounce: bool,
        score: bool,
        active: bool = True,
        left: bool = False,
        color = WHITE
    ):
        self.orientation = orientation
        self.x = x
        self.y = y
        self.length = length
        self.bounce = bounce
        self.score = score
        self.active = active
        self.color = color
        self.left = left

        if self.orientation:  # horizontal
            self.rect = pygame.Rect(x, y, length, WALL_THICKNESS)
        else:  # vertical
            self.rect = pygame.Rect(x, y, WALL_THICKNESS, length)

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color, self.rect)
