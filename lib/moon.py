import os, sys
sys.path.extend([os.path.join('.', 'lib')])
import data
from orbital import derive_semiminor_axis

class Moon:
    def __init__(self, rel):
        """
        rel (str): Relational URL embedded in Planet.moons[*].rel data
        Returns a Moon (obj) by provided name
        Pro Tip: Moon objects are created when a Planet object is instantiated and has natural satellites, Planet.moonData[*].Moon
        """
        _moon = data.get_moon_data(rel)
        [setattr(self, key, _moon[key]) for key in _moon.keys()]
        self.semiminorAxis = round(derive_semiminor_axis(self))
        self.volValue = self.vol['volValue']
        self.volExponent = self.vol['volExponent']
        self.massValue = self.mass['massValue']
        self.massExponent = self.mass['massExponent']
        self.volumeRawKG = self.volValue * (10**self.volExponent)
        self.massRawKG = self.massValue * (10**self.massExponent)
        self.keys = list(_moon.keys()) + list(('volValue', 'volExponent', 'massValue', 'massExponent', 'volumeRawKG', 'massRawKG'))

    def scale_distance(self, scale_exp= 4.0):
        """
        scale_exp: float (the exponent used to scale semiminor and semimajor axis axis/(10**scale_exp) )
        Returns Moon (scaled distance quantities)"""
        self.semimajorAxis = self.semimajorAxis/(10**float(scale_exp))
        self.semiminorAxis = self.semiminorAxis/(10**float(scale_exp))
        return self

    def scale_mass(self, scale_exp = 5.0):
        """
        scale_exp: float (the exponent used to scale massRawKG and volumeRawKG value/(10**scale_exp) )
        Returns Moon (scaled mass quantities)"""
        self.volExponent = self.volExponent - (scale_exp)
        self.massExponent = self.massExponent - (scale_exp)
        self.massRawKG = self.massValue * (10**self.massExponent)
        self.volumeRawKG = self.volValue * (10**self.volExponent)
        return self
    
    def scale_moon(self,scale_size = 1.0,scale_mass = 10.0,scale_dist = 2.5):
        """
        scale_size: float (the exponent used to scale meanRadius and equaRadius  'radius/(10**scale_exp)' )
        scale_mass: float (the exponent used to scale massRawKG and volumeRawKG 'quantity/(10**scale_exp)' )
        scale_dist: float (the exponent used to scale semiminor and semimajor axis 'axis/(10**scale_exp)' )
        Returns Moon (scaled size, mass and distance quantities)
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