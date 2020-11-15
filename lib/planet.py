from __future__ import annotations
import os, sys
sys.path.extend([os.path.join('.', 'lib')])
import data
from orbital import derive_semiminor_axis
from moon import Moon



class Planet:
    def __init__(self, name: str, debug: bool = False) -> Planet:
        """
        name: str (English name of a planet in the Solar System)
        debug (bool): enables debug messages
        Returns a Planet (obj) by provided name
        """
        _planet = data.get_planet_data(name)
        # NOTE: keys from the dictionary object are added as class attributes to self
        for k in _planet.keys():
            print(f"INFO: adding attribute ({k}) with value ({_planet[k]}) to {_planet['englishName']}") if debug else None
            setattr(self, k,  _planet[k])
        self.semiminorAxis = round(derive_semiminor_axis(self))
        # NOTE: hack to avoid IDE errors, key is dynamically set from returned `planet` JSON object
        self.moons = self.moons 
        self.vol = self.vol 
        self.mass = self.mass 
        self.sideralOrbit = self.sideralOrbit
        # NOTE: any moons owned by planet are instantiated as moon.Moon objects and available in Planet.moonData[]
        if self.moons == None:
            self.moonData = []
        else:
            self.moonData = []
            for moon in self.moons:
                if moon == None:
                    continue
                print(f"INFO: adding moon {moon['rel']}") if debug else None
                moonobj = Moon(moon['rel'], debug=True)
                if not hasattr(moonobj, 'id') or not hasattr(moonobj, 'semimajorAxis') or not hasattr(moonobj, 'semiminorAxis'):
                    print(f"INFO: the moon with relational URL {moon['rel']} has critical or required values missing, it will be skipped in plotting")
                    continue
                self.moonData.append(moonobj)
        # NOTE: store scale values
        self.scaleMassExp = 0.0 
        self.scaleSizeExp = 0.0 
        self.scaleDistExp = 0.0
        # NOTE: unwrap dictionary values for convenience
        self.volValue = self.vol['volValue']
        self.volExponent = self.vol['volExponent']
        self.massValue = self.mass['massValue']
        self.massExponent = self.mass['massExponent']
        # NOTE: calculate raw KG values for convenience
        self.volumeRawKG = self.volValue * (10**self.volExponent)
        self.massRawKG = self.massValue * (10**self.massExponent)
        ############################################################################################################
        # NOTE: calculate distance from sun in AU                                                                  #
        # NOTE: calculate harmonic frequency value                                                                 #
        # NOTE: AU value for orbital harmonies set during scale to properly capture scaled AU and harmonic values  #
        # SOURCE km->au: https://www.wolframalpha.com/input/?i=1+km+in+AU                                          #
        # SOURCE au->km: https://www.wolframalpha.com/input/?i=1+AU+in+km                                          #        
        # 1.496*(10**(8-scale_exp)) -> 1 au in km (scaled)                                                         #
        # 6.685*(10**-(9-scale_exp)) -> 1 km in au (scaled)                                                        #     
        ############################################################################################################
        self.distanceFromSunInAU = self.semimajorAxis*( 6.685 * (10**-float(9) ) )
        self.harmonicFrequency = (self.distanceFromSunInAU**3)/(self.sideralOrbit**2)        
        self.keys = list(_planet.keys()) + list(('semiminorAxis', 'volValue', 'volExponent', 'massValue', 'massExponent', 'volumeRawKG', 'massRawKG', 'distanceFromSunInAU','harmonicFrequency', 'scaleMassExp','scaleSizeExp','scaleDistExp'))

    def scale_distance(self, scale_exp: float = 4.2, debug: bool = False) -> Planet:
        """
        scale_exp: float (the exponent used to scale semiminor and semimajor axis axis/(10**scale_exp) )
        debug (bool): enables debug messages
        Returns a Planet (obj) with distance quantities scaled by [QUANTITY/(10**scale_exp)]
        """
        print(f"INFO: unscaled values semimajorAxis ({self.semimajorAxis}) semiminorAxis ({self.semiminorAxis})") if debug else None
        self.scaleDistExp  = scale_exp 
        self.semimajorAxis = self.semimajorAxis/(10**scale_exp)
        self.semiminorAxis = self.semiminorAxis/(10**scale_exp)
        print(f"INFO: scaled values semimajorAxis ({self.semimajorAxis}) semiminorAxis ({self.semiminorAxis})") if debug else None
        return self

    def scale_mass(self, scale_exp: float = 5.0, debug: bool = False) -> Planet:
        """
        scale_exp: float float (the exponent used to scale massRawKG and volumeRawKG value/(10**scale_exp) )
        debug (bool): enables debug messages
        Returns Planet object, scaled mass values
        """
        print(f"INFO: unscaled values volExponent ({self.volExponent}) massExponent ({self.massExponent})") if debug else None
        self.scaleMassExp = scale_exp
        self.volExponent = self.volExponent - (scale_exp)
        self.massExponent = self.massExponent - (scale_exp)
        self.massRawKG = self.massValue * (10**self.massExponent)
        self.volumeRawKG = self.volValue * (10**self.volExponent)
        print(f"INFO: scaled values volExponent ({self.volExponent}) massExponent ({self.massExponent})") if debug else None
        return self
    
    def scale_planet(self,scale_size: float = 1.0, scale_mass: float = 5.0, scale_dist: float = 4.2, debug: bool = False) -> Planet:
        """
        scale_size: float (the exponent used to scale meanRadius and equaRadius  'radius/(10**scale_exp)' )
        scale_mass: float (the exponent used to scale massRawKG and volumeRawKG 'quantity/(10**scale_exp)' )
        scale_dist: float (the exponent used to scale semiminor and semimajor axis 'axis/(10**scale_exp)' 
        debug (bool): enables debug messages
        Returns Planet (scaled size, mass and distance values)
        """
        self.meanRadius = self.meanRadius
        self.equaRadius = self.equaRadius
        print(f"INFO: unscaled values meanRadius ({self.meanRadius}) equaRadius ({self.equaRadius}) semimajorAxis ({self.semimajorAxis}) semiminorAxis ({self.semiminorAxis})  volExponent ({self.volExponent}) volValueRawKG ({self.volValue*(10**self.volExponent)}) massExponent ({self.massExponent}) massRawKG ({self.massValue*(10**self.massExponent)})") if debug else None
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
        self.distanceFromSunInAU = self.distanceFromSunInAU / (10**(scale_size))
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
