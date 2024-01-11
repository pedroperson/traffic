from model import *
from car_controller import CarController
from display import print_road
from traffic_light import TrafficLight, LightController, opposite_direction
import time
from map import generate_random_path
from map_2 import Map, Intersection


def run_simulation():
    time_steps = 3000  # Total number of time steps for the simulation
    dt = 0.02  # Time step duration
    street_length = Meters(100)  # From intersection to intersection

    the_map, cars, lights = init_test_map(street_length)

    last_time = int(time.time())
    for i in range(time_steps):
        # dt = time.time() - last_time
        last_time += dt
        step(cars, lights, dt, last_time, the_map)
        print_road(cars, (210, 0), lights)

    print("Simulation complete.")


def init_test_map(edge_length: Meters):
    the_map = Map(3, edge_length)

    # Initialize and place the traffic lights
    lights = []

    def new_traffic_light(x, y):
        l = TrafficLight(x, y, cycle_period=20, proportionX=0.5)
        lights.append(l)
        the_map.set_traffic_light(l)

    new_traffic_light(0, 0)
    new_traffic_light(100, 0)
    new_traffic_light(200, 0)

    # Initialize and place the cars
    cars = []

    def new_car(x, speed):
        car = Car(x, 0, speed, Direction.E)
        cars.append(car)
        the_map.insert_car(car)

    new_car(1, 0)
    new_car(10, 20)
    new_car(20, 20)
    new_car(30, 20)
    new_car(40, 20)
    new_car(50, 20)
    new_car(60, 20)
    new_car(100, 20)
    new_car(120, 16)
    new_car(140, 10)
    new_car(160, 6)
    new_car(180, 0)

    # TODO: connect cars that dont have a car ahead to the outgoing in their destination directions

    return the_map, cars, lights


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


# Note: To run the simulation, call run_stop_simulation()
run_simulation()
