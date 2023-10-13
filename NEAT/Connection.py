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

from Config import Config

if typing.TYPE_CHECKING:
    from Node import Node


class Connection:
    def __init__(self, from_node: Node, to_node: Node, *, idn: int = None):
        self.idn = idn
        self.from_node, self.to_node = from_node, to_node
        self.weight = random.uniform(Config.WEIGHT_THRESHOLD[0], Config.WEIGHT_THRESHOLD[1])
        self.split_to: Node = None
        self.is_enabled = True

    def __eq__(self, other):
        if not isinstance(other, Connection):
            return False
        return self.from_node.__eq__(other.from_node) and self.to_node.__eq__(other.to_node)

    def __hash__(self):
        return float(self.from_node.idn * Config.MAX_NUMBER_OF_NODES + self.to_node.idn)
