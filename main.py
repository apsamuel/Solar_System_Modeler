import os, sys

LIB_HOME='/Users/photon/DevOps/Projects/Solar_System_Model'
os.chdir(LIB_HOME)
sys.path.extend([os.path.join('.', 'lib')])
import data as data
import planet, moon, sun
from planet import Planet
from moon import Moon
from sun import Sun
from copy import copy
import orbital as orbital
import blender as blender 
import utilz as utilz
import dev as dev
import importlib

# create the solar system (planets & moons), this takes some time 
Planet.make_system(debug=True)

# scale down solar system objects
Planet.scale_planets(debug=True)
Moon.scale_moons(debug=True)

# use properties of solar system to configure scene props, like a cool kid
blender.scene_props(seperate_u=False)


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

