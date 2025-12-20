# main.py
import pygame
from settings import WIDTH, HEIGHT, FPS, BLACK

import pygame
from settings import WIDTH, HEIGHT, FPS, NUM_IA, layers_size, PATH_L, PATH_R, GEN
from game import Game
from IA.IA import Genetic_IA
from IA.Evolution import mutate

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
        running = game.update()
        game.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

def main():
    for _ in range(20):
        IAsL = []
        IAsR = []

        for i in range(NUM_IA):
            IAsL.append(Genetic_IA(layers_size))
            IAsR.append(Genetic_IA(layers_size))
            IAsL[i].load_from_path(PATH_L+str(GEN)+".json")
            IAsR[i].load_from_path(PATH_R+str(GEN)+".json")
            mutate(IAsL[i])
            mutate(IAsR[i])

        play(IAsL, IAsR)
    

if __name__ == "__main__":
    main()
