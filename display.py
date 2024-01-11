from math import ceil
from model import *
import sys
import time


# Assuming 1d horizontal road for now
def print_road(CARS, whole_length: Meters, lights):
    # Length of each text character
    DX = whole_length / 100
    ROAD_WIDTH = ceil(whole_length / DX)

    # Print the road in a line of text
    for x in range(ROAD_WIDTH):
        # Check if there is a car at this position
        car = None
        for c in CARS:
            # idk why this actually works
            if c.position >= (x * DX, 0) and c.position < ((x + 1) * DX, 0):
                car = c
                break

        intersection = None
        for l in lights:
            if l.positionX >= x * DX and l.positionX < (x + 1) * DX:
                intersection = l
                break

        if intersection:
            print("O", end="") if intersection.green_for_X else print("X", end="")
        if car:
            print("@", end="")
        else:
            print(".", end="")
    print("")
    sys.stdout.write("\033[F")
    time.sleep(0.001)
