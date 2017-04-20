#from Adafruit_PWM_Servo_Driver import PWM
from time import sleep

class ServoSettings:
    """
    :param int pin_number:
        Number from the hat board that the servo is plugged into.

    :param int min_setting:
        min and max set how far up or down the servo moves.
    
    :param int max_setting:
        min and max set how for up or down the servo moves.
    
    :param float speed:
        how fast or slow the servo moves.
        Setting to 0.0 is full speed.
        This just sets a wait time.

    :param int steps:
        Used along with speed, how far to move.

        For example:
            if min = 400 and max = 450,
            then we will move to 405, sleep,
            then we move to 410, sleep, 415, sleep
            
            The sleep time is set by the speed setting.
    
    :pamarm bool reverse_min_and_max:
        Servos can be mounted differently and up is down and down is up.
        Setting this to True will reverse the expected directions to match 
        your robot.
    """

    def __init__(self, 
                 pin_number, 
                 min_setting, 
                 max_setting,
                 speed=0.5,
                 steps=5,
                 reverse_min_and_max = False):
          self.pin = pin_number
          self._min = min_setting
          self._max = max_setting
          self.speed = speed
          self.reverse_min_and_max = reverse_min_and_max

    @property
    def min(self):
        if self.reverse_min_and_max:
            return self._max
        else:
            return self._min
    
    @property
    def max(self):
        if self.reverse_min_and_max:
            return self._min
        else:
            return self._max


class Grabber:
    """
    Creates a grabbing claw using two mini servos, to slowly grab something of a known size such as a foosball.
    
    This class assumes you are using the pwm servo hat or other compatible library.
    
    .. note:: I wanted to create variables such as servo_left or servo_right, and open, or closed, but so much of that depends on
    how the servos are mounted. I went with generic naming no the paramaters as you can see below. 
    
    :param PWM servo_hat:
        This is the Adafruit PWM Servo Hat initialized in the main code.
    
    :param int servo1_pin:
        Number where the servo is plugged into the servo hat.
        
    :param int servo2_pin:
        Number where the servo is plugged into the servo hat.
        
    :param int servo_min:
        One of the limits for how open or closed the grabber claw is.
           
    :param int servo_max:
         One of the limits for how open or closed the grabber claw is.
    
    :param int step_size:
        How far to move the servo in between sleep cycles
        
    :param float speed:
        How fast or slow to grab something.
        This really just adjusts the wait time between movements.
        How long to wait before making the next micro movement.
    
    :param ServoSettings servo_lifter:
        The servo settings for the servo to lift the grabber up
        after it grabs the ball. 
    
    """
    
    # user servo_min and servo_max to adjust how far the grabber opens or closes    
    def __init__(self,
                 servo_hat,
                 servo1_pin,
                 servo2_pin,
                 lifter = None, #use newer settings object
                 servo_min=400,
                 servo_max=450,
                 step_size=5,
                 speed=0.05,
                 servo_1_min = None,
                 servo_1_max = None,
                 servo_2_min = None,
                 servo_2_max = None
                ):

          self.servo_hat = servo_hat
          self.servo1_pin = servo1_pin
          self.servo2_pin = servo2_pin
          self.lifter = lifter
          self.lifter_last_state = 0 # 0 or 1
          self.max = servo_max
          self.min = servo_min
          self.step_size = step_size
          self.speed = speed
          self.last_position = 0 # rename to last_state, it is either 0 or 1 for open or closed when using both servos at same time.
          self.servo_1_last_state = 0
          self.servo_2_last_state = 1 # we want opposite of other servo since grabber  
          self.servo_1_min = servo_1_min,
          self.servo_1_max = servo_1_max,
          self.servo_2_min = servo_2_min,
          self.servo_2_max = servo_2_max
          
          if servo_1_min is None:
            self.servo_1_min = self.min
          if servo_1_max is None:
            self.servo_1_max = self.max
          if servo_2_min is None:
            self.servo_2_min = self.min
          if servo_2_max is None:
            self.servo_2_max = self.max

          #ensure servos are where we want them.
          if lifter is not None:
            self.lift_up_or_down()
          #self.grab_release()
        

    # Either grabs or releases
    def grab_release(self):
          """
          Either grabs or releases using both servos.
          Using just one servo to pick up a small ball is a more efficient use of servos,
          but when you need to move both, this is the method to use.
          """
          pin1_position = self.servo_1_min #pin1 position
          pin2_position = self.servo_2_max #pin2 position
        
          self.last_position = 1 - self.last_position
          #switch the starting values  
          if self.last_position == 1:
                pin1_position =  self.servo_1_max
                pin2_position =  self.servo_2_min

          while(self.min <= pin1_position <= self.max):
                if self.last_position == 1:
                    self.servo_hat.setsPWM(self.servo1_pin, 0, pin1_position)
                    self.servo_hat.setPWM(self.servo2_pin, 0, pin2_position)
                    pin1_position = pin1_position - self.step_size
                    pin2_position = pin2_position + self.step_size
                if self.last_position == 0:
                    self.servo_hat.setPWM(self.servo1_pin, 0, pin1_position)
                    self.servo_hat.setPWM(self.servo2_pin ,0 ,pin2_position)
                    pin1_position = pin1_position + self.step_size
                    pin2_position = pin2_position - self.step_size
                sleep(self.speed)
                
    def servo_1_open_or_close(self):
          pin1_position = self.servo_1_min #pin1 position
        
          self.servo_1_last_state = 1 - self.servo_1_last_state
          #switch the starting values  
          if self.servo_1_last_state == 1:
                pin1_position =  self.servo_1_max

          while(self.servo_1_min <= pin1_position <= self.servo_1_max): 
                self.servo_hat.setPWM(self.servo1_pin, 0, pin1_position)
                if self.servo_1_last_state == 1:
                    pin1_position = pin1_position - self.step_size
                if self.servo_1_last_state == 0:
                    pin1_position = pin1_position + self.step_size
                sleep(self.speed)
        
    def servo_2_open_or_close(self):
        #set default
        pin2_position = self.servo_2_min #pin2 position
    
        self.servo_2_last_state = 1 - self.servo_2_last_state
        #switch the starting values  
        if self.servo_2_last_state == 1:
            pin2_position =  self.servo_2_max

        while(self.servo_2_min <= pin2_position <= self.servo_2_max): 
            self.servo_hat.setPWM(self.servo2_pin, 0, pin2_position)
            if self.servo_2_last_state == 1:
                pin2_position = pin2_position - self.step_size
            if self.servo_2_last_state == 0:
                pin2_position = pin2_position + self.step_size
            sleep(self.speed)

    def lift_up_or_down(self):
        position = self.lifter.min #set default position
    
        self.lifter_last_state = 1 - self.lifter_last_state
        #switch the starting values  
        if self.lifter_last_state == 1:
            position =  self.lifter.max

        while(self.lifter.min <= position <= self.lifter.max): 
            self.servo_hat.setPWM(self.lifter.pin, 0, position)
            if self.lifter_last_state == 1:
                position = position - self.step_size
            if self.lifter_last_state == 0:
                position = position + self.step_size
            sleep(self.lifter.speed)    
