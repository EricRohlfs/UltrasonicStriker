//https://github.com/EricRohlfs/UltrasonicStriker
//numbers are in mm

// Part 2 of 2 for SG90 servo powered competition foosball gripper

coatHangerDiameterActual =2;
screwHoleSize = 5.5;
//main block
base_h = 9.15; //height
x=18;
y=40;
z= 4;

hornCenterX = (x/2) - (screwHoleSize/2)- (coatHangerDiameterActual/2);
coatLongX = x-3;
horn_spacing = 5;
front_horn_y = -10;
horn_left_x = 4;
horn_right_x = hornCenterX -2;
back_horn_y = 5;
$fn=50;

module ZipTieHole (){
    zipTieWidth = 1.5; // adjust if zip ties don't fit
    zipTieDepth = 2.7; //adjust if zip ties groves need to be deeper
    cube([zipTieWidth, zipTieDepth, base_h +.1],center=true);
 }

difference (){
    cube([x,y,z]);
   
    //servohorn set screw and horn zip tie holes
    translate([hornCenterX +screwHoleSize/2 ,17,-.1]){
        cylinder(d=screwHoleSize, h= z+.5);
        
        // back left horn zip tie holes
        translate([horn_left_x, back_horn_y, -.1]) {
            ZipTieHole();
            translate([0,horn_spacing,0]) ZipTieHole();
        } 
        //front right horn
        translate([horn_right_x, front_horn_y, -.1]) {
            ZipTieHole();
            translate([0,horn_spacing,0]) ZipTieHole();
        }
        //front left horn
        translate([-horn_left_x,front_horn_y, -.1]) {
            ZipTieHole();
            translate([0,horn_spacing,0]) ZipTieHole();
        }
         //back right horn
        translate([-horn_left_x,back_horn_y, -.1]) {
            ZipTieHole();
            translate([0,horn_spacing,0]) ZipTieHole();
        }
    }
    
    count = 4;
    //coat hanger side
    for (i=[0:count]){
        yy = 3 + (y/count) * i;
        translate([coatLongX,yy,-.1]) ZipTieHole();
        } 
        
    //back two zip tie hols for bent coat hanger   
    for (i=[0:1]){
        yy = (7  * i);
        rotate([0,0,90])translate([y-2, yy-10,-.1]) ZipTieHole();
    }  
}
   