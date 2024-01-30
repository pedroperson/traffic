from math import ceil
import sys
import time
from typing import List
from enum import Enum

from model import *
from map import Map
from car import Car

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from car_controller import CarController


ROAD = "."
CAR = "@"
NOTHING = " "
INTERSECTION = "*"
LIGHT_ON_X = "-"
LIGHT_ON_Y = "|"
LIGHT_YELLOW = "Y"


class Display:
    def __init__(self, map: Map, cars: [Car], dt: Seconds):
        self.a_map = map
        self.dt = dt
        self.cars = cars
        self.fig, self.ax = plt.subplots()

    def display(self, state):
        self.ax.clear()
        self.add_map()
        for car in state.cars:
            self.add_car(car)

    def animate(self, frames):
        self.anim = FuncAnimation(self.fig, self.update, frames=frames, repeat=False)
        plt.show()

    def update(self, frame):
        self.display()
        self.state.current_time += self.dt

    def add_car(self, car: Car):
        # Plot the car
        self.ax.scatter(car.position[0], car.position[1], color="black")

        # Set the x and y self.axis labels
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")

        # Set the title
        self.ax.set_title("Car")

    def add_map(self):
        # Plot the intersections and roads
        for i, row in enumerate(self.a_map.intersections):
            for j, intersection in enumerate(row):
                self.ax.scatter(
                    intersection.position[0], intersection.position[1], color="blue"
                )

                # Plot the road to the right
                if j < self.a_map.nodes_per_row - 1:
                    next_intersection = self.a_map.intersections[i][j + 1]
                    self.ax.plot(
                        [intersection.position[0], next_intersection.position[0]],
                        [intersection.position[1], next_intersection.position[1]],
                        color="black",
                    )

                # Plot the road below
                if i < self.a_map.nodes_per_row - 1:
                    next_intersection = self.a_map.intersections[i + 1][j]
                    self.ax.plot(
                        [intersection.position[0], next_intersection.position[0]],
                        [intersection.position[1], next_intersection.position[1]],
                        color="black",
                    )

        # Set the x and y self.axis labels
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")

        # Set the title
        self.ax.set_title("Map")


# Assuming 1d horizontal road for now
def print_road(cars: List[Car], whole_length: Meters, map: Map):
    # Length of each text character
    DX = whole_length / 30
    DY = whole_length / 15
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
                    elif intersec.is_green(Direction.N):
                        s = s[:x] + LIGHT_ON_Y + s[x + 1 :]
                    else:
                        s = s[:x] + LIGHT_YELLOW + s[x + 1 :]

        return s

    # Print the road in a line of text
    for y in range(ROAD_HEIGHT):
        print(horizontal_road(y, DY))

    time.sleep(0.005)
    for y in range(ROAD_HEIGHT):
        sys.stdout.write("\033[F")


def in_x(x, dx, position):
    return position[0] >= x * dx and position[0] < (x + 1) * dx


def in_y(y, dy, position):
    return position[1] >= y * dy and position[1] < (y + 1) * dy


# from math import ceil
# import sys
# import time
# from typing import List
# from enum import Enum

# import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib.animation as animation

# from model import *
# from map import Map
# from car import Car


# ROAD = "."
# # CAR = "@"
# # NOTHING = " "
# INTERSECTION = "*"
# LIGHT_ON_X = "-"
# LIGHT_ON_Y = "|"

# # Constants to represent different types of cells
# NOTHING = 0
# CAR = 1
# GREEN_INTERSECTION = 2
# RED_INTERSECTION = 3

# def display_roads(cars: List[Car], whole_length:Meters, map: Map, num_roads):
#     # Length of each text character
#     DX = whole_length / 40
#     DY = whole_length / 20
#     ROAD_WIDTH = ceil(whole_length / DX)
#     ROAD_HEIGHT = ceil(whole_length / DY)

#     # Create a 2D array to represent all the roads
#     roads = np.full((ROAD_HEIGHT * num_roads, ROAD_WIDTH), NOTHING)

#     # Create a figure and axes
#     fig, ax = plt.subplots()

#     # Create a color map
#     cmap = plt.get_cmap('binary')
#     cmap.set_over('red')  # Cars are red
#     cmap.set_under('green')  # Green intersections are green
#     cmap.set_bad('blue')  # Red intersections are blue

#     # Display the roads
#     im = ax.imshow(roads, cmap=cmap, interpolation='nearest')

#     def update(frame):
#         # Clear the roads
#         roads.fill(NOTHING)

#         # Add the cars and intersections to each road
#         for i in range(num_roads):
#             for car in cars:
#                 if not in_y(i * ROAD_HEIGHT, DY, car.position):
#                     continue

#                 x = round(car.position[0] / DX)
#                 y = round(car.position[1] / DY) + i * ROAD_HEIGHT
#                 if y < ROAD_HEIGHT and x < ROAD_WIDTH:
#                     roads[y][x] = CAR

#             for row in map.intersections:
#                 for intersec in row:
#                     if not in_y(i * ROAD_HEIGHT, DY, intersec.position):
#                         continue

#                     x = round(intersec.position[0] / DX)
#                     y = round(intersec.position[1] / DY) + i * ROAD_HEIGHT
#                     if intersec.is_green(Direction.E):
#                         roads[y][x] = GREEN_INTERSECTION
#                     else:
#                         roads[y][x] = RED_INTERSECTION

#         # Update the image data
#         im.set_data(roads)
#         return im

#     # Create the animation
#     ani = animation.FuncAnimation(fig, update, frames=100, interval=200)

#     plt.show()


# # Assuming 1d horizontal road for now
# def print_road(cars: List[Car], whole_length: Meters, map: Map):
#     # Length of each text character
#     DX = whole_length / 40
#     DY = whole_length / 20
#     ROAD_WIDTH = ceil(whole_length / DX)
#     ROAD_HEIGHT = ceil(whole_length / DY)

#     def horizontal_road(y, dy):
#         s = ""
#         for _ in range(ROAD_WIDTH):
#             s += ROAD

#         for car in cars:
#             if not in_y(y, dy, car.position):
#                 continue

#             x = round(car.position[0] / DX)
#             s = s[:x] + CAR + s[x + 1 :]

#         for row in map.intersections:
#             for intersec in row:
#                 if not in_y(y, dy, intersec.position):
#                     continue

#                 x = round(intersec.position[0] / DX)
#                 if intersec.light is None:
#                     s = s[:x] + INTERSECTION + s[x + 1 :]
#                 else:
#                     if intersec.is_green(Direction.E):
#                         s = s[:x] + LIGHT_ON_X + s[x + 1 :]
#                     else:
#                         s = s[:x] + LIGHT_ON_Y + s[x + 1 :]

#         return s

#     # Print the road in a line of text
#     for y in range(ROAD_HEIGHT):
#         print(horizontal_road(y, DY))

#     time.sleep(0.001)
#     for y in range(ROAD_HEIGHT):
#         sys.stdout.write("\033[F")


# def in_x(x, dx, position):
#     return position[0] >= x * dx and position[0] < (x + 1) * dx


# def in_y(y, dy, position):
#     return position[1] >= y * dy and position[1] < (y + 1) * dy
