import unittest
from unittest.mock import Mock

from car_controller import (
    CarController,
    too_fast,
    too_close_to_car_in_front,
    too_close_to_intersection,
    calculate_distance,
)

from car import Car
from path import Path
from intersection import Intersection
from model import *

# Constants used in the original code, define them here or import if they are available in the module
TURN_TIME = 10  # example value
METERS = 1.0  # example value
CAR_MIN_DISTANCE = 5.0  # example value
SPEED_BUFFER = 2.0  # example value


class TestCarController(unittest.TestCase):
    def setUp(self):
        # Setup Mock Car and Intersection objects
        self.car = Mock(spec=Car)
        self.intersection = Mock(spec=Intersection)
        self.car_controller = CarController()

    def test_too_fast(self):
        self.assertTrue(too_fast(60, 55))
        self.assertFalse(too_fast(50, 55))
        self.assertTrue(too_fast(55, 55))

    def test_calculate_distance(self):
        point_a = (0, 0)
        point_b = (3, 4)
        self.assertEqual(
            calculate_distance(point_a, point_b), 5.0
        )  # 3-4-5 right triangle

    def test_too_close_to_intersection(self):
        car = Car(0, 0, 5, Direction.N)
        car.path = Mock(spec=Path)

        self.intersection.position = (0, 5)
        self.intersection.is_green.return_value = True

        # Car is approaching a green light at a safe distance
        self.assertFalse(too_close_to_intersection(car, self.intersection))

        # Car is approaching a red light but has enough distance to stop
        self.intersection.is_green.return_value = False
        self.assertTrue(too_close_to_intersection(car, self.intersection))

    def test_too_close_to_car_in_front(self):
        self.car.position = (0, 0)

        car_in_front = Mock(spec=Car)

        # Test safe distance
        car_in_front.back_position.return_value = (0, 10)
        self.car.speed = 1
        self.assertFalse(too_close_to_car_in_front(self.car, car_in_front))

        # Test too close
        car_in_front.back_position.return_value = (0, 4)
        self.assertTrue(too_close_to_car_in_front(self.car, car_in_front))

    def test_too_close_to_car_in_front_edge_cases(self):
        self.car.position = (0, 0)

        # No car in front
        self.assertFalse(too_close_to_car_in_front(self.car, None))

        # Car in front at the same position
        car_in_front_same_position = Mock(spec=Car)
        car_in_front_same_position.back_position.return_value = (0, 0)
        self.assertTrue(too_close_to_car_in_front(self.car, car_in_front_same_position))

        # Test with different speeds
        car_in_front = Mock(spec=Car)
        car_in_front.back_position.return_value = (0, 8)
        for speed in [1, 5, 10]:
            self.car.speed = speed
            self.assertTrue(too_close_to_car_in_front(self.car, car_in_front))


if __name__ == "__main__":
    unittest.main()
