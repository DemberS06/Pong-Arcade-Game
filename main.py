# main.py
import pygame
from settings import WIDTH, HEIGHT, FPS, BLACK

import pygame
from settings import WIDTH, HEIGHT, FPS, NUM_IA, layers_size, PATH_L, PATH_R, GEN
from game import Game
from IA.IA import Genetic_IA
from IA.Evolution import mutate, merge

def play(IAsL, IAsR):
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()

    game = Game(screen, IAsL, IAsR)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.handle_input()
        running = game.updateIA()
        game.draw()

        pygame.display.flip()
        clock.tick(FPS)
    game.save_IA(IAsL, IAsR)
    pygame.quit()

def main():
    BESTL = Genetic_IA(layers_size)
    BESTR = Genetic_IA(layers_size)

    BESTL.load_from_path(PATH_L+str(GEN)+".json")
    #BESTR.load_from_path(PATH_R+str(GEN)+".json")
    for _ in range(10000):
        IAsL = []
        IAsR = []

        for i in range(NUM_IA):
            IAsL.append(merge([BESTL]))
            IAsR.append(merge([BESTR]))
            
            if i>0:
                mutate(IAsL[i])
                mutate(IAsR[i])

        play(IAsL, IAsR)

        BESTL=IAsL[0]
        BESTR=IAsR[0]
    

if __name__ == "__main__":
    main()
