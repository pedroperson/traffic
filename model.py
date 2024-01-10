from enum import Enum
from typing import Tuple

# UNITS:
# time: seconds (s)
Seconds = float
# distance: meters (m)
Meters = float
Point = Tuple[Meters, Meters]
# speed: meters per second (m/s)
# acceleration: meters per second squared (m/s^2)

# REFERENCE VALUES:
# ACCELERATION : For buses, accelerations of up to 1.0 m/s2 helps passengers move naturally inside the vehicle. For cars, a comfortable rate of acceleration is 1.5 to 2.0 m/s2
# SPEED: Highway speeds in the US are typically around 26.8 m/s (60mph~100kph)
MAX_SPEED = 27
# LENGTH: American cars range 3.5-5.5 meters in length (mini cooper to for f-150) with a width of 1.5-2 meters
CAR_LENGTH = Meters(5.2)
CAR_WIDTH = Meters(1.7)
# DISTANCE: Safe distance behind car in front is around 1 meters for every km/h of speed -> 3.6 meters per m/s
SPEED_BUFFER = 3.6  # meters per m/s

# The minimum distance that must be kept when cars are stopped. This is to simulate the fact that cars are not bumper to bumper when stopped.
CAR_MIN_DISTANCE = 2  # meters


# Simulation is 2D, so we keep cardinal directions
class Direction(Enum):
    N = 0  # North
    E = 1  # East
    S = 2  # South
    W = 3  # West


# A map to convert the direction to a tuple of (delta_x, delta_y)
direction_map = {
    Direction.N: (0, 1),
    Direction.E: (1, 0),
    Direction.S: (0, -1),
    Direction.W: (-1, 0),
}


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

        # The car behind me: keep this reference to tell the intersection to track that once I have passed
        self.car_behind = None
        # Car in front: keep reference so we can measure its speed and position and know whether we need to brake as to no crash against them.
        self.car_in_front = None

    def __str__(self):
        return f"Car(pos={self.position}, speed={self.speed}, dir={self.direction})"
