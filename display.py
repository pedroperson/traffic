import math

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
    