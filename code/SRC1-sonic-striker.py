#!/usr/bin/python
#Working SRC 2017 Code for 4 Servo Control 
#2 Drive wheels, 1 Gripper and 1 Arm
#Revised 11.29.16 - Kevin Pace

# http://belikeotherpeople.co.uk/elevatedtopography/?p=138 
import sys
import threading
from Adafruit_PWM_Servo_Driver import PWM
from sonic_striker_steppers import Motor
import time
try: #try to import the gpio libraries (need to download) and throw an exception if there is an error
        import RPi.GPIO as gpio
except RuntimeError:
        print "error importing the gpio library which is probably because you need to run this program with sudo"

gpio.cleanup()

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
#pwm = PWM(0x40)
pwm = PWM(0x41)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096
servoZero = (servoMax-servoMin)/2 + servoMin

#these are pwm ports not gpio
servoLeft = 0
servoRight = 1
servoLift = 2
#servoGrip = 3
servo_echo = 4

#Striker actuator
striker_gpio1 = 13
striker_gpio2 = 15

# four gpio pins are needed for the striker steper
striker_stepper_IN1 = 31
striker_stepper_IN2 = 32
striker_stepper_IN3 = 33
striker_stepper_IN4 = 36

gpio.setmode(gpio.BOARD)


#.5ms 1.5ms 2.5ms

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

# Simple Servo Calls
def ServoClockwise(channel):
        pwm.setPWM(channel, 0, servoMin)

def ServoCounterClockwise(channel):
        pwm.setPWM(channel, 0, servoMax)

def ServoStop(channel):
        pwm.setPWM(channel, 0, servoZero)


#for the turn left and turn right functions, edit the sleep values for back up and turn to get the servo timing correct
def turnLeft(): 
        print "right button pressed!"
        #back up
        ServoClockwise(servoLeft)
        ServoCounterClockwise(servoRight)
        time.sleep(1.2) #edit this
        #turn left
        print "second part of left turn"
        ServoClockwise(servoLeft)
        ServoClockwise(servoRight)
        time.sleep(0.8) #edit this

def turnRight():
        print "left button pressed"
        #back up
        ServoClockwise(servoLeft)
        ServoCounterClockwise(servoRight)
        time.sleep(1.2) #edit this
        #turn right
        ServoCounterClockwise(servoLeft)
        ServoCounterClockwise(servoRight)
        time.sleep(0.8) # edit this



# ULTRASONIC MODE
#set GPIO Pins
GPIO_TRIGGER = 38
GPIO_ECHO = 40

#set GPIO direction
gpio.setup(GPIO_TRIGGER,gpio.OUT)
gpio.setup(GPIO_ECHO,gpio.IN)
# Turn ultrasonic sensor off
gpio.output(GPIO_TRIGGER, False)

#The HC-SR04 sensor requires a short 10uS pulse to trigger the module, which will cause the sensor to start the ranging program (8 ultrasound bursts at 40 kHz) in order to obtain an echo response. So, to create our trigger pulse, we set out trigger pin high for 10uS then set it low again.
def sonic_get_distance():
    gpio.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    gpio.output(GPIO_TRIGGER, False)
    pulse_start = time.time()
    pulse_end = time.time()
    #save startTime
    while gpio.input(GPIO_ECHO)==0:
       pulse_start = time.time()
    #save arrivalTime
    while gpio.input(GPIO_ECHO)==1:
       pulse_end = time.time()
       
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150 
    #distance = (pulse_duration * 34300) / 2
    distance = round(distance,2)
        #gpio.cleanup()
    print(distance)
    return distance # in cm

#def sonic_get_distance_loop():
#need to do something different than this to interrupt the program
#     try:
#        while True:
#            dist = distance()
#            print ("Measured Distance = %.1f cm" % dist)
#            time.sleep(1)
 
        # Reset by pressing CTRL + C
#    except KeyboardInterrupt:
#        print("Measurement stopped by User")
#        GPIO.cleanup()   

#Striker Stepper control
#def striker_rotate_left():
#        pwm.setPWM(channel, 0, servoMin)
#        striker_stepper_IN1



# STRIKER 
"""
Using an universal power door actuator and an L298N H-Bridge
the code will move the actuator forward, wait, then retract
"""
gpio.setup(striker_gpio1, gpio.OUT) #gpio27
gpio.setup(striker_gpio2, gpio.OUT) #gpio22

def strike():
       #forward
       print("strike")
       gpio.output(striker_gpio1, gpio.HIGH)
       time.sleep(.04)
       gpio.output(striker_gpio1, gpio.LOW)
       #pause
       #time.sleep(1)
       #backward
       #gpio.output(striker_gpio2, gpio.HIGH)
       #time.sleep(.03)
       #gpio.output(striker_gpio2, gpio.LOW)


