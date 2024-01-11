from model import *
from typing import Dict, Optional


class GPS(Enum):
    x = 0
    y = 1
    dx = 2
    dy = 3


opposite_direction = {
    Direction.N: Direction.S,
    Direction.S: Direction.N,
    Direction.E: Direction.W,
    Direction.W: Direction.E,
}


# PAGE 1
class TrafficLight:
    def __init__(
        self,
        positionX: Meters,
        positionY: Meters,
        proportionX=0.5,
        cycle_period: Seconds = 20,
        safety_time: Seconds = 3,
    ):
        self.positionX = positionX
        self.positionY = positionY
        self.proportionX = proportionX
        self.cycle_period = cycle_period
        self.green_for_X = True
        self.safety_time = safety_time
        self.last_crossed = [0, 0, 0, 0]

    def set_state(self, state: bool):
        self.green_for_X = state

    # Probably need a from and to direction
    def can_go(self, direction: Direction, incoming_car: Car):
        if direction == Direction.E or direction == Direction.W:
            light_is_green = self.green_for_X
        else:
            light_is_green = not self.green_for_X

        if not light_is_green:
            return False, False

        left_arrow = self.has_enough_time_to_cross(incoming_car)
        # I think this return is confusing
        return (light_is_green, left_arrow)

    def has_enough_time_to_cross(self, incoming_car: Car):
        if incoming_car is None:
            return True

        # Avoiding a divide by 0 error
        if incoming_car.speed == 0:
            return True

        intersection = (self.positionX, self.positionY)
        distance = calculate_distance(incoming_car.position, intersection)
        time_to_cross = distance / incoming_car.speed

        return time_to_cross > self.safety_time

    # TODO: Need to update these!
    def just_crossed(self, car, direction: Direction):
        self.last_crossed[direction.value] = car

    def last_crossing(self, direction: Direction):
        return self.last_crossed[direction.value]

    def left_vicinity(self, car):
        if car in self.last_crossed:
            self.last_crossed[self.last_crossed.index(car)] = 0


class LightController:
    def update_state(light: TrafficLight, time_stamp):
        proptime = (int(time_stamp) % light.cycle_period) / light.cycle_period
        if proptime < light.proportionX:
            light.set_state(True)
        else:
            light.set_state(False)


import math


def calculate_distance(point1: Point, point2: Point) -> Meters:
    x1, y1 = point1
    x2, y2 = point2
    return math.hypot(x2 - x1, y2 - y1)
