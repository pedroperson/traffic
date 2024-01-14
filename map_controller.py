from typing import List, Optional

from model import *
from car import Car
from map import Map
from path import Path
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

            if car.path.next_target() == None:
                # TODO: Remove car from map
                continue

            if not car_passed_intersection(car, car.target_intersection.position):
                continue

            from_intersection: Intersection = car.target_intersection
            from_direction = car.direction
            car_behind = car.car_behind

            path: Path = car.path
            next_direction = path.next_direction()
            next_point = path.next_target()
            path.step()

            # Find the intersection the car will head to next
            if next_point is not None:
                next_intersection = map.intersection_at_index(
                    next_point[0], next_point[1]
                )
                # Reposition car to the next intersection
                car.target_intersection = next_intersection
                car.reposition(from_intersection.position, next_direction)

                # Insert the car in the next lane
                last_car_in_lane = last_car(next_direction, next_intersection)
                if last_car_in_lane == None:
                    # Set car as first and only in line
                    next_intersection.incoming_car[
                        opposite_direction[next_direction]
                    ] = car

                    # Try connecting to the next lane over instead
                    car.car_in_front = last_car_in_next_lane(car.path, map)
                else:
                    # Connect car to end of intersection line
                    last_car_in_lane.car_behind = car
                    car.car_in_front = last_car_in_lane
            else:
                car.target_intersection = None

            # Set the car behind as the first in line for the original intersection
            from_intersection.incoming_car[
                opposite_direction[from_direction]
            ] = car_behind

            # Save our car as the outgoing for the original intersection
            from_intersection.outgoing_car[next_direction] = car

            # Connect the car that was behind us to a potential car in the next lane
            car_behind.car_in_front = last_car_in_next_lane(car.path, map)


def next_intersection(map: Map, next_point, direction: Direction):
    if next_point is None:
        return None
    return map.intersection_at_index(next_point[0], next_point[1])


def last_car_in_next_lane(path: Path, map: Map):
    direction = path.next_direction()
    intersection = intersection(map, path.next_target(), direction)
    if intersection is None:
        return None

    return last_car(direction, intersection)


def car_passed_intersection(car: Car, intersection_position: Point):
    return is_ahead(car.direction, car.position, intersection_position)


def last_car(heading: Direction, intersection: Intersection) -> Optional[Car]:
    car_in_front = intersection.incoming_car[opposite_direction[heading]]
    if car_in_front == None:
        return None

    # Find the last car in line
    while car_in_front.car_behind != None:
        print(
            " car_in_front.car_behind",
            car_in_front.car_behind,
            car_in_front.car_behind.position,
        )
        car_in_front = car_in_front.car_behind

    return car_in_front


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
    # Set car as last outgoing
    intersection.outgoing_car[car.direction] = car

    # Connect the car to the car furthest back in the lane, setting it as the last
    last = last_car(car.direction, intersection)
    if last is not None:
        last.car_behind = car
        car.car_in_front = last


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
