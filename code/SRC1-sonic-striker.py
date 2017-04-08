#!/usr/bin/python
#Working SRC 2017 Code for 4 Servo Control
#2 Drive wheels, 1 Gripper and 1 Arm
#Revised 11.29.16 - Kevin Pace
#Refactored / 2016-4-7 Eric Rohlfs

# http://belikeotherpeople.co.uk/elevatedtopography/?p=138
import sys
import threading
from Adafruit_PWM_Servo_Driver import PWM
from sonic_striker_steppers import Motor
import time
from DistanceSensor import DistanceSensor
from ServoWheels import ServoWheels, ServoBasics
from striker import StrikerCommands
from Grabber import Grabber

try: #try to import the gpio libraries (need to download) and throw an exception if there is an error
        import RPi.GPIO as gpio
except Exception:
        print "error importing the gpio library which is probably because you need to run this program with sudo"


# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
try:
        pwm = PWM(0x41)
except:
        pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

pwm.setPWMFreq(60) # Set frequency to 60 Hz

"""
  pwm is the ServoHat
  pwm pins should be assigned in one place.
  This helps keep things organized
"""

#pwm pin assignment
left_wheel_pin = 0
right_wheel_pin = 1
servoLift = 2
show_hide_striker_pin = 4
grip_left_pin = 6
grip_right_pin = 7


"""
  GPIO pins are assigned here to keep them organized
  GPIO numbers are unusal,
    they have different numbers for each pin depending on the mode.
    if you are having issues google "raspberry pi and GPIO"
"""
#GPIO pin assignment
gpio.setmode(gpio.BOARD)

#GPIO Striker Actuator
striker_pin = 15 #gpio22
striker_reverse_pin = 16 #gpio23

# four gpio pins are needed for the striker steper
# Note: not all robots have a rotating striker head.
striker_stepper_IN1 = 32 #gpio12
striker_stepper_IN2 = 33 #gpio13
striker_stepper_IN3 = 36 #gpio16
striker_stepper_IN4 = 35 #gpio19

# ULTRASONIC
#set GPIO Pins
ball_trigger_pin = 40 #gpio21
ball_echo_pin = 38 #gpio20


#wall_trigger = None
#wall_echo = None
#wall_sensor = DistanceSensor(gpio, wall_echo, wall_trigger)

# Stepper motor to turn the Ultrasonic Sensor
#  This may go away and instead we will just turn the whole robot.
#sonic_in1 = 7 #gipo4 Normal Robot
sonic_in1 = 22 #gipo25  James Robot since 4 is broken on his pi
sonic_in2 = 11 #gpio17
sonic_in3 = 12 #gpio18
sonic_in4 = 13 #gpio27

# ULTRASONIC STEPPER
sonic_motor = Motor([sonic_in1,
                     sonic_in2,
                     sonic_in3,
                     sonic_in4])

#construct a ball sensor to find the ball using a Distance Sensor
ball_sensor = DistanceSensor(gpio, ball_echo_pin, ball_trigger_pin, sonic_motor)

# The wheels that make the robot go forward and backward
wheels = ServoWheels(pwm,left_wheel_pin, right_wheel_pin)

# access to the raw servo commands
# mainly used to stop motors on key_up
servo = ServoBasics(pwm)


"""
Using an universal power door actuator and an L298N H-Bridge
the code will move the actuator forward, wait, then retract
"""
# STRIKER
wedge_motor = Motor([striker_stepper_IN1,
                     striker_stepper_IN2,
                     striker_stepper_IN3,
                     striker_stepper_IN4])

striker = StrikerCommands(gpio,
                          striker_pin,
                          striker_reverse_pin,
                          pwm,
                          wedge_motor,
                          show_hide_striker_pin)

grabber = Grabber(pwm,
                  grip_left_pin,
                  grip_right_pin,
                  servo_min = 200,
                  servo_max=300)

        
# Keyboard stuff

import Tkinter as tk

class MyFrame(tk.Frame):
    _sonic_last = 0 # could break wires if we do a full turn

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

            #Shutdown robot safetly when the escape key is pressed.    
            if event.char == "K" or event.keysym == 'Escape':
              text.insert('end', ' Quit ')  
              #put motors back to original position
              #so we don't have to spend so much time calibrating
              ball_sensor.turn_to_zero()
              striker.turn_wedge_zero() #home or center
              root.destroy()

            #Wheels
            elif event.char == "w" or event.keysym == 'Up':
              text.insert('end', ' FORWARD ')
              wheels.foward() 
            elif event.char == "s" or event.keysym == 'Right':
              text.insert('end', ' RIGHT_TURN ')
              wheels.turn_right()
            elif event.char == "z" or event.keysym == 'Down':
              text.insert('end', ' BACKWARD ')
              wheels.backward()
            elif event.char == "a" or event.keysym == 'Left':
              text.insert('end', ' LEFT_TURN ')
              wheels.turn_left() 
              
            #Servo Striker
            elif event.char =="1":
              ds = "%f cm " % ball_sensor.distance()
              text.insert('end',"Distance: " + ds)
            elif event.char == "2":
              # self.sonic_last = self.sonic_last - 10
              # turn_sonic(self.sonic_last)
              ball_sensor.turn(-10)
              #text.insert('end'," " + str(self.sonic_last) + " ")
            elif event.char == "3":
              # self.sonic_last = self.sonic_last + 10
              # turn_sonic(self.sonic_last)
              ball_sensor.turn(10)
              #text.insert('end'," " + str(self.sonic_last) + " ")    
            elif event.char in ["5"]:
              striker.hide_striker()
              text.insert('end',"striker up down ")
            elif event.char == "6":
              #change the number for bigger or smaller turns  
              striker.turn_wedge(10)
              text.insert('end',"turning striker")
            elif event.char == "7":
              #change the number for bigger or smaller turns  
              striker.turn_wedge(-10)
              text.insert('end',"turning striker")
            elif event.char == "9":
              grabber.grab_release()
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



# Program

root = tk.Tk()
root.geometry('800x600')
root.attributes('-fullscreen', False)
text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 12))
text.pack()
text.insert('end', 'Ultrasonic Striker for STEM Robotics')
app1 = MyFrame(root)
root.mainloop()

print("done")

