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
from NEAT import NodeType
from NEAT.utils import sigmoid


class CalcNode:
    def __init__(self, *, x: float, y: float, node_type: NodeType, idn: float):
        self.idn = idn
        self.x, self.y = x, y
        self.output = 0
        self.node_type = node_type
        self.connections_to: list[CalcConnection] = []

    def calculate(self):
        for connection_to in self.connections_to:
            if not connection_to.is_enabled:
                continue

            self.output += connection_to.weight * connection_to.from_node.output

        if self.node_type != NodeType.INPUT:
            self.output = sigmoid(self.output)

    def __repr__(self):
        return f"CalcNode<output {self.output}>"

    def __hash__(self):
        return self.idn


class CalcConnection:
    def __init__(self, from_node: CalcNode, to_node: CalcNode, weight: float, is_enabled: bool):
        self.from_node, self.to_node = from_node, to_node
        self.weight = weight
        self.is_enabled = is_enabled

    def __repr__(self):
        return f"CalcConnection<enabled {self.is_enabled} weight {self.weight}>"

    def __hash__(self):
        return float(self.from_node.idn * Config.MAX_NUMBER_OF_NODES + self.to_node.idn)
