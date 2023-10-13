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
from __future__ import annotations

import copy
import random
import typing

from Config import Config
from NEAT.Connection import Connection
from NEAT.Genome import Genome
from NEAT.Node import Node, NodeType
from NEAT.Species import Species
from NEAT.calculating import CalcNode
from NEAT.utils import IdentificationCollection

if typing.TYPE_CHECKING:
    from NEAT.Client import Client


class NEAT:
    def __init__(self, clients: list[Client], structure: tuple[int, int]):
        self.generation = 1

        self.__species: list[Species] = []
        self.__clients: list[Client] = clients
        self.__structure = structure

        self.__global_nodes: IdentificationCollection[Node] = IdentificationCollection(sort_key=lambda n: n.x)
        self.__global_connections: IdentificationCollection[Connection] = IdentificationCollection()

        self.__init_global_nodes()
        self.__init_client_structure()

        for client in self.__clients:
            client.genome._Genome__add_random_connection()

    def next_generation(self):
        self.generation += 1

        self.__generate_species()
        self.__remove_bad_clients()
        self.__remove_extinct_species()
        self.__crossover_genomes()
        self.__mutate_genomes()

        # Update the ui
        for client in self.__clients:
            client.predict(tuple(0.1 for _ in range(Config.STRUCTURE[0])))

    def get_new_node(self, x: float, y: float, *, node_type: NodeType = NodeType.HIDDEN) -> Node:
        new_node = Node(idn=self.__get_node_identification(), x=x, y=y, node_type=node_type)
        self.__global_nodes.add(new_node)
        return new_node

    def get_connection(self, from_node: Node, to_node: Node) -> Connection:
        connection = Connection(
            from_node=from_node,
            to_node=to_node
        )
        connection.idn = connection.__hash__()

        if self.__global_connections.contains(connection):
            return self.__global_connections.get(connection.idn)

        self.__global_connections.add(connection)
        return connection

    def get_species(self) -> list[Species]:
        return self.__species

    def __get_node_identification(self) -> float:
        return float(self.__global_nodes.size())

    def __generate_species(self):
        # Reset species
        for species in self.__species:
            species.reset()

        for client in self.__clients:
            if len(self.__species) == 0:
                # No species yet, generate a new one
                self.__species.append(Species(client))
                continue

            species_copy = copy.copy(self.__species)
            random.shuffle(species_copy)

            for species in species_copy:
                if species.is_compatible(client):
                    species.add(client)
                    break
            else:
                self.__species.append(Species(client))

        for species in self.__species:
            species.members.sort(key=lambda c: c.fitness, reverse=True)

    def __remove_bad_clients(self):
        for species in self.__species:
            elements_to_remove = round(len(species.members) / 100 * Config.PERCENT_OF_CLIENTS_TO_REMOVE)

            for i in range(elements_to_remove):
                client = species.members.pop()
                client.species = None

    def __remove_extinct_species(self):
        new_species = self.__species.copy()
        for species in self.__species:
            if len(species.members) <= 1:
                species.go_extinct()
                new_species.remove(species)
        self.__species = new_species

    def __crossover_genomes(self):
        for client in self.__clients:
            if client.species is None:
                random_species: Species = random.choice(self.__species)

                new_genome = random_species.breed()
                new_genome.neat = self

                client.genome = new_genome
                random_species.add(client, breedable=False)

        for species in self.__species:
            species.resolve_breedable()

    def __mutate_genomes(self):
        for client in self.__clients:
            client.set_neat(self)
            client.genome.do_random_mutation()

    def __init_global_nodes(self):
        for input_num in range(0, self.__structure[0]):
            self.__global_nodes.add(Node(
                idn=self.__get_node_identification(),
                x=0,
                y=input_num / 10,
                node_type=NodeType.INPUT
            ))

        for output_num in range(self.__structure[0], self.__structure[0] + self.__structure[1]):
            self.__global_nodes.add(Node(
                idn=self.__get_node_identification(),
                x=1,
                y=(output_num - self.__structure[0]) / 10,
                node_type=NodeType.OUTPUT
            ))

    def __init_client_structure(self):
        for input_num in range(0, self.__structure[0]):
            for client in self.__clients:
                client.genome.nodes.add(
                    Node(
                        idn=self.__global_nodes.get(input_num).idn,
                        x=0,
                        y=input_num / 10,
                        node_type=NodeType.INPUT
                    )
                )

                client.calculator.calc_nodes.add(
                    CalcNode(
                        idn=self.__global_nodes.get(input_num).idn,
                        x=0,
                        y=input_num / 10,
                        node_type=NodeType.INPUT
                    )
                )

        for output_num in range(self.__structure[0], self.__structure[0] + self.__structure[1]):
            for client in self.__clients:
                output_node = Node(
                    idn=self.__global_nodes.get(output_num).idn,
                    x=1,
                    y=(output_num - Config.STRUCTURE[0]) / 10,
                    node_type=NodeType.OUTPUT
                )
                output_node.value = 0.5

                client.genome.nodes.add(output_node)

                client.calculator.calc_nodes.add(
                    CalcNode(
                        idn=self.__global_nodes.get(output_num).idn,
                        x=1,
                        y=(output_num - Config.STRUCTURE[0]) / 10,
                        node_type=NodeType.OUTPUT
                    )
                )

        # Set Neat for each client
        for client in self.__clients:
            client.set_neat(self)
