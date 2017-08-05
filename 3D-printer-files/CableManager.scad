sides = 15;
x = 10;
y=60+ sides*2;
z= 7;
cable= 2.3;
spacing = 2.7;
$fn=50;

difference(){
    cube([x, y, z]);
    for(i=[0:20]){
        yy = ( spacing) * i;
        translate([-1,sides +yy,z])
        rotate([0,90,0])
        cylinder(d=cable,h=20);
        }
}