# Usage Snippets

## general usage patterns

```ruby

# set LIB_HOME to location of checkout
import os, sys
import importlib
sys.path.extend([os.path.join('.', 'lib')])
LIB_HOME='/Users/photon/DevOps/Projects/Solar_System_Model'
os.chdir(LIB_HOME)
import data # import data module
import planet # import planet module
from planet import Planet # import Planet class
import moon # import moon module
from moon import Moon # import Moon class
from copy import copy
import orbital # import orbital module
import importlib # use importlib to easily reload changes
# only use the below imports within blender, much of the processes will not work without the bpy context.
import blender # import blender module
import dev #setup internal functions

# instantiate some planets


# instantiate planets but don't scale
mercury = Planet('mercury', debug=True)
venus = Planet('venus', debug=True)
earth = Planet('earth', debug=True)
mars = Planet('mars', debug=True)
jupiter = Planet('jupiter', debug=True)
saturn = Planet('saturn', debug=True)
uranus = Planet('uranus', debug=True)
neptune = Planet('neptune', debug=True)





# get planetary stats
planets = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

# save a copy of your planets before changing them
planetsSaved = [copy(i) for i in planets]

# get all moon data in one array
flatten = lambda t: [item for sublist in t for item in sublist]
moonDatas = flatten([i.moonData for i in planets])

# get a sorted list of planet or moon distances
sortedPlanetDistances = sorted([i.semimajorAxis for i in planets])
sortedMoonDistances = sorted([i.semimajorAxis for i in moonDatas])


# calculate scaling exponents for a consisent scene scale

planetaryScales = [dict({i.englishName: i.calculate_scale_exponents()}) for i in planets]


# dynamically scale planets based on their mass, size, and orbital distances
earth.scale_planet(scale_size=earth.calculate_scale_exponents()['size_scale_exp'], scale_dist=earth.calculate_scale_exponents()['dist_scale_exp'], scale_mass=earth.calculate_scale_exponents()['size_mass_exp'])

# dynamically scale all the planets
scaledPlanets = [
    i.scale_planet(scale_size=i.calculate_scale_exponents()['scale_size_exp'], scale_dist=i.calculate_scale_exponents()['scale_dist_exp'],scale_mass=i.calculate_scale_exponents()['scale_mass_exp'], debug=True) for i in planets
]

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
