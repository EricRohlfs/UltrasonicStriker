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
from DistanceSensor import DistanceSensor 

try: #try to import the gpio libraries (need to download) and throw an exception if there is an error
        import RPi.GPIO as gpio
except RuntimeError:
        print "error importing the gpio library which is probably because you need to run this program with sudo"

gpio.cleanup()
gpio.setmode(gpio.BOARD)

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
grip_left = 6
grip_right = 7

#Striker actuator
striker_gpio1 = 15 #gpio22
striker_gpio2 = 16 #gpio23

# four gpio pins are needed for the striker steper
striker_stepper_IN1 = 32 #gpio12
striker_stepper_IN2 = 33 #gpio13
striker_stepper_IN3 = 36 #gpio16
striker_stepper_IN4 = 35 #gpio19

# ULTRASONIC
#set GPIO Pins
GPIO_TRIGGER = 40 #gpio21
GPIO_ECHO = 38 #gpio20
ball_sensor = DistanceSensor(gpio, GPIO_ECHO, GPIO_TRIGGER)
#wall_sensor =


sonic_in1 = 7 #gipo4
sonic_in2 = 11 #gpio17
sonic_in3 = 12 #gpio18
sonic_in4 = 13 #gpio27


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
       # print "right button pressed!"
        #back up
        ServoClockwise(servoLeft)
        ServoCounterClockwise(servoRight)
        time.sleep(1.2) #edit this
        #turn left
       # print "second part of left turn"
        ServoClockwise(servoLeft)
        ServoClockwise(servoRight)
        time.sleep(0.8) #edit this

def turnRight():
       # print "left button pressed"
        #back up
        ServoClockwise(servoLeft)
        ServoCounterClockwise(servoRight)
        time.sleep(1.2) #edit this
        #turn right
        ServoCounterClockwise(servoLeft)
        ServoCounterClockwise(servoRight)
        time.sleep(0.8) # edit this


# ULTRASONIC STEPPER


sonic_direction = Motor([sonic_in1,sonic_in2,sonic_in3,sonic_in4])
#sonic_direction.mode = 2
def turn_sonic(degrees):
        sonic_direction.rpm = 5
        mm = sonic_direction
        #print "Pause in seconds: " + `mm._T`
        #m.mode = 2
        mm.move_to(degrees)
        #GPIO.cleanup()

        


# STRIKER
"""
Using an universal power door actuator and an L298N H-Bridge
the code will move the actuator forward, wait, then retract
"""
gpio.setup(striker_gpio1, gpio.OUT)
gpio.setup(striker_gpio2, gpio.OUT)

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
#striker_direction.mode = 2

def turn_striker(degrees):
        striker_direction.rpm = 5
        m = striker_direction
        print "Pause in seconds: " + `m._T`
        #m.mode = 2
        m.move_to(degrees)

# STRIKER SERVO moves the striker out of the way of the sonic sensor

def hide_striker(up_down):
        if up_down == 1:
          pwm.setPWM(servo_echo, 0, 475)
        elif up_down == 0:
          pwm.setPWM(servo_echo,0,230)

# 0 = open, 1 = closed   
def grabber(open_closed):
        #close
        if open_closed == 1: 
                pwm.setPWM(grip_left,0,300)
                pwm.setPWM(grip_right,0,200)
        #open        
        if open_closed == 0:
                pwm.setPWM(grip_left,0,200)
                pwm.setPWM(grip_right,0,300)
        
# Keyboard stuff

import Tkinter as tk

class MyFrame(tk.Frame):
    _striker_last = 0
    _striker_updown = 0 #either 0 or 1
    _sonic_last = 0 # could break wires if we do a full turn
    _grabber_last = 0 

    @property
    def striker_last(self):
        return self._striker_last
    @striker_last.setter
    def striker_last(self,value):
        type(self)._striker_last = value
    
    @property
    def grabber_last(self):
        return self._grabber_last
    @grabber_last.setter
    def grabber_last(self,value):
        type(self)._grabber_last = value

    @property
    def sonic_last(self):
        return self._sonic_last
    @striker_last.setter
    def sonic_last(self,value):
        type(self)._sonic_last = value

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


    #keys in use w,s,k,z,a,u,d,c,o,t,g,n,1,2,3,4,5
    def key_press(self, event):
        if self.afterId != None:
            self.after_cancel( self.afterId )
            self.afterId = None
        else:
            #print 'key pressed %s' % event.char

            if event.char == "K" or event.keysym == 'Escape':
              text.insert('end', ' Quit ')
              pwm.setPWM(0, 0, servoZero)
              #put motors back to original position
              #so we don't have to spend so much time calibrating
              turn_sonic(0)
              turn_striker(0)
              hide_striker(1)
              root.destroy()

            elif event.char == "w" or event.keysym == 'Up':
              text.insert('end', ' FORWARD ')
              ServoCounterClockwise(servoLeft)
              ServoClockwise(servoRight)
            elif event.char == "s" or event.keysym == 'Right':
              text.insert('end', ' RIGHT_TURN ')
              ServoCounterClockwise(servoLeft)
              ServoCounterClockwise(servoRight)
            elif event.char == "z" or event.keysym == 'Down':
              text.insert('end', ' BACKWARD ')
              ServoClockwise(servoLeft)
              ServoCounterClockwise(servoRight)
            elif event.char == "a" or event.keysym == 'Left':
              text.insert('end', ' LEFT_TURN ')
              ServoClockwise(servoLeft)
              ServoClockwise(servoRight)
            #elif event.char == "u":
            #  text.insert('end', ' UP ')
            #  ServoClockwise(servoLift)
            #elif event.char == "d":
            #  text.insert('end', ' DOWN ')
            #  ServoCounterClockwise(servoLift)

            #servo striker
            elif event.char =="1":
              ds = "%f cm " % ball_sensor.distance()
              text.insert('end',"Distance: " + ds)
            elif event.char == "2":
              self.sonic_last = self.sonic_last - 10
              turn_sonic(self.sonic_last)
              text.insert('end'," " + str(self.sonic_last) + " ")
            elif event.char == "3":
              self.sonic_last = self.sonic_last + 10
              turn_sonic(self.sonic_last)
              text.insert('end'," " + str(self.sonic_last) + " ")    
            elif event.char in ["5"]:
              hide_striker(self.striker_updown)
              self.striker_updown = 1 - self.striker_updown
              text.insert('end',"striker up down ")
            elif event.char == "6":
              self.striker_last = self.striker_last + 10
              turn_striker(self.striker_last)
              text.insert('end',"turning striker")
            elif event.char == "7":
              self.striker_last = self.striker_last - 10
              turn_striker(self.striker_last)
              text.insert('end',"turning striker")
            elif event.char == "9":
                self.grabber_last = 1 - self.grabber_last
                grabber(self.grabber_last)
            elif event.char == "0":
              text.insert('end',' strike ')
              strike()
            

    def key_release(self, event):
        self.afterId = self.after_idle( self.process_release, event )

    def process_release(self, event):
        ServoStop(servoLeft)
        ServoStop(servoRight)
        #ServoStop(servoLift)
        #ServoStop(servoGrip)
        #print 'key release %s' % event.char
        self.afterId = None



# Program
pwm.setPWMFreq(60)                        # Set frequency to 60 Hz


root = tk.Tk()
root.geometry('800x600')
root.attributes('-fullscreen', False)
text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 12))
text.pack()
text.insert('end', 'Ultrasonic Striker for STEM Robotics')
app1 = MyFrame(root)
root.mainloop()

print("done")

