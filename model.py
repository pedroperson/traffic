from enum import Enum
from typing import Tuple, Dict

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
MAX_SPEED = 27  # m/s
# LENGTH: American cars range 3.5-5.5 meters in length (mini cooper to for f-150) with a width of 1.5-2 meters
CAR_LENGTH = Meters(5.2)
CAR_WIDTH = Meters(1.7)
# DISTANCE: Safe distance behind car in front is around 1 meters for every km/h of speed -> 3.6 meters per m/s
SPEED_BUFFER = 3.6  # meters per m/s

# The minimum distance that must be kept when cars are stopped. This is to simulate the fact that cars are not bumper to bumper when stopped.
CAR_MIN_DISTANCE = Meters(2)

# Cars need to slow down to turn. google suggests 15 mph -> 6.7 m/s
TURN_SPEED = 6.7  # m/s
# We will assume all cars will take a constant amount of time to turn left
TURN_TIME = Seconds(6)


# Simulation is 2D, so we keep cardinal directions
class Direction(Enum):
    N = 0  # North
    E = 1  # East
    S = 2  # South
    W = 3  # West


# A map to convert the direction to a tuple of (delta_x, delta_y)
direction_deltas: Dict[Direction, Tuple[int, int]] = {
    Direction.N: (0, 1),
    Direction.E: (1, 0),
    Direction.S: (0, -1),
    Direction.W: (-1, 0),
}

opposite_direction = {
    Direction.N: Direction.S,
    Direction.S: Direction.N,
    Direction.E: Direction.W,
    Direction.W: Direction.E,
}

# Direction where if heading in the key direction, a left turn would put me in the value direction
direction_to_the_left = {
    Direction.N: Direction.W,
    Direction.S: Direction.E,
    Direction.E: Direction.N,
    Direction.W: Direction.S,
}
