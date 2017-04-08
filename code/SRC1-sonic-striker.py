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
from ServoWheels import ServoWheels, ServoBasics
from striker import StrikerCommands

try: #try to import the gpio libraries (need to download) and throw an exception if there is an error
        import RPi.GPIO as gpio
except Exception:
        print "error importing the gpio library which is probably because you need to run this program with sudo"

gpio.cleanup()
gpio.setmode(gpio.BOARD)

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
try:
        pwm = PWM(0x40)
except:
        pwm = PWM(0x41)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

#these are pwm ports not gpio
left_wheel_pin = 0
right_wheel_pin = 1
servoLift = 2
#servoGrip = 3
show_hide_striker_pin = 4
grip_left = 6
grip_right = 7

#Striker actuator
striker_pin = 15 #gpio22
striker_reverse_pin = 16 #gpio23

# four gpio pins are needed for the striker steper
striker_stepper_IN1 = 32 #gpio12
striker_stepper_IN2 = 33 #gpio13
striker_stepper_IN3 = 36 #gpio16
striker_stepper_IN4 = 35 #gpio19

# ULTRASONIC
#set GPIO Pins
ball_trigger = 40 #gpio21
ball_echo = 38 #gpio20
ball_sensor = DistanceSensor(gpio, ball_echo, ball_trigger)

#wall_trigger = None
#wall_echo = None
#wall_sensor = DistanceSensor(gpio, wall_echo, wall_trigger)


sonic_in1 = 7 #gipo4
sonic_in2 = 11 #gpio17
sonic_in3 = 12 #gpio18
sonic_in4 = 13 #gpio27

wheels = ServoWheels(pwm,left_wheel_pin, right_wheel_pin)
servo = ServoBasics(pwm)

# ULTRASONIC STEPPER


sonic_direction = Motor([sonic_in1,sonic_in2,sonic_in3,sonic_in4])
#sonic_direction.mode = 2
def turn_sonic(degrees):
        sonic_direction.rpm = 5
        mm = sonic_direction
        mm.move_to(degrees)

# STRIKER
"""
Using an universal power door actuator and an L298N H-Bridge
the code will move the actuator forward, wait, then retract
"""
wedge_motor = Motor([striker_stepper_IN1,striker_stepper_IN2,striker_stepper_IN3,striker_stepper_IN4])

striker = StrikerCommands(gpio,
                          striker_pin,
                          striker_reverse_pin,
                          pwm,
                          wedge_motor,
                          show_hide_striker_pin
                          )



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
    _sonic_last = 0 # could break wires if we do a full turn
    _grabber_last = 0 

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
              
              #put motors back to original position
              #so we don't have to spend so much time calibrating
              turn_sonic(0)
              striker.turn_wedge_zero(0) #home or center
              root.destroy()

            elif event.char == "w" or event.keysym == 'Up':
              text.insert('end', ' FORWARD ')
              wheels.foward() 
              #ServoCounterClockwise(servoLeft)
              #ServoClockwise(servoRight)
            elif event.char == "s" or event.keysym == 'Right':
              text.insert('end', ' RIGHT_TURN ')
              wheels.turn_right()
              #ServoCounterClockwise(servoLeft)
              #ServoCounterClockwise(servoRight)
            elif event.char == "z" or event.keysym == 'Down':
              text.insert('end', ' BACKWARD ')
              wheels.backward()
              #ServoClockwise(servoLeft)
              #ServoCounterClockwise(servoRight)
            elif event.char == "a" or event.keysym == 'Left':
              text.insert('end', ' LEFT_TURN ')
              wheels.turn_left() 
              #ServoClockwise(servoLeft)
              #ServoClockwise(servoRight)
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
              striker.hide_striker(self.striker_updown)
              text.insert('end',"striker up down ")
            elif event.char == "6":
              striker.turn_wedge(10)
              text.insert('end',"turning striker")
            elif event.char == "7":
              striker.turn_wedge(-10)
              text.insert('end',"turning striker")
            elif event.char == "9":
              self.grabber_last = 1 - self.grabber_last
              grabber(self.grabber_last)
            elif event.char == "0":
              text.insert('end',' strike ')
              striker.strike()
            

    def key_release(self, event):
        self.afterId = self.after_idle( self.process_release, event )

    def process_release(self, event):
        servo.servo_stop(left_wheel_pin)
        servo.servo_stop(right_wheel_pin)
        #print 'key release %s' % event.char
        self.afterId = None
    
    @property
    def grabber_last(self):
        return self._grabber_last
    @grabber_last.setter
    def grabber_last(self,value):
        type(self)._grabber_last = value

    @property
    def sonic_last(self):
        return self._sonic_last


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

