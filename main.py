import random
import sys

import pygame

from Config import Config
from NEAT import NEAT
from NEAT.Client import Client

pygame.init()
SCREEN = pygame.display.set_mode((Config.SW, Config.SH))
FONT = pygame.font.SysFont("Arial", 12)
current_client = 0

seed = random.randrange(sys.maxsize)
random.seed(1703487886160643318)
print(seed)


class FlappyClient(Client):
    def __init__(self):
        super().__init__()
        self.fitness = random.uniform(0, 20)

    def draw(self):
        for node in self.calculator.calc_nodes:
            pygame.draw.circle(
                SCREEN,
                (0, 0, 0),
                (node.x * Config.NODE_X_MULTIPLIER + Config.NETWORK_PADDING[0],
                 node.y * Config.NODE_Y_MULTIPLIER + Config.NETWORK_PADDING[1]),
                Config.NODE_RADIUS + abs(node.output * 2)
            )

            pygame.draw.circle(
                SCREEN,
                (255, 255, 255),
                (node.x * Config.NODE_X_MULTIPLIER + Config.NETWORK_PADDING[0],
                 node.y * Config.NODE_Y_MULTIPLIER + Config.NETWORK_PADDING[1]),
                Config.NODE_RADIUS - 2
            )

            val_text = FONT.render(f"{round(node.output, 2)}", True, (0, 0, 0))
            SCREEN.blit(
                val_text,
                (
                    node.x * Config.NODE_X_MULTIPLIER + Config.NETWORK_PADDING[0] - val_text.get_width() / 2,
                    node.y * Config.NODE_Y_MULTIPLIER + Config.NETWORK_PADDING[1] - val_text.get_height() / 2
                )
            )

            for connection in node.connections_to:
                color = (0, 0, 0)

                if not connection.is_enabled:
                    color = (0, 255, 0)
                elif connection.weight < 0:
                    color = (255, 0, 0)

                pygame.draw.line(
                    SCREEN,
                    color,
                    (
                        connection.from_node.x * Config.NODE_X_MULTIPLIER + Config.NETWORK_PADDING[
                            0] + Config.NODE_RADIUS + abs(connection.from_node.output * 2),
                        connection.from_node.y * Config.NODE_Y_MULTIPLIER + Config.NETWORK_PADDING[1]
                    ),
                    (
                        connection.to_node.x * Config.NODE_X_MULTIPLIER + Config.NETWORK_PADDING[
                            0] - Config.NODE_RADIUS - abs(connection.to_node.output * 2),
                        connection.to_node.y * Config.NODE_Y_MULTIPLIER + Config.NETWORK_PADDING[1]
                    ),
                    max(1, round(abs(connection.weight) * 3))
                )


clients = [FlappyClient() for i in range(Config.AMOUNT_OF_CLIENTS)]
neat = NEAT(clients, structure=Config.STRUCTURE)

inputs = (0, 0, 0)

while True:
    SCREEN.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                inputs = (inputs[0] + 0.5, inputs[1] + 0.5, inputs[2] + 0.5)
                clients[current_client].predict(inputs)
            elif event.y == -1:
                inputs = (inputs[0] - 0.5, inputs[1] - 0.5, inputs[2] - 0.5)
                clients[current_client].predict(inputs)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                neat.next_generation()
                clients[current_client].predict(inputs)
            if event.key == pygame.K_RIGHT:
                current_client = (current_client + 1) % Config.AMOUNT_OF_CLIENTS
            if event.key == pygame.K_LEFT:
                current_client = (current_client - 1) % Config.AMOUNT_OF_CLIENTS

    clients[current_client].draw()

    species = neat.get_species()

    for i, species_ in enumerate(species):
        species_num = FONT.render(f"Species {i}", True, (0, 0, 0))
        SCREEN.blit(species_num, (Config.SW - species_num.get_width(), species_num.get_height() * i + 5))

    text = FONT.render(f"Current Client: {current_client}", True, (0, 0, 0))
    SCREEN.blit(text, (0, 0))

    pygame.display.flip()
