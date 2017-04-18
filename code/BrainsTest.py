#http://www.voidspace.org.uk/python/mock/mock.html

import unittest
from unittest.mock import Mock as mock, patch
from ServoWheels import ServoWheels, ServoBasics
from Brains import Brains


class BrainsTest(unittest.TestCase):

    def test_is_wall_is_true_when_both_sensors_report_close_to_same_distance(self):
        ball_sensor = mock(name='ball_sensor')
        ball_sensor.distance.return_value = 10.5

        wall_sensor = mock(name='wall_sensor')
        wall_sensor.distance.return_value = 10

        brain = Brains(ball_sensor, wall_sensor, None, None)

        self.assertTrue(brain.is_wall())

        #print(ball_sensor.mock_calls)
        ball_sensor.dispose()
        wall_sensor.dispose()

    def test_is_wall_is_false_when_both_distances_are_very_different(self):

        ball_sensor = mock(name='ball_sensor')
        ball_sensor.distance.return_value = 10.5
        
        wall_sensor = mock(name='wall_sensor')
        wall_sensor.distance.return_value = 50

        brain = Brains(ball_sensor, wall_sensor, None, None)

        self.assertFalse(brain.is_wall())
        
        ball_sensor.dispose()
        wall_sensor.dispose()

    def test_drive_time_calc_given_10_cm(self):
        brain = Brains(None, None, None, None)
        drive_time = brain.get_drive_time(10)
        #print(drive_time)
        self.assertEqual(0.5471, drive_time)

    def test_drive_time_calc_given_50_cm(self):
        brain = Brains(None, None, None, None)
        drive_time = brain.get_drive_time(50)
        #print(drive_time)
        self.assertEqual(2.7356, drive_time)

    @patch('time.sleep', return_value=None)
    def test_drive_to_strike_zone_goes_foward(self, patched_time_sleep):
        ball_sensor = mock(name='ball_sensor')
        ball_sensor.distance.return_value = 50

        wall_sensor = mock(name='wall_sensor')
        wall_sensor.distance.return_value = 60

        wheels = mock(name='wheels')
        
        brain = Brains(ball_sensor, wall_sensor, wheels, None)
        brain.drive_to_strike_zone()

        wheels.foward.assert_called()
        wheels.dispose()

    @patch('time.sleep', return_value=None)
    def test_drive_overshot_strike_zone_goes_backward(self, patched_time_sleep):
        ball_sensor = mock(name='ball_sensor')
        ball_sensor.distance.return_value = 3

        wall_sensor = mock(name='wall_sensor')
        wall_sensor.distance.return_value = 60

        wheels = mock()
        
        brain = Brains(ball_sensor, wall_sensor, wheels, None)
        brain.drive_to_strike_zone()

        wheels.foward.assert_not_called()
        wheels.backward.assert_called()
        wheels.dispose()

    def test_if_is_in_strike_zone_drive_to_strike_zone_does_nothing(self):

        ball_sensor = mock(name='ball_sensor')
        ball_sensor.distance.return_value = 10.5

        wall_sensor = mock(name='wall_sensor')
        wall_sensor.distance.return_value = 60

        wheels = mock()
        
        brain = Brains(ball_sensor, wall_sensor, wheels, None)
        brain.strike_zone_center = 10
        brain.drive_to_strike_zone()
        wheels.foward.assert_not_called()
        wheels.backward.assert_not_called()
        wheels.dispose()

        

if __name__ == '__main__':
    unittest.main()
