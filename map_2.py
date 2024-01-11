from traffic_light import TrafficLight, opposite_direction
from model import *
import math
from typing import Dict, Optional


class Intersection:
    def __init__(self, x: Meters, y: Meters):
        self.x = x
        self.y = y
        self.traffic_light = None
        # Direction the car is coming from
        self.incoming_car: Dict[Direction, Optional[Car]] = {
            Direction.N: None,
            Direction.E: None,
            Direction.S: None,
            Direction.W: None,
        }
        # Direction the car left towards
        self.outgoing_car: Dict[Direction, Optional[Car]] = {
            Direction.N: None,
            Direction.E: None,
            Direction.S: None,
            Direction.W: None,
        }

    def set_traffic_light(self, traffic_light: TrafficLight):
        self.traffic_light = traffic_light

    def can_go(self, direction: Direction):
        # Everything is allowed fuck it go!
        if self.traffic_light is None:
            return (True, True)

        incoming_car = self.incoming_car[opposite_direction[direction]]
        # Ask the traffic light if a car could currently go in this direction
        return self.traffic_light.can_go(direction, incoming_car)


class Map:
    def __init__(self, nodes_per_row: int, edge_length: Meters):
        self.intersections: list[list[Intersection]] = [
            [
                Intersection(i * edge_length, j * edge_length)
                for j in range(nodes_per_row)
            ]
            for i in range(nodes_per_row)
        ]
        self.nodes_per_row = nodes_per_row
        self.edge_length = edge_length

    def set_traffic_light(self, traffic_light: TrafficLight):
        x = int(traffic_light.positionX / self.edge_length)
        y = int(traffic_light.positionY / self.edge_length)
        self.intersections[x][y].set_traffic_light(traffic_light)

    def insert_car(self, car: Car):
        insert_car_in_lane(car, self)
        insert_as_outgoing(car, self)

    # We will use closest_intersection to attach cars to their next intersection
    def closest_intersection(
        self, position_x: Meters, position_y: Meters, direction: Direction
    ) -> Intersection:
        # Scale dimensions from meters to nodes
        x = position_x / self.edge_length
        y = position_y / self.edge_length

        # TODO: I think the case when x or y is exatly an integer is not handled correctly, or at least not usefully for us, but maybe it wont matter

        # Round according to direction
        if direction == Direction.N:
            # Handle case where we are exactly on an intersection. in that case we want to return the next intesection in that direction
            if y % 1 == 0:
                y += 1

            return self.intersections[math.floor(x)][math.ceil(y)]
        elif direction == Direction.S:
            if y % 1 == 0:
                y -= 1
            return self.intersections[math.ceil(x)][math.floor(y)]
        elif direction == Direction.E:
            if x % 1 == 0:
                x += 1
            return self.intersections[math.ceil(x)][math.ceil(y)]
        elif direction == Direction.W:
            if x % 1 == 0:
                x -= 1
            return self.intersections[math.floor(x)][math.floor(y)]
        else:
            raise ValueError("Invalid direction")

    def next_intersection(self, intersection: Intersection, direction: Direction):
        x = int(intersection.x / self.edge_length)
        y = int(intersection.y / self.edge_length)
        if direction == Direction.N:
            if y + 1 >= self.nodes_per_row:
                return None
            return self.intersections[x][y + 1]
        elif direction == Direction.S:
            if y - 1 < 0:
                return None
            return self.intersections[x][y - 1]
        elif direction == Direction.E:
            if x + 1 >= self.nodes_per_row:
                return None
            return self.intersections[x + 1][y]
        elif direction == Direction.W:
            if x - 1 < 0:
                return None
            return self.intersections[x - 1][y]
        else:
            raise ValueError("Invalid direction")

    # Reorganize the map relationships if cars have passed their intersection
    # TODO: This should be done by the map
    # TODO: This needs to take path into account
    # TODO: Needs to update the intersection
    # TODO: Needs to update cars ahead and behind
    # TODO: Needs to update the position and direction of current car
    def deal_with_cars_past_intersection(self, CARS: "list[Car]"):
        for car in CARS:
            if car_passed_intersection(car):
                # TODO: This should be the destination of the car, not the current direction
                from_intersection = car.next_intersection
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
                next_intersection = self.next_intersection(
                    from_intersection, destination
                )
                car.next_intersection = next_intersection
                # TODO: Update car ahead and behind relations
                # TODO: Update the outgoing and incoming arrays in both interections
                # car.next_intersection.car_passed(car)


def insert_car_in_lane(car: Car, the_map: Map):
    # A car in connected to the intersection in the direction it is going
    intersection = the_map.closest_intersection(
        car.position[0], car.position[1], car.direction
    )
    car.next_intersection = intersection

    if intersection is None:
        return

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


def is_ahead(d, position, other_position):
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


# Not sure this belongs here
def car_passed_intersection(car: Car):
    if car.next_intersection is None:
        return False

    return is_ahead(
        car.direction, car.position, (car.next_intersection.x, car.next_intersection.y)
    )


# Test map 2
# map2 = Map(5, 10)
# map2.set_traffic_light(0, 0, TrafficLight(0, 0, 0.5))
# map2.set_traffic_light(1, 0, TrafficLight(0, 1, 0.5))
# print(map2.closest_intersection(8, 0, Direction.W).traffic_light)

# print(map2.closest_intersection(18, 0, Direction.W).traffic_light)
# print(map2.closest_intersection(28, 0, Direction.W).traffic_light)
