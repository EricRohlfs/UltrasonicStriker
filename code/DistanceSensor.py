import time 

class DistanceSensor:

    def __init__(self, gpio, echo=None, trigger=None):
        self.speed_of_sound = 343.26 # m/s
        self._gpio = gpio
        self._trigger = trigger
        self._echo = echo
        self._gpio.setup(self._trigger, gpio.OUT)
        self._gpio.setup(self._echo, gpio.IN)
        
    #The HC-SR04 sensor requires a short 10uS pulse
    #  to trigger the module, which will cause the sensor
    #  to start the ranging program (8 ultrasound bursts
    #  at 40 kHz) in order to obtain an echo response. So,
    #  to create our trigger pulse, we set out trigger pin
    #  high for 10uS then set it low again.

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
        #print(distance)
        return distance # in cm
