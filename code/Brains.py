import time

class Brains:
    """
    Brings all the sensors together to make decisions with the goal
    of creating a smarter robot.

    :param float strike_zone_center:
        Distance from the ultrasonic sensor to the center of the striker.
        The perfect place to stop to strike the ball.

    :param float strike_zone_tolerance:
        How close can we get to the center and still strike
        the ball.  We will never stop on the center exactly, so
        we need to know how close is good enough given the limitations
        of our robot.

    """

    def __init__(self, 
                ball_sensor, 
                wall_sensor, 
                wheels, 
                striker, 
                strike_zone_center = 5.5,
                strike_zone_tolerance = 0.75):
        self.ball_sensor = ball_sensor
        self.wall_sensor = wall_sensor
        self.wheels = wheels
        self.striker = striker
        self.strike_zone_center = strike_zone_center
        self.strike_zone_tolerance = strike_zone_tolerance

    def is_wall(self):
        """
        Tries to answer the question isWall.
        If both sensors do not report the same distance
        chances are we see a ball
        """
        ball_distance = self.ball_sensor.distance()
        wall_distance = self.wall_sensor.distance()
        delta = abs(wall_distance - ball_distance )
        if 0 <= delta <= 5 :
            return True
        else:
            return False

    def is_in_strike_zone(self, ball_distance):
        """
        The robot will never stop exactly on center, but we want to get
        as close as we can and still have a chance of striking the ball.

        The strike_zone_center should be the distance you need the center of 
        the ball to be for the striker to work.

        The strike_zone_tolerance is the + or - number that the striker will still 
        work, it might not work as well, but you may never hit the exact
        center.

        """
        lower_zone = self.strike_zone_center - self.strike_zone_tolerance
        upper_zone = self.strike_zone_center + self.strike_zone_tolerance
        if  lower_zone <= ball_distance <= upper_zone :
            return True
        else:
            return False

    def drive_to_strike_zone(self):
        #if we don't have a ball nothing to do here.
        if self.is_wall():
            return

        ball_distance = self.ball_sensor.distance() 

        if self.is_in_strike_zone(ball_distance):
            return # nothing to do if we are in the zone

        how_far_to_go = abs(ball_distance - self.strike_zone_center)
        drive_duration = self.get_drive_time(how_far_to_go)

        if ball_distance > self.strike_zone_center :
            print("foward")
            self.wheels.foward()
            time.sleep(drive_duration)
            self.wheels.stop()

        elif ball_distance < self.strike_zone_center :
             self.wheels.backward()
             time.sleep(drive_duration)
             self.wheels.stop()


    def get_drive_time(self, distance_to_go):
       """
       how long the robot should go forward or backward till 
       the ball is in the strike zone
       """
       rpm = 50 #parallax continuous rotation servo can do 50 revolutions per minute
       wheel_diameter = 6.985 #cm or the vex wheels we are using are 2.75 inch wheels 6.985 is the cm conversion
       circumference = wheel_diameter * 3.14
       revolutions_needed = distance_to_go / circumference 
       time_for_one_rotation = 60/50 # in seconds
       result = round(revolutions_needed * time_for_one_rotation, 4)
       #todo: might need to shave little bit to account for processing time.
       return result
