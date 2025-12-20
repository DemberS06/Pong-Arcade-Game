# ball.py
from typing import Iterable
import random
import pygame
from utils.collition import predict_segment_rect
from settings import WIDTH, HEIGHT

class Ball:
    def __init__(self, x: float, y: float, color, direction, speed: float = 6.0, radius: float = 6.0):
        self.pos = pygame.Vector2(float(x), float(y))
        d = pygame.Vector2(direction)
        if d.length_squared() == 0:
            d = pygame.Vector2(1, 0)
        else:
            d = d.normalize()
        self.direction = d
        self.speed = float(speed)
        self.radius = float(radius)
        self.color = color

    @property
    def velocity(self) -> pygame.Vector2:
        return self.direction * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), int(self.radius))

    def _apply_horizontal_collision(self):
        self.direction.y = -self.direction.y
        if self.direction.length_squared() == 0:
            self.direction = pygame.Vector2(1, 0)
        else:
            self.direction = self.direction.normalize()

    def _apply_vertical_collision_random(self):
        old_dx = self.direction.x
        new_dx = -old_dx if abs(old_dx) > 1e-6 else -1.0
        new_dy = random.uniform(-0.9, 0.9)
        new_dir = pygame.Vector2(new_dx, new_dy)
        if new_dir.length_squared() == 0:
            new_dir = pygame.Vector2(-1 if new_dx < 0 else 1, 0)
        self.direction = new_dir.normalize()

    def move_with_collision(self, objects):
        start = pygame.Vector2(self.pos)
        end = start + self.velocity

        nearest = None
        nearest_obj = None
        nearest_d2 = None

        for obj in objects:
            
            rect = getattr(obj, "rect", None)
            col_type, point = predict_segment_rect(start, end, rect, radius=self.radius)
            if col_type == "none":
                continue
            d2 = (point - start).length_squared()
            if nearest is None or d2 < nearest_d2:
                nearest = (col_type, point)
                nearest_obj = obj
                nearest_d2 = d2

        if nearest is None:
            self.pos = end
            return False, 0, 0

        col_type, collision_point = nearest
        self.pos = pygame.Vector2(collision_point)

        # si es score, no rebotamos
        if hasattr(nearest_obj, "score") and nearest_obj.score:
            self.pos = pygame.Vector2(WIDTH/2, HEIGHT/2)
            if nearest_obj.left:
                return True, 0, 1
            else:
                return True, 1, 0
            

        # si es bounce horizontal
        if col_type == "horizontal":
            self.direction.y *= -1
            self.direction = self.direction.normalize()
            return True, 0, 0

        # vertical, pero bounce normal
        if col_type == "vertical":
            # paddle o pared vertical rebote
            # invertir X
            self.direction.x *= -1
            # añadir random pequeño a Y
            self.direction.y += random.uniform(-0.3, 0.3)
            if self.direction.length_squared() == 0:
                self.direction = pygame.Vector2(1, 0)
            else:
                self.direction = self.direction.normalize()
            return True, 0, 0

        return False, 0, 0