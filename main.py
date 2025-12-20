# main.py
import pygame
from settings import WIDTH, HEIGHT, FPS, BLACK

import pygame
from settings import WIDTH, HEIGHT, FPS, NUM_IA, layers_size
from game import Game
from IA.IA import Genetic_IA

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
    IAsL = []
    IAsR = []

    for i in range(NUM_IA):
        IAsL.append(Genetic_IA(layers_size))
        IAsR.append(Genetic_IA(layers_size))

    play(IAsL, IAsR)
    

if __name__ == "__main__":
    main()
