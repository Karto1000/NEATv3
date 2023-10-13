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

from enum import Enum


class NodeType(Enum):
    INPUT = 1
    HIDDEN = 2
    OUTPUT = 3


class Node:
    def __init__(self, *, x: float, y: float, node_type: NodeType = NodeType.HIDDEN, idn: float = None):
        self.idn = idn
        self.x, self.y = x, y
        self.node_type = node_type

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return other.idn == self.idn

    def __hash__(self):
        return self.idn

    def __repr__(self):
        return f"Node<idn {self.idn} x {self.x} y {self.y}>"
