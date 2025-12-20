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

        BEST_L = Genetic_IA(layers_size)
        BEST_R = Genetic_IA(layers_size)

        BEST_L.load_from_path(PATH_L+str(GEN)+".json")
        BEST_R.load_from_path(PATH_R+str(GEN)+".json")

        for i in range(NUM_IA):
            IAsL.append(mutate(BEST_L))
            IAsR.append(mutate(BEST_R))
            

        play(IAsL, IAsR)
    

if __name__ == "__main__":
    main()
