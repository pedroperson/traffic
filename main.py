from model import *
from car_controller import CarController, car_passed_intersection
from display import print_road
from traffic_light import TrafficLight, LightController, opposite_direction
import time
from map import generate_random_path
from map_2 import Map, Intersection
from path import Path


def run_simulation():
    time_steps = 3000  # Total number of time steps for the simulation
    dt = 0.02  # Time step duration
    street_length = Meters(100)  # From intersection to intersection
    nodes_per_row = 3  # Number of intersections per row

    the_map, cars, lights = init_test_map(nodes_per_row, street_length)

    current_time = 0
    for _ in range(time_steps):
        step(cars, lights, dt, current_time, the_map)
        print_road(cars, (210, 0), lights)
        current_time += dt

    print("Simulation complete.")


def step(CARS: "list[Car]", lights, dt, current_time, the_map: Map):
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

    the_map.deal_with_cars_past_intersection(CARS)


def init_test_map(nodes_per_row: int, edge_length: Meters):
    the_map = Map(nodes_per_row, edge_length)

    # Initialize and place the traffic lights
    lights = []
    new_traffic_light(0, 0)
    new_traffic_light(100, 0)
    new_traffic_light(200, 0)

    # Initialize and place the cars
    cars = []
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

    def new_traffic_light(x, y):
        l = TrafficLight(x, y, cycle_period=20, proportionX=0.5)
        lights.append(l)
        the_map.set_traffic_light(l)

    def new_car(x, speed):
        car = Car(x, 0, speed, Direction.E)
        # Since the direction is East
        start_x = int(car.position[0] / the_map.edge_length)
        start_y = int(car.position[1] / the_map.edge_length)

        # Generate a path till the end of the map
        car.path = Path(
            the_map.nodes_per_row,
            the_map.nodes_per_row,
            (start_x, start_y),
            (2, 0),
        )

        cars.append(car)
        the_map.insert_car(car)

    return the_map, cars, lights


# Note: To run the simulation, call run_stop_simulation()
run_simulation()
