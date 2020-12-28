#!/usr/bin/env python

import os, sys, importlib

from copy import copy, deepcopy
#LIB_HOME=os.path.dirname( os.path.realpath('__file__') )
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
from texture import Tex
import orbital as orbital
import utilz as utilz
import blender as blender 
import dev as dev

# use properties of solar system to configure scene props, like a cool kid
blender.scene_props(seperate_u=False)

# instantiate and 'warmup' a texture library, use library features to autogenerate height, normal and specular maps

# NOTE: 
tex = Tex()
tex.fetchitems(path=tex.default_path)
tex.fetchitems(itemtypes=['height', 'normal', 'specular'],path=tex.default_path)


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

blender.plot_planet(Planet.byname('Saturn'), debug=True)
blender.add_orbital_drivers(Planet.byname('Saturn'))
blender.plot_natural_satellites(Planet.byname('Saturn'))

blender.plot_planet(Planet.byname('Uranus'), debug=True)
blender.add_orbital_drivers(Planet.byname('Uranus'))
blender.plot_natural_satellites(Planet.byname('Uranus'))

blender.plot_planet(Planet.byname('Neptune'), debug=True)
blender.add_orbital_drivers(Planet.byname('Neptune'))
blender.plot_natural_satellites(Planet.byname('Neptune'))



#example of texturing a planet

blender.add_surface_displacement(ss.sun, tex.getattr('Sun','height'))
#blender.add_texture(ss.sun, tex)
blender.sun_texture(ss.sun, tex)
blender.add_solar_dynamics(ss.sun)

blender.add_surface_displacement(Planet.byname('Mercury'), tex.getattr('Mercury','height'))
blender.add_texture(Planet.byname('Mercury'), tex)

blender.add_surface_displacement(Planet.byname('Venus'), tex.getattr('Venus','height'))
blender.add_texture(Planet.byname('Venus'), tex)

blender.add_surface_displacement(Planet.byname('Earth'), tex.getattr('Earth','height'))
blender.add_texture(Planet.byname('Earth'), tex)
blender.add_surface_displacement(Moon.byname('Moon'), tex.getattr('Moon','height'))
blender.add_texture(Moon.byname('Moon'), tex)

blender.add_surface_displacement(Planet.byname('Mars'), tex.getattr('Mars','height'))
blender.add_texture(Planet.byname('Mars'), tex)

blender.add_surface_displacement(Planet.byname('Jupiter'), tex.getattr('Jupiter','height'))
blender.add_texture(Planet.byname('Jupiter'), tex)

blender.add_surface_displacement(Planet.byname('Saturn'), tex.getattr('Saturn','height'))
blender.add_texture(Planet.byname('Saturn'), tex)

blender.add_surface_displacement(Planet.byname('Uranus'), tex.getattr('Uranus','height'))
blender.add_texture(Planet.byname('Uranus'), tex)


blender.add_surface_displacement(Planet.byname('Neptune'), tex.getattr('Neptune','height'))
blender.add_texture(Planet.byname('Neptune'), tex)


# add tracking camera for planets 
blender.add_planet_trackcam(Planet.byname('Mercury'))
blender.add_planet_trackcam(Planet.byname('Venus'))
blender.add_planet_trackcam(Planet.byname('Earth'))
blender.add_planet_trackcam(Planet.byname('Mars'))
blender.add_planet_trackcam(Planet.byname('Jupiter'))


blender.plot_atmosphere(Planet.byname('Earth'))

#blender.add_surface_displacement(Planet.byname('Jupiter'), tex.getattr('Jupiter','height'))
#blender.add_surface_displacement(Planet.byname('Saturn'), tex.getattr('Saturn','height'))
#blender.add_surface_displacement(Planet.byname('Uranus'), tex.getattr('Uranus','height'))
#blender.add_surface_displacement(Planet.byname('Neptune'), tex.getattr('Neptune','height'))


