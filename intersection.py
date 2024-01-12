from model import *
from light import Light
from typing import Dict, Optional
from math import hypot

TURN_TIME = Seconds(6)


class Intersection:
    def __init__(self, x: Meters, y: Meters):
        self.x = x
        self.y = y
        # I think id rather use the position as a tuple than as two variable
        self.position: Point = (x, y)
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

    def is_green(self, car_heading: Direction):
        # Everything is allowed fuck it go!
        if self.light is None:
            return True

        # We interpret the light as green for X if it is on and Y if it is off
        is_green_for_x = self.light.is_on
        if car_heading == Direction.E or car_heading == Direction.W:
            return is_green_for_x
        return not is_green_for_x

    def have_time_to_turn_left(self, current_direction: Direction):
        incoming_car = self.incoming_car[current_direction]
        if incoming_car is None:
            return True

        # Avoiding a divide by zero error
        if incoming_car.speed == 0:
            return True

        distance = calculate_distance(incoming_car.position, self.position)
        time_to_cross = distance / incoming_car.speed
        return time_to_cross > TURN_TIME


def calculate_distance(point1: Point, point2: Point) -> Meters:
    x1, y1 = point1
    x2, y2 = point2
    return hypot(x2 - x1, y2 - y1)
