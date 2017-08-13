//https://github.com/EricRohlfs/UltrasonicStriker
//numbers are in mm

handleLength = 70;
numberOfZipTieHoles = 3;

// Part 1 of 2 for SG90 servo powered foosball gripper
// A coat hanger is bent into two different arms
// and attached via zip ties
$fn=50;
//servoHornLength = 34; //adjust if you have different horn size

//hornStrapWidth = 1.5; // adjust if zip ties don't fit
//hornStrapDepth = 2.7; //adjust if zip ties groves need to be deeper

//Tweak these numbers if necessary, the largest positive number is closest to coat hanger hole
//servoHornZipTieChannelPlacement= [-9, -3.5, 2.75, 6.25];

//coatHangerDiameterActual =2;
//coatHangerDiameter = coatHangerDiameterActual +.25;
//coatHangerChannel = coatHangerDiameter;
//coatHangerHole = coatHangerChannel +.65;

sg90Margin = .25; //cause the hole needs to be a tad bigger than the object
sg90StickerAdjustment = .2;//stickers were getting ripped off because it was too tight
sg90Width = 12.3 + sg90Margin + sg90StickerAdjustment;
sg90Depth = 22.8 + sg90Margin;
sg90Height = 26.5; //must be greater that base_h

sg90CavityBack = -sg90Width/2; //back edge reference point for the arm and zip ties
sg90CavityBackZip = sg90CavityBack - hornStrapWidth;
sg90Thick = 12.1;
sg90InsertReal = 15.4;
sg90InsertOffset = .35;
sg90Insert = sg90InsertReal+ sg90InsertOffset;

//main block
base_h = sg90Thick-.1;  //height
base_w = sg90Width + 11; // width
base_d = sg90Depth + handleLength; //adjust this for length

end_size = 8;
cav_x = 4; //cable cavity x
cav_y = 9; // cable cavity y

safe_zone = end_size + sg90Insert +cav_y *2;

zip_from_edge = 1.5;
zip_width= 3.2;
zip_depth= 1.5;

module main_body(){
   cube([base_w,base_d,base_h]);
    }
  
module cableCavity(){
    cable_offset =3.1;
    translate([sg90Insert -sg90InsertOffset - cav_x -cable_offset, sg90Depth -.1,0])cube([cav_x,cav_y,sg90Thick]);
    
    }
    
module SG90ServoCavity(){
    //place to mount sg90 servo
    translate([-.01,end_size,0]){ 
        cube([sg90Insert,sg90Depth,sg90Thick]);
        cableCavity();
        }
    } 
   
module ServoHornZipTieChanels(){
     for(i=servoHornZipTieChannelPlacement){
         spacing = i * 1.4 ;
         translate([-(base_w * .35), -(spacing),0]) cube([hornStrapWidth, hornStrapDepth, base_h +.1],center=true);
    }
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

 module ZipTieHole (){
      //translate([-5 , 13,0])
     //translate([ servoCavityX - servoCavityCenterOffset -.75 , 1.7 + sg90Depth/2  ,0])
     
     rotate([0,0,0])cube([zip_depth,zip_width, base_h +.5]);
     }
 
     
difference (){
    main_body();
    //servo_horn_screw_access();
    SG90ServoCavity();
    
    //end zip tie hole for securing servo
    translate([zip_from_edge,end_size - zip_width  -1.25,0])ZipTieHole();
    //servo zip tie hole other side
    translate([zip_from_edge,end_size + sg90Depth +1.25 ,0])ZipTieHole();
    //some holes to mount to the robot
    for(i=[1:numberOfZipTieHoles]){
        translate([zip_from_edge,base_d -7 * i ,0])ZipTieHole();
        translate([base_w - zip_from_edge*2, base_d -7 * i ,0])ZipTieHole();
    }
    
    
}

