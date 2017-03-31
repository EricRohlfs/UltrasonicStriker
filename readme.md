Ultrasonic Striker for educational robot that has to strike a small ball to make it move.  Usually a ping-pong ball or a foosball.

The parts for this attachment are fairly cheap on ebay.

There is some fabrication needed to make the striker.

# Things to learn.

* Measuring distance with ultrasonic range finder
* Making stepper motors go left or right
* Making servo motors go left or right
* Making a linear actuator go forward and backward (universal car door unlock actuator)
* Convert electricity from 5v to 12v.
* Writing or organizing code using python

# Images

![Wiring Diagram](https://github.com/ericrohlfs/ultrasonicstriker/raw/master/images/UltrasonicStriker.png "Wiring Diagram")

# Parts Explained

## The Striker

The striker is a common car door locker.  
![Universal Car Door Lock Actuator](https://github.com/ericrohlfs/ultrasonicstriker/raw/master/images/UniversalDoorLockActuator.jpg)

## The Striker Driver

LM298 board from ebay for about $2.00

![LM298](https://github.com/ericrohlfs/ultrasonicstriker/raw/master/images/LM298.jpg)

## Power Supply

Any 5 volt portable power bank.
![Power Bank](https://github.com/ericrohlfs/ultrasonicstriker/raw/master/images/5vPortablePowerBank.jpg)

## Power Converter

We need this to convert 5 volts to 12 volt.  We are using a buck type of converter.
See the very small brass screw, we need to use an Ohm meter and turn the screw to make sure we output 12v and not 35v.  35v will blow up our electronics.
![Buck Power Up](https://github.com/ericrohlfs/ultrasonicstriker/raw/master/images/xl6009-PowerConverter.jpg)


## Ultrasonic Sensor

We need to create a voltage divider using two resistors to make this work.
![HC-SR04](https://github.com/ericrohlfs/ultrasonicstriker/raw/master/images/hc-sr04-ultrasonic-sensor.jpg)
