# Usage Snippets

## general usage patterns

```ruby

# set LIB_HOME to location of checkout
import os, sys
import importlib
sys.path.extend([os.path.join('.', 'lib')])
LIB_HOME='/Users/photon/DevOps/Projects/Solar_System_Model'
os.chdir(LIB_HOME)
import data # import data class
from planet import Planet # import Planet class
import moon # import moon module
from moon import Moon # import Moon class
import blender # import blender functions
import orbital # import orbital functions
import importlib # use importlib to easily reload changes
import dev #setup internal functions

# instantiate some planets
venus = Planet('venus', debug=True)
venus.scale_planet(debug=True)
mercury = Planet('mercury',debug=True)
mercury.scale_planet(debug=True)
earth = Planet('earth',debug=True)
earth.scale_planet(debug=True)
mars = Planet('mars',debug=True)
mars.scale_planet(debug=True)
jupiter = Planet('jupiter',debug=True)
jupiter.scale_planet(debug=True)
saturn = Planet('saturn',debug=True)
saturn.scale_planet(debug=True)
uranus = Planet('uranus',debug=True)
uranus.scale_planet(debug=True)
neptune = Planet('neptune',debug=True)
neptune.scale_planet(debug=True)

# instantiate planets but don't scale
venus = Planet('venus')
mercury = Planet('mercury')
earth = Planet('earth')
mars = Planet('mars')
jupiter = Planet('jupiter')
saturn = Planet('saturn')
uranus = Planet('uranus')
neptune = Planet('neptune')

# configure scene properties (IMPORTANT)
blender.scene_props()

# plot mercury, configure mercury orbital drivers
blender.primitive_planet_add(mercury)
# NOTE: motion drivers are attached to the empty representing the object, but not the object
blender.add_orbital_drivers('empty_Mercury',mercury)

# plot venus, configure venus orbital drivers
blender.primitive_planet_add(venus)
blender.add_orbital_drivers('empty_Venus',venus)

# plot earth, configure earths orbital drivers, and plot earths natural satellite
blender.primitive_planet_add(earth)
blender.add_orbital_drivers('empty_Earth',earth)
blender.primitive_natural_satellites_add(earth)

# plot mars, configure mars orbital drivers, and plot mars natural satellites
mars = Planet('mars')
mars.scale_planet()
blender.primitive_planet_add(mars)
blender.add_orbital_drivers('empty_Mars',mars)
blender.primitive_natural_satellites_add(mars)
```

## reload libs

```ruby
import data  
import planet
import moon
import orbital  
import blender
import dev
import importlib

importlib.reload(data)
importlib.reload(planet)
importlib.reload(moon)
importlib.reload(orbital)
importlib.reload(blender)
from planet import Planet  
from moon import Moon
```
