from random import choice, sample
from typing import List, Optional, Tuple

from model import Direction, direction_deltas

IndexPoint = Tuple[int, int]


class Path:
    def __init__(self, start: IndexPoint, end: IndexPoint):
        self.s = start
        self.e = end
        self.index = 0

        pts, dirs = generate_paths_to_node(start, end)
        self.path = pts
        self.path_directions = dirs

    # Call this to move to the next target
    def step(self):
        if not self.reached_end():
            self.index += 1

    def start(self):
        return self.s

    def end(self):
        return self.e

    def reached_end(self):
        return self.index + 1 >= len(self.path)

    def previous_target(self):
        if self.index - 1 < 0:
            return None
        return self.path[self.index - 1]

    def previous_direction(self):
        if self.index - 1 < 0:
            return None
        return self.path_directions[self.index - 1]

    def target(self):
        return self.path[self.index]

    def target_direction(self):
        return self.path_directions[self.index]

    def next_target(self):
        if self.index + 1 >= len(self.path):
            return None
        return self.path[self.index + 1]

    def next_direction(self):
        if self.index + 1 >= len(self.path_directions):
            return None
        return self.path_directions[self.index + 1]


def generate_paths_to_node(
    start: IndexPoint, end: IndexPoint
) -> Tuple[List[IndexPoint], List[Direction]]:
    pos: IndexPoint = tuple(start)
    path_directions: List[Direction] = []
    path_points: List[IndexPoint] = []
    while pos != end:
        # For any two points, there are at most 2 directions we can go in if we want to get closer to the end point at every step
        dir = choice(possible_directions(pos, end))
        path_directions.append(dir)

        pos = add_tuples(pos, direction_deltas[dir])
        path_points.append(pos)

    return path_points, path_directions


def possible_directions(start: IndexPoint, end: IndexPoint) -> List[Direction]:
    possible_directions = []
    if start[0] < end[0]:
        possible_directions.append(Direction.E)
    if start[0] > end[0]:
        possible_directions.append(Direction.W)
    if start[1] < end[1]:
        possible_directions.append(Direction.N)
    if start[1] > end[1]:
        possible_directions.append(Direction.S)

    return possible_directions


def add_tuples(x, y):
    return (x[0] + y[0], x[1] + y[1])
