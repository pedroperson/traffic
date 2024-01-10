from model import *
from car_controller import CarController
from display import print_road
from traffic_light import TrafficLight, LightController
import time
from map import generate_random_path
from map_2 import Map


def run_simulation():
    LEN = Meters(100)
    # Initialize the environment
    m = Map(3, LEN)

    lights = []

    def new_traffic_light(x, y):
        l = TrafficLight(x, y, cycle_period=20, proportionX=0.5)
        lights.append(l)
        m.set_traffic_light(int(x / LEN), int(y / LEN), l)

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
        Car(120, 0, 0, Direction.E),
        Car(140, 0, 0, Direction.E),
        Car(160, 0, 1, Direction.E),
        Car(180, 0, 0, Direction.E),
    ]

    # Connect cars to themselves ->TODO: this is bad now, should do it through the intersaction
    for i in range(len(cars)):
        if i > 0:
            cars[i].car_behind = cars[i - 1]
        if i < len(cars) - 1:
            cars[i].car_in_front = cars[i + 1]

    # Connect cars to their next intersection
    for i, car in enumerate(cars):
        car.next_intersection = m.closest_intersection(
            car.position[0], car.position[1], car.direction
        )

        # TODO: connect intersection to car as well

    time_steps = 800  # Total number of time steps for the simulation
    dt = 0.1  # Time step duration
    last_time = int(time.time())
    for i in range(time_steps):
        # dt = time.time() - last_time
        last_time += dt
        step(cars, lights, dt, last_time)
        print_road(cars, (200, 0), lights)

    print("Simulation complete.")


def step(CARS, lights, dt, current_time):
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


# Note: To run the simulation, call run_stop_simulation()
run_simulation()
