from math import floor, ceil

from model import *
from intersection import Intersection


class Map:
    def __init__(self, nodes_per_row: int, road_length: Meters):
        self.intersections: list[list[Intersection]] = [
            [
                Intersection(i * road_length, j * road_length)
                for j in range(nodes_per_row)
            ]
            for i in range(nodes_per_row)
        ]
        self.nodes_per_row = nodes_per_row
        self.road_length = road_length

    def intersection(self, position: Point) -> Intersection:
        # TODO: is there a problem with the round down?
        x_index = int(position[0] / self.road_length)
        y_index = int(position[1] / self.road_length)
        return self.intersections[x_index][y_index]

    def intersection_at_index(self, node_x: int, node_y: int) -> Intersection:
        return self.intersections[node_x][node_y]

    # TODO: could probably make this simpler and shorter
    # We will use closest_intersection to attach cars to their next intersection
    def closest_intersection(
        self, position_x: Meters, position_y: Meters, direction: Direction
    ) -> Intersection:
        # Scale dimensions from meters to nodes
        x = position_x / self.road_length
        y = position_y / self.road_length

        # TODO: I think the case when x or y is exatly an integer is not handled correctly, or at least not usefully for us, but maybe it wont matter

        # TODO: Use direction_map from model.py

        # Round according to direction
        if direction == Direction.N:
            # Handle case where we are exactly on an intersection. in that case we want to return the next intesection in that direction
            if y % 1 == 0:
                y += 1

            return self.intersections[floor(x)][ceil(y)]
        elif direction == Direction.S:
            if y % 1 == 0:
                y -= 1
            return self.intersections[ceil(x)][floor(y)]
        elif direction == Direction.E:
            if x % 1 == 0:
                x += 1
            return self.intersections[ceil(x)][ceil(y)]
        elif direction == Direction.W:
            if x % 1 == 0:
                x -= 1
            return self.intersections[floor(x)][floor(y)]
        else:
            raise ValueError("Invalid direction")

    # TODO: Could be shortened!
    def next_intersection(self, intersection: Intersection, direction: Direction):
        x = int(intersection.position[0] / self.road_length)
        y = int(intersection.position[1] / self.road_length)
        # TODO: Use direction_map from model.py

        if direction == Direction.N:
            if y + 1 >= self.nodes_per_row:
                return None
            return self.intersections[x][y + 1]
        elif direction == Direction.S:
            if y - 1 < 0:
                return None
            return self.intersections[x][y - 1]
        elif direction == Direction.E:
            if x + 1 >= self.nodes_per_row:
                return None
            return self.intersections[x + 1][y]
        elif direction == Direction.W:
            if x - 1 < 0:
                return None
            return self.intersections[x - 1][y]
        else:
            raise ValueError("Invalid direction")
