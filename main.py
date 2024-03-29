from typing import List

from model import *
from car_controller import CarController
from map_controller import MapController
from light import Light
from car import Car
from map import Map
from path import Path
from display import Display, print_road
from pycasso.pycasso import Pycasso
from display2 import draw_state


class State:
    the_map: Map
    cars: List[Car]
    lights: List[Light]
    current_time: Seconds


def run_simulation():

    pycasso = Pycasso(400, 400)

    time_steps = 2000  # Total number of time steps for the simulation
    dt: Seconds = 0.1  # Time step duration
    street_length: Meters = 100  # From intersection to intersection
    nodes_per_row = 5  # Number of intersections per row

    state = init_test_map(nodes_per_row, street_length)

    map_width = street_length * (nodes_per_row - 1)

    # display_obj = Display(state.the_map, state.cars, dt)

    # display_obj.animate(time_steps)

    for _ in range(time_steps):
        step(state, dt)
        # display_obj.display(state)
        # print_road(state.cars, map_width, state.the_map)
        draw_state(pycasso, state.cars, map_width, state.the_map)
        state.current_time += dt

    print("Simulation complete.")


def step(state: State, dt: Seconds):
    for light in state.lights:
        light.update_state(state.current_time)

    # Adjust the speed before updating the position
    for car in state.cars:
        CarController.adjust_speed(
            car,
            MAX_SPEED,
            dt,
        )

    # Finally adjust positions
    for car in state.cars:
        car.move_forward(dt)

    # Some cars will have moved past their intersections, so we tell the map to deal with them
    MapController.deal_with_cars_past_intersection(state.the_map, state.cars)


# Create a test map with 3 lights and a few cars going East
def init_test_map(nodes_per_row: int, road_length: Meters) -> State:
    the_map = Map(nodes_per_row, road_length)

    # Initialize and place the traffic lights
    lights = []

    def new_traffic_light(x, y):
        l = Light(cycle_period=60, proportion_x=0.5)
        lights.append(l)
        intersection = the_map.intersection((x, y))
        intersection.set_light(l)

    for j in range(nodes_per_row - 1):
        for i in range(nodes_per_row - 1):
            new_traffic_light((i + 1) * road_length, j * road_length)

    # Initialize and place the cars
    cars = []

    def new_car(x, y, speed):
        car = Car(x, y, speed, Direction.E)
        # TODO: update this to handle any direction and the path! maybe we just move the car at the end of path generation. maybe we should just graduate from this test function
        # ASsuming the direction is East
        start_x = int(car.position[0] / the_map.road_length)
        start_y = int(car.position[1] / the_map.road_length)
        end = (nodes_per_row - 1, nodes_per_row - 1)
        # Generate a path till the end of the map
        car.path = Path((start_x, start_y), end, start_direction=Direction.E)
        # Align car to path
        car.direction = car.path.path_directions[0]

        cars.append(car)
        MapController.insert_car(the_map, car)

    # for j in range(0, 200, road_length):
    for i in range(0, 200, 10):
        new_car(i, road_length, 20)
    # TODO: connect cars that dont have a car ahead to the outgoing in their destination directions

    # Return the initial state
    state = State()
    state.the_map = the_map
    state.cars = cars
    state.lights = lights
    state.current_time = 0
    return state


print("Starting simulation...")
# Note: To run the simulation, call run_stop_simulation()
run_simulation()

print("Simulation complete.")
