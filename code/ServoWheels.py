#from Adafruit_PWM_Servo_Driver import PWM

class ServoBasics:
    
    def __init__(self, pwm, servo_min = 150, servo_max = 600):
          self._pwm = pwm
          self._servo_min = servo_min
          self._servo_max = servo_max
          self._servo_zero = (self._servo_max-self._servo_min)/2 + self._servo_min

    # Simple Servo Calls
    def servo_clockwise(self, channel):
          self._pwm.setPWM(channel, 0, self._servo_min)

    def servo_counter_clockwise(self, channel):
          self._pwm.setPWM(channel, 0, self._servo_max)

    # needed for continuous rotaton servos,
    # standard servos automatically stop when they move to the number given
    def servo_stop(self, channel):
          self._pwm.setPWM(channel, 0, self._servo_zero)

class ServoWheels:

    def __init__(self, pwm, left_wheel, right_wheel, switch_foward_backward_commands = False ):
          self._pwm = pwm
          self.basics = ServoBasics(self._pwm)
          self._left_wheel = left_wheel
          self._right_wheel = right_wheel
          self._switch_left_right_commands = False
          self._switch_foward_backward_commands = switch_foward_backward_commands  
    
    #for the turn left and turn right functions, edit the sleep values for back up and turn to get the servo timing correct
    def turn_left(self):
          if(self._switch_left_right_commands):
               self.basics.servo_counter_clockwise(self._left_wheel)
               self.basics.servo_counter_clockwise(self._right_wheel)
          else:
               self.basics.servo_clockwise(self._left_wheel)
               self.basics.servo_clockwise(self._right_wheel)

    def turn_right(self):
          if(self._switch_left_right_commands):
               self.basics.servo_clockwise(self._left_wheel)
               self.basics.servo_clockwise(self._right_wheel)
          else:
               self.basics.servo_counter_clockwise(self._left_wheel)
               self.basics.servo_counter_clockwise(self._right_wheel)
            
    def foward(self):
          if(self._switch_foward_backward_commands):
               print("forward switched")
               self.basics.servo_counter_clockwise(self._left_wheel)
               self.basics.servo_clockwise(self._right_wheel)
          else:  
               self.basics.servo_clockwise(self._left_wheel)
               self.basics.servo_counter_clockwise(self._right_wheel)
           
    def backward(self):
          if(self._switch_foward_backward_commands):
               self.basics.servo_clockwise(self._left_wheel)
               self.basics.servo_counter_clockwise(self._right_wheel)
          else:  
               self.basics.servo_counter_clockwise(self._left_wheel)
               self.basics.servo_clockwise(self._right_wheel)

    def stop(self):
          self.basics.servo_stop(self._left_wheel)
          self.basics.servo_stop(self._right_wheel) 
        
    @property
    def switch_left_right_commands(self):
          """
          When ``True`` reverses the turn left or right commands.
          Useful when robot servos are mounted differently.
          """
          
          return self._switch_left_right_commands

    @switch_left_right_commands.setter
    def switch_left_right_commands(self,value):
          self._switch_left_right_commands = value
    
    @property
    def switch_foward_backward_commands(self):
          return self._switch_foward_backward_commands

    @switch_foward_backward_commands.setter
    def switch_foward_backward_commands(self, value):
          self._switch_foward_backward_commands = value
          
