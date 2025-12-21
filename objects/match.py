# match.py
import pygame
import random

from objects.paddle import Paddle
from objects.ball import Ball

from settings import (
    WHITE,
    PAD_LX, PAD_RX, PAD_Y,
    BALL_X, BALL_Y, BALL_DIRL, BALL_DIRR, BALL_DIRD, BALL_DIRU, BALL_RADIUS, BALL_SPEED
)


class Match:
    def __init__(self, color = WHITE,
                 pdl_lftx = PAD_LX, pdl_lfty = PAD_Y, pdl_lfta = True, pdl_lft_ia=False,
                 pdl_rgtx = PAD_RX, pdl_rgty = PAD_Y, pdl_rgta = True, pdl_rgt_ia=False,
                 ballx = BALL_X, bally = BALL_Y, ballr = BALL_RADIUS, balls = BALL_SPEED,
                 balld = pygame.Vector2(random.uniform(BALL_DIRL, BALL_DIRR), random.uniform(BALL_DIRD, BALL_DIRU))
                 ):
        self.color = color
        self.lft_ia = pdl_lft_ia
        self.rgt_ia = pdl_rgt_ia
        self.lft = Paddle(x=pdl_lftx, y=pdl_lfty, color=color, active=pdl_lfta)
        self.rgt = Paddle(x=pdl_rgtx, y=pdl_rgty, color=color, active=pdl_rgta)
        self.ball = Ball(x=ballx, y=bally, color=color, direction=balld, speed=balls, radius=ballr)
        self.lft_points = 0
        self.rgt_points = 0

    def active(self, pnt_lmt = 3):
        if self.lft_points>=pnt_lmt or self.rgt_points>=pnt_lmt:
            return False
        if self.lft.active==False and self.rgt.active==False:
            return False
        return True