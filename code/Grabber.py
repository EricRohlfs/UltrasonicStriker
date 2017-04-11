from Adafruit_PWM_Servo_Driver import PWM
from time import sleep

class Grabber:
    """
    Creates a grabbing claw using two mini servos, to slowly grab something of a known size such as a foosball.
    
    This class assumes you are using the pwm servo hat or other compatible library.
    
    .. note:: I wanted to create variables such as servo_left or servo_right, and open, or closed, but so much of that depends on
    how the servos are mounted. I went with generic naming no the paramaters as you can see below. 
    
    :param pwm:
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
        
    :param float sleep_duration:
        How long to wait before making the next micro movement.
    
    """
    last_position = 0
    # user servo_min and servo_max to adjust how far the grabber opens or closes    
    def __init__(self,
                 pwm,
                 servo1_pin,
                 servo2_pin,
                 servo_min=200,
                 servo_max=300,
                 step_size=15,
                 sleep_duration=0.2
                ):

          self.pwm = pwm
          self.servo1_pin = servo1_pin
          self.servo2_pin = servo2_pin
          self.max = servo_max
          self.min = servo_min
          self.step_size = step_size
          self.sleep_duration = sleep_duration

    # Either grabs or releases
    def grab_release(self):
          pin1_pos = self.min #pin1 position
          pin2_pos = self.max #pin2 position
        
          self.last_position = 1 - self.last_position
          #switch the starting values  
          if last_pos == 1:
                pin1_pos =  self.max
                pin2_pos =  self.min

          while(self.min <= pin1_pos <= self.max):  
                if self.last_position == 1:
                    self.pwm.setPWM(self.servo1_pin, 0, pin1_pos)
                    self.pwm.setPWM(self.servo2_pin, 0, pin2_pos)
                    pin1_pos = pin1_pos - self.step_size
                    pin2_pos = pin2_pos + self.step_size
                if self.last_position == 0:
                    self.pwm.setPWM(self.servo1_pin, 0, pin1_pos)
                    self.pwm.setPWM(self.servo2_pin ,0 ,pin2_pos)
                    pin1_pos = pin1_pos + self.step_size
                    pin2_pos = pin2_pos - self.step_size
          sleep(self.sleep_duration)
