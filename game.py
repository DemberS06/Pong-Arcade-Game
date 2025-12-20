# game.py
import pygame
import random
from settings import BLACK, WHITE
from objects.paddle import Paddle

from objects.wall import Wall

from settings import (
    PAD_LX, PAD_RX, PAD_Y,
    BALL_X, BALL_Y, BALL_RADIUS, BALL_SPEED, BALL_DIR,
    WALL_HX, WALL_UY, WALL_DY, WALL_HLN, WALL_LX, WALL_RX, WALL_VY, WALL_VLN, 
    SCORE_X, SCORE_Y, NUM_IA, TRAINING, PATH_L, PATH_R, PNTS_LMT
)

from objects.ball import Ball

from IA.IA import Genetic_IA
from IA.Evolution import merge

class Game:
    def __init__(self, screen, IAsL, IAsR):
        self.screen = screen
        self.IAsL=IAsL
        self.IAsR=IAsR

        self.ball = Ball(BALL_X, BALL_Y, WHITE, direction=BALL_DIR, speed=BALL_SPEED, radius=BALL_RADIUS)
        self.left_paddle =  Paddle(PAD_LX, PAD_Y, active=True)
        self.right_paddle = Paddle(PAD_RX, PAD_Y, active=True)

        self.balls = []
        self.pad_lft = []
        self.pad_rgt = []
        self.points_lft = []
        self.points_rgt = []
        self.pointsl=0
        self.pointsr=0

        for i in range(NUM_IA):
            color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
            self.balls.append(Ball(BALL_X, BALL_Y, color, direction=BALL_DIR, speed=BALL_SPEED, radius=BALL_RADIUS))
            self.pad_lft.append(Paddle(PAD_LX, PAD_Y, color=color, active=True))
            self.pad_rgt.append(Paddle(PAD_RX, PAD_Y, color=color, active=True))
            self.points_lft.append(0)
            self.points_rgt.append(0)

        self.walls = [
            # horizontales (rebote)
            Wall(True, WALL_HX, WALL_UY, WALL_HLN, bounce=True, score=False, color=WHITE),
            Wall(True, WALL_HX, WALL_DY, WALL_HLN, bounce=True, score=False, color=WHITE),

            # verticales (puntos)
            Wall(False, WALL_LX, WALL_VY, WALL_VLN, bounce=False, score=True, left=True,  color=WHITE),
            Wall(False, WALL_RX, WALL_VY, WALL_VLN, bounce=True, score=False, left=False, color=WHITE),
        ]

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

    def updateIA(self):
        ok = False
        for i in range(NUM_IA):
            if self.points_lft[i]>=PNTS_LMT or self.points_rgt[i]>=PNTS_LMT:
                continue
            else:
                ok=True
            objects = []
            objects.append(self.pad_lft[i])
            objects.append(self.pad_rgt[i])
            
            for w in self.walls:
                if w.active:
                    objects.append(w)
            
            collided, lft, rgt = self.balls[i].move_with_collision(objects)

            if collided:
                if lft or rgt:
                    self.points_lft[i]+=lft
                    self.points_rgt[i]+=rgt
                else:
                    self.balls[i].speed+=0.1
                    self.points_lft[i]+=0.1
            
            ball_pos=self.balls[i].get_pos()
            ball_vel=self.balls[i].get_vel()

            inputL = [self.pad_lft[i].rect.x, self.pad_lft[i].rect.y, ball_pos.x, ball_pos.y, ball_vel.x, ball_vel.y]
            inputR = [self.pad_rgt[i].rect.x, self.pad_rgt[i].rect.y, ball_pos.x, ball_pos.y, ball_vel.x, ball_vel.y]

            if TRAINING<=0:
                self.pad_lft[i].move(self.IAsL[i].query(inputL))
            if TRAINING>=0:
                self.pad_rgt[i].move(self.IAsR[i].query(inputR))
        return ok

    def update(self):

        if self.updateIA():
            return True
        else:
            BestL = []
            BestR = []
            mxl=0
            mxr=0

            for i in range(NUM_IA):
                if self.points_lft[i]>self.points_lft[mxl]:
                    mxl=i
                    BestL.clear()
                if self.points_lft[i]==self.points_lft[mxl]:
                    BestL.append(self.IAsL[i])
                
                if self.points_rgt[i]>self.points_rgt[mxr]:
                    mxr=i
                    BestR.clear()
                if self.points_rgt[i]==self.points_rgt[mxr]:
                    BestR.append(self.IAsR[i])
            
            if TRAINING <= 0:
                IALft = merge(BestL)
                IALft.save_to_path(PATH_L+str(0)+".json")
            
            if TRAINING >=0:
                IARgt = merge(BestR)
                IARgt.save_to_path(PATH_R+str(0)+".json")
            
            return False
        

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

        if TRAINING<=0:
            for pd in self.pad_lft:
                pd.draw(self.screen)
        if TRAINING>=0:
            for pd in self.pad_rgt:
                pd.draw(self.screen)
        for bll in self.balls:
            bll.draw(self.screen)
        #self.left_paddle.draw(self.screen)
        #self.right_paddle.draw(self.screen)
        #self.ball.draw(self.screen)

        for i in range (NUM_IA):
            if self.points_lft[i]>=PNTS_LMT or self.points_rgt[i]>=PNTS_LMT:
                continue
            font = pygame.font.SysFont("Arial", 48)
            score_text = font.render(str(self.points_lft[i])+"   "+str(self.points_rgt[i]), True, (255,255,255))
            self.screen.blit(score_text, (SCORE_X, SCORE_Y))

