import time
#from StepperMotors import Motor
#import RPi.GPIO 
#from Adafruit_PWM_Servo_Driver import PWM

class StrikerCommands:
    """
    Attachment for a small robot to strike a foosball or ping pong ball.

    The universal car door unlock actuator is the central piece of hardware
    in this solution.  The full implementation strikes the ball vertically
    to make it move.

    One way to visualize this is to imagine a person hammering a nail into 
    a piece of wood.  Now replace the nail with a foosball and replace 
    the hammer head with something shaped like a wedge of cheese.

    The full implementation must move the wedge out of the way
    so the ultrasonic distance sensor can look for the ball and not 
    have the striker head get in the way.

    :param RPi.GPIO gpio:
        So we can access the general input and output ports 
        on the raspberry pi to make stuff move or to get input 
        from sensors.

    :param int strike_pin:
        GPIO pin number used make the striker strike (like a hammer.)
        This is connected to the motor driver board (L298N) that
        drives the Universal Car Door Unlock Actuator

    :param int reverse_pin:
        GPIO pin number used to make the striker go back to the original positon.
        (This may not be required )
        This is connected to the motor driver board (L298N) that
        drives the Universal Car Door Unlock Actuator

    :param PWM pwm:
        Used to access the HAT board to make some servos move.
        
        If the striker is not mounted to a servo, this setting 
        can be ignored.

    :param MOTOR wedge_motor: 
        Used to make the wedge motor go left or right.  By changing the direction
        of the wedge we can control where the ball roles when we strike it.

        If the striker is striking mounted horizontally and is strikes the ball
        like a pool stick hitting a cue ball (in the game of pool), then this 
        setting can be ignored, having a rotating head does not do much in this 
        setup.

        Example::

            striker_stepper_IN1 = 32 #gpio12
            striker_stepper_IN2 = 33 #gpio13
            striker_stepper_IN3 = 36 #gpio16
            striker_stepper_IN4 = 35 #gpio19

            wedge_motor = Motor([striker_stepper_IN1,
                        striker_stepper_IN2,
                        striker_stepper_IN3,
                        striker_stepper_IN4])
            
    :param int rotate_striker_pin:
        The hat board number of the servo used to rotate the striker out of the
        way of the ultrasonic distance finder.  (Not really a pin, but the name 
        is easy.)

        If the striker is not mounted to a servo, this setting 
        can be ignored.

    :param int rotate_min:
        We need to move the striker out of the way of the ultrasonic distance 
        sensor and put it back when we are ready to strike.
        The rotate_min and rotate_max settings allow for the user to make
        approprate adjustments.  Generally speaking, the striker should be perpendicular
        to the floor when ready to strike.

        If the striker is not mounted to a servo, this setting 
        can be ignored.

    :param int rotate_max:
        We need to move the striker out of the way of the ultrasonic distance 
        sensor and put it back when we are ready to strike.
        The rotate_min and rotate_max settings allow for the user to make
        approprate adjustments.  Generally speaking, the striker should be perpendicular
        to the floor when ready to strike.
       
       If the striker is not mounted to a servo, this setting 
        can be ignored.

    :param bool min_is_hidden:
        Allows for changing if min or max is having the servo out of the way of 
        the ultrasonic sensor

    """
    
    def __init__(self, 
                 gpio,
                 strike_pin,
                 reverse_pin,
                 servo_hat,
                 wedge_motor,
                 rotate_striker_pin,
                 rotate_min = 230,
                 rotate_max = 475,
                 min_is_hidden = True,
                 power = 0.06,
                 reverse_power = 0.01):

        gpio.setup(strike_pin, gpio.OUT)
        gpio.setup(reverse_pin, gpio.OUT)

        self.gpio = gpio
        self.strike_pin = strike_pin
        self.reverse_pin = reverse_pin
        self.pwm = servo_hat
        self.wedge_motor = wedge_motor
        self.rotation_pin = rotate_striker_pin
        self.rotate_max = rotate_max
        self.rotate_min = rotate_min

        self.wedge_motor.rpm = 5
        self.power = power
        self.reverse_power = reverse_power

        #used internally
        self._rotation_position = 0
        self._wedge_position = 0
        self.min_is_hidden = min_is_hidden

        
    def strike(self, reverse=False):
       """
       """
      
       if reverse:
           print("striker up")
           self.gpio.output(self.reverse_pin, self.gpio.HIGH)
           time.sleep(self.reverse_power) # you may need to tweak this number if striker does not bounce back up
           self.gpio.output(self.reverse_pin, self.gpio.LOW)
           
       else:
           print("strike")
           self.gpio.output(self.strike_pin, self.gpio.HIGH)
           time.sleep(self.power) # you may need to tweak this number if striker does not bounce back up
           self.gpio.output(self.strike_pin, self.gpio.LOW)
       

    def hide_striker(self):
        """
        Gets the striker out of the way of the distance sensor.
        """
        if self.min_is_hidden:
          self.pwm.setPWM(self.rotation_pin, 0, self.rotate_min)
        else:
          self.pwm.setPWM(self.rotation_pin, 0, self.rotate_max)      

    def show_hide_striker(self):
        """
        When called either moves the the striker out of the way 
        of the Ultrasonic Distance Sensor or puts it back so 
        the ball can be hit. The hardware is a standard servo
        plugged into the servo hat.
        """
        if self._rotation_position == 1:
          self.pwm.setPWM(self.rotation_pin, 0, self.rotate_max)
        elif self._rotation_position == 0:
          self.pwm.setPWM(self.rotation_pin,0,self.rotate_min)
        #trick to switch between 0 or a 1 
        self._rotation_position = 1 - self._rotation_position

    def turn_wedge(self, degrees):
        """
        Rotates the wedge that makes contact with the foosball
        and allows us to control where the ball goes.

        :param int degrees:
            Negative numbers move one direction and positive
            numbers move the other direction, relative to 
            the current position.
        """
        m = self.wedge_motor
        #print "Pause in seconds: " + `m._T`
        self._wedge_position = self._wedge_position + degrees
        m.move_to(self._wedge_position)
        
    def turn_wedge_zero(self):
        """
        Will rotate the wedge to the zero position.
        Should be used when shutting down the robot or 
        when closing the program.

        Future plans involve other sensors that can help make
        the robot smarter and the robot can determine the direction
        to strike the ball.  In these scenarios the position of
        wedge is important.
        """
        self.wedge_motor.move_to(0)

    #useful if your bot shuts down and you have to re-align the wedge and set to zero
    def zero_out_wedge_position(self):
        """
        If the wedge is not in the proper position,
        the user can align it and then set that position
        to zero. Helpful if the robot is not cleanly shutdown.
        """
        self._wedge_position = 0
