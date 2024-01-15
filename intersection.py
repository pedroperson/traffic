from typing import Dict, Optional
from math import hypot

from model import Point, Meters, Direction, Seconds, TURN_TIME
from light import Light
from car import Car

# We need a concept of a very long time, so we can use it to represent a car that is not turning left
LIKE_SUPER_LONG = TURN_TIME * 1000


class Intersection:
    def __init__(self, x: Meters, y: Meters):
        self.position: Point = (x, y)
        # Each intersection may have a light attached to them
        self.light: Optional[Light] = None

        # Direction the car is coming from
        self.incoming_car: Dict[Direction, Optional[Car]] = {
            Direction.N: None,
            Direction.E: None,
            Direction.S: None,
            Direction.W: None,
        }

        # Direction the car left towards
        self.outgoing_car: Dict[Direction, Optional[Car]] = {
            Direction.N: None,
            Direction.E: None,
            Direction.S: None,
            Direction.W: None,
        }

    def set_light(self, light: Light):
        self.light = light

    def is_green(self, my_heading: Direction):
        # Everything is allowed fuck it go!
        if self.light is None:
            return True

        # We interpret the light as green for X if it is on and Y if it is off
        is_green_for_x = self.light.is_on

        if my_heading == Direction.E or my_heading == Direction.W:
            return is_green_for_x
        return not is_green_for_x

    def time_to_opposing_car_arrival(self, my_heading: Direction) -> Seconds:
        incoming_car = self.incoming_car[my_heading]
        if incoming_car is None:
            return LIKE_SUPER_LONG

        # Avoiding a divide by zero error
        if incoming_car.speed == 0:
            return LIKE_SUPER_LONG

        distance = calculate_distance(incoming_car.position, self.position)
        # IDK: Maybe assuming current speed isn't enough
        return distance / incoming_car.speed


def calculate_distance(point1: Point, point2: Point) -> Meters:
    x1, y1 = point1
    x2, y2 = point2
    return hypot(x2 - x1, y2 - y1)
