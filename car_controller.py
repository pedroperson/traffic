import math

from model import *
from car import Car
from intersection import Intersection

# We need a concept of a very long time, so we can use it to represent a car that is not turning left
LIKE_SUPER_LONG = TURN_TIME * 1000
SAFETY_FACTOR = 2
INTERSECTION_WIDTH = 20


class CarController:
    def adjust_speed(
        car: Car,
        max_speed: float,
        dt: Seconds,
    ):
        if too_fast(car.speed, max_speed):
            car.brake(dt)
            return

        if car.target_intersection and too_close_to_intersection(
            car, car.target_intersection
        ):
            car.brake(dt)
            return

        if car.car_in_front and too_close_to_car_in_front(car, car.car_in_front):
            car.brake(dt)
            return

        car.accelerate(dt)


def too_fast(car_speed: float, max_speed: Meters) -> bool:
    return car_speed >= max_speed


def too_close_to_car_in_front(behind: Car, ahead: Car) -> bool:
    if ahead is None:
        return False

    d = calculate_distance(behind.position, ahead.back_position())
    if d < CAR_MIN_DISTANCE:
        return True

    # TODO: actually do math here. We need to consider the speed of the car in front of us, not just some guideline for speed
    safe_distance = behind.speed * SPEED_BUFFER
    return d - CAR_MIN_DISTANCE <= safe_distance * SAFETY_FACTOR


def can_stop_in_time(car: Car, point: Point, safety_factor) -> bool:
    d = calculate_distance(car.position, point)
    if d < CAR_MIN_DISTANCE:
        return False
    return d - CAR_MIN_DISTANCE > car.stopping_distance() * safety_factor


def too_close_to_intersection(car: Car, intersection: Intersection) -> bool:
    # If there is no next intersection, we are definitely not close it
    if intersection is None:
        return False

    distance_to_intersection = calculate_distance(car.position, intersection.position)

    # Light is red OR yellow, check if we are too close to intersection
    if not intersection.is_green(car.direction):
        # TODO: Allow turning right on red

        # Really the car should just stop here, but if we are super fast nd close to light to a point we can't even stop anymore, we just close our eyes and go through cus life is too short to even care
        minimum_stopping_distance = car.stopping_distance()
        # Can't stop anymore, even if we stomp on them breaks
        if distance_to_intersection < minimum_stopping_distance:
            return False

        # We are close enough to have to worry about stopping but still close enough to stop
        return (
            distance_to_intersection - INTERSECTION_WIDTH
            <= minimum_stopping_distance * SAFETY_FACTOR
        )

    turning_left = direction_to_the_left[car.direction] == car.path.next_direction()
    turning_right = not turning_left and not car.direction == car.path.next_direction()

    # Light is green, turning left
    if turning_left:
        # NEWER THINKING:
        # We assume the light will be green forever. If it turns red on us and we can't stop we just keep going through

        # Lets start with the case of no opposing car, so we just need to worry about us. To make a turn, we need to make sure we aren't too fast for a turn
        if should_slow_down_for_turning_speed(car, intersection):
            return True

        # Ok lets worry about the car incoming in the opposing lane
        opposing = intersection.opposing_car(car.direction)

        # If  there is no car incoming and we dont need to slow down, then we are good to keep accelerating
        if opposing is None:
            return False

        # Lets consider the case where there is an incoming car but we can make the turn before they get here
        # The car in the opposing lane is going to be at the intersection at this time ...
        opposing_arrival = time_to_car_arrival(intersection.position, opposing)
        # ... and it must be there later than us for us to be safely able to turn
        i_can_make_this_turn = (
            min_time_to_intersection(car, intersection) + TURN_TIME > opposing_arrival
        )
        if i_can_make_this_turn:
            return False

        # So now we have the situation where there is a car in the opposing lane but we are so far that it doesnt matter. No matter what we can stop to zero in time
        extra_safety_factor = 1.5 * SAFETY_FACTOR
        if can_stop_in_time(car, intersection.position, extra_safety_factor):
            return False

        # So finally at this point we know we are not too fast for the turn, but there is a car incoming and we cannot make the turn on time, and can't stop soon enough, so breeak
        return True

    # Turning right
    if turning_right:
        if should_slow_down_for_turning_speed(car, intersection):
            return True

    return False


# HELPER MATH FUNCTIONS
def time_to_car_arrival(position, car: Car) -> Seconds:
    distance = calculate_distance(car.position, position)
    # Avoiding a divide by zero error
    speed = car.speed if car.speed > 0.1 else 0.1
    # IDK: Maybe assuming current speed isn't enough, maybe the max speed needs to be taken into account
    return distance / speed


def calculate_distance(a: Point, b: Point) -> Meters:
    return math.hypot(b[0] - a[0], b[1] - a[1])


def distance_to_slow_down(car: Car, target_speed):
    return (car.speed**2 - target_speed**2) / (2 * car.deceleration)


def time_to_reach_speed(speed, target_speed, acceleration):
    return (speed - target_speed) / (acceleration)


def should_slow_down_for_turning_speed(car: Car, intersection: Intersection) -> bool:
    d = calculate_distance(car.position, intersection.position)
    distance_to_turn_speed = distance_to_slow_down(car, TURN_SPEED)
    return d <= distance_to_turn_speed * SAFETY_FACTOR


# What if I go as fast as I can till the intersection, and then I slow down to turning speed
def min_time_to_intersection(car: Car, intersection: Intersection) -> Seconds:
    distance_car_to_intersection = calculate_distance(
        car.position, intersection.position
    )
    # we are going to slow down at some point to turning speed
    # IDK: assuming current speed here but maybe it should be max_speed even
    distance_to_turn_speed = distance_to_slow_down(car, TURN_SPEED)

    # Now we need to calculate the distance we have left before having to slow down for the turn
    distance_in_full_speed = distance_car_to_intersection - distance_to_turn_speed
    # Assuming constant speed, in future could take acceleration and max speed into account but i dont think it matters much
    speed = car.speed if car.speed > 0.1 else 0.1
    time_in_full_speed = distance_in_full_speed / speed
    # Since we are going to calculate in time now, we need the time it takes to slow down to turning speed
    time_to_slow = time_to_reach_speed(speed, TURN_SPEED, car.deceleration)

    return (time_in_full_speed + time_to_slow) * SAFETY_FACTOR
