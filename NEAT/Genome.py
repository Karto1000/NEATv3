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

import random
import typing

import numpy

from Config import Config
from NEAT.Connection import Connection
from NEAT.Node import Node
from NEAT.utils import IdentificationCollection

if typing.TYPE_CHECKING:
    from NEAT import NEAT


class Genome:
    def __init__(self):
        self.connections: IdentificationCollection[Connection] = IdentificationCollection(sort_key=lambda c: c.idn)
        self.nodes: IdentificationCollection[Node] = IdentificationCollection(sort_key=lambda e: e.x)
        self.neat: NEAT = None

    def do_random_mutation(self):
        weights = [
            Config.ACTIONS_CHANCES.get("CHANCE_TO_REPLACE_WEIGHT"),
            Config.ACTIONS_CHANCES.get("CHANCE_TO_ADD_CONNECTION"),
            Config.ACTIONS_CHANCES.get("CHANCE_TO_ADD_NODE"),
            Config.ACTIONS_CHANCES.get("CHANCE_TO_SHIFT"),
            Config.ACTIONS_CHANCES.get("CHANCE_TO_TOGGLE"),
            Config.ACTIONS_CHANCES.get("NONE")
        ]

        operations = [
            self.__replace_random_weight,
            self.__add_random_connection,
            self.__add_random_node,
            self.__shift_random_weight,
            self.__toggle_random_connection,
            None
        ]

        fun: typing.Optional[typing.Callable] = numpy.random.choice(operations, p=weights)

        if fun is not None:
            fun()

    @classmethod
    def crossover(cls, better: 'Genome', worse: 'Genome') -> 'Genome':
        better_idn = list(map(lambda c: c.idn, better.connections.items()))
        worse_idn = list(map(lambda c: c.idn, worse.connections.items()))

        merged_idn = list(dict.fromkeys([*better_idn, *worse_idn]))
        merged_idn.sort()

        better_greatest_connection = better.connections.get(-1)
        worse_greatest_connection = worse.connections.get(-1)

        if better_greatest_connection.idn > worse_greatest_connection.idn:
            greater_genome = better
            smaller_genome = worse
        elif better_greatest_connection.idn < worse_greatest_connection.idn:
            greater_genome = worse
            smaller_genome = better
        else:
            greater_genome, smaller_genome = random.sample([better, worse], 2)

        new_genome = Genome()

        for idn in merged_idn:
            better_connection = better.connections.get(idn)
            worse_connection = worse.connections.get(idn)

            # Both
            if better_connection and worse_connection:
                chosen_connection = random.choice([better_connection, worse_connection])
                new_genome.connections.add(chosen_connection)
                continue

            if idn > smaller_genome.connections.get(-1).idn:
                # Excess
                # Add to new genome if the greater genome is the better genome
                if greater_genome == better:
                    new_genome.connections.add(greater_genome.connections.get(idn))
                    continue

            if better_connection and not worse_connection:
                # Disjoint Better
                new_genome.connections.add(better_connection)
                continue

            if worse_connection and not better_connection:
                # Disjoint Worse
                new_genome.connections.add(worse_connection)

        for i in range(Config.STRUCTURE[0] + Config.STRUCTURE[1]):
            new_genome.nodes.add(better.nodes.get(float(i)))

        for connection in new_genome.connections:
            if not new_genome.nodes.contains(connection.from_node):
                new_genome.nodes.add(connection.from_node)
            if not new_genome.nodes.contains(connection.to_node):
                new_genome.nodes.add(connection.to_node)

        return new_genome

    @classmethod
    def distance(cls, first: 'Genome', second: 'Genome') -> float:
        self_sorted_connections = sorted(first.connections.items(), key=lambda c: c.idn)
        other_sorted_connections = sorted(second.connections.items(), key=lambda c: c.idn)

        # They are the same
        if len(self_sorted_connections) == len(other_sorted_connections):
            return 0

        # One of the genomes has no connections
        if len(self_sorted_connections) == 0 or len(other_sorted_connections) == 0:
            return 1

        if self_sorted_connections[-1].idn > other_sorted_connections[-1].idn:
            larger_connections = self_sorted_connections
            smaller_connections = other_sorted_connections
        else:
            larger_connections = other_sorted_connections
            smaller_connections = self_sorted_connections

        larger_index = 0
        smaller_index = 0

        disjoint_genes = 0
        weight_difference = 0
        similar_weights = 0

        while larger_index < len(larger_connections) and smaller_index < len(smaller_connections):
            larger_connection = larger_connections[larger_index]
            smaller_connection = smaller_connections[smaller_index]

            if larger_connection.idn == smaller_connection.idn:
                larger_index += 1
                smaller_index += 1
                similar_weights += 1
            elif larger_connection.idn > smaller_connection.idn:
                smaller_index += 1
                disjoint_genes += 1
            else:
                larger_index += 1
                disjoint_genes += 1

        weight_difference /= similar_weights if similar_weights > 0 else 1
        excess_genes = len(larger_connections) - larger_index

        n = max(len(larger_connections), len(smaller_connections))
        n = 1 if n < 20 else n

        return disjoint_genes / n + excess_genes / n + weight_difference

    def __add_connection(self, first: Node, second: Node):
        new_connection = self.neat.get_connection(first, second)
        self.connections.add(new_connection)

    def __add_node(self, connection: Connection):
        if connection.split_to:
            new_node = connection.split_to
        else:
            new_node = self.neat.get_new_node(
                round(connection.from_node.x + (connection.to_node.x - connection.from_node.x) / 2, 2),
                round(connection.from_node.y + (connection.to_node.y - connection.from_node.y) / 2, 2)
            )
            connection.split_to = new_node

        new_from_connection = self.neat.get_connection(connection.from_node, new_node)
        new_from_connection.weight = 1

        new_to_connection = self.neat.get_connection(new_node, connection.to_node)
        new_to_connection.weight = connection.weight

        self.nodes.add(new_node)

        self.connections.add(new_from_connection)
        self.connections.add(new_to_connection)

        self.connections.remove(connection)

    @staticmethod
    def __shift_weight(connection: Connection):
        amount = random.uniform(Config.WEIGHT_SHIFT_THRESHOLD[0], Config.WEIGHT_SHIFT_THRESHOLD[1])
        connection.weight += amount

    @staticmethod
    def __toggle_connection(connection: Connection):
        connection.is_enabled = not connection.is_enabled

    @staticmethod
    def __replace_weight(connection: Connection):
        connection.weight = random.uniform(Config.WEIGHT_THRESHOLD[0], Config.WEIGHT_THRESHOLD[1])

    def __add_random_connection(self):
        first_node = random.choice(list(filter(lambda n: n.x < 1, self.nodes)))
        second_node = random.choice(list(filter(lambda n: n.x > first_node.x and n.idn != first_node.idn, self.nodes)))

        for connection in self.connections:
            if connection.from_node == first_node and connection.to_node == second_node:
                return

        self.__add_connection(first_node, second_node)

    def __add_random_node(self):
        if len(self.connections) == 0:
            print("No connections to split")
            return

        connection = random.choice(self.connections)
        self.__add_node(connection)

    def __shift_random_weight(self):
        if len(self.connections) == 0:
            print("No connections to shift weight of")
            return

        connection = random.choice(self.connections)
        self.__shift_weight(connection)

    def __toggle_random_connection(self):
        if len(self.connections) == 0:
            print("No connections to toggle weight of")
            return

        connection = random.choice(self.connections)
        self.__toggle_connection(connection)

    def __replace_random_weight(self):
        if len(self.connections) == 0:
            print("No connections to replace weight of")
            return

        connection = random.choice(self.connections)
        self.__replace_weight(connection)
