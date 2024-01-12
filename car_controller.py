import math

from model import *
from car import Car
from intersection import Intersection


class CarController:
    def adjust_speed(
        car: Car,
        max_speed: float,
        dt: Seconds,
    ):
        if (
            too_fast(car.speed, max_speed)
            or too_close_to_intersection(car, car.next_intersection)
            or too_close_to_car_in_front(car, car.car_in_front)
        ):
            car.brake(dt)
        else:
            car.accelerate(dt)

    def update_position(car: Car, dt: Seconds):
        car.move_forward(dt)


# TODO: NEEDS WORK
def too_close_to_car_in_front(behind: Car, ahead: Car) -> bool:
    if ahead is None:
        return False

    d = calculate_distance(behind.position, ahead.back_position())
    if d < CAR_MIN_DISTANCE:
        return True

    SAFETY_MARGIN = 2
    # TODO: actually do math here. now i have the stopping ditance precalculated so it should be easy
    # Super cop out here using a constant speed buffer
    # Actually this is really bad because we are not accounting for the fact that the car in front might be slowing down or how fast its going
    safe_distance = behind.speed * SPEED_BUFFER
    return d - CAR_MIN_DISTANCE <= safe_distance * SAFETY_MARGIN


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

    SAFETY_MARGIN = 2

    return d - CAR_MIN_DISTANCE <= car.stopping_distance() * SAFETY_MARGIN


def too_fast(car_speed: float, max_speed: Meters) -> bool:
    return car_speed >= max_speed


# HELPER MATH FUNCTIONS


def calculate_distance(point1: Point, point2: Point) -> Meters:
    x1, y1 = point1
    x2, y2 = point2
    return math.hypot(x2 - x1, y2 - y1)
