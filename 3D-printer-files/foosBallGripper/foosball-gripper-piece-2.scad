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
     

module ZipTieHole (){
  rotate([0,0,0]) cube([hornStrapWidth, hornStrapDepth, base_h +.1],center=true);
 }
 
 
x=18;
y=40;
z= 4;
difference (){
   
  
    
    cube([x,y,z]);
    screwHoleSize = 5.5;
    hornCenterX = (x/2) - (screwHoleSize/2)- (coatHangerDiameterActual/2) ;//-(9.75);//7.8
    //servohorn set screw
    translate([hornCenterX +screwHoleSize/2 ,17,-.1])cylinder(d=screwHoleSize, h= z+.5);
    count = 4;
    //coat hanger side
    coatLongX = x-3;
    for (i=[0:count]){
        yy = 3 + (y/count) * i;
        translate([coatLongX,yy,-.1]) ZipTieHole();
        } 
        
    //back two    
    for (i=[0:1]){
        yy = (7  * i);
        rotate([0,0,90])translate([y-2, yy-10,-.1]) ZipTieHole();
    }  


   //from left horn
    translate([coatLongX - 3, 6,-.1]) {
        ZipTieHole();
        translate([0,4,0]) ZipTieHole();
    }
    
    //back left horn
    translate([coatLongX - 3, 25,-.1]) {
        ZipTieHole();
        translate([0,5,0]) ZipTieHole();
    }
    
    //front right horn
    translate([hornCenterX -2 , 6,-.1]) {
        ZipTieHole();
        translate([0,5,0]) ZipTieHole();
    }
    //back right horn
    translate([hornCenterX -2, 25,-.1]) {
        ZipTieHole();
        translate([0,6,0]) ZipTieHole();
    }
}
   