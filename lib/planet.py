import os, sys
sys.path.extend([os.path.join('.', 'lib')])
import data
from orbital import derive_semiminor_axis
from moon import Moon



class Planet:
    def __init__(self, name):
        """
        name: str (English name of a planet in the Solar System)
        Returns a Planet (obj) by provided name
        """
        _planet = data.get_planet_data(name)
        # recurse planet dict keys, setting each to a class attribute
        [setattr(self, key, _planet[key]) for key in _planet.keys()]
        self.semiminorAxis = round(derive_semiminor_axis(self))
        if self.moons == None:
            self.moonData = []
        else:
            self.moonData = [
                Moon(moon['rel']) for moon in self.moons
            ]

        #self.keys = list(_planet.keys())
        self.volValue = self.vol['volValue']
        self.volExponent = self.vol['volExponent']
        self.massValue = self.mass['massValue']
        self.massExponent = self.mass['massExponent']
        self.volumeRawKG = self.volValue * (10**self.volExponent)
        self.massRawKG = self.massValue * (10**self.massExponent)
        self.keys = list(_planet.keys()) + list(('semiminorAxis', 'volValue', 'volExponent', 'massValue', 'massExponent', 'volumeRawKG', 'massRawKG'))

    def scale_distance(self, scale_exp = 4.0):
        """
        scale_exp: float (the exponent used to scale semiminor and semimajor axis axis/(10**scale_exp) )
        Returns a Planet (obj) with distance quantities scaled by [QUANTITY/(10**scale_exp)]
        """
        self.semimajorAxis = self.semimajorAxis/(10**scale_exp)
        self.semiminorAxis = self.semiminorAxis/(10**scale_exp)
        return self

    def scale_mass(self, scale_exp = 5.0):
        """
        scale_exp: float float (the exponent used to scale massRawKG and volumeRawKG value/(10**scale_exp) )
        Returns Planet object, scaled mass values
        """
        self.volExponent = self.volExponent - (scale_exp)
        self.massExponent = self.massExponent - (scale_exp)
        self.massRawKG = self.massValue * (10**self.massExponent)
        self.volumeRawKG = self.volValue * (10**self.volExponent)
        return self
    
    def scale_planet(self,scale_size = 1.0, scale_mass = 10.0, scale_dist = 4.0):
        """
        scale_size: float (the exponent used to scale meanRadius and equaRadius  'radius/(10**scale_exp)' )
        scale_mass: float (the exponent used to scale massRawKG and volumeRawKG 'quantity/(10**scale_exp)' )
        scale_dist: float (the exponent used to scale semiminor and semimajor axis 'axis/(10**scale_exp)' 
        Returns Planet (scaled size, mass and distance values)
        """
        self.semimajorAxis = self.semimajorAxis/(10**scale_dist)
        self.semiminorAxis = self.semiminorAxis/(10**scale_dist)
        self.volExponent = self.volExponent - (scale_mass)
        self.massExponent = self.massExponent - (scale_mass)
        self.massRawKG = self.massValue * (10**self.massExponent)
        self.volumeRawKG = self.volValue * (10**self.volExponent)
        self.meanRadius = self.meanRadius / (10**(scale_size)) 
        self.equaRadius = self.equaRadius / (10**(scale_size))
        return self

