//https://github.com/EricRohlfs/UltrasonicStriker
//numbers are in mm

// Part 1 of 2 for SG90 servo powered foosball gripper
// A coat hanger is bent into two different arms
// and attached via zip ties
$fn=50;
servoHornLength = 34; //adjust if you have different horn size

hornStrapWidth = 1.5; // adjust if zip ties don't fit
hornStrapDepth = 2.7; //adjust if zip ties groves need to be deeper

//Tweak these numbers if necessary, the largest positive number is closest to coat hanger hole
servoHornZipTieChannelPlacement= [-9, -3.5, 2.75, 6.25];

coatHangerDiameterActual =2;
coatHangerDiameter = coatHangerDiameterActual +.25;
coatHangerChannel = coatHangerDiameter;
coatHangerHole = coatHangerChannel +.65;

sg90Margin = .1; //cause the hole needs to be a tad bigger than the object
sg90StickerAdjustment = .2;//stickers were getting ripped off because it was too tight
sg90Width = 12.3 + sg90Margin + sg90StickerAdjustment;
sg90Depth = 22.8 + sg90Margin;
sg90Height = 26.5; //must be greater that base_h

sg90CavityBack = -sg90Width/2; //back edge reference point for the arm and zip ties
sg90CavityBackZip = sg90CavityBack - hornStrapWidth;

//main block
base_h = 9.15;  //height
base_w = sg90Width + 10; // width
base_d = sg90Depth + 14; //46 is original; //depth

//was 7 - hornStrap, not sure why I couldn't get exact width, so just added the last number
armMountWidth = base_w/2 - sg90Width/2 - hornStrapWidth +2.75;
armMountHeight = 20;
armMountY = base_d/2 + 6;
armMountTY = -armMountY -1.5;
armTransX = sg90CavityBack -.9;

//servo horn set screw
setScrewHoleRadius = 2;//make this bigger if yor screwdrive does not fit

//The big hole in the midddle of the piece
servoCavityCenterOffset = 7;
servoCavityX = (base_w - sg90Width - servoCavityCenterOffset);
servoCavityY = 0;

module main_body(){
   cube([base_w,base_d,base_h],center=true);
    }
    
module SG90ServoCavity(){
    //place to mount sg90 servo
    translate([servoCavityX,servoCavityY,0]) cube([sg90Width,sg90Depth,sg90Height],true);
    }
    
 //decided not to go this route, but if someone wants to implement, here is a start
 module SG90ServoMountingHole(){
     sg90screwHoleOffest = 1;
     sg90screwHoleRadius = .5;
     sg90ScrewTabDepth = 4.45;
     translate([base_w/2 - sg90Width /2,sg90Depth/2 + sg90screwHoleOffest,0]) cylinder(h= base_h + 1 ,r= sg90screwHoleRadius,center=true);
    }
    
module servo_horn_screw_access(){
    //hole for servo horn screw so you can quickly swap out broken servo on competition day
    setScrewHoleHeight = base_w * 1.5;
    rotate([0,90,0]) translate([0,0,-(base_w/1.99)]) cylinder(h= setScrewHoleHeight,r= setScrewHoleRadius);
}    
   
module ServoHornZipTieChanels(){
     for(i=servoHornZipTieChannelPlacement){
         spacing = i * 1.4 ;
         translate([-(base_w * .35), -(spacing),0]) cube([hornStrapWidth, hornStrapDepth, base_h +.1],center=true);
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
        y = armMountY/numberOfHoles * i;
        z = armMountHeight/2 - coatHangerDiameter -holeDistanceFromTop;
        translate([0,y,z]) ArmZipTieHole();
    }
}    
 module ArmMount(){
    translate([armTransX,armMountTY,6]){
        difference(){
            $fn=50;
            cube([armMountWidth , armMountY, armMountHeight +1],true);
            //flanges at the top so zip ties don't have a hard angle
            //todo:make dynamic
            flangex = 2;
            flangey = 0;
            flangez = armMountHeight/2 +1.75;
           translate([-flangex,flangey,flangez])rotate([0,45,0]) cube([2, armMountY +1 , 5],true);
            translate([flangex,flangey,flangez])rotate([0,-45,0]) cube([2, armMountY +1 , 5],true);
            
            //top groove for the coat hanger
            coatHangerBottomOffset = 2.5;
            rotate([90,0,0]) translate([0,armMountHeight/2 ,- base_w  -10]) cylinder(h= base_d *2,d= coatHangerChannel);
            
        //back coat hanger groove
        translate([0,-armMountTY/2,0])cylinder(h=22, d=coatHangerChannel, center=true);
            
         //back groove inside bendy angle
         translate([0,-armMountTY/2,7])rotate([-45,0,0])cube([coatHangerChannel,10,coatHangerChannel +3], center=true);
        
       translate([0,-armMountTY/2 ,8.5])rotate([-15,0,0])cube([coatHangerChannel,20,coatHangerChannel +3], center=true);
             ArmZipTieHoles();
       }
     }
}

