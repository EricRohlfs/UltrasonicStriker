import time 

class DistanceSensor:

    """
    Distance sensor code and supports an attached stepper motor to turn the 
    distanc sensor.

    :param RPi.GPIO gpio:
        General Purpose In and Out library for raspberry pi.

    :param int echo:
        Echo pin number

    :param int trigger:
        trigger pin number

    :param Motor motor:
        Stepper motor.

        The current implementation is not using this functionality, and the ultrasonic sensors 
        are mounted directly to the robot and the whole robot turns.
        
    """

    #motor is to turn 
    def __init__(self, gpio, echo, trigger, motor = None):
        self.speed_of_sound = 343.26 # m/s
        self._gpio = gpio
        self._trigger = trigger
        self._echo = echo
        self._gpio.setup(self._trigger, gpio.OUT)
        self._gpio.setup(self._echo, gpio.IN)
        #todo: put if not None check
        self.motor = motor
        self._motor_position = 0
        self.timeout_message = 'The Distance Sensor took too long. Is it Plugged in?'
        self.timeout = 0.9

    """    
    The HC-SR04 sensor requires a short 10uS pulse
      to trigger the module, which will cause the sensor
      to start the ranging program (8 ultrasound bursts
      at 40 kHz) in order to obtain an echo response. So,
      to create our trigger pulse, we set out trigger pin
      high for 10uS then set it low again.
    """
    
    def distance(self):
        """
        returns the distance in centimeters
        """
        # declaring variables, the times are overwritten later.
        pulse_start = time.time()
        pulse_end = time.time()
        
        #start the sensor
        self._gpio.output(self._trigger, True)
        time.sleep(0.00001)
        self._gpio.output(self._trigger, False)
        
        #save startTime
        while self._gpio.input(self._echo) == 0:
           pulse_start = time.time()

        #save arrivalTime
        while self._gpio.input(self._echo) == 1:
           pulse_end = time.time()
           pulse_duration = pulse_end - pulse_start
           
           #prevent a runaway loop
           if pulse_duration > self.timeout :
                   raise TimeoutError(self.timeout_message)

        #calculate distance in centimeters
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance,2)
        #print(self._echo)
        return distance # in cm

    def turn(self, degrees):
        """
        Will turn distanc sensor if it is attached to a stepper motor.
        """
        self.motor.rpm = 5
        m = self.motor
        #print "Pause in seconds: " + `m._T`
        self._motor_position = self._motor_position + degrees
        m.move_to(self._motor_position)
        
    def turn_to_zero(self):
        """
        Will move the sensor to zero if attached to a stepper motor.
        """
        self.motor.move_to(0)

    def zero_out_wedge_position(self):
        """
        Useful if your bot shuts down and you have to re-align the wedge and set to zero
        """
        self._motor_position = 0
