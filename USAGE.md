# Usage Snippets

## general usage patterns

```python

import os, sys
import importlib
LIB_HOME='/Users/photon/DevOps/Projects/Solar_System_Model'
os.chdir(LIB_HOME)
sys.path.extend([os.path.join('.', 'lib')])
import data as data
import planet, moon
from planet import Planet
from moon import Moon
from copy import copy
import orbital as orbital
import blender as blender
import utilz as utilz
import dev as dev
```

```python
# create the solar system (planets & moons), this takes some time 
Planet.make_system(debug=True)
```

```python
# scale down solar system objects
Planet.scale_planets(debug=True)
Moon.scale_moons(debug=True)
```

```python
# use properties of solar system to configure scene props, like a cool kid
blender.scene_props(seperate_u=False)
```

```python
#plot scene planets/moons, set orbital drivers
blender.plot_planet(Planet.byname('Mercury'), debug=True)
blender.add_orbital_drivers(Planet.byname('Mercury'))

blender.plot_planet(Planet.byname('Venus'), debug=True)
blender.add_orbital_drivers(Planet.byname('Venus'))

blender.plot_planet(Planet.byname('Earth'), debug=True)
blender.add_orbital_drivers(Planet.byname('Earth'))
blender.plot_natural_satellites(Planet.byname('Earth'), debug=True)

blender.plot_planet(Planet.byname('Mars'), debug=True)
blender.add_orbital_drivers(Planet.byname('Mars'))
blender.plot_natural_satellites(Planet.byname('Mars'), debug=True)

blender.plot_planet(Planet.byname('Jupiter'), debug=True)
blender.add_orbital_drivers(Planet.byname('Jupiter'))
blender.plot_natural_satellites(Planet.byname('Jupiter'))
```

```python
#XYZ function for sphere
x= radius * ( sin(u)*sin(v) )  
y = radius * (cos(u)*sin(v) )
z = radius*(cos(v))




#XYZ function for hemisphere (sits like a dome)
## u = 0,2pi v = 0, radius
x=sqrt(semimajorAxis**2 - v**2)*(cos(u))
y=sqrt(semiminorAxis**2 - v**2)*(sin(u))
z=v

#XYZ function for hemisphere (flipped on z axis, like cup)
x=sqrt(10**2 - v**2)*(cos(u))
y=sqrt(10**2 - v**2)*(sin(u))
z=-v


```
