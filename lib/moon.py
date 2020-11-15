from __future__ import annotations  
import os, sys
sys.path.extend([os.path.join('.', 'lib')])
import data
from orbital import derive_semiminor_axis
import json

class Moon:
    def __init__(self, rel: str, debug: bool = False) -> Moon:
        """
        rel (str): Relational URL embedded in Planet.moons[*].rel data
        debug (bool): enables debug messages
        Returns a Moon (obj) by provided name
        Pro Tip: Moon objects are created when a Planet object is instantiated and has natural satellites, Planet.moonData[*].Moon
        """
        _moon = data.get_moon_data(rel)
        # NOTE: some moons have poorly formatted JSON strings and will be skipped
        if _moon == None: 
            print(f"WARNING: the moon with relational URL {rel} was not available, it will be skipped in plotting")
            return None
        # NOTE: some moons have no volume or mass data, and therefore will be skipped
        if _moon['mass'] == None or _moon['vol'] == None:
            print(f"WARNING: the moon with relational URL {rel} has None values for volume mass, it will be skipped in plotting")
            return None
        # [setattr(self, key, _moon[key]) for key in _moon.keys() if _moon != None]
        for k in _moon.keys():
            print(f"INFO: add key ({k}) with value ({_moon[k]}) to {_moon['englishName']}") if debug else None
            setattr(self, k,  _moon[k])
        self.scaleMassExp = 0.0 
        self.scaleSizeExp = 0.0 
        self.scaleDistExp = 0.0
        self.semiminorAxis = round(derive_semiminor_axis(self))
        self.volValue = self.vol['volValue']
        self.volExponent = self.vol['volExponent']
        self.massValue = self.mass['massValue']
        self.massExponent = self.mass['massExponent']
        self.volumeRawKG = self.volValue * (10**self.volExponent)
        self.massRawKG = self.massValue * (10**self.massExponent)
        self.keys = list(_moon.keys()) + list(('volValue', 'volExponent', 'massValue', 'massExponent', 'volumeRawKG', 'massRawKG', 'scaleMassExp','scaleSizeExp','scaleDistExp'))
        # NOTE: some moons may have no equaRadius data (see jupiter), in these cases fall back to setting radius by meanRadius value
        if self.equaRadius == 0:
            self.equaRadius = self.meanRadius

    def scale_distance(self, scale_exp: float = 4.2, debug: bool = False) -> Moon:
        """
        scale_exp: float (the exponent used to scale semiminor and semimajor axis axis/(10**scale_exp) )
        debug (bool): enables debug messages
        Returns Moon (scaled distance quantities)"""
        print(f"INFO: unscaled values semimajorAxis ({self.semimajorAxis}) semiminorAxis ({self.semiminorAxis})") if debug else None
        self.scaleDistExp  = scale_exp 
        self.semimajorAxis = self.semimajorAxis/(10**float(scale_exp))
        self.semiminorAxis = self.semiminorAxis/(10**float(scale_exp))
        print(f"INFO: scaled values semimajorAxis ({self.semimajorAxis}) semiminorAxis ({self.semiminorAxis})") if debug else None
        return self

    def scale_mass(self, scale_exp: float = 5.0, debug: bool = False) -> Moon:
        """
        scale_exp: float (the exponent used to scale massRawKG and volumeRawKG value/(10**scale_exp) )
        debug (bool): enables debug messages
        Returns Moon (scaled mass quantities)"""
        print(f"INFO: unscaled values volExponent ({self.volExponent}) massExponent ({self.massExponent})") if debug else None
        self.scaleMassExp = scale_exp
        self.volExponent = self.volExponent - (scale_exp)
        self.massExponent = self.massExponent - (scale_exp)
        self.massRawKG = self.massValue * (10**self.massExponent)
        self.volumeRawKG = self.volValue * (10**self.volExponent)
        print(f"INFO: scaled values volExponent ({self.volExponent}) massExponent ({self.massExponent})") if debug else None 
        return self
    
    def scale_moon(self,scale_size: float = 1.0,scale_mass: float = 5.0,scale_dist: float = 2.5, debug: bool = False) -> Moon:
        """
        scale_size: float (the exponent used to scale meanRadius and equaRadius  'radius/(10**scale_exp)' )
        scale_mass: float (the exponent used to scale massRawKG and volumeRawKG 'quantity/(10**scale_exp)' )
        scale_dist: float (the exponent used to scale semiminor and semimajor axis 'axis/(10**scale_exp)' )
        debug (bool): enables debug messages
        Returns Moon (scaled size, mass and distance quantities)
        """
        print(f"INFO: unscaled values meanRadius ({self.meanRadius}) equaRadius ({self.equaRadius}) semimajorAxis ({self.semimajorAxis}) semiminorAxis ({self.semiminorAxis}) volExponent ({self.volExponent}) volValueRawKG ({self.volValue*(10**self.volExponent)}) massExponent ({self.massExponent}) massRawKG ({self.massValue*(10**self.massExponent)})") if debug else None
        self.scaleDistExp = scale_dist 
        self.scaleMassExp = scale_mass 
        self.scaleSizeExp = scale_size
        self.semimajorAxis = self.semimajorAxis/(10**scale_dist)
        self.semiminorAxis = self.semiminorAxis/(10**scale_dist)
        self.volExponent = self.volExponent - (scale_mass)
        self.massExponent = self.massExponent - (scale_mass)
        self.massRawKG = self.massValue * (10**self.massExponent)
        self.volumeRawKG = self.volValue * (10**self.volExponent)
        self.meanRadius = self.meanRadius / (10**(scale_size)) 
        self.equaRadius = self.equaRadius / (10**(scale_size))
        print(f"INFO: scaled values meanRadius ({self.meanRadius}) equaRadius ({self.equaRadius}) semimajorAxis ({self.semimajorAxis}) semiminorAxis ({self.semiminorAxis}) volExponent ({self.volExponent}) volValueRawKG ({self.volValue*(10**self.volExponent)}) massExponent ({self.massExponent}) massRawKG ({self.massValue*(10**self.massExponent)})") if debug else None
        return self