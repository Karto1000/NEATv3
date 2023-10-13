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
from Config import Config
from NEAT import Client
from NEAT.Connection import Connection
from NEAT.Node import Node
from NEAT.calculating import CalcNode, CalcConnection
from NEAT.utils import IdentificationCollection


class Calculator:
    def __init__(self, client: Client):
        self.client: Client = client
        self.calc_nodes: IdentificationCollection[CalcNode] = IdentificationCollection()

    def predict(self, inputs: tuple[float, ...]) -> tuple[float, ...]:
        nodes: list[Node] = self.client.genome.nodes.items()
        connections: list[Connection] = self.client.genome.connections.items()

        self.calc_nodes.clear()

        for node in nodes:
            calc_node = CalcNode(
                x=node.x,
                y=node.y,
                node_type=node.node_type,
                idn=float(node.idn)
            )

            self.calc_nodes.add(calc_node)

        # Set outputs
        for i in range(Config.STRUCTURE[0]):
            self.calc_nodes.get(i).output = inputs[i]

        for connection in connections:
            calc_from = self.calc_nodes.get(float(connection.from_node.idn))
            calc_to = self.calc_nodes.get(float(connection.to_node.idn))

            calc_connection = CalcConnection(
                from_node=calc_from,
                to_node=calc_to,
                is_enabled=connection.is_enabled,
                weight=connection.weight
            )

            calc_to.connections_to.append(calc_connection)

        for node in self.calc_nodes:
            node.calculate()

        outputs = tuple(map(lambda n: n.output, self.calc_nodes.items()[Config.STRUCTURE[1]:]))
        return outputs
