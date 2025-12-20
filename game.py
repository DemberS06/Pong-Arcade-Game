# game.py
import pygame
from settings import WIDTH, HEIGHT, BLACK, WHITE
from objects.paddle import Paddle

from objects.wall import Wall
from settings import (
    WIDTH, HEIGHT,
    WALL_THICKNESS,
    TOP_WALL_Y, BOTTOM_WALL_Y,
    LEFT_WALL_X, RIGHT_WALL_X, PADDLE_x, PADDLE_WIDTH
)

from objects.ball import Ball

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.ball = Ball(WIDTH/2, HEIGHT/2, WHITE, direction=(0.8, -0.6), speed=6, radius=8)
        self.left_paddle = Paddle(PADDLE_x,                         HEIGHT // 2 - 50, active=True)
        self.right_paddle = Paddle(WIDTH - PADDLE_x - PADDLE_WIDTH, HEIGHT // 2 - 50, active=False)
        self.walls = [
            # horizontales (rebote)
            Wall(True, PADDLE_x, 3*WALL_THICKNESS,          WIDTH-2*PADDLE_x, bounce=True, score=False, color=WHITE),
            Wall(True, PADDLE_x, HEIGHT - 4*WALL_THICKNESS, WIDTH-2*PADDLE_x, bounce=True, score=False, color=WHITE),

            # verticales (puntos)
            Wall(False, 0,                                 0, HEIGHT, bounce=False, score=True, left=True, color=BLACK),
            Wall(False, WIDTH - WALL_THICKNESS, 0, HEIGHT, bounce=False, score=True, left=False, color=BLACK),
        ]
        self.pointsl=0
        self.pointsr=0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.left_paddle.move(-1)
        if keys[pygame.K_s]:
            self.left_paddle.move(1)
        if keys[pygame.K_UP]:
            self.right_paddle.move(-1)
        if keys[pygame.K_DOWN]:
            self.right_paddle.move(1)

    def update(self):
        objects = []
        #if self.left_paddle.active:
        objects.append(self.left_paddle)
        #if self.right_paddle.active:
        objects.append(self.right_paddle)

        for w in self.walls:
            if w.active:    
                objects.append(w)

        collided, lft, rgt = self.ball.move_with_collision(objects)

        if collided:
            if lft or rgt:
                self.pointsl+=lft
                self.pointsr+=rgt
            else:
                self.ball.speed+=0.1
        pass

    def draw(self):
        self.screen.fill(BLACK)
        for wall in self.walls:
            if wall.active:
                wall.draw(self.screen)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        font = pygame.font.SysFont("Arial", 48)
        score_text = font.render(str(self.pointsl)+"   "+str(self.pointsr), True, (255,255,255))
        self.screen.blit(score_text, (WIDTH/2, 30))

