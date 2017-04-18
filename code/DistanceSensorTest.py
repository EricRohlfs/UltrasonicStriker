import unittest
from unittest.mock import Mock as mock, patch
from DistanceSensor import DistanceSensor
import time 

class DistanceSensorTest(unittest.TestCase):

    def simulate_pin_going_high_after_one_second(self, value):
        """
        simulate the ultrasonic sensor for an run away time scenario.
        This happens when the ultrasonic sensor is not working correctly
        and the app would freeze without the error being thrown.
        """
        if self.pin_tracking_state is 0:
            time.sleep(1)
            return 1

    def simulate_pin_sunny_day_scenario(self, value):
        """
        simulate the ultrasonic sensor for an expected scenario.
        """
        # pin is zero by default, so we want to move to 1
        # to get to the second while statement in the distance function
        if self.pin_tracking_state is 0:
            # set to .5 as an intermediate tracking state 
            self.pin_tracking_state =.5 
            return 1 #but set the pin value to 1
        # we want to wait some time while in the second while loop in the distance function
        if self.pin_tracking_state is .5:
            time.sleep(.0001)
            self.pin_tracking_state = 1
            return 1
        # set pin back to zero to break out of the 2nd while loop
        # so we can do some math
        if self.pin_tracking_state is 1 :
            self.pin_tracking_state = 0
            return self.pin_tracking_state

    def test_distance_throws_a_time_out_error_when_timeout_limit_is_reached(self):
        self.pin_tracking_state = 0
        gpio = mock(name='gpio')
        gpio.input = mock(side_effect = self.simulate_pin_going_high_after_one_second)
        sensor = DistanceSensor(gpio, 1, 2)
        sensor.timeout = 0.95
        try:
            sensor.distance()
        except TimeoutError as e:
            self.assertEqual(e.args[0], sensor.timeout_message)
            gpio.dispose()

    def test_distance_returns_distance_in_centimeters(self):
        self.pin_tracking_state = 0
        gpio = mock(name='gpio')
        gpio.input = mock(side_effect = self.simulate_pin_sunny_day_scenario)
        sensor = DistanceSensor(gpio, 1, 2)
        sensor.timeout = 0.95
        distance = sensor.distance()
        #not very valid test, but is better than nothing
        print(distance)
        self.assertTrue(distance > 5)
        self.assertTrue(distance < 150)
        gpio.dispose()


if __name__ == '__main__':
    unittest.main()