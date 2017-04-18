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
    
    # user servo_min and servo_max to adjust how far the grabber opens or closes    
    def __init__(self,
                 pwm,
                 servo1_pin,
                 servo2_pin,
                 servo_min=400,
                 servo_max=450,
                 step_size=5,
                 sleep_duration=0.05
                 servo_1_min = None,
                 servo_1_max = None,
                 servo_2_min = None,
                 servo_2_max = None
                ):

          self.pwm = pwm
          self.servo1_pin = servo1_pin
          self.servo2_pin = servo2_pin
          self.max = servo_max
          self.min = servo_min
          self.step_size = step_size
          self.sleep_duration = sleep_duration
          self.last_position = 0 # rename to last_state, it is either 0 or 1 for open or closed when using both servos at same time.
          self.servo_1_last_state = 0
          self.servo_2_last_state = 0  
          self.servo_1_min = servo_1_min,
          self.servo_1_max = servo_1_max,
          self.servo_2_min = servo_2_min,
          self.servo_2_max = servo_2_max
          
          if self.servo_1_min is None:
            self.servo_1_min = self.min
          if self.servo_1_max is None:
            self.servo_1_max = self.max
          if self.servo_2_min is None:
            self.servo_2_min = self.min
          if self.servo_2_max is None:
            self.servo_2_max = self.max
        

    # Either grabs or releases
    def grab_release(self):
        """
        Either grabs or releases using both servos.
        Using just one servo to pick up a small ball is a more efficient use of servos,
        but when you need to move both, this is the method to use.
        """
          pin1_pos = self.servo_1_min #pin1 position
          pin2_pos = self.servo_2_max #pin2 position
        
          self.last_position = 1 - self.last_position
          #switch the starting values  
          if self.last_position == 1:
                pin1_pos =  self.servo_1_max
                pin2_pos =  self.servo_2_min

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
                
        def servo_1_open_or_close(self):
            pin1_pos = self.servo_1_min #pin1 position
        
            self.self.servo_1_last_state = 1 - self.servo_1_last_state
            #switch the starting values  
            if self.servo_1_last_state == 1:
                pin1_pos =  self.servo_1_max

            while(self.servo_1_min <= pin1_pos <= self.servo_1_max): 
                 self.pwm.setPWM(self.servo1_pin, 0, pin1_pos)
                if self.servo_1_last_state == 1:
                    pin1_pos = pin1_pos - self.step_size
                if self.servo_1_last_state == 0:
                    pin1_pos = pin1_pos + self.step_size
                sleep(self.sleep_duration)
        
        def servo_2_open_or_close(self):
            #set default
            pin2_pos = self.servo_2_max #pin2 position
        
            self.servo_2_last_state = 1 - self.servo_2_last_state
            #switch the starting values  
            if self.servo_2_last_state == 1:
                pin1_pos =  self.servo_1_max
                pin2_pos =  self.servo_2_min

            while(self.servo_2_min <= pin1_pos <= self.servo_2_max): 
                self.pwm.setPWM(self.servo2_pin, 0, pin2_pos)
                if self.servo_2_last_state == 1:
                    pin2_pos = pin2_pos + self.step_size
                if self.servo_2_last_state == 0:
                    pin2_pos = pin2_pos - self.step_size
                sleep(self.sleep_duration)
            
