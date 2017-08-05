//https://github.com/EricRohlfs/UltrasonicStriker
//numbers are in mm

// Part 1 of 2 for SG90 servo powered foosball gripper
// A coat hanger is bent into two different arms
// and attached via zip ties

servoHornLength = 34; //adjust if you have different horn size

hornStrapWidth = 1.25; // adjust if zip ties don't fit
hornStrapDepth = 2.3; //adjust if zip ties groves need to be deeper

//Tweak these numbers if necessary, 7 is closest to coat hanger hole
servoHornZipTieChannelPlacement= [-9, -3.5, 3.5, 7];

coatHangerDiameter = 2;
coatHangerChannel = coatHangerDiameter;
coatHangerHole = coatHangerChannel +.2;

sg90Margin = .1;
sg90StickerAdjustment = .2;
sg90Width = 12.3 + sg90Margin + sg90StickerAdjustment;
sg90Depth = 22.8 + sg90Margin;
sg90Height = 26.5; //must be greater that base_h

sg90ScrewTabDepth = 4.45;

sg90CavityBack = -sg90Width/2;
sg90CavityBackZip = sg90CavityBack - hornStrapWidth;

sg90screwHoleOffest = 1;
sg90screwHoleRadius = .5;

//main block
base_h = 9.15;  //height
base_w = sg90Width + 10; // width
base_d = 46; //depth
main_bottom = base_h*1.5;

//7 should be base_w - hornstrapWidth - back servo hole
armMountWidth = 7 - hornStrapWidth;
armMountHeight = 20;
armMountY1 = base_d/2; //switch Y and Y1 names are backward
armMountY = -24;

//servo horn set screw
setScrewHoleHeight = 150;
setScrewHoleRadius = 1.5;

servoCavityX = (base_w - sg90Width - 7);
servoCavityY = 0;

module miniround(size, radius)
{
    $fn=50;
    x = size[0]-radius/2;
    y = size[1]-radius/2;

    minkowski()
    {
        cube(size=[x,y,size[2]],center=true);
        cylinder(r=radius);
        // Using a sphere is possible, but will kill performance
        //sphere(r=radius);
    }
}

module main_body(){
   cube([base_w,base_d,base_h],center=true);
    }
    
module SG90ServoCavity(){
    //place to mount sg90 servo
    translate([servoCavityX,servoCavityY,0]) cube([sg90Width,sg90Depth,sg90Height],true);
    }
    
 module SG90ServoMountingHole(){
     translate([base_w/2 - sg90Width /2,sg90Depth/2 + sg90screwHoleOffest,0]) cylinder(h= base_h + 1 ,r= sg90screwHoleRadius,center=true);
    }
    
module servo_horn_screw_access(){
    //hole for servo horn screw so you can quickly swap out broken servo on competition day
    rotate([0,90,0]) translate([0,0,-(base_w/1.99)]) cylinder(h= setScrewHoleHeight,r= setScrewHoleRadius);
    }    
   
module ServoHornZipTieChanels(){
     for(i=servoHornZipTieChannelPlacement){
         spacing = i * 1.4 ;
         translate([-(base_w * .25), -(spacing),0]) cube([hornStrapWidth, hornStrapDepth, base_h +.1],center=true);
    }
 }
 
 module ServoHornNotch(){
        translate([-(base_w/2),0,0]) cube([1.75,servoHornLength,base_h +.1],true);
     }
     
 module ArmZipTieHole (){
      rotate([0,90,0]) cube([hornStrapWidth, hornStrapDepth, base_h +.1],center=true);
     }
     
 module ArmZipTieHoles(){
     numberOfHoles = 3;//must be the same as the array size of holes (sizeof(holes) did not work
     holeDistanceFromTop = 1.5;
     //-1 for one on the left, 0 for center, 1 for one on the right
     holes = [-1,0,1];
     for(i=holes){
        y = armMountY1/numberOfHoles * i;
        z = armMountHeight/2 - coatHangerDiameter -holeDistanceFromTop;
        translate([0,y,z]) ArmZipTieHole();
        //x1=x1 + 2;
    }
}    
 module ArmMount(){
    translate([sg90CavityBackZip,armMountY,6]){
        difference(){
            $fn=50;
            cube([armMountWidth -.1, armMountY1, armMountHeight +1],true);
            //flanges at the top 
            //todo:make dynamic
           translate([-2,0,11.75])rotate([0,45,0]) cube([2, armMountY1 +1 , 5],true);
            translate([2,0,11.75])rotate([0,-45,0]) cube([2, armMountY1 +1 , 5],true);
            //top coat hanger groove
            coatHangerBottomOffset = 2.5;
            rotate([90,0,0]) translate([0,armMountHeight/2 ,- base_w  -10]) cylinder(h= base_d *2,d= coatHangerChannel);
            
        //back coat hanger groove
        translate([0,-armMountY/2,0])cylinder(h=22, d=coatHangerChannel, center=true);
         //back groove inside bendy angle
          
         translate([0,-armMountY/2,7])rotate([-45,0,0])cube([coatHangerChannel,10,coatHangerChannel +3], center=true);
        
       translate([0,-armMountY/2 ,8.5])rotate([-15,0,0])cube([coatHangerChannel,20,coatHangerChannel +3], center=true);
             ArmZipTieHoles();
       }
     }
}

module CoatHangerHole(){
     translate([sg90CavityBackZip, armMountY/2,2]) cylinder(h=base_h, d=coatHangerHole,center=true);
    }
    

     
module ServoCableHole(){
    //tod: make hole for cable
    sg90CableHoleWidth = 3.75 + .5;
    sg90CableHoleDepth = 4.75;
    translate([ servoCavityX , -sg90StickerAdjustment + sg90Depth/2 + sg90CableHoleDepth/2 ,0])
    cube([sg90CableHoleWidth, sg90CableHoleDepth,base_h + 1],true);
    }


difference (){
    main_body();
    servo_horn_screw_access();
    SG90ServoCavity();
    //SG90ServoMountingHole();
    //mirror([0,-base_d,0]) SG90ServoMountingHole();
    ServoHornZipTieChanels();
    ServoHornNotch();
    ServoCableHole();
    CoatHangerHole();//todo: tie this in with arm module
    
}
ArmMount();
   



   