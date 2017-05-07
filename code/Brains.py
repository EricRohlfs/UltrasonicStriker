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

    :param float ball_finding_turn_size:
        Do you want to make big turns or small turns when
        looking for the ball?  Bigger numbers do bigger turns,
        smaller numbers create smaller turns.

        Technically this just sets the time to sleep between the 
        turning and stoping the turn.

    :param float is_wall_sensitivity:
        Could be the width of the ball or a much greater distance,
        helps adjust for answering the question is wall?
    """

    def __init__(self, 
                ball_sensor, #this could be ultrasonic or TOF
                wall_sensor, 
                wheels, 
                striker,
                strike_zone_center = 87,
                strike_zone_tolerance = 0,
                ball_finding_turn_size = 0.04,
                is_wall_sensitivity = 10,
                sensor_to_striker_distance = 0 ):
        self.ball_sensor = ball_sensor
        self.wall_sensor = wall_sensor
        self.wheels = wheels
        self.striker = striker
        self.strike_zone_center = strike_zone_center
        self.strike_zone_tolerance = strike_zone_tolerance
        self.ball_finding_turn_size = ball_finding_turn_size
        self._keep_finding_the_ball = True
        self.is_wall_sensitivity = is_wall_sensitivity
        self.sensor_to_striker_distance = sensor_to_striker_distance
        self.search_ticks = 8
        self.find_ball_first_time = True

    def find_ball(self):
        if self.striker is not None:
            self.striker.hide_striker()
            time.sleep(.2)
        if self.find_ball_first_time:    
            self.find_ball_left()
            self.find_ball_first_time = False
            
        l_success = self.find_ball_left()
        print(l_success)
        if l_success is not None:
            r_success = self.find_ball_right()
            print(r_success)
        #if l_success:
        #    self.drive_to_strike_zone()
            #center up
            #self.wheels.turn_left()
            #time.sleep(self.ball_finding_turn_size)
            #self.wheels.stop()
        #if r_success:
        #    self.drive_to_strike_zone()
            #center up
            #self.wheels.turn_left()
            #time.sleep(self.ball_finding_turn_size)
            #self.wheels.stop()
        
    def find_ball_left_and_drive_to_ball(self):
        """
        Looks for the ball by turning left and then drives to
        the ball and stops.
        """
        self.find_ball_left()
        self.drive_to_strike_zone()
        #center up
        self.wheels.turn_left()
        time.sleep(self.ball_finding_turn_size)
        self.wheels.stop()
        

    def find_ball_right_and_drive_to_ball(self):
        """
        Looks for the ball by turning right and then drives to
        the ball and stops.
        """
        self.find_ball_right()
        self.drive_to_strike_zone()

    def find_ball_left(self):
        """
        Looks for the ball by turning the robot left.
        """
        self.is_wall() #calling now for warm up
        if self.striker is not None:
            self.striker.hide_striker()
            time.sleep(.2)
            
        self._keep_finding_the_ball = True
        i = 1
        while self.is_wall():
            if i > self.search_ticks:
                break
            self.wheels.turn_left()
            time.sleep(self.ball_finding_turn_size)
            self.wheels.stop()
            time.sleep(0.2)
            i = i + 1
            print(i)
        
        if i < self.search_ticks:
            return True
        else:
            return False
        
    def find_center(self,last = 0):
        print("finding center")
        if last is 0:
            #set last for first call in the loop
            last = self.ball_sensor.distance()

        if self.is_wall() is False:
            self.wheels.turn_left()
            time.sleep(self.ball_finding_turn_size)
            self.wheels.stop()
            time.sleep(.15) #let robot stop shaking around
            current = self.ball_sensor.distance()
            if current < last :
                print(current)
                print(last)
                self.find_center(last=current)
            else:
                #back up one
                self.wheels.turn_right()
                time.sleep(self.ball_finding_turn_size)
                self.wheels.stop()
                 
    def find_ball_right(self):
        """
        Looks for the ball by turning the robot right.
        """
        if self.striker is not None:
            self.striker.hide_striker()
            time.sleep(.1)
            
        self._keep_finding_the_ball = True
        i = 0
        while self.keep_finding_the_ball and self.is_wall() :
            if i > self.search_ticks * 2:
                break
            self.wheels.turn_right()
            time.sleep(self.ball_finding_turn_size)
            self.wheels.stop()
            time.sleep(0.2)
            i = i + 1
            print(i)
        if i < self.search_ticks * 2:
            return True
        else:
            return False    
         
    def stop_finding_the_ball(self):
        """
        Manual override to stop searching for the ball.
        Helpful if you need to change from searching left
        to searching right.
        """
        self.keep_finding_the_ball = False

    def is_wall(self):
        """
        Tries to answer the question isWall.
        If both sensors do not report the same distance
        chances are we see a ball
        """
        ball_distance = self.ball_sensor.distance()
        time.sleep(.05)
        wall_distance = self.wall_sensor.distance()
        #print("ball distance %f" % ball_distance)
        delta = abs(wall_distance - ball_distance)
        if delta <= self.is_wall_sensitivity :
            #print("is wall with delta " , delta)
            return True
        else:
            #print("is not wall with delta ", delta)
            return False

    def is_ball_in_strike_zone(self, ball_distance):
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
            print("drive to strike zone is_wall True, doing nothing")
            return
        if self.striker is not None:
            self.striker.hide_striker()
            time.sleep(.1)
            
        ball_distance = self.ball_sensor.distance()
        print(ball_distance)

        if self.is_ball_in_strike_zone(ball_distance):
            print("DriveToStrikeZone ball is in strike zone")
            return # nothing to do if we are in the zone

        how_far_to_go = abs(ball_distance - self.strike_zone_center)
        drive_duration = self.calculate_driving_time(how_far_to_go) * .7

        if ball_distance > self.strike_zone_center :
            print("foward" , drive_duration)
            self.wheels.foward()
            time.sleep(drive_duration)
            self.wheels.stop()
            #self.drive_to_strike_zone()

        elif ball_distance < self.strike_zone_center :
             print("backward")
             #self.wheels.backward()
             #time.sleep(drive_duration)
             #self.wheels.stop()

    def calculate_driving_time(self, distance_to_go):
       """
       how long the robot should go forward or backward till 
       the ball is in the strike zone
       """
       rpm = 50 #parallax continuous rotation servo can do 50 revolutions per minute
       wheel_diameter = 69.85 #mm or the vex wheels we are using are 2.75 inch wheels 6.985 is the cm conversion
       circumference = wheel_diameter * 3.14
       revolutions_needed = (distance_to_go + self.sensor_to_striker_distance) / circumference 
       time_for_one_rotation = 60/rpm # in seconds
       result = round(revolutions_needed * time_for_one_rotation, 4)
       
       #todo: might need to shave little bit to account for processing time.
       return result 

    @property
    def keep_finding_the_ball(self):
        return self._keep_finding_the_ball
    @keep_finding_the_ball.setter
    def keep_finding_the_ball(self,value):
        self._keep_finding_the_ball = value
