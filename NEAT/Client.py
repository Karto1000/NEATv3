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

import typing

from NEAT.Genome import Genome
from NEAT.calculating.Calculator import Calculator

if typing.TYPE_CHECKING:
    from NEAT.Species import Species
    from NEAT import NEAT


class Client:
    def __init__(self):
        self.genome = Genome()
        self.fitness = 0.0
        self.species: Species = None
        self.neat: NEAT = None
        self.calculator: Calculator = Calculator(self)

    def predict(self, inputs: tuple[float, ...]) -> tuple[float, ...]:
        return self.calculator.predict(inputs)

    def set_neat(self, neat: NEAT):
        self.neat = neat
        self.genome.neat = neat
