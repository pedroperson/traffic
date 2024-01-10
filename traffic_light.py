from main import *


class GPS(Enum):
    x = 0
    y = 1
    dx = 2
    dy = 3


# PAGE 1
class TrafficLight:
    def __init__(
        self, positionX=1, positionY=1, proportionX=0.5, cycle_period=20, safety_time=3
    ):
        self.positionX = positionX
        self.positionY = positionY
        self.proportionX = proportionX
        self.cycle_period = cycle_period
        self.green_for_X = True
        self.safety_time = safety_time
        self.last_crossed = [0, 0, 0, 0]

    def display_light(self, cars, time_stamp):
        proptime = (int(time_stamp) % self.cycle_period) / self.cycle_period
        if proptime < self.proportionX:
            self.green_for_X = True
        else:
            self.green_for_X = False

        if cars[Direction.N.value]:
            northbound_time = (
                cars[Direction.N.value][GPS.y.value] - self.positionY
            ) / cars[Direction.N.value][GPS.dy.value]
        if cars[Direction.E.value]:
            eastbound_time = (
                cars[Direction.E.value][GPS.x.value] - self.positionX
            ) / cars[Direction.E.value][GPS.dx.value]
        if cars[Direction.S.value]:
            southbound_time = (
                cars[Direction.S.value][GPS.y.value] - self.positionY
            ) / cars[Direction.S.value][GPS.dy.value]
        if cars[Direction.W.value]:
            westbound_time = (
                cars[Direction.W.value][GPS.x.value] - self.positionX
            ) / cars[Direction.W.value][GPS.dx.value]

        ## return ((northbound_light, northbound_left_arrow),(eastbound_light, eastbound_left_arrow),(southbound_light, southbound_left_arrow),(westbound_light, westbound_left_arrow),

        northbound_light = not self.green_for_X
        northbound_left_arrow = (
            not self.green_for_X
        ) and southbound_time > self.safety_time
        southbound_light = not self.green_for_X
        southbound_left_arrow = (
            not self.green_for_X
        ) and northbound_time > self.safety_time

        eastbound_light = self.green_for_X
        eastbound_left_arrow = self.green_for_X and westbound_time > self.safety_time
        westbound_light = self.green_for_X
        westbound_left_arrow = self.green_for_X and eastbound_time > self.safety_time

        return (
            (northbound_light, northbound_left_arrow),
            (eastbound_light, eastbound_left_arrow),
            (southbound_light, southbound_left_arrow),
            (westbound_light, westbound_left_arrow),
        )

    def just_crossed(self, car, direction: Direction):
        self.last_crossed[direction.value] = car

    def last_crossing(self, direction: Direction):
        return self.last_crossed[direction.value]

    def left_vicinity(self, car):
        if car in self.last_crossed:
            self.last_crossed[self.last_crossed.index(car)] = 0


# PAGE 2

import time

step_data = (
    (4, 1.3, 0, 0.45),
    (3.7, 1, 0.30, 0),
    (4, 0.1, 0, -0.20),
    (4.4, 1, -0.30, 0),
)
trafficlight1 = TrafficLight(4, 1, 0.3, 20)
trafficlight1.display_light(step_data, time.time())

trafficlight1.just_crossed(123123, Direction.E)
print(trafficlight1.last_crossing(Direction.E))
trafficlight1.left_vicinity(89)
print(trafficlight1.last_crossing(Direction.E))
trafficlight1.left_vicinity(123123)
print(trafficlight1.last_crossing(Direction.E))


# PAGE 3
# trafficlight1.last_crossed.index(123123)
elem = 1
trafficlight1.last_crossed.index(elem) if elem in trafficlight1.last_crossed else -1
