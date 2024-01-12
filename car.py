from typing import Optional

from model import Meters, Direction, direction_map, CAR_LENGTH, CAR_WIDTH


class Car:
    def __init__(
        self,
        x: Meters,
        y: Meters,
        speed: float,
        direction: Direction,
        length: Meters = CAR_LENGTH,
        acceleration=5,
        deceleration=5,
    ):
        self.position = (x, y)
        self.speed = speed
        self.direction = direction
        # length of the car in the direction of travel
        self.length = length
        # width of car perpendicular to direction of travel. We are only going to use this for rendering now, so I'm keeping it constant.
        self.width = CAR_WIDTH

        # REVISIT LATER: We will be assuming a constant acceleration and deceleration to simplify the problem. This makes the gas and brake pedals effectively on/off buttons.
        self.acceleration = acceleration
        self.deceleration = deceleration

        # Keep track of the back position of the car cus that's what the driver behind will be worried about
        delta_x, delta_y = direction_map[self.direction]
        self.back_position = (
            self.position[0] - delta_x * self.length,
            self.position[1] - delta_y * self.length,
        )

        # TODO: move this knowledge away from the car, it belongs in the controller or higher
        # The car behind me: keep this reference to tell the intersection to track that once I have passed
        self.car_behind: Optional[Car] = None
        # Car in front: keep reference so we can measure its speed and position and know whether we need to brake as to no crash against them.
        self.car_in_front: Optional[Car] = None
        # Another reason to keep this out model, : Optional[Intersection]  is the type hint here but we cant use it because of circular imports
        self.next_intersection = None
        # Not really optional, this should be created at init, but not here in this class. Car should not know about the map at all
        self.path = None
        # A cache for the stopping distance so we dont have to calculate it every time
        self.stopping_distance: Meters = 0

    def __str__(self):
        return f"Car(pos={self.position}, speed={self.speed}, dir={self.direction})"
