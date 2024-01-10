from model import *
from car_controller import CarController
from display import print_road


def step(CARS, red_light, dt):
    # TODO: set light state first so cars can react to it

    for car in CARS:
        CarController.adjust_speed(car, car.car_in_front, red_light, MAX_SPEED, dt)

    for car in CARS:
        CarController.update_position(car, dt)


def run_stop_simulation():
    # We are simulating just a stright road to a eternally red light
    cars = generate_cars()
    red_light = (600, 0)

    time_steps = 100  # Total number of time steps for the simulation
    dt = 1  # Time step duration

    for i in range(time_steps):
        step(cars, red_light, dt)
        print_road(cars, red_light)

    print("Simulation complete.")


def generate_cars():
    CARS = [
        Car(-400, 0, 40, Direction.E),
        Car(-300, 0, 10, Direction.E),
        Car(-200, 0, 4, Direction.E),
        Car(-10, 0, 1, Direction.E),
        Car(100, 0, 0, Direction.E),
        Car(300, 0, 1, Direction.E),
        Car(330, 0, 20, Direction.E),
    ]

    for i in range(len(CARS)):
        if i > 0:
            CARS[i].car_behind = CARS[i - 1]
        if i < len(CARS) - 1:
            CARS[i].car_in_front = CARS[i + 1]

    return CARS


# Note: To run the simulation, call run_stop_simulation()
run_stop_simulation()
