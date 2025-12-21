# game.py
import pygame
import random
from settings import BLACK, WHITE, WIDTH, HEIGHT

from settings import (
    PADDLE_HEIGHT, BALL_A, PATH_L, PATH_R, SCORE_X, SCORE_Y, UPG,
    WALL_HX, WALL_UY, WALL_DY, WALL_HLN, WALL_LX, WALL_RX, WALL_VY, WALL_VLN, 
    NUM_IA, TRAINING, PNTS_LMT, GEN, U_COL, U_MOV, U_DIS, U_LIM, U_WIN, U_LOSE,
    P_LFT_IA, P_RGT_IA
)

from objects.paddle import Paddle
from objects.ball import Ball
from objects.wall import Wall
from objects.match import Match

from IA.IA import Genetic_IA
from IA.Evolution import merge

class Game:
    def __init__(self, screen, i=0):
        self.screen = screen

        self.nUPG=UPG
        if i%2<=0: self.nUPG=NUM_IA-UPG

        self.matchs = []
        self.match = Match(pdl_lfta=True, pdl_rgta=True)

        for _ in range(NUM_IA):
            color = (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
            dir = pygame.Vector2(-random.uniform(-0.7, -0.8), (0.5-random.randint(0, 0))*random.uniform(0.9, 0.9))
            self.matchs.append(Match(color=color, balld=dir, pdl_lft_ia=True, pdl_rgt_ia=True))

        for i in range(min(NUM_IA, self.nUPG)):
            self.matchs[i].ball.direction=pygame.Vector2(-random.uniform(-0.7, -0.8), (0.5-random.randint(1, 1))*random.uniform(0.9, 0.9))

        self.walls = [
            # horizontales (rebote)
            Wall(True, WALL_HX, WALL_UY, WALL_HLN, bounce=True, score=False, color=WHITE),
            Wall(True, WALL_HX, WALL_DY, WALL_HLN, bounce=True, score=False, color=WHITE),

            # verticales (puntos)
            Wall(False, WALL_LX, WALL_VY, WALL_VLN, bounce=False, score=True, left=True,  color=BLACK),
            Wall(False, WALL_RX, WALL_VY, WALL_VLN, bounce=False, score=True, left=False, color=BLACK),
        ]

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.match.lft.move(-1)
        if keys[pygame.K_s]:
            self.match.lft.move(1)
        if keys[pygame.K_UP]:
            self.match.rgt.move(-1)
        if keys[pygame.K_DOWN]:
            self.match.rgt.move(1)

    def get_fitness(self, coll, p1, p2, ly, ny, by, mv):
        res = p1*U_WIN-p2*U_LOSE
        if coll: res+=             U_COL
        res+=(1-abs(ny+PADDLE_HEIGHT/2-by)/HEIGHT)*U_DIS
        res+=(  abs(ly-ny)/HEIGHT)*U_MOV
        if mv!=0 and ly==ny: res+= U_LIM

        return res

    def save_IA(self, IAsL, IAsR):
        LBestL = []
        LBestR = []
        mxl=0
        mxr=0

        for i in range(NUM_IA):
            if self.matchs[i].lft_points>=self.matchs[mxl].lft_points:
                mxl=i
                LBestL.clear()
            if self.matchs[i].lft_points==self.matchs[mxl].lft_points:
                LBestL.append(IAsL[i])
            
            if self.matchs[i].rgt_points>=self.matchs[mxr].rgt_points:
                mxr=i
                LBestR.clear()
            if self.matchs[i].rgt_points==self.matchs[mxr].rgt_points:
                LBestR.append(IAsR[i])
        
        if TRAINING <= 0:
            IAsL[0] = merge(LBestL)
            IAsL[0].save_to_path(PATH_L+str(GEN)+".json")
        
        if TRAINING >=0:
            IAsR[0] = merge(LBestR)
            IAsR[0].save_to_path(PATH_R+str(GEN)+".json")

    def updateIA(self, IAsL, IAsR):
        ok = False
        for (L, R, M) in zip(IAsL, IAsR, self.matchs):
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

            if collided: M.ball.speed+=BALL_A
            
            ball_pos=M.ball.get_pos()
            ball_vel=M.ball.get_vel()

            inputL = [(M.lft.rect.y+PADDLE_HEIGHT/2)/HEIGHT, (ball_pos.x-M.lft.rect.x)/WIDTH, (ball_pos.y-PADDLE_HEIGHT/2-M.lft.rect.y)/HEIGHT, ball_vel.x/WIDTH, ball_vel.y/HEIGHT]
            inputR = [(M.rgt.rect.y+PADDLE_HEIGHT/2)/HEIGHT, (ball_pos.x-M.rgt.rect.x)/WIDTH, (ball_pos.y-PADDLE_HEIGHT/2-M.rgt.rect.y)/HEIGHT, ball_vel.x/WIDTH, ball_vel.y/HEIGHT]
            
            if TRAINING<=0:
                ly=M.lft.rect.y
                move=L.query(inputL)
                M.lft.move(move)
                M.lft_points+=self.get_fitness(coll = collided, p1 = lft, p2 = rgt, ly = ly, ny = M.lft.rect.y, by = ball_pos.y, mv=move)
            if TRAINING>=0:
                ly=M.rgt.rect.y
                move=R.query(inputR)
                M.rgt.move(move)
                M.rgt_points+=self.get_fitness(coll = collided, p1 = rgt, p2 = lft, ly = ly, ny = M.rgt.rect.y, by = ball_pos.y, mv=move)
        return ok       

    def update(self, BESTL, BESTR):
        if self.match.active(PNTS_LMT)==False:
            return False
        
        obj = []
        obj.append(self.match.lft)
        obj.append(self.match.rgt)

        for w in self.walls:
            if w.active:
                obj.append(w)
        
        collided, lft, rgt = self.match.ball.move_with_collision(obj)

        if collided:
            if lft or rgt:
                self.match.lft_points+=lft
                self.match.rgt_points+=rgt
            else:
                self.match.ball.speed+=BALL_A

        ball_pos=self.match.ball.get_pos()
        ball_vel=self.match.ball.get_vel()

        if P_LFT_IA:
            inputL = [(self.match.lft.rect.y+PADDLE_HEIGHT/2)/HEIGHT, (ball_pos.x-self.match.lft.rect.x)/WIDTH, (ball_pos.y-PADDLE_HEIGHT/2-self.match.lft.rect.y)/HEIGHT, ball_vel.x/WIDTH, ball_vel.y/HEIGHT]
            move=BESTL.query(inputL)
            self.match.lft.move(move)
        if P_RGT_IA:
            inputR = [(self.match.rgt.rect.y+PADDLE_HEIGHT/2)/HEIGHT, (ball_pos.x-self.match.rgt.rect.x)/WIDTH, (ball_pos.y-PADDLE_HEIGHT/2-self.match.rgt.rect.y)/HEIGHT, ball_vel.x/WIDTH, ball_vel.y/HEIGHT]
            move=BESTR.query(inputR)
            self.match.rgt.move(move)
        
        return True

    def draw(self, i = -1):
        self.screen.fill(BLACK)
        for wall in self.walls:
            if wall.active:
                wall.draw(self.screen)


        if i==-1 and self.match.active(PNTS_LMT):
            self.match.lft.draw(self.screen)
            self.match.rgt.draw(self.screen)
            self.match.ball.draw(self.screen)
            font = pygame.font.SysFont("Arial", 48)
            score_text = font.render(str(self.match.lft_points)+"   "+str(self.match.rgt_points), True, self.match.color)
            self.screen.blit(score_text, (SCORE_X, SCORE_Y))
            return

        ok = 0

        for M in self.matchs:
            if M.active(PNTS_LMT)==False:
                continue
            
            if TRAINING<=0:
                M.lft.draw(self.screen)
            if TRAINING>=0:
                M.rgt.draw(self.screen)
            M.ball.draw(self.screen)

            if ok: continue
            ok=1
            font = pygame.font.SysFont("Arial", 48)
            score_text = font.render("G: "+str(i)+"                   "+str(M.lft_points)+"   "+str(M.rgt_points), True, M.color)
            self.screen.blit(score_text, (SCORE_X, SCORE_Y))

