import time 

class DistanceSensor:


    def __init__(self, gpio, echo=None, trigger=None):
        #if max_distance <= 0:
        #    raise ValueError('invalid maximum distance (must be positive)')
        try:
            self.speed_of_sound = 343.26 # m/s
            #self._max_distance = max_distance
            self._gpio = gpio
            self._trigger = trigger
            self._echo = echo
            #self._echo = Event()
            #self._echo_rise = None
            #self._echo_fall = None
            #self._trigger.pin.function = 'output'
            #self._trigger.pin.state = False
            #self.pin.edges = 'both'
            #self.pin.bounce = None
            #def callback():
            #    if self._echo_rise is None:
            #        self._echo_rise = time()
            #    else:
            #        self._echo_fall = time()
            #    self._echo.set()
            #self.pin.when_changed = callback
            #self._queue.start()

            self._gpio.setup(self._trigger,gpio.OUT)
            self._gpio.setup(self._echo,gpio.IN)
        except:
            self.close()

    def close(self):
        print("close")
        #try:
        #    self.close()
        #except AttributeError:
        #    if self._trigger is not None:
        #        raise
        #else:
        #    self._trigger = None

    #The HC-SR04 sensor requires a short 10uS pulse to trigger the module, which will cause the sensor to start the ranging program (8 ultrasound bursts at 40 kHz) in order to obtain an echo response. So, to create our trigger pulse, we set out trigger pin high for 10uS then set it low again.

    #@property
    def distance(self):
        self._gpio.output(self._trigger, True)
        time.sleep(0.00001)
        self._gpio.output(self._trigger, False)
        pulse_start = time.time()
        pulse_end = time.time()
        #save startTime
        while self._gpio.input(self._echo)==0:
           pulse_start = time.time()
        #save arrivalTime
        while self._gpio.input(self._echo)==1:
           pulse_end = time.time()
           #stop runaway loop
           counter = pulse_end - pulse_start
           if counter > 2:
                   return 0

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        #distance = (pulse_duration * 34300) / 2
        distance = round(distance,3)
            #gpio.cleanup()
        print(distance)
        return distance # in cm


    #@property
    #def gpio(self):
    #    return self._gpio
    
    #@property
    #def max_distance(self):
        """
        The maximum distance that the sensor will measure in meters. This value
        is specified in the constructor and is used to provide the scaling
        for the :attr:`value` attribute. When :attr:`distance` is equal to
        :attr:`max_distance`, :attr:`value` will be 1.
        """
     #   return self._max_distance

    @property
    #def distance(self):
    #    """
    #    Returns the current distance measured by the sensor in meters. Note
    #    that this property will have a value between 0 and
    #    :attr:`max_distance`.
    #    """
    #    return self.value * self._max_distance

    @property
    def trigger(self):
        """
        Returns the :class:`Pin` that the sensor's trigger is connected to.
        """
        return self._trigger

    @property
    def echo(self):
        """
        Returns the :class:`Pin` that the sensor's echo is connected to. This
        is simply an alias for the usual :attr:`pin` attribute.
        """
        return self._echo
