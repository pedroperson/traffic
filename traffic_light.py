from model import *


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

    def display_light(self, cars, time_stamp):
        LightController.update_state(self, time_stamp)
        return (
            self.can_go(Direction.N, cars),
            self.can_go(Direction.E, cars),
            self.can_go(Direction.S, cars),
            self.can_go(Direction.W, cars),
        )

    def just_crossed(self, car, direction: Direction):
        self.last_crossed[direction.value] = car

    def last_crossing(self, direction: Direction):
        return self.last_crossed[direction.value]

    def left_vicinity(self, car):
        if car in self.last_crossed:
            self.last_crossed[self.last_crossed.index(car)] = 0

    def can_go(self, direction: Direction, cars):
        if direction == Direction.E or direction == Direction.W:
            light_is_green = self.green_for_X
        else:
            light_is_green = not self.green_for_X

        if not light_is_green:
            return False, False

        left_arrow = self.has_enough_time_to_cross(direction, cars)
        # I think this return is confusion
        return (light_is_green, left_arrow)

    # NEEDSWORK: Make this work with dictionary of cars
    def has_enough_time_to_cross(self, direction: Direction, cars):
        opposite = opposite_direction[direction]
        car = cars[opposite]

        if car is None:
            return True

        if direction == Direction.E or direction == Direction.W:
            dir = GPS.x.value
            deltadir = GPS.dx.value
        else:
            dir = GPS.y.value
            deltadir = GPS.dy.value

        time_to_cross = (car[dir] - self.positionX) / car[deltadir]
        return time_to_cross > self.safety_time

    def set_state(self, state):
        self.green_for_X = state


class LightController:
    def update_state(light: TrafficLight, time_stamp):
        proptime = (int(time_stamp) % light.cycle_period) / light.cycle_period
        if proptime < light.proportionX:
            light.set_state(True)
        else:
            light.set_state(False)
