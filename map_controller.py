from typing import List

from model import *
from car import Car
from map import Map
from intersection import Intersection


class MapController:
    def insert_car(map: Map, car: Car):
        insert_car_in_lane(car, map)
        insert_as_outgoing(car, map)

    # Reorganize the map relationships if cars have passed their intersection
    # TODO: I think this is still not the right place to do this! this only use the map once, and the used knowdge is not specific to this package. we need a higher level manager to do this, or just make it a loose function
    # TODO: This needs to take path into account
    # TODO: Needs to update the intersection
    # TODO: Needs to update cars ahead and behind
    # TODO: Needs to update the position and direction of current car
    # THESE SHOULD PROBABLY NOT BE CARS, THEY SHOULD BE DRIVERS OR NOT VEHICLE BUT CARS
    def deal_with_cars_past_intersection(map: Map, CARS: List[Car]):
        for car in CARS:
            if car.target_intersection is None:
                continue

            if not car_passed_intersection(car, car.target_intersection.position):
                continue

            # Get intersection
            origin = car.target_intersection
            origin: Intersection = origin
            direction = car.direction
            # next_direction = car.next_direction()

            # next_intersection = map.next_intersection(origin, next_direction)
            # find last car in the new lane
            # Connect car to end of intersection line
            # OPTIONALLY: Connect intersectino to car if it is the first one
            # Connect old intersection to car
            # origin.

            # Connect old intersection to car behind
            # OPTIONALLY: Set car position and direction to align with the new intersection
            # Connect car to intersection
            # car.target_intersection = next_intersection

            # TODO: This should be the destination of the car, not the current direction
            from_intersection = car.target_intersection
            from_direction = car.direction
            # set up the next car here from the incoming and outgoing shit
            path = car.path
            # TODO: This should probably be a path function
            next_target = path.next_target()
            destination = None
            if next_target is None:
                # Pretend car is just going to continue going straight
                destination = car.direction
            else:
                target = path.target()
                if target[0] > next_target[0]:
                    destination = Direction.E
                elif target[0] < next_target[0]:
                    destination = Direction.W
                elif target[1] > next_target[1]:
                    destination = Direction.N
                elif target[1] < next_target[1]:
                    destination = Direction.S

            path.step()

            # Get and attach next target intersection
            next_intersection = map.next_intersection(from_intersection, destination)
            car.target_intersection = next_intersection
            # TODO: Update car ahead and behind relations
            # TODO: Update the outgoing and incoming arrays in both interections
            # car.next_intersection.car_passed(car)


def car_passed_intersection(car: Car, intersection_position: Point):
    return is_ahead(car.direction, car.position, intersection_position)


# This belongs with the function above, the map doesn't need to know about this necessarily
def insert_car_in_lane(car: Car, the_map: Map):
    # A car in connected to the intersection in the direction it is going
    intersection = the_map.closest_intersection(
        car.position[0], car.position[1], car.direction
    )
    car.target_intersection = intersection

    if intersection is None:
        return

    # TODO: Break this out into another function
    # In the point of view of the intersection, the car is incoming from the opposite direction
    opposite_dir = opposite_direction[car.direction]
    # Get the car closest to the intersection so that we can find out how to insert this car in the lane
    first_car = intersection.incoming_car[opposite_dir]

    # Start assuming our car is the first one
    car_behind = first_car
    car_in_front = None

    index = 0
    while car_behind is not None:
        if is_ahead(car.direction, car.position, car_behind.position):
            break
        car_in_front = car_behind
        car_behind = car_behind.car_behind
        index += 1

    # Connect the car to the intersection
    if index == 0:
        intersection.incoming_car[opposite_dir] = car

    # Connect the car to the cars in front and behind
    if car_in_front is not None:
        car_in_front.car_behind = car
        car.car_in_front = car_in_front

    if car_behind is not None:
        car_behind.car_in_front = car
        car.car_behind = car_behind


# This belong with the function above, the map doesn't need to know about this necessarily
# Now hit it from the back so we can fill out the outgoing car lists
def insert_as_outgoing(car: Car, the_map: Map):
    # Pretend we are coming from the opposite direction to get the intersection behind us
    intersection = the_map.closest_intersection(
        car.position[0], car.position[1], opposite_direction[car.direction]
    )
    if intersection is None:
        return

    last_car = intersection.outgoing_car[car.direction]
    if last_car is None:
        intersection.outgoing_car[car.direction] = car
        return

    if is_ahead(car.direction, car.position, last_car.position):
        return

    intersection.outgoing_car[car.direction] = car
    last_car.car_behind = car
    car.car_in_front = last_car


def is_ahead(d: Direction, position: Point, other_position: Point):
    if d == Direction.N:
        return position[1] > other_position[1]
    elif d == Direction.S:
        return position[1] < other_position[1]
    elif d == Direction.E:
        return position[0] > other_position[0]
    elif d == Direction.W:
        return position[0] < other_position[0]
    else:
        raise ValueError("Invalid direction")
