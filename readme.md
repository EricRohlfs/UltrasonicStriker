Ultrasonic Striker for educational robot that has to strike a small ball to make it move.  Usually a ping-pong ball or a foosball.

The parts for this attachment are fairly cheap on ebay.

There is some fabrication needed to make the striker.

# Things to learn.

* Measuring distance with ultrasonic range finder
* Making stepper motors go left or right
* Making servo motors go left or right
* Making a linear actuator go forward and backward (universal car door unlock actuator)
* Convert electricity from 5v to 12v.
* Open and run a python program using IDLE

# Overall Wiring Diagram

![Wiring Diagram](https://github.com/ericrohlfs/ultrasonicstriker/raw/master/images/UltrasonicStriker.png "Wiring Diagram")

# Parts Explained

## The Striker

Price: $3.50

The striker is a common car door locker.  
![Universal Car Door Lock Actuator](https://github.com/ericrohlfs/ultrasonicstriker/raw/master/images/UniversalDoorLockActuator.jpg)

## The Striker Driver

Price: $2.00

LM298 board. 

![LM298](https://github.com/ericrohlfs/ultrasonicstriker/raw/master/images/LM298.jpg)

## Power Supply

Price: $10.00

Any 5 volt portable power bank.
![Power Bank](https://github.com/ericrohlfs/ultrasonicstriker/raw/master/images/5vPortablePowerBank.jpg)

## Power Converter

Price: $3.50

We need this to convert 5 volts to 12 volt.  We are using a buck type of converter.
See the very small brass screw, we need to use an Ohm meter and turn the screw to make sure we output 12v and not 35v.  35v will blow up our electronics.
![Buck Power Up](https://github.com/ericrohlfs/ultrasonicstriker/raw/master/images/xl6009-PowerConverter.jpg)


## Ultrasonic Sensor

Price: $2.00

Measures distance using sound

We need to create a voltage divider using two resistors to make this work.

![HC-SR04](https://github.com/ericrohlfs/ultrasonicstriker/raw/master/images/HC-SR04-Ultrasonic-Sensor.jpg)

## Stepper Motors

The stepper motors are more precise than servos and we use them to turn the striker head so the ball goes where we want it to go.

Currently we are using a second stepper to turn the ultrasonic range finder, but we may no need this, and instead will turn the whole robot.

Price: $3.00

The stepper motor is a 28BYJ-48. 

The motor driver is the unl2003.

![Motor and Driver](https://github.com/ericrohlfs/ultrasonicstriker/raw/master/images/unl2003-stepper-motor-driver.JPG)

## Servo Motors

Price: $10.00

This is NOT the continuous rotation servo used as the wheels of the robot.

![Standard Servo](https://github.com/ericrohlfs/ultrasonicstriker/raw/master/images/futaba-s3004-standard-servo_1.jpg)

## Servo Motor Driver 

Price: $20.00 or $3.00

Adafruit 16 Channel PWM Servo Hat

or if you are on a budget you can use the PCA9685 16 Channel 12-bit PWM 

(Please support Adafruit if you can, they have made STEM easy for all of us.)

![PWM Servo Hat](https://github.com/ericrohlfs/ultrasonicstriker/raw/master/images/adafruit-16-channel-pwm-servo-hat.png)

# Brains

Price: $29.00 - $39.00

Raspberry Pi

![Raspberry Pi](https://github.com/ericrohlfs/ultrasonicstriker/raw/master/images/raspberry-pi.jpg)

# Miscellaneous Supplies

* JB Weld
* Wooden Dowel - more info soon
* Jumper Wires - mostly female-to-female 
* Few resistors
* Soldering Iron and Solder
* Old USB cable you can destroy
