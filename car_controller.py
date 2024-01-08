from main import  *


class CarController():
    def adjust_speed( car: Car, car_in_front:Car, stop_position: Meters,max_speed:float, dt: Seconds):
        #  assuming always closed intersection for now
        if slow_for_intersection(car, stop_position) \
            or too_close_to_car_in_front(car, car_in_front) \
            or too_fast(car, max_speed):
             CarController.slow_down(car, dt)
        else:
             CarController.speed_up(car, dt)

    def update_position(car: Car, dt:Seconds):
        delta_x, delta_y = direction_map[car.direction]
        car.position = (car.position[0] + delta_x * car.speed * dt, 
                         car.position[1] + delta_y * car.speed * dt)
        
        car.back_position = (car.position[0] - delta_x * car.length, 
                              car.position[1] - delta_y * car.length)

    def speed_up(car: Car, dt:Seconds):
        car.speed += car.acceleration * dt 

    def slow_down(car: Car, dt:Seconds):
        car.speed -=  car.deceleration * dt
        if car.speed < 0:
            car.speed = 0
     
# DECISION LOGIC

def too_fast(car:Car, max_speed:Meters) -> bool:
    return car.speed >= max_speed

def too_close_to_car_in_front(behind: Car, ahead: Car) -> bool:
    if ahead is None:
        return False
    
    d = distance_between_points(behind.position, ahead.back_position)
    if d < CAR_MIN_DISTANCE:
        return True
    
    SAFETY_MARGIN = 2
    # Super cop out here using a constant speed buffer
    # Actually this is really bad because we are not accounting for the fact that the car in front might be slowing down or how fast its going
    safe_distance = behind.speed * SPEED_BUFFER 
    return d - CAR_MIN_DISTANCE <= safe_distance * SAFETY_MARGIN

def slow_for_intersection(car:Car, stop_position: Meters) -> bool:
    d = distance_between_points(car.position, stop_position)
    if d < 2:
        return True
    
    SAFETY_MARGIN = 2
    safe_distance = stopping_distance(car.speed,car.deceleration) 
    return d - CAR_MIN_DISTANCE <= safe_distance * SAFETY_MARGIN

# HELPER MATH FUNCTIONS
def stopping_distance(speed:float, deceleration:float):
    return (speed ** 2) / (2 * deceleration)  

def distance_between_points(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    # optimization: Check if the x or y coordinates are the same so we can avoid the square root operation
    if x1 == x2:
        # Distance is the absolute difference in y-coordinates
        return abs(y2 - y1)
    elif y1 == y2:
        # Distance is the absolute difference in x-coordinates
        return abs(x2 - x1)
    else:
        # Use the standard Euclidean distance formula
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

