from traffic_light import TrafficLight
from model import *
import math


class Intersection:
    def __init__(self, x: Meters, y: Meters):
        self.x = x
        self.y = y
        self.traffic_light = None

    def set_traffic_light(self, traffic_light: TrafficLight):
        self.traffic_light = traffic_light

    def can_go(self, direction: Direction):
        # Everything is allowed fuck it go!
        if self.traffic_light is None:
            return (True, True)
        # TODO: Need to get rid of this pasing in car stuff. The traffic light should remember this by itself
        cars = {
            Direction.N: (4, 1.3, 0, 0.45),
            Direction.E: (3.7, 1, 0.30, 0),
            Direction.S: (4, 0.1, 0, -0.20),
            Direction.W: (4.4, 1, -0.30, 0),
        }
        return self.traffic_light.can_go(direction, cars)


class Map:
    def __init__(self, nodes_per_row: int, edge_length: Meters):
        self.intersections: list[list[Intersection]] = [
            [
                Intersection(i * edge_length, j * edge_length)
                for j in range(nodes_per_row)
            ]
            for i in range(nodes_per_row)
        ]
        self.nodes_per_row = nodes_per_row
        self.edge_length = edge_length

    def set_traffic_light(self, x: int, y: int, traffic_light: TrafficLight):
        self.intersections[x][y].set_traffic_light(traffic_light)

    # We will use closest_intersection to attach cars to their next intersection
    def closest_intersection(
        self, position_x: Meters, position_y: Meters, direction: Direction
    ) -> TrafficLight:
        # Scale dimensions from meters to nodes
        x = position_x / self.edge_length
        y = position_y / self.edge_length

        # TODO: I think the case when x or y is exatly an integer is not handled correctly, or at least not usefully for us, but maybe it wont matter

        # Round according to direction
        if direction == Direction.N:
            return self.intersections[math.floor(x)][math.ceil(y)]
        elif direction == Direction.S:
            return self.intersections[math.ceil(x)][math.floor(y)]
        elif direction == Direction.E:
            return self.intersections[math.ceil(x)][math.ceil(y)]
        elif direction == Direction.W:
            return self.intersections[math.floor(x)][math.floor(y)]
        else:
            raise ValueError("Invalid direction")


# Test map 2
# map2 = Map(5, 10)
# map2.set_traffic_light(0, 0, TrafficLight(0, 0, 0.5))
# map2.set_traffic_light(1, 0, TrafficLight(0, 1, 0.5))
# print(map2.closest_intersection(8, 0, Direction.W).traffic_light)

# print(map2.closest_intersection(18, 0, Direction.W).traffic_light)
# print(map2.closest_intersection(28, 0, Direction.W).traffic_light)
