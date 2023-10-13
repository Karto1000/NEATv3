# -----------------------------------------------------------
# Copyright (c) YPSOMED AG, Burgdorf / Switzerland
# YDS INNOVATION - Digital Innovation
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# email diginno@ypsomed.com
# author: Tim Leuenberger (Tim.leuenberger@ypsomed.com)
# -----------------------------------------------------------
import random

from Config import Config
from NEAT.Client import Client
from NEAT.Genome import Genome


class Species:
    def __init__(self, representative: Client):
        self.members: list[Client] = [representative]
        self.representative: Client = representative

        self.not_breedable = []

    def is_compatible(self, client: Client) -> bool:
        return Genome.distance(client.genome, self.representative.genome) < Config.MIN_ADD_DISTANCE

    def resolve_breedable(self):
        for el in self.not_breedable:
            self.add(el)
            el.species = self

    def add(self, client: Client, *, breedable=True):
        if not breedable:
            self.not_breedable.append(client)
        else:
            self.members.append(client)
            client.species = self

    def breed(self) -> Genome:
        first_client, second_client = random.sample(self.members, 2)

        better_client = first_client if first_client.fitness > second_client.fitness else second_client
        worse_client = first_client if better_client == second_client else second_client

        return Genome.crossover(better_client.genome, worse_client.genome)

    def reset(self):
        pass

    def go_extinct(self):
        self.representative.species = None

        for member in self.members:
            member.species = None

        self.members.clear()

    def __repr__(self):
        return f"Species<{self.members.__repr__()}, representative: {self.representative.__repr__()}>"
