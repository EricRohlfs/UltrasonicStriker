import unittest
from unittest.mock import Mock as mock, patch, PropertyMock, call
from Striker import StrikerCommands

class StrikerTests(unittest.TestCase):

     def test_hide_striker_can_reverse_the_default_setting(self):    
        gpio = mock()
        servo_hat = mock()
        wedge_motor= mock()
        striker = StrikerCommands(gpio, 10, 11, servo_hat, wedge_motor, 12,
                         rotate_min=250, rotate_max=400, min_is_hidden=False)
        #method under test
        striker.hide_striker()

        servo_hat.setPWM.assert_called_with(12, 0, 400)
        
        servo_hat.dispose()
        gpio.dispose()
        servo_hat.dispose()
        wedge_motor.dispose()

if __name__ == '__main__':
    unittest.main()