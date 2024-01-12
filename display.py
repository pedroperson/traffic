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
    DX = whole_length / 120
    ROAD_WIDTH = ceil(whole_length / DX)

    # Print the road in a line of text
    for x in range(ROAD_WIDTH):
        # Check if there is a car at this position
        car = None
        for c in cars:
            # idk why this actually works
            if c.position >= (x * DX, 0) and c.position < ((x + 1) * DX, 0):
                car = c
                break

        intersection = None
        for row in map.intersections:
            for i in row:
                if i.position[0] >= x * DX and i.position[0] < (x + 1) * DX:
                    intersection = i
                    break
            if intersection:
                break

        if intersection:
            char = (
                " "
                if intersection.light is None
                else "O"
                if intersection.light.is_on
                else "X"
            )
            print(char, end="")
        if car:
            print("@", end="")
        else:
            print(".", end="")
    print("")
    sys.stdout.write("\033[F")
    time.sleep(0.001)
