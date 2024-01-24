import math

from model import *
from car import Car
from intersection import Intersection

# We need a concept of a very long time, so we can use it to represent a car that is not turning left
LIKE_SUPER_LONG = TURN_TIME * 1000
SAFETY_FACTOR = 2


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

    # TODO: actually do math here. We need to consider the speed of the car in front of us, not just some guideline for speed
    safe_distance = behind.speed * SPEED_BUFFER
    return d - CAR_MIN_DISTANCE <= safe_distance * SAFETY_FACTOR


def can_stop_in_time(car: Car, point: Point) -> bool:
    d = calculate_distance(car.position, point)
    if d < CAR_MIN_DISTANCE:
        return False
    return d - CAR_MIN_DISTANCE > car.stopping_distance() * SAFETY_FACTOR


# TODO: needs work
def too_close_to_intersection(car: Car, intersection: Intersection) -> bool:
    # If there is no next intersection, we are definitely not close it
    if intersection is None:
        return False

    # Light is red, check if we are too close to intersection
    if not intersection.is_green(car.direction):
        return not can_stop_in_time(car, intersection.position)

    # Light is green, turning left
    if direction_to_the_left[car.direction] == car.path.next_direction():
        # NEWER THINKING:
        # Lets assume the light will be green forever and all we have to worry about is us and the opposing car

        # If we even further assume that there is no opposing car, then we just need to worry about us. In that case, to make a turn we need to make sure we are goig to be able to slow down to the turning speed
        d = calculate_distance(car.position, intersection.position)
        distance_to_turn_speed = distance_to_slow_down(
            car.speed, TURN_SPEED, car.deceleration
        )
        can_i_slow_down_to_turning_speed = d > distance_to_turn_speed * SAFETY_FACTOR
        if not can_i_slow_down_to_turning_speed:
            return True

        opposing = intersection.opposing_car(car.direction)
        # If i know there is no car incoming, and that we are far enough that we dont need to slow down, then we dont need to slow down
        if opposing is None:
            return False

        # ok, now lets consider the opposing car being too close and blocking us
        # One edge is, what if i go as fast as i can till the intersection, and then I slow down to turning speed-> will the opposing car get the the intersection before that time
        distance_car_to_intersection = calculate_distance(
            car.position, intersection.position
        )
        distance_to_turn_speed = distance_to_slow_down(
            car.speed, TURN_SPEED, car.deceleration
        )
        distance_in_full_speed = distance_car_to_intersection - distance_to_turn_speed
        # Assuming constant speed, in future could take acceleration and max speed into account but i dont think it matters much
        speed = car.speed if car.speed > 0.1 else 0.1
        time_in_full_speed = distance_in_full_speed / speed
        time_to_slow = time_to_reach_speed(speed, TURN_SPEED, car.deceleration)

        min_time_to_intersection = (time_in_full_speed + time_to_slow) * SAFETY_FACTOR

        opposing_arrival = time_to_car_arrival(intersection.position, opposing)

        i_can_make_this_turn = min_time_to_intersection + TURN_TIME > opposing_arrival
        if not i_can_make_this_turn:
            return True

        # Now, what if we are so far away that we can't make the turn obvious like i dont even care about the opposing car yet, maybe we should do this check before this set of checks
        return False

        i_can_fukin_turn_left_whenever = True
        if i_can_fukin_turn_left_whenever is True:
            if car.speed > TURN_SPEED:
                return distance > safety_factor * distance_to_slow_down(
                    car.speed, TURN_SPEED, car.deceleration
                )
            else:
                print("i dont freaking know")

        # The other extreme is a left turn i can never turn, and that become a red light

        i_can_fNEVER_ukin_turn_left_whenever = True
        if i_can_fNEVER_ukin_turn_left_whenever is True:
            return (
                distance - CAR_MIN_DISTANCE <= car.stopping_distance() * safety_factor
            )

        # Alright, First i need to know how long it will take me to get to the intersection

        # TODO: When close enough, need to query intersection to see if there is a car coming from the opposite direction, It should account for our stopping distance

    # TODO: Take right turn on red into account
    return False


# HELPER MATH FUNCTIONS
def time_to_car_arrival(position, car: Car) -> Seconds:
    if car is None:
        return LIKE_SUPER_LONG

    # Avoiding a divide by zero error
    if car.speed == 0:
        return LIKE_SUPER_LONG

    distance = calculate_distance(car.position, position)
    # IDK: Maybe assuming current speed isn't enough
    return distance / car.speed


def calculate_distance(a: Point, b: Point) -> Meters:
    return math.hypot(b[0] - a[0], b[1] - a[1])


def distance_to_slow_down(speed, target_speed, deceleration):
    return (speed**2 - target_speed**2) / (2 * deceleration)


def time_to_reach_speed(speed, target_speed, acceleration):
    return (speed - target_speed) / (acceleration)
