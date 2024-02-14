from typing import Dict, Optional
from math import hypot

from model import Point, Meters, Direction, Seconds, TURN_TIME, Lightcolor
from light import Light
from car import Car


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

        if my_heading == Direction.E or my_heading == Direction.W:
            return self.light.x_light is Lightcolor.Green
        return self.light.y_light is Lightcolor.Green

    def opposing_car(self, my_heading: Direction):
        return self.incoming_car[my_heading]
