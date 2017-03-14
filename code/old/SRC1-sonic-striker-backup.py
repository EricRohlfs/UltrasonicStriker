#!/usr/bin/python
#Working SRC 2017 Code for 4 Servo Control 
#2 Drive wheels, 1 Gripper and 1 Arm
#Revised 11.29.16 - Kevin Pace
 
import sys
import threading
from Adafruit_PWM_Servo_Driver import PWM
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
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096
servoZero = (servoMax-servoMin)/2 + servoMin

servoLeft = 0
servoRight = 1
servoLift = 2
#servoGrip = 3
servo_echo = 4


#gpio setup here
#outPin = 38
# this is for the auto bumbers, which we are not using
#inPin = 40 #assign the gpio pins to variables
#inPin2 = 38
#define inPin3 here below
""" inPin3 = """

gpio.setmode(gpio.BOARD)

#gpio.setup(outPin, gpio.OUT, initial=gpio.HIGH) #set the output pin to a permanent high, this will go directly into the input pin once the button is pressed
#gpio.setup(inPin, gpio.IN) #setup pin 21 as input
#gpio.setup(inPin2, gpio.IN)
#uncomment below to set the inPin3 to GPIO input
""" gpio.setup(inPin3, gpio.IN) """

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

"""  Here is the heart of the autonomous mode! """

#def autoMode():
#        print "got here"
#        while True:
#                ServoCounterClockwise(servoLeft)
#                ServoClockwise(servoRight)
#                print gpio.input(inPin), "  ", gpio.input(inPin2)
#                if gpio.input(inPin) == 1: #if the button is pressed, back off the wall and turn left
#                        print "break button pressed"
#                        break
#                elif gpio.input(inPin2) == 1: #where inPin2 should be the button on the left side of the robot
#                        turnRight() #function I defined above
                
                #uncomment below but make sure to define inPin3 as whichever GPIO pin you intend to have the right switch hooked up to
#                """ elif gpio.input(inPin3) == 1
#                        turnleft() """


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

#Ultrasonic Servo




# STRIKER 
"""
Using an universal power door actuator and an L298N H-Bridge
the code will move the actuator forward, wait, then retract
"""
#gpio.setup(13, gpio.OUT)
#gpio.setup(15, gpio.OUT)

#def strike():
       #forward
#       gpio.output(13, gpio.HIGH)
#       sleep(.05)
#       gpio.output(13, gpio.LOW)
       #pause
#       sleep(.4)
       #backward
#       gpio.output(15, gpio.HIGH)
#       sleep(.05)
#       gpio.output(15, gpio.LOW)


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

    #keys in use w,s,k,z,a,u,d,c,o,l,t,g,n
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
            #elif event.char == "l":
            #  text.insert('end', ' Stop Auto Mode ')
            #  autoMode() #refer to the defined function above
            # striker code
            #elif event.char == "t":
            #  text.insert('end',' strike ')
            #  strike()
            elif event.char =="g":
              #d = sonic_get_distance()
              ds = "%f cm " % sonic_get_distance()
              text.insert('end',"Distance: " + ds)
            elif event.char == "n":
              pulseU = 1
              setServoPulse(servo_echo, servoMin)      
              text.insert("servo", "ultrasonic servo")
             

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

