import pygame# paddle.py
from settings import PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED, WHITE, HEIGHT

class Paddle:
    def __init__(self, x, y, color = WHITE, active: bool=True):
        self.rect = pygame.Rect(
            x,
            y,
            PADDLE_WIDTH,
            PADDLE_HEIGHT
        )
        self.speed = PADDLE_SPEED
        self.color = color
        self.active = active
        self.points = 0

    def move(self, direction):
        self.rect.y += direction * self.speed
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)