module CoatHangerHole(){
     translate([armTransX,armMountTY/2,2]) cylinder(h=base_h, d=coatHangerHole,center=true);
    }
       
module ServoCableHole(){
    //tod: make hole for cable
    sg90CableHoleWidth = 3.75 + .6;//last number makes hole a bit wider than the cable
    sg90CableHoleDepth = 4.75;//seems like enough room, but can be changed
    translate([ servoCavityX , -.1 + sg90Depth/2 + sg90CableHoleDepth/2 ,0])
    cube([sg90CableHoleWidth, sg90CableHoleDepth,base_h + 1],true);
    }

//a bit diferent than the horn zip tie hole
//if the servo moves around a zip tie can be used to secure the 
//servo instead of screwing the sero to the piece.
 module ServoZipTieHole (){
      //translate([-5 , 13,0])
     translate([ servoCavityX - servoCavityCenterOffset -.75 , 1.7 + sg90Depth/2  ,0])
     cube([hornStrapWidth, hornStrapDepth, base_h +.5],center=true);
     }
     
module RemoveExtraPlastic(){
    sg90MountingTab = 5;
    sg90CableHoleWidth = sg90Width + servoCavityCenterOffset/2;
    sg90CableHoleDepth = 4.75;//seems like enough room, but can be changed
    translate([servoCavityX + .9, -base_d/2, 0])
    cube([sg90CableHoleWidth, sg90CableHoleDepth,base_h + 1],true);
    
    }
module ZipTieHole (){
  rotate([0,0,0]) cube([hornStrapWidth, hornStrapDepth, base_h +.1],center=true);
 }
 
 
x=27;
y=55;
z= 4;
difference (){
    //main_body();
    //servo_horn_screw_access();
    //SG90ServoCavity();
    //ServoZipTieHole();
    //SG90ServoMountingHole();
    //mirror([0,-base_d,0]) SG90ServoMountingHole();
    //ServoHornZipTieChanels();
    //ServoHornNotch();
    //ServoCableHole();
    //CoatHangerHole();//todo: tie this in with arm module
    //RemoveExtraPlastic();
  
    
    cube([x,y,z]);
    translate([x/2,y/2,-.1])cylinder(d=4, h= z+.5);
    count = 4;
    //coat hanger side
    for (i=[0:count]){
        yy = 4 + (y/count) * i;
        translate([x-4,yy,-.1]) ZipTieHole();
        } 
    //back two    
    count2 = 1;
    for (i=[0:count2]){
            yy = (10  * i);
            rotate([0,0,90])translate([x*2-3,yy-16,-.1]) ZipTieHole();
            }  
     //servo horn set screw
    rotate([90,0,0]) translate([x/2,y/2,-.1])cylinder(d=4, h= z+.5);
     //sero horn zip tie 
     for (i=[0:1]){
            yy = (11  * i);
            translate([9,(7.5 + yy) ,-.1]) ZipTieHole();
            translate([18.5,(7.5 + yy) ,-.1]) ZipTieHole();
            
            //visual aids
            //todo: could add visual aids so can clearly show cross sections
            }  
     for (i=[0:1]){
            yy = (11  * i);
            translate([9,(y/2+7.5 + yy) ,-.1]) ZipTieHole();
            translate([18.5,(y/2 +7.5 + yy) ,-.1]) ZipTieHole();
            } 
}
   