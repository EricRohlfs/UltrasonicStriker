;//numbers are in mm

servoHornLength = 34; //adjust if you have different horn size

hornStrapWidth = 1.2; // adjust if zip ties don't fit
hornStrapDepth = 2.3; //adjust if zip ties groves need to be deeper

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

armMountWidth = 7;
armMountHeight = 20;

//main block
base_h = 9.15;  //height
base_w = sg90Width + 10; // width
base_d = 46; //depth
main_bottom = base_h*1.5;

//servo horn set screw
setScrewHoleHeight = 150;
setScrewHoleRadius = 1.5;

servoCavityX = (base_w - sg90Width - 7);
servoCavityY = 0;

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
     for(i=[-7.5, -2.5, 2.5, 7.5]){
         spacing = i * 1.4 ;
         translate([-(base_w * .15), -(spacing),0]) cube([hornStrapWidth, hornStrapDepth, base_h +.1],center=true);
    
    }
 }
 
 module ServoHornNotch(){
        translate([-(base_w/2),0,0]) cube([1.75,servoHornLength,base_h +.1],true);
     }
     
 module ArmMount(){{
        translate([sg90CavityBackZip,-24,6]){
            
            difference(){
                $fn=50;
                cube([armMountWidth - hornStrapWidth,
                      base_d/2,armMountHeight +1],true);
                
                //minkowski()
                //{
                  //cube([armMountWidth,base_d/2,armMountHeight],true);
                  //rotate([0,0,90])cylinder(r=4,h=4,true);
               // }
                
                coatHangerBottomOffset = 2.5;
                rotate([90,0,0]) translate([0,armMountHeight/2 ,- base_w  -10]) cylinder(h= base_d *2,d= coatHangerChannel);
            
                //translate([0,0,0]) cube([armMountWidth +.01,base_d *.1,armMountHeight +.01],true);
                //todo:math so at end of block
            translate([0,12,0])cylinder(h=22, d=coatHangerChannel, center=true);
           }}
       }
            
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
    translate([sg90CavityBackZip, -24/2,0]) cylinder(h=base_h +1, d=coatHangerHole,center=true);
}

ArmMount();
   