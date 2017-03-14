// Mark Benson

// 23/07/2013

// Creative commons non commercial

// Wheel for maze mouse
// Shaft fitting for 28BYJ-48 geared stepper
// http://www.thingiverse.com/thing:122070

difference()
{
    
    
    //striker 
    //translate([60,0,0])
    fooz = 36; //diameter of a foosball is 36mm 
    strike_height =90;
    
    //cut at an angle
    difference()
    {
        cylinder(r=fooz,h=strike_height,$fn=100);  
        translate([0,fooz/1.5  , strike_height * .85]) 
        rotate([40,0,0]) 
        cube([fooz*2, fooz*2, fooz*3],center=true);
        
    }   
   
   /*
	union()
	{
		//rim
		cylinder(r=60/2,h=4,$fn=100);

		//boss
		cylinder(r=12/2,h=7,$fn=100);
	}

	union()
	{
		//shaft cutout (shaft with flat)
		translate([0,0,1])
		intersection()
		{
			cylinder(r=5/2,h=8,$fn=40);
			translate([0,0,4]) cube([3,8,10], center=true);
		}

		//rim groove cutout
		translate([0,0,2])
		rotate_extrude(convexity=10, $fn=100)
		translate([30,0,10])
		rotate([0,0,45])
		square([2,2],center=true);

		//holes in the wheel
		for(i = [0:5])
		{
			rotate(i*360/6,[0,0,1])
			translate([19,0,-1])
			cylinder(r=17.5/2,h=8,$fn=40);
		}

	}
    */
    
    
   
}

