import math

from model import *
from car import Car
from intersection import Intersection

# We need a concept of a very long time, so we can use it to represent a car that is not turning left
LIKE_SUPER_LONG = TURN_TIME * 1000


class CarController:
    def adjust_speed(
        car: Car,
        max_speed: float,
        dt: Seconds,
    ):
        if (
            too_fast(car.speed, max_speed)
            or too_close_to_intersection(car, car.target_intersection)
            or too_close_to_car_in_front(car, car.car_in_front)
        ):
            car.brake(dt)
        else:
            car.accelerate(dt)


def too_fast(car_speed: float, max_speed: Meters) -> bool:
    return car_speed >= max_speed


# TODO: NEEDS WORK
def too_close_to_car_in_front(behind: Car, ahead: Car) -> bool:
    if ahead is None:
        return False

    d = calculate_distance(behind.position, ahead.back_position())
    if d < CAR_MIN_DISTANCE:
        return True

    SAFETY_MARGIN = 2
    # TODO: actually do math here. We need to consider the speed of the car in front of us, not just some guideline for speed
    safe_distance = behind.speed * SPEED_BUFFER
    return d - CAR_MIN_DISTANCE <= safe_distance * SAFETY_MARGIN


# TODO: needs work
def too_close_to_intersection(car: Car, intersection: Intersection) -> bool:
    if intersection is None:
        return False

    # TODO: Now we need to consider the path we are going, if we are going to turn left right or go straight

    # Assuming we are going straight for now
    if intersection.is_green(car.direction):
        return False

    d = calculate_distance(car.position, intersection.position)
    if d < CAR_MIN_DISTANCE:
        return True

    # Turning left
    if direction_to_the_left[car.direction] == car.path.next_direction():
        # TODO: When close enough, Check if needs to slow down for turn
        # Need the distance to reach the turning speed
        # If that times some safety factor is less than the distance to the intersection , then we need to slow down
        inte: Intersection = car.target_intersection
        opposing = inte.opposing_car(car.direction)
        safe_time = time_to_opposing_car_arrival(inte.position, opposing)

        # TODO: When close enough, need to query intersection to see if there is a car coming from the opposite direction, It should account for our stopping distance

    SAFETY_MARGIN = 2

    return d - CAR_MIN_DISTANCE <= car.stopping_distance() * SAFETY_MARGIN


# HELPER MATH FUNCTIONS
def time_to_opposing_car_arrival(position, opposing_car: Car) -> Seconds:
    if opposing_car is None:
        return LIKE_SUPER_LONG

    # Avoiding a divide by zero error
    if opposing_car.speed == 0:
        return LIKE_SUPER_LONG

    distance = calculate_distance(opposing_car.position, position)
    # IDK: Maybe assuming current speed isn't enough
    return distance / opposing_car.speed


def calculate_distance(a: Point, b: Point) -> Meters:
    return math.hypot(b[0] - a[0], b[1] - a[1])
