#http://www.voidspace.org.uk/python/mock/mock.html

import unittest
from unittest.mock import Mock as mock, patch, PropertyMock
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
        drive_time = brain.calculate_driving_time(10)
        self.assertEqual(0.5471, drive_time)

    def test_drive_time_calc_given_50_cm(self):
        brain = Brains(None, None, None, None)
        drive_time = brain.calculate_driving_time(50)
        self.assertEqual(2.7356, drive_time)

    @patch('time.sleep', return_value=None)
    def test_drive_to_strike_zone_goes_foward(self, patched_time_sleep):
        ball_sensor = mock(name='ball_sensor')
        ball_sensor.distance.return_value = 50
        wall_sensor = mock(name='wall_sensor')
        wall_sensor.distance.return_value = 60
        wheels = mock(name='wheels')
        
        brain = Brains(ball_sensor, wall_sensor, wheels, None)
        #method under test
        brain.drive_to_strike_zone()

        wheels.foward.assert_called()

        wheels.dispose()
        ball_sensor.dispose()
        wall_sensor.dispose()

    @patch('time.sleep', return_value=None)
    def test_drive_overshot_strike_zone_goes_backward(self, patched_time_sleep):
        ball_sensor = mock(name='ball_sensor')
        ball_sensor.distance.return_value = 3
        wall_sensor = mock(name='wall_sensor')
        wall_sensor.distance.return_value = 60
        wheels = mock(name='wheels')
        
        brain = Brains(ball_sensor, wall_sensor, wheels, None)
        #method under test
        brain.drive_to_strike_zone()

        wheels.foward.assert_not_called()
        wheels.backward.assert_called()
        wheels.dispose()
        ball_sensor.dispose()
        wall_sensor.dispose()

    def test_drive_to_strike_zone_when_the_ball_is_already_in_strike_zone_nothing_happens(self):
        ball_sensor = mock(name='ball_sensor')
        ball_sensor.distance.return_value = 10.5
        wall_sensor = mock(name='wall_sensor')
        wall_sensor.distance.return_value = 60
        wheels = mock(name='wheels')
        
        brain = Brains(ball_sensor, wall_sensor, wheels, None)
        brain.strike_zone_center = 10
        #method under test
        brain.drive_to_strike_zone()
        wheels.foward.assert_not_called()
        wheels.backward.assert_not_called()
        wheels.dispose()

    def test_can_stop_find_ball_left_command_while_running(self):
        wheels = mock(name='wheels')

        with patch('__main__.Brains.keep_finding_the_ball', new_callable=PropertyMock) as mock_keep_finding:
            brain = Brains(None, None, wheels, None)
            brain.is_wall = mock(return_value = True)
            mock_keep_finding.side_effect = [True, True, True, False]
            brain.find_ball_left()
            #if we do not have a runaway loop then this appears to work
            wheels.turn_left.assert_any_call()
            wheels.stop.assert_any_call()
        wheels.dispose()

    def test_can_stop_find_ball_right_command_while_running(self):
        wheels = mock(name='wheels')
        wheels.turn_left.assert_not_called() # double check no side effects
        wheels.turn_right.assert_not_called() # ensure no side effects
        with patch('__main__.Brains.keep_finding_the_ball', new_callable=PropertyMock) as mock_keep_finding:
            brain = Brains(None, None, wheels, None)
            brain.is_wall = mock(return_value = True)
            mock_keep_finding.side_effect = [True, True, True, False]
            brain.find_ball_right()
            wheels.turn_right.assert_any_call()
            wheels.stop.assert_any_call()
        wheels.dispose()
    
    def test_is_wall_stops_find_ball_left_command(self):
        wheels = mock(name='wheels')
        wheels.turn_left.assert_not_called() # double check no side effects

        brain = Brains(None, None, wheels, None)
        brain.is_wall = mock(side_effect = [True, True, True, False] )
        
        #method under test
        brain.find_ball_left()
        
        wheels.turn_left.assert_any_call()
        wheels.stop.assert_any_call()

        wheels.dispose()
    
    def test_find_ball_left_command_ensure_default_keep_finding_is_set_to_true(self):
        wheels = mock(name='wheels')
        wheels.turn_left.assert_not_called() # double check no side effects

        brain = Brains(None, None, wheels, None)
        #_keep_finding_the_ball is normally true, setting to false is best way to test
        brain._keep_finding_the_ball = False 
        # iterate through a few trues, then a false.
        brain.is_wall = mock(side_effect = [True, True, True, False] )
        #call the method under test
        brain.find_ball_left()
        
        wheels.turn_left.assert_any_call()
        wheels.stop.assert_any_call()
        
        #cleanup
        wheels.dispose()
    

if __name__ == '__main__':
    unittest.main()
