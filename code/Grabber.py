from Adafruit_PWM_Servo_Driver import PWM

class Grabber:

    last_position = 0
    # user servo_min and servo_max to adjust how far the grabber opens or closes    
    def __init__(self,
                 pwm,
                 servo1_pin,
                 servo2_pin,
                 servo_min=200,
                 servo_max=300):

          self.pwm = pwm
          self.servo1_pin = servo1_pin
          self.servo2_pin = servo2_pin
          self.max = servo_max
          self.min = servo_min

    # Either grabs or releases
    def grab_release(self):
          self.last_position = 1 - self.last_position
          if self.last_position == 1: 
                self.pwm.setPWM(self.servo1_pin, 0, self.max)
                self.pwm.setPWM(self.servo2_pin, 0, self.min)        
          if self.last_position == 0:
                self.pwm.setPWM(self.servo1_pin, 0, self.min)
                self.pwm.setPWM(self.servo2_pin ,0 ,self.max)  

