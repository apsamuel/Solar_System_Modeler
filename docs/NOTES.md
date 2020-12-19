# NOTES

## XYZ Functions (Parametric Formula describing commonly used shapes)

### XYZ function for hemisphere (sits like a dome)

`x=sqrt(semimajorAxis**2 - v**2)*(cos(u))`

`y=sqrt(semiminorAxis**2 - v**2)*(sin(u))`

`z=v`

* `u = (0, 2*pi), v = (0, radius)`
  
### XYZ function for hemisphere (flipped on z axis, like cup)

`x=sqrt(radius**2 - v**2)*(cos(u))`

`y=sqrt(radius**2 - v**2)*(sin(u))`

`z=-v`

### XYZ function for sphere

`x= radius * ( sin(u)*sin(v) )`

`y = radius * (cos(u)*sin(v) )`

`z = radius*(cos(v))`

* `u = (0,2*pi), v=(0,2*pi)`

### XYZ function for ellipsoid

`x= semimajorAxis * ( sin(u)*sin(v) )`

`y = semiminorAxis * (cos(u)*sin(v) )`

`z = semimajorAxis*(cos(v))`

* `u = (0,2*pi), v=(0,2*pi)`

### XYZ function for torus

`x=(1+0.5*cos(u))*sin(v)`

`y=(1+0.5*cos(u))*cos(v)`

`z=0.5*sin(u)`

### Example of calling primitive_xyz_function_surface() to generate a torus

```python
bpy.ops.mesh.primitive_xyz_function_surface(x_eq="(1+0.5*cos(u))*sin(v)", y_eq="(1+0.5*cos(u))*cos(v)", z_eq="0.5*sin(u)", range_u_min=0, range_u_max=6.28319, range_u_step=32, wrap_u=False, range_v_min=0, range_v_max=6.28319, range_v_step=128, wrap_v=False, close_v=False, n_eq=1, a_eq="0", b_eq="0", c_eq="0", f_eq="0", g_eq="0", h_eq="0")
```

### Example of selecting vertices (faces) in python 

```python
vert_list = [vert for vert in mesh.vertices]
for vert in face.vertices:
    vert_list[vert].select = True
    face.select = True
```

```shell
https://blenderartists.org/t/selecting-a-face-through-the-api/497406/2
https://blender.stackexchange.com/questions/2776/how-to-read-vertices-of-quad-faces-using-python-api
```

determining angle omega

we need 3 points in the XY plane to make a right triangle

* (0,0) point of origin
  * the origin, center mass of the Sun
* (semimajor_axis, 0) & (-semimajor_axis, 0)
  * idealized bounds of the planetary orbit, not accounting for semiminor
* (object_x, object_y)
  * the location of the object at any given time (frame)
* CONDITIONS
  * quadrants
    * if object_x is positive, and object_y is positive, object is in QUADRANT 1
      * a point in a straight line from the object to the x-axis is
        * x=object_x,y=0


Additional Improvements

* The scene will need a light, the best idea so far is to just put a "sun" lamp at the scene origin (underneath the actual sun.. figure that one out later)
* bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
* All objects should have the shade smooth property set, and subsurface modifiers added
* bpy.ops.object.shade_smooth()
* bpy.ops.object.modifier_add(type='SUBSURF')


Texturing planets in blender

---


* bump maps are applied as displacement modifiers
* bpy.ops.object.modifier_add(type='DISPLACE')
* bpy.context.object.modifiers["Displace"].strength = 0.001

texture coordinate -> vector mapping (rotations x 90 deg, z 180 deg) -> image texture (albedo) -> principled bsdf -> material output 
