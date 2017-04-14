import unittest
from unittest.mock import MagicMock as mock
from ServoWheels import ServoWheels, ServoBasics

class ServoBasicsTest(unittest.TestCase):


    def setUp(self):
        self.pwm = mock(name='pwm')
        self.real = ServoBasics(self.pwm, servo_min=160, servo_max=230)

    def tearDown(self):
        self.pwm.dispose()

    def test_servo_clockwise_can_use_non_default_values(self):
        self.real.servo_clockwise(10)
        self.pwm.setPWM.assert_called_with(10,0,160)

    def test_servo_counter_clockwise_can_use_non_default_values(self):
        self.real.servo_counter_clockwise(11)
        self.pwm.setPWM.assert_called_with(11,0,230)

    def test_servo_stop_uses_expected_vaules(self):
        self.real.servo_stop(12)
        self.pwm.setPWM.assert_called_with(12,0,195.0)

if __name__ == '__main__':
    unittest.main()
