from random import choice
from typing import List, Tuple

from model import Direction, direction_deltas

IndexPoint = Tuple[int, int]


class Path:
    def __init__(self, start: IndexPoint, end: IndexPoint, start_direction=None):
        # Keep an index to know where we are in the path
        self.index = 0

        if start_direction is not None:
            start = (
                start[0] + direction_deltas[start_direction][0],
                start[1] + direction_deltas[start_direction][1],
            )

        pts, dirs = generate_paths_to_node(start, end)

        # Add the first move in
        if start_direction is not None:
            pts.insert(0, start)
            dirs.insert(0, start_direction)

        # Keep a list of points to help find intersections
        self.path = pts
        # Keep a list of directions to help with repositioning
        self.path_directions = dirs

    # Call this to move to the next target
    def step(self):
        if not self.reached_end():
            self.index += 1

    def reached_end(self):
        return self.index + 1 >= len(self.path)

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
    pos = tuple(start)
    path_directions = []
    path_points = []
    while pos != end:
        # For any two points, there are at most 2 directions we can go in if we want to get closer to the end point at every step
        dir = choice(possible_directions(pos, end))

        delta = direction_deltas[dir]
        pos = pos[0] + delta[0], pos[1] + delta[1]

        path_directions.append(dir)
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
