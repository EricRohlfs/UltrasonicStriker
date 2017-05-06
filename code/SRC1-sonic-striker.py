#If your robot does not have a feature set it to false
has_ball_sensor = True
has_wall_sensor = True
has_wheels = True
has_grabber = True
has_striker = True
has_tank_turret = False

#!/usr/bin/python
#Revised 11.29.16 - Kevin Pace
#Rewritten 2016-4-7 Eric Rohlfs

# http://belikeotherpeople.co.uk/elevatedtopography/?p=138
import sys
import threading
from Adafruit_PWM_Servo_Driver import PWM
from StepperMotors import Motor
import time
from DistanceSensor import DistanceSensor
from ServoWheels import ServoWheels, ServoBasics
from striker import StrikerCommands
from Grabber import Grabber, ServoSettings
from Brains import Brains
from ST_VL6180x_scale3 import VL6180X_3 as VL6180X

try: #try to import the gpio libraries (need to download) and throw an exception if there is an error
        import RPi.GPIO as gpio
except Exception:
        print("error importing the gpio library which is probably because you need to run this program with sudo")


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

servo_hat.setPWMFreq(50) # Set frequency to 50 HZ normally 60 but using so many smaller servos.

"""
  pwm is the ServoHat
  pwm pins should be assigned in one place.
  This helps keep things organized
"""

#servo_hat pin assignment
left_wheel_pin = 0
right_wheel_pin = 1
servoLift = 2
turret_pin = 3
show_hide_striker_pin = 4
gripper_1_pin = 8
gripper_1_lifter_pin = 9


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

# Four gpio pins are needed for the striker stepper
# Note: not all robots have a rotating striker head.
striker_stepper_IN1 = 29 #or gpio5
striker_stepper_IN2 = 31 #or gpio6
striker_stepper_IN3 = 32 #or gpio12
striker_stepper_IN4 = 33 # or gpio13

# ULTRASONIC
#set GPIO Pins
ball_sensor_trigger_pin = 40 #or gpio21
ball_sensor_echo_pin = 38 # or gpio20
wall_sensor_trigger_pin = 36 # or gpio 16
wall_sensor_echo_pin = 35 # or gpio 19

# Stepper motor to turn the Ultrasonic Sensor
#  This may go away and instead we will just turn the whole robot.
#sonic_in1 = 7 #gipo4 Normal Robot
sonic_in1 = 22 #gipo25  James Robot since 4 is broken on his pi
sonic_in2 = 11 #gpio17
sonic_in3 = 12 #gpio18
sonic_in4 = 13 #gpio27

# The wheels that make the robot go forward and backward
if has_wheels:
  wheels = ServoWheels(servo_hat,left_wheel_pin, right_wheel_pin, switch_foward_backward_commands = True)

#construct a ball sensor to find the ball using a Distance Sensor
if has_ball_sensor:
  #ball_sensor = DistanceSensor(gpio, ball_sensor_echo_pin, ball_sensor_trigger_pin, None)
  #ball_sensor = None
  tof_address = 0x29
  ball_sensor = VL6180X(address=tof_address, debug=False)
  if ball_sensor.idModel != 0xB4:
    print"Not a valid sensor id: %X" % ball_sensor.idModel

if has_wall_sensor:
  wall_sensor = DistanceSensor(gpio, wall_sensor_echo_pin, wall_sensor_trigger_pin, None)

if has_striker:
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
                          rotate_min = 100,
                          rotate_max = 305)

if has_grabber:
  lift = ServoSettings(gripper_1_lifter_pin,440,475)
  
  grabber = Grabber(servo_hat,
                  gripper_1_pin,
                  None,
                  lifter= lift,
                  servo_min = 130,
                  servo_max=200
                  )

if has_ball_sensor and has_wall_sensor and has_wheels and has_striker:
   brains = Brains(ball_sensor, wall_sensor, wheels, striker)
   brains.is_wall_sensitivity = 25



if has_tank_turret:
   turret = ServoBasics(servo_hat)     

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

    #keys in use w,s,k,z,a,u,d,c,o,t,g,n,1,2,3,4,5,6,7,8,9,0,r,p
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
              #ball_sensor.turn_to_zero()
              striker.turn_wedge_zero() #home or center
              gpio.cleanup()  
              root.destroy()
              
             
            #Wheels
            #if you need to switch foward and backward, set in constructor
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
              
            #Brains
            elif event.char =="1":                  
              brains.find_ball_left()
              text.insert('end',"find ball left")
              
            elif event.char == "2":
              brains.find_ball_right()
              text.insert('end',"find ball right")
              
            elif event.char == "p":
              ball_distance = "999"      
              # mainly for testing when the robot boots up
              try: 
                ball_distance = (": %d mm" % ball_sensor.distance() )
              except:
                text.insert('end'," failded")
                
              wall_distance = "%.0f mm " % wall_sensor.distance()
              text.insert('end'," ball wall: " + ball_distance + " " + wall_distance )

            elif event.char == "[":
              brains.find_ball()
              #brains.drive_to_strike_zone()
              #brains.is_ball_in_strike_zone()
              #calculate_driving_time
            elif event.char == "]":
              #brains.find_ball()
              brains.drive_to_strike_zone()
              #brains.is_ball_in_strike_zone()
              #calculate_driving_time  
            
            #grabber
            elif event.char in ["3"]:
              grabber.servo_1_open_or_close()
              text.insert('end',"grabber.servo1 ") 
            elif event.char in ["4"]:
              grabber.lift_up_or_down()
              text.insert('end',"grabber.lifter ") 

            #striker
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
              text.insert('end',' strike ')
              striker.strike()

            elif event.char == "0":
              text.insert('end',' striker up ')
              striker.strike(reverse=True)

            #Tank cannon style striker with continuous rotation servo
            # not recomended, but one team has this  
            elif event.char == "-":
              turret.servo_clockwise(turret_pin)      
            elif event.char == "=":
              turret.servo_counter_clockwise(turret_pin)       
              
            
    def key_release(self, event):
        self.afterId = self.after_idle( self.process_release, event )

    def process_release(self, event):
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
