//units mm
holes = 20;
sides = 15;
x = 4;

z= 4;
cable= 2.7;
spacing = .75;
y= holes * (cable +spacing)+ sides*2;
$fn=50;

difference(){
    cube([x, y, z]);
    for(i=[0:20]){
        yy = (cable + spacing) * i;
        translate([-1,sides +yy,z-.25])
        rotate([0,90,0])
        cylinder(d=cable,h=20);
        }
        text("OpenSCAD", font = "Liberation Sans");
}