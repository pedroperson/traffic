from model import *
import math
from map_2 import Intersection


class CarController:
    def adjust_speed(
        car: Car,
        max_speed: float,
        dt: Seconds,
    ):
        #  assuming always closed intersection for now
        if (
            too_fast(car, max_speed)
            or too_close_to_intersection(car, car.next_intersection)
            or too_close_to_car_in_front(car, car.car_in_front)
        ):
            slow_down_car(car, dt)
        else:
            speed_up_car(car, dt)

    def update_position(car: Car, dt: Seconds):
        delta_x, delta_y = direction_map[car.direction]
        car.position = (
            car.position[0] + delta_x * car.speed * dt,
            car.position[1] + delta_y * car.speed * dt,
        )

        car.back_position = (
            car.position[0] - delta_x * car.length,
            car.position[1] - delta_y * car.length,
        )

    # Fuck was this a mistake?
    # Separating this step so we can perform the calculation before we update the speed and position for this step. Furthermore, we can perform this calculation only once and use its value as often as we need.
    def cache_stopping_distance(car: Car):
        car.stopping_distance = stopping_distance(car.speed, car.deceleration)


def speed_up_car(car: Car, dt: Seconds):
    car.speed += car.acceleration * dt


def slow_down_car(car: Car, dt: Seconds):
    car.speed -= car.deceleration * dt
    if car.speed < 0:
        car.speed = 0


# NEEDS WORK
def too_close_to_car_in_front(behind: Car, ahead: Car) -> bool:
    if ahead is None:
        return False

    d = calculate_distance(behind.position, ahead.back_position)
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

    # IDK: Should this be the opposite direction?
    can_go = intersection.can_go(car.direction)

    # TODO: Make this work with turning and such
    if can_go[0]:
        return False

    d = calculate_distance(car.position, (intersection.x, intersection.y))
    if d < CAR_MIN_DISTANCE:
        return True

    SAFETY_MARGIN = 2

    return d - CAR_MIN_DISTANCE <= car.stopping_distance * SAFETY_MARGIN


def too_fast(car: Car, max_speed: Meters) -> bool:
    return car.speed >= max_speed


# HELPER MATH FUNCTIONS
def stopping_distance(speed: float, deceleration: float):
    return (speed**2) / (2 * deceleration)


def calculate_distance(point1: Point, point2: Point) -> Meters:
    x1, y1 = point1
    x2, y2 = point2
    return math.hypot(x2 - x1, y2 - y1)
