#!/usr/bin/python
#Working SRC 2017 Code for 4 Servo Control
#2 Drive wheels, 1 Gripper and 1 Arm
#Revised 11.29.16 - Kevin Pace
#Refactored / 2016-4-7 Eric Rohlfs

# http://belikeotherpeople.co.uk/elevatedtopography/?p=138
import sys
import threading
from Adafruit_PWM_Servo_Driver import PWM
from StepperMotors import Motor
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
        servo_hat = PWM(0x41)
except:
        servo_hat = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#servo_hat = PWM(0x40, debug=True)

servo_hat.setPWMFreq(60) # Set frequency to 60 Hz

"""
  pwm is the ServoHat
  pwm pins should be assigned in one place.
  This helps keep things organized
"""

#servo_hat pin assignment
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
striker_stepper_IN1 = 29 #or gpio5
striker_stepper_IN2 = 31 #or gpio6
striker_stepper_IN3 = 32 #or gpio12
striker_stepper_IN4 = 33 # or gpio13

# ULTRASONIC
#set GPIO Pins
ball_finder_trigger_pin = 40 #or gpio21
ball_finder_echo_pin = 38 # or gpio20
wall_finder_trigger_pin = 36 # or gpio 16
wall_finder_echo_pin = 35 # or gpio 19

# Stepper motor to turn the Ultrasonic Sensor
#  This may go away and instead we will just turn the whole robot.
#sonic_in1 = 7 #gipo4 Normal Robot
sonic_in1 = 22 #gipo25  James Robot since 4 is broken on his pi
sonic_in2 = 11 #gpio17
sonic_in3 = 12 #gpio18
sonic_in4 = 13 #gpio27

#construct a ball sensor to find the ball using a Distance Sensor
ball_finder = DistanceSensor(gpio, ball_finder_echo_pin, ball_finder_trigger_pin, None)

wall_finder = DistanceSensor(gpio, wall_finder_echo_pin, wall_finder_trigger_pin, None)

# The wheels that make the robot go forward and backward
wheels = ServoWheels(servo_hat,left_wheel_pin, right_wheel_pin)

# access to the raw servo commands
# mainly used to stop motors on key_up
servo = ServoBasics(servo_hat)


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
                          servo_hat,
                          wedge_motor,
                          show_hide_striker_pin,
                          rotate_min = 150,
                          rotate_max = 360)

grabber = Grabber(servo_hat,
                  grip_left_pin,
                  grip_right_pin,
                  servo_min = 300,
                  servo_max=450)

        
# Keyboard stuff

import Tkinter as tk

class MyFrame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # method call counter
        self.pack()
        self.afterId = None
        root.bind('<KeyPress>', self.key_press)
        root.bind('<KeyRelease>', self.key_release)


    #keys in use w,s,k,z,a,u,d,c,o,t,g,n,1,2,3,4,5,6,7,8,9,0,r
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
              #ball_finder.turn_to_zero()
              striker.turn_wedge_zero() #home or center
              gpio.cleanup()  
              root.destroy()
              

            #Reverse Left Or Right Keys for the wheels
            elif event.char == "r":
              wheels.reverse_forward_back = True       
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
              #ball_distance = "%f cm " % ball_finder.distance()
              wall_distance = "%f cm " % wall_finder.distance()
              #text.insert('end'," ball wall: " + ball_distance + " " + wall_distance )
              text.insert('end'," ball wall: " + wall_distance + " "   )
            #elif event.char == "2":
              # self.sonic_last = self.sonic_last - 10
              # turn_sonic(self.sonic_last)
              #ball_finder.turn(-10)
              #text.insert('end'," " + str(self.sonic_last) + " ")
            #elif event.char == "3":
              # self.sonic_last = self.sonic_last + 10
              # turn_sonic(self.sonic_last)
              #ball_finder.turn(10)
              #text.insert('end'," " + str(self.sonic_last) + " ")    
            elif event.char in ["5"]:
              striker.show_hide_striker()
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
        #servo.servo_stop(left_wheel_pin)
        #servo.servo_stop(right_wheel_pin)
        #print 'key release %s' % event.char
        wheels.stop()
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

