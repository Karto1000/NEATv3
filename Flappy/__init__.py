import random

import numpy.random
import pygame

from Config import Config
from NEAT import NEAT
from NEAT.Client import Client

pygame.init()
SCREEN = pygame.display.set_mode((Config.SW, Config.SH))
FONT = pygame.font.Font("./assets/fonts/PixelifySans-Regular.ttf", 24)
pygame.display.set_caption("Flappy Bird AI")

seed = random.randrange(pow(2, 32))
random.seed(seed)
numpy.random.seed(seed)


class Game:
    def __init__(self):
        self.birds = [Bird() for _ in range(Config.AMOUNT_OF_CLIENTS)]
        self.neat = NEAT(self.birds, structure=Config.STRUCTURE)
        self.current_client = 0

        self.background_image = pygame.image.load("assets/background.png")
        self.bird_image = pygame.transform.scale(pygame.image.load("assets/bird.png"), (50, 50))
        pygame.display.set_icon(self.bird_image)

    def draw(self):
        for x in range(0, 800, 360):
            SCREEN.blit(
                self.background_image,
                (x, 0)
            )

        for i, bird in enumerate(self.birds):
            bird.draw(is_current_client=self.current_client == i)

        text = FONT.render(f"Current Client: {self.current_client}", True, (255, 255, 255))
        SCREEN.blit(text, Config.TEXT_PADDING)


class Bird(Client):
    def __init__(self):
        super().__init__()
        self.sprite_width, self.sprite_height = 50, 50
        self.x, self.y = 50, Config.SH // 2 - self.sprite_height // 2

    def draw(self, is_current_client: bool):
        if is_current_client:
            SCREEN.blit(
                game.bird_image,
                (self.x, self.y)
            )


game = Game()

while True:
    SCREEN.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    game.draw()

    # species = neat.get_species()
    #
    # for i, species_ in enumerate(species):
    #     species_num = FONT.render(f"Species {i}", True, (0, 0, 0))
    #     SCREEN.blit(species_num, (Config.SW - species_num.get_width() - 5, species_num.get_height() * i + 5))

    pygame.display.flip()
