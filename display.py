from math import ceil
import sys
import time
from typing import List
from enum import Enum

from model import *
from map import Map
from car import Car


ROAD = "."
CAR = "@"
NOTHING = " "
INTERSECTION = "*"
LIGHT_ON_X = "-"
LIGHT_ON_Y = "|"


# Assuming 1d horizontal road for now
def print_road(cars: List[Car], whole_length: Meters, map: Map):
    # Length of each text character
    DX = whole_length / 40
    DY = whole_length / 20
    ROAD_WIDTH = ceil(whole_length / DX)
    ROAD_HEIGHT = ceil(whole_length / DY)

    def horizontal_road(y, dy):
        s = ""
        for _ in range(ROAD_WIDTH):
            s += ROAD

        for car in cars:
            if not in_y(y, dy, car.position):
                continue

            x = round(car.position[0] / DX)
            s = s[:x] + CAR + s[x + 1 :]

        for row in map.intersections:
            for intersec in row:
                if not in_y(y, dy, intersec.position):
                    continue

                x = round(intersec.position[0] / DX)
                if intersec.light is None:
                    s = s[:x] + INTERSECTION + s[x + 1 :]
                else:
                    if intersec.is_green(Direction.E):
                        s = s[:x] + LIGHT_ON_X + s[x + 1 :]
                    else:
                        s = s[:x] + LIGHT_ON_Y + s[x + 1 :]

        return s

    # Print the road in a line of text
    for y in range(ROAD_HEIGHT):
        print(horizontal_road(y, DY))

    time.sleep(0.001)
    for y in range(ROAD_HEIGHT):
        sys.stdout.write("\033[F")


def in_x(x, dx, position):
    return position[0] >= x * dx and position[0] < (x + 1) * dx


def in_y(y, dy, position):
    return position[1] >= y * dy and position[1] < (y + 1) * dy
