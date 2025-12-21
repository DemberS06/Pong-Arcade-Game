# game.py
import pygame
import random
from settings import BLACK, WHITE, WIDTH, HEIGHT

from settings import (
    PAD_LX, PAD_RX, PAD_Y,
    BALL_X, BALL_Y, BALL_RADIUS, BALL_SPEED,
    WALL_HX, WALL_UY, WALL_DY, WALL_HLN, WALL_LX, WALL_RX, WALL_VY, WALL_VLN, 
    SCORE_X, SCORE_Y, NUM_IA, TRAINING, PATH_L, PATH_R, PNTS_LMT, GEN
)

from objects.paddle import Paddle
from objects.ball import Ball
from objects.wall import Wall
from objects.match import Match

from IA.IA import Genetic_IA
from IA.Evolution import merge

class Game:
    def __init__(self, screen, IAsL, IAsR):
        self.screen = screen
        self.IAsL=IAsL
        self.IAsR=IAsR

        self.ball = Ball(BALL_X, BALL_Y, WHITE, direction=pygame.Vector2(random.uniform(-1, 0), random.uniform(-1, 1)), speed=BALL_SPEED, radius=BALL_RADIUS)
        self.left_paddle =  Paddle(PAD_LX, PAD_Y, active=True)
        self.right_paddle = Paddle(PAD_RX, PAD_Y, active=True)

        self.matchs = []
        self.pointsl=0
        self.pointsr=0

        for _ in range(NUM_IA):
            color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
            dir = pygame.Vector2(random.uniform(-1, -0.9), random.uniform(-0.4, 0.4))
            self.matchs.append(Match(color=color, balld=dir, pdl_lft_ia=True, pdl_rgt_ia=True))

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
        for (L, R, M) in zip(self.IAsL, self.IAsR, self.matchs):
            if M.active(PNTS_LMT)==False:
                continue
            else:
                ok=True
            obj = []
            obj.append(M.lft)
            obj.append(M.rgt)

            for w in self.walls:
                if w.active:
                    obj.append(w)
            
            collided, lft, rgt = M.ball.move_with_collision(obj)

            if collided:
                if lft or rgt:
                    M.lft_points+=lft-rgt*2
                    M.rgt_points+=rgt
                else:
                    M.ball.speed+=0.01
                    M.lft_points+=0.05
            
            ball_pos=M.ball.get_pos()
            ball_vel=M.ball.get_vel()

            inputL = [M.lft.rect.x/WIDTH, M.lft.rect.y/HEIGHT, ball_pos.x/WIDTH, ball_pos.y/HEIGHT, ball_vel.x/BALL_SPEED, ball_vel.y/BALL_SPEED]
            inputR = [M.rgt.rect.x/WIDTH, M.rgt.rect.y/HEIGHT, ball_pos.x/WIDTH, ball_pos.y/HEIGHT, ball_vel.x/BALL_SPEED, ball_vel.y/BALL_SPEED]
            inputL[0]=0
            if TRAINING<=0:
                M.lft_points+=M.lft.move(L.query(inputL))/5000000 + (WIDTH-abs(M.lft.rect.y+PAD_Y/2-ball_pos.y))/WIDTH/3000000
            #if TRAINING>=0:
                #self.pad_rgt[i].points+=self.pad_rgt[i].move(self.IAsR[i].query(inputR))/4000
        return ok
    

        for i in range(NUM_IA):
            if self.pad_lft[i].points>=PNTS_LMT or self.pad_rgt[i].points>=PNTS_LMT:
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
                    self.pad_lft[i].points+=lft-rgt*2
                    self.pad_rgt[i].points+=rgt
                else:
                    self.balls[i].speed+=0.01
                    self.pad_lft[i].points+=0.05
            
            ball_pos=self.balls[i].get_pos()
            ball_vel=self.balls[i].get_vel()

            inputL = [self.pad_lft[i].rect.x/WIDTH, self.pad_lft[i].rect.y/HEIGHT, ball_pos.x/WIDTH, ball_pos.y/HEIGHT, ball_vel.x/BALL_SPEED, ball_vel.y/BALL_SPEED]
            inputR = [self.pad_rgt[i].rect.x/WIDTH, self.pad_rgt[i].rect.y/HEIGHT, ball_pos.x/WIDTH, ball_pos.y/HEIGHT, ball_vel.x/BALL_SPEED, ball_vel.y/BALL_SPEED]
            inputL[0]=0
            if TRAINING<=0:
                self.pad_lft[i].points+=self.pad_lft[i].move(self.IAsL[i].query(inputL))/5000000 + (WIDTH-abs(self.pad_lft[i].rect.y+PAD_Y/2-ball_pos.y))/WIDTH/3000000
            if TRAINING>=0:
                self.pad_rgt[i].points+=self.pad_rgt[i].move(self.IAsR[i].query(inputR))/4000
        return ok

    def update(self):

        if self.updateIA():
            return True
        else:
            return False
            LBestL = []
            LBestR = []
            mxl=0
            mxr=0

            for i in range(NUM_IA):
                if self.points_lft[i]>=self.points_lft[mxl]:
                    mxl=i
                    LBestL.clear()
                if self.points_lft[i]==self.points_lft[mxl]:
                    LBestL.append(self.IAsL[i])
                
                if self.points_rgt[i]>self.points_rgt[mxr]:
                    mxr=i
                    LBestR.clear()
                if self.points_rgt[i]==self.points_rgt[mxr]:
                    LBestR.append(self.IAsR[i])
            
            from main import BESTL, BESTR
            if TRAINING <= 0:
                BESTL = merge(LBestL)
                BESTL.save_to_path(PATH_L+str(GEN)+".json")
            
            if TRAINING >=0:
                BESTR = merge(LBestR)
                BESTR.save_to_path(PATH_R+str(GEN)+".json")
            
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

        #self.left_paddle.draw(self.screen)
        #self.right_paddle.draw(self.screen)
        #self.ball.draw(self.screen)

        for M in self.matchs:
            if M.active(PNTS_LMT)==False:
                continue
            
            if TRAINING<=0:
                M.lft.draw(self.screen)
            if TRAINING>=0:
                M.rgt.draw(self.screen)
            M.ball.draw(self.screen)

            font = pygame.font.SysFont("Arial", 48)
            score_text = font.render(str(M.lft_points)+"   "+str(M.rgt_points), True, (255,255,255))
            self.screen.blit(score_text, (SCORE_X, SCORE_Y))

