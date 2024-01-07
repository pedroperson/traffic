from main import  *


def print_road(CARS, stop_position):
    DX = 4
    ROAD_WIDTH =  math.ceil(stop_position[0] / DX)
    
    # Print the road
    for x in range(ROAD_WIDTH):
        # Check if there is a car at this position
        car = None
        for c in CARS:
            if c.position >= (x * DX, 0) and c.position < ((x + 1) * DX, 0):
                car = c
                break
        if car:
            print("c", end="")
        elif stop_position[0] >= (x * DX) and stop_position[0] < ((x + 1) * DX):
            print("X", end="")
        else:
            print(".", end="")
    print("")
    
     
MAX_SPEED =  16
def run_stop_simulation():
    # Initialize the car and the stop position
    CARS = [
        Car(0, 0, 40, Direction.E),
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
    time_steps = 600  # Total number of time steps for the simulation
    dt = 0.1  # Time step duration

    for step in range(time_steps):
        # print(f"Time Step {step + 1}")
        
        # Adjust car speeds based on the decision logic
        for car in CARS:

            #  assuming intersection is closed
            if slow_for_intersection(car, stop_position):
                # print("slow")
                car.slow_down(dt)

            elif car.car_in_front and too_close_to_car_in_front(car, car.car_in_front):
                car.slow_down(dt)

            elif too_fast(car, MAX_SPEED):
                car.slow_down(dt)

            else:
                car.speed_up(dt)

        # Update the car's position
        for car in CARS:
            car.update_position(dt)

        # for car in CARS:
            # print(f"  Car Status: {car}")
        print_road(CARS, stop_position)
            

    print("Simulation complete.")

# Note: To run the simulation, call run_stop_simulation()
run_stop_simulation()

