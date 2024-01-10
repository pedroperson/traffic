from model import *
from car_controller import CarController
from display import print_road
from traffic_light import TrafficLight, LightController
import time
from map import generate_random_path
from map_2 import Map


def run_simulation():
    # Initialize the environment
    m = Map(3, 100)
    l1 = TrafficLight(0, 0, cycle_period=4)
    l2 = TrafficLight(100, 0, cycle_period=4)
    l3 = TrafficLight(200, 0, cycle_period=4)
    m.set_traffic_light(0, 0, l1)
    m.set_traffic_light(1, 0, l2)
    m.set_traffic_light(2, 0, l3)
    lights = [l1, l2, l3]

    # We are simulating just a stright road to a eternally red light

    cars = [
        Car(1, 0, 0, Direction.E),
        Car(30, 0, 20, Direction.E),
        Car(160, 0, 1, Direction.E),
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
        print(
            "INTERSECITON",
            car.next_intersection.x,
            car.next_intersection.y,
        )
        # TODO: connect intersection to car as well

    time_steps = 300  # Total number of time steps for the simulation
    dt = 1  # Time step duration
    last_time = time.time()
    for i in range(time_steps):
        dt = time.time() - last_time
        step(cars, lights, dt)
        print_road(cars, (200, 0))

    print("Simulation complete.")


def step(CARS, lights, dt):
    for light in lights:
        LightController.tick_light(light, time.time())

    for car in CARS:
        CarController.adjust_speed(
            car,
            car.car_in_front,
            MAX_SPEED,
            dt,
        )

    for car in CARS:
        CarController.update_position(car, dt)


# Note: To run the simulation, call run_stop_simulation()
run_simulation()
