from main import *
from car_controller import *

# Simple test cases for the adjust_speed function
def test_too_close_to_car_in_front():
    test_cases = [
        (Car(0, 0, 0, Direction.E), Car(40, 0, 0, Direction.E), False),

        (Car(0, 0, 60, Direction.E), Car(10, 0, 0, Direction.E), True),

        # Case 3: Car behind is at a safe distance and slower - should not be too close
        (Car(0, 0, 40, Direction.E), Car(500, 0, 50, Direction.E), False),

        # Case 4: Car behind is at the same speed but at the minimum safe distance - should not be too close
        (Car(0, 0, 50, Direction.E), Car(500, 0, 50, Direction.E), False),

        # Case 5: Car behind is at high speed but at a large distance - should not be too close
        (Car(0, 0, 26, Direction.E), Car(400, 0, 20, Direction.E), False),

        # Case 6: Car behind is at the same speed and too close - should be too close
        (Car(0, 0, 26, Direction.E), Car(40, 0, 26, Direction.E), True),
    ]

    dt = 0.1
    for i, (car_behind, car_in_front, expected_result) in enumerate(test_cases):
        result = too_close_to_car_in_front(car_behind, car_in_front)
        assert result == expected_result, f"Test case {i+1} failed: Expected {expected_result}, got {result}"

    print("All tests passed.")

test_too_close_to_car_in_front()


