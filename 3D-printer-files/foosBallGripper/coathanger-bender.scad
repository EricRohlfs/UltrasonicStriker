
screwDriverDiameter = 4.5;
coatHangerDiameter = 2;
mainDiameter = 28; //end product should be 35 but it will spring out so give room
mainHeight = 10;
sddOff = 2; //screw driver diameter offset
tob = screwDriverDiameter + sddOff * 2; //top of base

//base for the user to hold on to.  Stick a screw driver in the hole to create some leverage
difference(){
    translate([0,0,0])
        cylinder(d=mainDiameter*2 , h=screwDriverDiameter + sddOff*2);
    
    translate([-mainDiameter*1.5,0,screwDriverDiameter/2+ sddOff])
        rotate([0,90,0])
            cylinder(d=screwDriverDiameter, h= mainDiameter*3);
}

//Coat hanger bender section
translate([0,0,tob]){
    difference(){
        union(){
            cylinder(d=mainDiameter, h= mainHeight);
            translate([0,0,mainHeight/2+1])
                cylinder(d=mainDiameter +2.5, h= mainHeight/2 -1);
            translate([0,0,0])
                cylinder(d=mainDiameter + 2.5, h= mainHeight/2 -1);
        }
        translate([- mainDiameter/2,0,5])
            rotate([0,90,0])
                cylinder(d=coatHangerDiameter +.5, h= 8);
    }
}