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

class Config:
    STRUCTURE: tuple[int, int] = (3, 3)
    WEIGHT_THRESHOLD: tuple[float, float] = (-1, 1)
    WEIGHT_SHIFT_THRESHOLD: tuple[float, float] = (-0.5, 0.5)
    AMOUNT_OF_CLIENTS = 1
    MAX_NUMBER_OF_NODES = 100
    MIN_ADD_DISTANCE = 4
    PERCENT_OF_CLIENTS_TO_REMOVE = 50

    # Display Config
    SW, SH = 800, 800
    NETWORK_PADDING = (50, 50)
    NODE_RADIUS = 15

    NODE_X_MULTIPLIER = 400
    NODE_Y_MULTIPLIER = 450