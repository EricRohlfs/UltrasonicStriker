import unittest
from unittest.mock import Mock as mock, patch, PropertyMock, call
from Grabber import Grabber

class GrabberTests(unittest.TestCase):

     def test_can_open_or_close_servo_1(self):
        servo_hat = mock(name='servo_hat')
        servo1_pin = 6 #hat pin 6
        servo2_pin = 7 #hat pin 7
        grabber = Grabber(servo_hat, servo1_pin, servo1_pin)
        grabber.servo_1_open_or_close()
        servo_hat.setPWM.assert_called()
        servo_hat.dispose()

     def test_open_or_close_servo_1_called_executes_specific_pwm_calls(self):
        servo_hat = mock(name='servo_hat')
        grabber = Grabber(servo_hat, 6, 7, servo_min = 400, servo_max = 450)
        grabber.servo_1_last_state = 0
        grabber.servo_1_open_or_close()
        servo_hat.setPWM.assert_called()

        expected_calls =  [call(6, 0, 445),
                           call(6, 0, 440),
                           call(6, 0, 435),
                           call(6, 0, 430),
                           call(6, 0, 425),
                           call(6, 0, 420),
                           call(6, 0, 415),
                           call(6, 0, 410),
                           call(6, 0, 405),
                           call(6, 0, 400)]

        servo_hat.setPWM.assert_has_calls(expected_calls, any_order=False)
        servo_hat.dispose()
    
     def test_open_or_close_servo_2_called_executes_specific_pwm_calls(self):
        servo_hat = mock(name='servo_hat')
        grabber = Grabber(servo_hat, 6, 7, servo_min = 400, servo_max = 450)
        grabber.servo_2_last_state = 1 #just ensuring default for test
        #method under test
        grabber.servo_2_open_or_close()

        expected_calls =  [call(7, 0, 400),
                           call(7, 0, 405),
                           call(7, 0, 410),
                           call(7, 0, 415),
                           call(7, 0, 420),
                           call(7, 0, 425),
                           call(7, 0, 430),
                           call(7, 0, 435),
                           call(7, 0, 440),
                           call(7, 0, 445),
                           call(7, 0, 450)]

        servo_hat.setPWM.assert_has_calls(expected_calls, any_order=False)
        servo_hat.dispose()

     def test_open_or_close_servo_1_flips_last_state(self):
        servo_hat = mock(name='servo_hat')
        grabber = Grabber(servo_hat, 6, 7, servo_min = 400, servo_max = 450)
        grabber.servo_2_last_state = 0 #just ensuring default for test
        #ensure starting value
        self.assertEqual(0, grabber.servo_2_last_state)
        #method under test
        grabber.servo_2_open_or_close()
        #prove the value was changed
        self.assertEqual(1, grabber.servo_2_last_state)
        servo_hat.dispose()   

     def test_open_or_close_servo_2_flips_last_state(self):
        servo_hat = mock(name='servo_hat')
        grabber = Grabber(servo_hat, 6, 7, servo_min = 400, servo_max = 450)
        grabber.servo_2_last_state = 1 #just ensuring default for test
        #ensure starting value
        self.assertEqual(1, grabber.servo_2_last_state)
        #method under test
        grabber.servo_2_open_or_close()
        #prove the value was changed
        self.assertEqual(0, grabber.servo_2_last_state)
        servo_hat.dispose()

if __name__ == '__main__':
    unittest.main()