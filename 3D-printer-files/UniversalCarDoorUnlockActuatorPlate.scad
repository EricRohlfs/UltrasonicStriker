// a plate to help create a flat surface
// for mounting a universal car door lock linear actuator
// the big hole is for access to a servo set screw

//todo: bring in the tooth pattern for the futaba servo
// so we don't have to glue the servo horn to 
// the plate, we can just print the whole thing.
use <3rd-party/servo_arm.scad>

difference() {
    cube(size = [2, 4, 0.25], center = false);
    //servo set screw hole
    translate([1,1,-.5]) 
        cylinder(h=1, r=.25, center=false);
     
    //stuby thing on back of universal car door lock actuator
    translate([1,2.75,-0.5]) 
        cylinder(h=1, d=.25, center=false);    
    
    //stuby thing on back of universal car door lock actuator
    translate([1,3.5,-0.5]) 
        cylinder(h=1, d=.25, center=false);    
}