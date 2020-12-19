#!/usr/bin/env python

import os, sys, importlib

from copy import copy, deepcopy

LIB_HOME='/Users/photon/DevOps/Projects/Solar_System_Model'
os.chdir(LIB_HOME)
sys.path.extend([os.path.join('.', 'lib')])
import data as data
import planet as planet
import moon as moon
import sun as sun
import solarsystem as solarsystem
from planet import Planet
from moon import Moon
from sun import Sun
from solarsystem import SolarSystem
import orbital as orbital
import utilz as utilz
import blender as blender 
import dev as dev

# use properties of solar system to configure scene props, like a cool kid
blender.scene_props(seperate_u=False)

# create the solar system (planets & moons), this takes some time 
ss = SolarSystem(name='mysystem', debug=True)
ss.scale_solar_system(debug=True)


#space background..
blender.plot_expanse('/Users/photon/Downloads/Spherical/SPACE013SX.hdr')

#sun, aka origin.. 
blender.plot_sun(ss.sun, debug=True)

#some planets...
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


#example of texturing a planet
blender.add_surface_displacement(Planet.byname('Earth'), '/Users/photon/Downloads/8k_earth_daymap_bump.jpg')
blender.add_albedo(Planet.byname('Earth'), '/Users/photon/Downloads/8k_earth_daymap.jpg')
