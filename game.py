# game.py
import pygame
from settings import WIDTH, HEIGHT, BLACK
from objects.paddle import Paddle

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.left_paddle = Paddle(30, HEIGHT // 2 - 50)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.left_paddle.move(-1)
        if keys[pygame.K_s]:
            self.left_paddle.move(1)

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)
        self.left_paddle.draw(self.screen)
