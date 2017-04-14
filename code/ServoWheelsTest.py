#http://www.voidspace.org.uk/python/mock/mock.html

import unittest
from unittest.mock import Mock as mock
from ServoWheels import ServoWheels, ServoBasics

class ServoWheelsTest(unittest.TestCase):

    def setUp(self):
        self.pwm = mock(name='pwm')
        #self.pwm.setPWM()
        self.wheels = ServoWheels(self.pwm, 2, 3)

    def tearDown(self):
        self.pwm.dispose()
        #self.wheels.dispose()

    def test_can_turn_left(self):
        self.wheels.turn_left()
        #print(self.pwm.mock_calls)
        self.pwm.setPWM.assert_any_call(2,0,150)
        self.pwm.setPWM.assert_any_call(3,0,150)
       
        
    

if __name__ == '__main__':
    unittest.main()
