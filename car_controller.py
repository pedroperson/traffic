from model import  *
import math

class CarController():
    def adjust_speed( car: Car, car_in_front:Car, stop_position: Meters,max_speed:float, dt: Seconds):
        #  assuming always closed intersection for now
        if too_close_to_intersection(car, stop_position) \
          or too_close_to_car_in_front(car, car_in_front) \
          or too_fast(car, max_speed):
                slow_down_car(car, dt)
        else:
                speed_up_car(car, dt)

    def update_position(car: Car, dt:Seconds):
        delta_x, delta_y = direction_map[car.direction]
        car.position = (car.position[0] + delta_x * car.speed * dt, 
                         car.position[1] + delta_y * car.speed * dt)
        
        car.back_position = (car.position[0] - delta_x * car.length, 
                              car.position[1] - delta_y * car.length)

def speed_up_car(car: Car, dt: Seconds):
    car.speed += car.acceleration * dt

def slow_down_car(car: Car, dt: Seconds):
    car.speed = max(0, car.speed - car.deceleration * dt)    

def too_fast(car:Car, max_speed:Meters) -> bool:
    return car.speed >= max_speed

def too_close_to_car_in_front(behind: Car, ahead: Car) -> bool:
    if ahead is None:
        return False
    
    d = calculate_distance(behind.position, ahead.back_position)
    if d < CAR_MIN_DISTANCE:
        return True
    
    SAFETY_MARGIN = 2
    # Super cop out here using a constant speed buffer
    # Actually this is really bad because we are not accounting for the fact that the car in front might be slowing down or how fast its going
    safe_distance = behind.speed * SPEED_BUFFER 
    return d - CAR_MIN_DISTANCE <= safe_distance * SAFETY_MARGIN

def too_close_to_intersection(car:Car, intersection_position: Meters) -> bool:
    d = calculate_distance(car.position, intersection_position)
    if d < 2:
        return True
    
    SAFETY_MARGIN = 2
    safe_distance = stopping_distance(car.speed,car.deceleration) 
    return d - CAR_MIN_DISTANCE <= safe_distance * SAFETY_MARGIN

# HELPER MATH FUNCTIONS
def stopping_distance(speed:float, deceleration:float):
    return (speed ** 2) / (2 * deceleration)  

def calculate_distance(point1:Point, point2: Point) -> Meters:
    x1, y1 = point1
    x2, y2 = point2
    return math.hypot(x2 - x1, y2 - y1)