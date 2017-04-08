import time
from sonic_striker_steppers import Motor

class StrikerCommands:
    _rotation_position = 0
    _wedge_position = 0
    
    def __init__(self, 
                 gpio,
                 strike_pin,
                 reverse_pin,
                 pwm,
                 wedge_motor,
                 rotate_striker_pin,
                 rotate_min = 230,
                 rotate_max = 475):

        gpio.setup(strike_pin, gpio.OUT)
        #gpio.setup(reverse.pin, gpio.OUT)

        self.gpio = gpio
        self.strike_pin = strike_pin
        self.reverse_pin = reverse_pin
        self.pwm = pwm
        self.wedge_motor = wedge_motor
        self.rotation_pin = rotate_striker_pin
        self.rotate_max = rotate_max
        self.rotate_min = rotate_min
        
    def strike(self):
       #forward
       #print("strike")
       self.gpio.output(self.strike_pin, self.gpio.HIGH)
       time.sleep(.04) # you may need to tweak this number if striker does not bounce back up
       self.gpio.output(self.strike_pin, self.gpio.LOW)

       # if you need to manually retract the striker,
       #   uncomment the code below
       #pause
       #time.sleep(1)
       #backward
       #gpio.output(striker_gpio2, gpio.HIGH)
       #time.sleep(.03)
       #gpio.output(striker_gpio2, gpio.LOW)

    def hide_striker(self):
        if self._rotation_position == 1:
          self.pwm.setPWM(self.rotation_pin, 0, self.rotate_max)
        elif self._rotation_position == 0:
          self.pwm.setPWM(self.rotation_pin,0,self.rotate_min)
        #trick to switch between 0 or a 1 
        self._rotation_position = 1 - self._rotation_position

    def turn_wedge(self, degrees):
        self.wedge_motor.rpm = 5
        m = self.wedge_motor
        print "Pause in seconds: " + `m._T`
        #m.mode = 2
        self._wedge_position = self._wedge_position + degrees
        m.move_to(degrees)
        
    def turn_wedge_zero(self):
        self.wedge_motor.move_to(0)

    #useful if your bot shuts down and you have to re-align the wedge and set to zero
    def zero_out_wedge_position(self):
        self._wedge_position = 0