# STRIKER STEPPER

striker_direction = Motor([striker_stepper_IN1,striker_stepper_IN2,striker_stepper_IN3,striker_stepper_IN4])
striker_direction.mode = 2

def turn_striker(degrees):
        striker_direction.rpm = 5
        m = striker_direction
        print "Pause in seconds: " + `m._T`
        #m.mode = 2
        m.move_to(degrees)
       #GPIO.cleanup()

# STRIKER SERVO moves the striker out of the way of the sonic sensor

def hide_striker(up_down):
        if up_down == 1:
          pwm.setPWM(4, 0, 475)
        elif up_down == 0:
          pwm.setPWM(4,0,230)  
        #return up_down

# Keyboard stuff

import Tkinter as tk

class MyFrame(tk.Frame):
    _striker_last = 0
    
    _striker_updown = 0

    @property
    def striker_last(self):
        return self._striker_last
    @striker_last.setter
    def striker_last(self,value):
        type(self)._striker_last = value

    @property
    def striker_updown(self):
        return self._striker_updown
    @striker_updown.setter
    def striker_last(self,value):
        type(self)._striker_updown = value
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # method call counter
        self.pack()
        self.afterId = None
        root.bind('<KeyPress>', self.key_press)
        root.bind('<KeyRelease>', self.key_release)

   
     
     #def get_striker_last():
     #   return striker_last

     #def set_striker_last(degrees):
     #   striker_last = degrees

    #keys in use w,s,k,z,a,u,d,c,o,t,g,n,2,3
    def key_press(self, event):
        if self.afterId != None:
            self.after_cancel( self.afterId )
            self.afterId = None
        else:
            print 'key pressed %s' % event.char
            if event.char == "w":
              text.insert('end', ' FORWARD ')
              ServoCounterClockwise(servoLeft)
              ServoClockwise(servoRight)
            elif event.char == "s":
              text.insert('end', ' RIGHT_TURN ')
              ServoCounterClockwise(servoLeft)
              ServoCounterClockwise(servoRight)
            elif event.char == "K":
              text.insert('end', ' Quit ')
              pwm.setPWM(0, 0, servoZero)
              root.destroy()
            elif event.char == "z":
              text.insert('end', ' BACKWARD ')
              ServoClockwise(servoLeft)
              ServoCounterClockwise(servoRight)
            elif event.char == "a":
              text.insert('end', ' LEFT_TURN ')
              ServoClockwise(servoLeft)
              ServoClockwise(servoRight)
            elif event.char == "u":
              text.insert('end', ' UP ')
              ServoClockwise(servoLift)
            elif event.char == "d":
              text.insert('end', ' DOWN ') 
              ServoCounterClockwise(servoLift)
            #elif event.char == "c":
            #  text.insert('end', ' CLOSE_GRIP ')
            #  ServoClockwise(servoGrip)
            #elif event.char == "o":
            #  text.insert('end', ' OPEN_GRIP ') 
            #  ServoCounterClockwise(servoGrip)
            
            # striker code
            elif event.char == "t":
              text.insert('end',' strike ')
              strike()
            elif event.char =="g":
              #d = sonic_get_distance()
              ds = "%f cm " % sonic_get_distance()
              text.insert('end',"Distance: " + ds)
            elif event.char == "n":
              #pulseU = 1
              #setServoPulse(servo_echo, 1)
              #time.sleep(2)
              #setServoPulse(servo_echo, 4)
              #time.sleep(2)
              #setServoPulse(servo_echo, 8)

              pwm.setPWMFreq(50)
              #pwm.setPWM(4, 0, servomax)
              text.insert("end", "ultrasonic servo")
            elif event.char == "2":
              self.striker_last = self.striker_last + 20
              turn_striker(self.striker_last)
              text.insert('end',"turning striker")
            elif event.char == "3":
              self.striker_last = self.striker_last - 20    
              turn_striker(self.striker_last)
              text.insert('end',"turning striker")
            elif event.char == "9":
              hide_striker(self.striker_updown)
              self.striker_updown = 1 - self.striker_updown
              text.insert('end',"striker up down " )
              

    def key_release(self, event):
        self.afterId = self.after_idle( self.process_release, event )

    def process_release(self, event):
        ServoStop(servoLeft)
        ServoStop(servoRight)
        #ServoStop(servoLift)
        #ServoStop(servoGrip)
        print 'key release %s' % event.char
        self.afterId = None



# Program
pwm.setPWMFreq(60)                        # Set frequency to 60 Hz


root = tk.Tk()
root.geometry('800x600')
root.attributes('-fullscreen', False)
text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 12))
text.pack()
text.insert('end', 'STEM TRI-Fecta 2017')
app1 = MyFrame(root)
root.mainloop()

print("done")

