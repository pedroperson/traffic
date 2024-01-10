from traffic_light import TrafficLight


class Map:
    def __init__(self, size):
        self.trafficLights = [[None for i in range(size)] for j in range(size)]
        self.roads = [[[] for i in range(size)] for j in range(size)]

        for i in range(size):
            for j in range(size):
                if i == 0 and j == 0:
                    self.roads[i][j] = ["-inf", 0.0, 0.0, "-inf"]
                elif i == 0 and j == size - 1:
                    self.roads[i][j] = ["-inf", "-inf", 0.0, 0.0]
                elif i == 0 and j < size - 1:
                    self.roads[i][j] = ["-inf", 0.0, 0.0, 0.0]
                elif i == size - 1 and j == 0:
                    self.roads[i][j] = [0.0, 0.0, "-inf", "-inf"]
                elif i == size - 1 and j == size - 1:
                    self.roads[i][j] = [0.0, "-inf", "-inf", 0.0]
                elif i == size - 1 and j < size - 1:
                    self.roads[i][j] = [0.0, 0.0, "-inf", 0.0]
                elif i < size - 1 and j == 0:
                    self.roads[i][j] = [0.0, 0.0, 0.0, "-inf"]
                elif i < size - 1 and j == size - 1:
                    self.roads[i][j] = [0.0, "-inf", 0.0, 0.0]
                else:
                    self.roads[i][j] = [0.0, 0.0, 0.0, 0.0]

        for i in range(size):
            for j in range(size):
                self.trafficLights[i][j] = TrafficLight(i, j, 0.5)

    def get_traffic_light(self, x, y):
        return self.trafficLights[x][y]

    def set_traffic_light(self, x, y, traffic_light):
        self.trafficLights[x][y] = traffic_light

    def get_roads(self, x, y):
        return self.roads[x][y]

    def set_roads(self, x, y, roads):
        self.roads[x][y] = roads

    def set_road(self, x, y, direction, value):
        self.roads[x][y][direction] = value


import random


def generate_random_path(map, start=(0, 0), end=(1, 1)):
    def dfs(pos, path):
        x, y = pos
        if not (0 <= x < len(map) and 0 <= y < len(map[0])) or pos in path:
            return
        path.append(pos)
        if pos == end:
            paths.append(path.copy())
        else:
            # Only move towards the end point
            moves = []
            if x < end[0]:  # If current x is less than end x, can move down
                moves.append((1, 0))
            if y < end[1]:  # If current y is less than end y, can move right
                moves.append((0, 1))
            if x > end[0]:  # If current x is greater than end x, can move up
                moves.append((-1, 0))
            if y > end[1]:  # If current y is greater than end y, can move left
                moves.append((0, -1))
            for dx, dy in random.sample(moves, len(moves)):
                dfs((x + dx, y + dy), path)
        path.pop()

    paths = []
    dfs(start, [])
    return random.choice(paths) if paths else None


map = [[0.0] * 5] * 5


generate_random_path(map, (4, 4), (0, 3))

import matplotlib.pyplot as plt


def display_map(map, path, cars):
    size = len(map.roads)
    plt.figure(figsize=(size, size))

    # Display the map
    for i in range(size):
        for j in range(size):
            if map.roads[i][j] == ["-inf", 0.0, 0.0, "-inf"]:
                plt.text(j, size - 1 - i, "S", ha="center", va="center")
            elif map.roads[i][j] == ["-inf", "-inf", 0.0, 0.0]:
                plt.text(j, size - 1 - i, "E", ha="center", va="center")
            else:
                plt.text(j, size - 1 - i, "R", ha="center", va="center", color="yellow")

    # Display the cars
    for x, y in cars:
        plt.text(y, size - 1 - x, "C", ha="center", va="center", color="blue")

    # Display the path
    for x, y in path:
        plt.text(y, size - 1 - x, "P", ha="center", va="center", color="red")

    plt.xticks(range(size))
    plt.yticks(range(size))
    plt.grid(True)
    plt.show()


map = Map(5)
path = generate_random_path(map.roads)
cars = [(1, 1), (2, 2), (3, 3)]
display_map(map, path, cars)
