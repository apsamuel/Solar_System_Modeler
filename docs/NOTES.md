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
