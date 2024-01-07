from main import  *
from car_controller import CarController
from display import print_road

MAX_SPEED =  16
def run_stop_simulation():
    # Initialize the car and the stop position
    CARS = [
        Car(-1000, 0, 40, Direction.E),
        Car(-500, 0, 40, Direction.E),
        Car(-200, 0, 40, Direction.E),
        Car(-10, 0, 40, Direction.E),
        Car(100, 0, 0, Direction.E),
        Car(300, 0, 1, Direction.E),
        Car(330, 0, 20, Direction.E) 
    ]

    for i in range(len(CARS)):
        if i > 0:
            CARS[i].car_behind = CARS[i-1]
        if i < len(CARS) - 1:
            CARS[i].car_in_front = CARS[i+1]

    stop_position = (600,0)  # Example stop position

    # Simulation parameters
    time_steps = 200  # Total number of time steps for the simulation
    dt = 1  # Time step duration

    for step in range(time_steps):
        # print(f"Time Step {step + 1}")
        
        # Adjust car speeds based on the decision logic
        for car in CARS:
            CarController.adjust_speed(car, stop_position, MAX_SPEED, dt)

        # Update the car's position
        for car in CARS:
            CarController.update_position(car, dt)

        print_road(CARS, stop_position)
            

    print("Simulation complete.")

# Note: To run the simulation, call run_stop_simulation()
run_stop_simulation()

