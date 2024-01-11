from model import *
from car_controller import CarController
from traffic_light import TrafficLight, LightController
from map_2 import Map
from path import Path
from display import print_road
from typing import List


class State:
    the_map: Map
    cars: List[Car]
    lights: List[TrafficLight]
    current_time: Seconds


def run_simulation():
    time_steps = 3000  # Total number of time steps for the simulation
    dt = 0.02  # Time step duration
    street_length = Meters(100)  # From intersection to intersection
    nodes_per_row = 3  # Number of intersections per row

    state = init_test_map(nodes_per_row, street_length)

    for _ in range(time_steps):
        step(state, dt)
        print_road(state.cars, (210, 0), state.lights)
        state.current_time += dt

    print("Simulation complete.")


def step(state: State, dt: Seconds):
    for light in state.lights:
        LightController.update_state(light, state.current_time)

    # Calculate the stopping distance for each car before updating speed
    for car in state.cars:
        CarController.cache_stopping_distance(car)

    # Adjust the speed before updating the position
    for car in state.cars:
        CarController.adjust_speed(
            car,
            MAX_SPEED,
            dt,
        )

    # Finally adjust positions
    for car in state.cars:
        CarController.update_position(car, dt)

    # Some cars will have moved past their intersections, so we tell the map to deal with them
    state.the_map.deal_with_cars_past_intersection(state.cars)


# Create a test map with 3 lights and a few cars going East
def init_test_map(nodes_per_row: int, edge_length: Meters) -> State:
    the_map = Map(nodes_per_row, edge_length)

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

    # Return the initial state
    state = State()
    state.the_map = the_map
    state.cars = cars
    state.lights = lights
    state.current_time = 0
    return state


# Note: To run the simulation, call run_stop_simulation()
run_simulation()
