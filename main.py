from model import *
from car_controller import CarController
from display import print_road
from traffic_light import TrafficLight, LightController, opposite_direction
import time
from map import generate_random_path
from map_2 import Map


def run_simulation():
    LEN = Meters(100)
    # Initialize the environment
    the_map = Map(3, LEN)

    lights = []

    def new_traffic_light(x, y):
        l = TrafficLight(x, y, cycle_period=20, proportionX=0.5)
        lights.append(l)
        the_map.set_traffic_light(int(x / LEN), int(y / LEN), l)

    new_traffic_light(0, 0)
    new_traffic_light(100, 0)
    new_traffic_light(200, 0)

    # We are simulating just a stright road to a eternally red light

    cars = [
        Car(1, 0, 0, Direction.E),
        Car(10, 0, 20, Direction.E),
        Car(20, 0, 20, Direction.E),
        Car(30, 0, 20, Direction.E),
        Car(40, 0, 20, Direction.E),
        Car(50, 0, 20, Direction.E),
        Car(60, 0, 20, Direction.E),
        Car(100, 0, 20, Direction.E),
        Car(120, 0, 16, Direction.E),
        Car(140, 0, 10, Direction.E),
        Car(160, 0, 6, Direction.E),
        Car(180, 0, 0, Direction.E),
    ]

    # # Connect cars to themselves ->TODO: this is bad now, should do it through the intersaction
    # for i in range(len(cars)):
    #     if i > 0:
    #         cars[i].car_behind = cars[i - 1]
    #     if i < len(cars) - 1:
    #         cars[i].car_in_front = cars[i + 1]

    # Connect cars to their next intersection
    for i, car in enumerate(cars):
        next_intersection = the_map.closest_intersection(
            car.position[0], car.position[1], car.direction
        )
        car.next_intersection = next_intersection

        # I dont think this coninue is needed anymore
        if car.next_intersection is None:
            continue

        opposite_dir = opposite_direction[car.direction]
        last_car = next_intersection.incoming_car[opposite_dir]

        if last_car is None:
            next_intersection.incoming_car[opposite_dir] = car
        else:
            if is_ahead(car.direction, car.position, last_car.position):
                next_intersection.incoming_car[opposite_dir] = car
                # insert at front of the line
                car.car_behind = last_car
                last_car.car_in_front = car

            elif last_car.car_behind is None:
                # insert at end of the line
                car.car_in_front = last_car
                last_car.car_behind = car

            else:
                found = False
                while last_car.car_behind is not None:
                    last_car = last_car.car_behind
                    if is_ahead(car.direction, car.position, last_car.position):
                        found = True
                        break

                if not found:
                    # insert at end of the line
                    car.car_in_front = last_car
                    last_car.car_behind = car
                else:
                    # insert at middle of the line
                    car.car_behind = last_car
                    car.car_in_front = last_car.car_in_front
                    last_car.car_in_front = car

        # Now hit it from the back so we can fill out the outgoing car lists
        previous_intersection = the_map.closest_intersection(
            car.position[0], car.position[1], opposite_dir
        )

        first_car = previous_intersection.outgoing_car[car.direction]
        if first_car is None:
            previous_intersection.outgoing_car[car.direction] = car
        else:
            if is_behind(car.direction, car.position, first_car.position):
                previous_intersection.outgoing_car[car.direction] = car
                first_car.car_behind = car
                car.car_in_front = first_car

        # TODO: connect intersection to car as well

    time_steps = 3000  # Total number of time steps for the simulation
    dt = 0.02  # Time step duration
    last_time = int(time.time())
    for i in range(time_steps):
        # dt = time.time() - last_time
        last_time += dt
        step(cars, lights, dt, last_time, the_map)
        print_road(cars, (210, 0), lights)

    print("Simulation complete.")


def step(CARS, lights, dt, current_time, the_map: Map):
    for light in lights:
        LightController.tick_light(light, current_time)

    for car in CARS:
        CarController.adjust_speed(
            car,
            car.car_in_front,
            MAX_SPEED,
            dt,
        )

    for car in CARS:
        CarController.update_position(car, dt)

    # TODO: Move interections, car following who bla bla bla

    # Check if cars have passed their intersection
    for car in CARS:
        if car.next_intersection is None:
            continue
        # Take direction into account to know what dimension to look at
        passed = False
        if car.direction == Direction.E:
            if car.position[0] > car.next_intersection.x:
                passed = True
        elif car.direction == Direction.W:
            if car.position[0] < car.next_intersection.x:
                passed = True
        elif car.direction == Direction.N:
            if car.position[1] > car.next_intersection.y:
                passed = True
        elif car.direction == Direction.S:
            if car.position[1] < car.next_intersection.y:
                passed = True

        if passed:
            # TODO: This should be the destination of the car, not the current direction
            from_intersection = car.next_intersection
            from_direction = car.direction
            # set up the next car here from the incoming and outgoing shit

            destination = car.direction
            next_intersection = the_map.next_intersection(
                from_intersection, destination
            )
            car.next_intersection = next_intersection
            #  TODO: Update car ahead and behind relations
            # car.next_intersection.car_passed(car)

        # Check if car has passed the intersection


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


def is_behind(d, position, other_position):
    if d == Direction.N:
        return position[1] < other_position[1]
    elif d == Direction.S:
        return position[1] > other_position[1]
    elif d == Direction.E:
        return position[0] < other_position[0]
    elif d == Direction.W:
        return position[0] > other_position[0]
    else:
        raise ValueError("Invalid direction")


# Note: To run the simulation, call run_stop_simulation()
run_simulation()
