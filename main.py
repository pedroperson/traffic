from enum import Enum
import math

# ISSUES: Mainly we need to account for dt better! the acceleration needs to account for dt, and some of the function need to take dt into account. cus with constant accel we are making the velocity jump up and down like crazy in like a tenth of a second.

# UNITS: 
# time: seconds (s)
Seconds = float
# distance: meters (m)
Meters = float
# speed: meters per second (m/s)
# acceleration: meters per second squared (m/s^2)


# REFERENCE VALUES: 
# ACCELERATION : For buses, accelerations of up to 1.0 m/s2 helps passengers move naturally inside the vehicle. For cars, a comfortable rate of acceleration is 1.5 to 2.0 m/s2
# SPEED: Highway speeds in the US are typically around 26.8 m/s (60mph~100kph)
# LENGTH: American cars range 3.5-5.5 meters in length (mini cooper to for f-150) with a width of 1.5-2 meters
# DISTANCE: Safe distance behind car in front is around 1 meters for every km/h of speed -> 3.6 meters per m/s
SPEED_BUFFER = 3.6  # meters per m/s

# The minimum distance that must be kept when cars are stopped. This is to simulate the fact that cars are not bumper to bumper when stopped.
CAR_MIN_DISTANCE = 5  # meters


# Each direction will be represented by an integer
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
    Direction.W: (-1, 0)
}


class Car:
    def __init__(self, x :Meters, y:Meters, speed :float, direction:Direction, length:Meters=5.2, acceleration=5, deceleration=5):
        self.position = (x, y) 
        self.speed = speed 
        self.direction = direction
        # length of the car in the direction of travel
        self.length = length
        # width of car perpendicular to direction of travel. We are only going to use this for rendering now, so I'm keeping it constant.
        self.width  = Meters(1.7)

        # REVISIT LATER: We will be assuming a constant acceleration and deceleration to simplify the problem. This makes the gas and brake pedals effectively on/off buttons. 
        self.acceleration = acceleration  
        self.deceleration = deceleration

        # Keep track of the back position of the car cus that's what the driver behind will be worried about
        delta_x, delta_y = direction_map[self.direction]
        self.back_position = (self.position[0] - delta_x * self.length, 
                              self.position[1] - delta_y * self.length)
        
        # The car behind me: keep this reference to tell the intersection to track that once I have passed
        self.car_behind = None  
        # Car in front: keep reference so we can measure its speed and position and know whether we need to brake as to no crash against them.
        self.car_in_front = None

   
    def speed_up(self, dt:Seconds):
        self.speed += self.acceleration * dt 

    def slow_down(car, dt:Seconds):
        car.speed -=  car.deceleration * dt
        if car.speed < 0:
            car.speed = 0

    def update_position(self, dt:Seconds):
        delta_x, delta_y = direction_map[self.direction]
        self.position = (self.position[0] + delta_x * self.speed * dt, 
                         self.position[1] + delta_y * self.speed * dt)
        
        self.back_position = (self.position[0] - delta_x * self.length, 
                              self.position[1] - delta_y * self.length)

    def __str__(self):
        return f"Car(pos={self.position}, speed={self.speed}, dir={self.direction})"
    
# DECISION LOGIC

def too_fast(car:Car, max_speed:Meters) -> bool:
    return car.speed >= max_speed

def too_close_to_car_in_front(behind: Car, ahead: Car) -> bool:
    d = distance_between_points(behind.position, ahead.back_position)
    if d < CAR_MIN_DISTANCE:
        return True
    
    SAFETY_MARGIN = 2
    # Super cop out here using a constant speed buffer
    # Actually this is really bad because we are not accounting for the fact that the car in front might be slowing down or how fast its going
    safe_distance = behind.speed * SPEED_BUFFER * SAFETY_MARGIN
    return d - CAR_MIN_DISTANCE <= safe_distance

def slow_for_intersection(car:Car, stop_position: Meters) -> bool:
    d = distance_between_points(car.position, stop_position)
    if d < 2:
        return True
    
    SAFETY_MARGIN = 2
    safe_distance = stopping_distance(car.speed,car.deceleration) * SAFETY_MARGIN
    return d - CAR_MIN_DISTANCE <= safe_distance

# HELPER MATH FUNCTIONS
def stopping_distance(speed:float, deceleration:float):
    return (speed ** 2) / (2 * deceleration)  

def distance_between_points(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    # optimization: Check if the x or y coordinates are the same so we can avoid the square root operation
    if x1 == x2:
        # Distance is the absolute difference in y-coordinates
        return abs(y2 - y1)
    elif y1 == y2:
        # Distance is the absolute difference in x-coordinates
        return abs(x2 - x1)
    else:
        # Use the standard Euclidean distance formula
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

