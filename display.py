from math import ceil
import sys
import time
from typing import List

from model import *
from map import Map
from car import Car


# Assuming 1d horizontal road for now
def print_road(cars: List[Car], whole_length: Meters, map: Map):
    # Length of each text character
    DX = whole_length / 20
    DY = whole_length / 20
    ROAD_WIDTH = ceil(whole_length / DX)
    ROAD_HEIGHT = ceil(whole_length / DY)

    # Print the road in a line of text
    for y in range(ROAD_HEIGHT):
        for x in range(ROAD_WIDTH):
            intersection = None
            for row in map.intersections:
                for intersec in row:
                    if in_x(x, DX, intersec.position) and in_y(
                        y, DY, intersec.position
                    ):
                        intersection = intersec
                        break
                if intersection:
                    break

            if intersection:
                char = (
                    "*"
                    if intersection.light is None
                    else "-"
                    if intersection.light.is_on
                    else "|"
                )
                print(char, end="")
                continue

            # Check if there is a car at this position
            car_count = 0
            for c in cars:
                if in_x(x, DX, c.position) and in_y(y, DY, c.position):
                    car_count += 1

            if car_count > 0:
                print(str(car_count), end="")
            else:
                # TODO: Some of them should be empty if they are not roads
                print(".", end="")
        print("")

    # time.sleep(0.1)
    for y in range(ROAD_HEIGHT):
        sys.stdout.write("\033[F")


def in_x(x, dx, position):
    return position[0] >= x * dx and position[0] < (x + 1) * dx


def in_y(y, dy, position):
    return position[1] >= y * dy and position[1] < (y + 1) * dy
