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

    # Assuming we are going straight for now
    if intersection.is_green(car.direction):
        # TODO: Take right turn on red into account
        return False

    d = calculate_distance(car.position, intersection.position)
    if d < CAR_MIN_DISTANCE:
        return True

    # Turning left
    if direction_to_the_left[car.direction] == car.path.next_direction():
        # THINKING
        #  a car that curns left wants to stays as fast as possible till the intersectino
        # getting close it will need to adjust speed to the turning max speed
        # it may need to slow down further to 0 speed if there is a car incoming or the light turns red

        distance = calculate_distance(car.position, inte.position)

        stopping_distance = car.stopping_distance()

        # IDK maybe we can do a cheap ealy return here since we are so far away
        if distance > stopping_distance * 4:
            False

        # If its close enough we might need to adjust the speed
        # Now we need to worry about other cars
        inte: Intersection = car.target_intersection
        opposing = inte.opposing_car(car.direction)

        safety_factor = 1.5

        # The opposing car will reach us in:
        opposing_arrival = time_to_car_arrival(inte.position, opposing)
        # So i need(?) to know the minimum and maximum(?) times we will reach the intersection.
        # The minimum time is we stay at max speed till the minimum time we need to slow down to turn
        # the maximum is the car of in front us stop forever

        # ok maybe jus the minimum is enough
        # so maybe we should ask with the current speed?

        # We need to at fucking least slow down for the turn, so lets code that situation
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
                distance - CAR_MIN_DISTANCE <= car.stopping_distance() * SAFETY_MARGIN
            )

        # NOW I NEED THE MIDDLE TERM STUFF
        #  I need to know when it is that i need to start slowing down

        # TODO: When close enough, Check if needs to slow down for turn
        # Need the distance to reach the turning speed
        # If that times some safety factor is less than the distance to the intersection , then we need to slow down

        time_to_intersection = time_to_car_arrival(inte.position, car)

        time_to_stop = car.speed / car.deceleration

        stopping_distance = car.stopping_distance()

        distance = calculate_distance(car.position, inte.position)

        coasting_distance = distance - (stopping_distance * safety_factor)

        # Alright, First i need to know how long it will take me to get to the intersection

        # TODO: When close enough, need to query intersection to see if there is a car coming from the opposite direction, It should account for our stopping distance

    SAFETY_MARGIN = 2

    return d - CAR_MIN_DISTANCE <= car.stopping_distance() * SAFETY_MARGIN


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
