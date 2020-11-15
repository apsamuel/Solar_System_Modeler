from __future__ import annotations  
import os, sys
sys.path.extend([os.path.join('.', 'lib')])
import data
from orbital import derive_semiminor_axis
import json

class Moon:
    def __init__(self, rel: str, debug: bool = False):
        """
        rel (str): Relational URL embedded in Planet.moons[*].rel data
        debug (bool): enables debug messages
        Returns a Moon (obj) by provided name
        Pro Tip: Moon objects are created when a Planet object is instantiated and has natural satellites, Planet.moonData[*].Moon
        """
        _moon = data.get_moon_data(rel)
        NoneType = type(None)
        # NOTE: some moons have poorly formatted JSON strings and will be skipped
        if isinstance(_moon, NoneType): 
            print(f"WARNING: the moon with relational URL {rel} was not available, it will be skipped in plotting")
            return None

        if _moon['mass'] == None or _moon['vol'] == None:
            print(f"WARNING: the moon with relational URL {rel} has 0 mass or volume values, it will be skipped in plotting")
            return None

        # NOTE: some moons have no volume or mass data, and therefore will be skipped
        #if _moon['mass'] == None or _moon['vol'] == None:
        #if not hasattr(_moon, 'mass') or not hasattr(_moon, 'vol') or not hasattr(_moon, 'semimajorAxis') or not hasattr(_moon, 'semiminorAxis') or not hasattr(_moon, 'id'):
        #if 'mass' not in _moon or 'vol' not in _moon or 'semimajorAxis' not in _moon or 'semiminorAxis' not in _moon:
        #    print(f"WARNING: the moon with relational URL {rel} has None values for volume mass, it will be skipped in plotting")
        #    return None
        # [setattr(self, key, _moon[key]) for key in _moon.keys() if _moon != None]
        for k in _moon.keys():
            print(f"INFO: adding attribute ({k}) with value ({_moon[k]}) to {_moon['englishName']}") if debug else None
            setattr(self, k,  _moon[k])
        self.vol = self.vol 
        self.mass = self.mass 
        self.englishName = self.englishName
        self.name = self.name
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
        if self.englishName == "":
            self.englishName = self.name

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
    
    def scale_moon(self,scale_size: float = 1.0,scale_mass: float = 5.0,scale_dist: float = 2.6, debug: bool = False) -> Moon:
        """
        scale_size: float (the exponent used to scale meanRadius and equaRadius  'radius/(10**scale_exp)' )
        scale_mass: float (the exponent used to scale massRawKG and volumeRawKG 'quantity/(10**scale_exp)' )
        scale_dist: float (the exponent used to scale semiminor and semimajor axis 'axis/(10**scale_exp)' )
        debug (bool): enables debug messages
        Returns Moon (scaled size, mass and distance quantities)
        """
        self.meanRadius = self.meanRadius
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

    def calculate_scale_exponents(self, digits=5):
        distanceDigitCount = len(str(int(self.semimajorAxis)))
        sizeDigitCount = len(str(int(self.equaRadius)))
        massDigitCount = len(str(int( f"{int(self.massValue*(10**self.massExponent)):d}" )))
        print(f"semimajor digits: {distanceDigitCount} sizeDigitCount: {sizeDigitCount} mass")
        return dict({
            "dist_scale_exp": float(distanceDigitCount - digits),
            "size_scale_exp": float(sizeDigitCount - digits),
            "mass_scale_exp": float(massDigitCount - digits)
        })