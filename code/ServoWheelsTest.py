#http://www.voidspace.org.uk/python/mock/mock.html

import unittest
from unittest.mock import Mock as mock
from ServoWheels import ServoWheels, ServoBasics

class ServoWheelsTest(unittest.TestCase):

    def test_can_turn_right(self):
        pwm = mock(name='pwm')
        wheels = ServoWheels(pwm, 2, 3)
        wheels.turn_right()
        pwm.setPWM.assert_any_call(2,0,600)
        pwm.setPWM.assert_any_call(3,0,600)
        #print(pwm.mock_calls)
        pwm.dispose()

    def test_can_reverse_turn_right_command(self):
        pwm = mock(name='pwm')
        wheels = ServoWheels(pwm, 2, 3)
        wheels.switch_left_right_commands = True
        wheels.turn_right()
        pwm.setPWM.assert_any_call(2,0,150)
        pwm.setPWM.assert_any_call(3,0,150)
        #print(pwm.mock_calls)
        pwm.dispose()

    def test_can_turn_left(self):
        pwm = mock(name='pwm')
        wheels = ServoWheels(pwm, 2, 3)
        wheels.turn_left()
        pwm.setPWM.assert_any_call(2,0,150)
        pwm.setPWM.assert_any_call(3,0,150)
        #print(pwm.mock_calls)
        pwm.dispose()

    def test_switch_left_right_commands_swaps_commands(self):
        pwm = mock(name='pwm')
        wheels = ServoWheels(pwm, 2, 3)
        wheels.switch_left_right_commands = True
        wheels.turn_left()
        pwm.setPWM.assert_any_call(2,0,600)
        pwm.setPWM.assert_any_call(3,0,600)
        #print(pwm.mock_calls)
        pwm.dispose()

    def test_foward_with_reverse_command(self):
        pwm = mock(name='pwm')
        wheels = ServoWheels(pwm, 2, 3)
        wheels.switch_foward_backward_commands = True
        wheels.foward()
        pwm.setPWM.assert_any_call(2,0,600)
        pwm.setPWM.assert_any_call(3,0,150)
        #print(pwm.mock_calls)
        pwm.dispose()

    def test_foward(self):
        pwm = mock(name='pwm')
        wheels = ServoWheels(pwm, 2, 3)
        wheels.foward()
        pwm.setPWM.assert_any_call(2,0,150)
        pwm.setPWM.assert_any_call(3,0,600)
        #print(pwm.mock_calls)
        pwm.dispose()

    def test_backward(self):
        pwm = mock(name='pwm')
        wheels = ServoWheels(pwm, 2, 3)
        wheels.backward()
        pwm.setPWM.assert_any_call(2,0,600)
        pwm.setPWM.assert_any_call(3,0,150)
        #print(pwm.mock_calls)
        pwm.dispose()

    def test_backward_with_rever_command_set(self):
        pwm = mock(name='pwm')
        wheels = ServoWheels(pwm, 2, 3)
        wheels.switch_foward_backward_commands = True
        wheels.backward()
        pwm.setPWM.assert_any_call(2,0,150)
        pwm.setPWM.assert_any_call(3,0,600)
        #print(pwm.mock_calls)
        pwm.dispose()
        
    def test_stop_stops_both_servos(self):
        pwm = mock(name='pwm')
        wheels = ServoWheels(pwm, 2, 3)
        wheels.stop()
        #print(pwm.mock_calls)
        pwm.setPWM.assert_any_call(2,0,375.0)
        pwm.setPWM.assert_any_call(3,0,375.0)
        pwm.dispose()


if __name__ == '__main__':
    unittest.main()
