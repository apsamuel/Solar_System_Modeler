from __future__ import annotations
import os, sys, weakref, pickle, glob, ctypes
sys.path.extend([os.path.join('.', 'lib')])
import data
from orbital import derive_semiminor_axis
from moon import Moon
import json
import numpy as np



class Planet:
    _limits = {
        "moon": {
            "min_radius": 750.00, 
            "max_radius": ctypes.c_uint(-1).value - 100000.00, 
            "min_distance": 0, 
            "max_distance": ctypes.c_uint(-1).value - 100000.00, 
            "min_mass": 0, 
            "max_mass": ctypes.c_uint(-1).value - 100000.00, 
            "min_volume": 0, 
            "max_volume": ctypes.c_uint(-1).value - 100000.00 
            },
        "planet": {
            "min_radius": 0, 
            "max_radius":  ctypes.c_uint(-1).value - 100000.00, 
            "min_distance": 0, 
            "max_distance": ctypes.c_uint(-1).value - 100000.00, 
            "min_mass": 0, 
            "max_mass": ctypes.c_uint(-1).value - 100000.00, 
            "min_volume": 0, 
            "max_volume": ctypes.c_uint(-1).value - 100000.00
        }
    }

    _planets = [
        'mercury',
        'venus',
        'earth',
        'mars',
        'jupiter',
        'saturn',
        'uranus',
        'neptune'
    ]
    _instances = []
    def __init__(self, name: str, moon_limits: dict = {"size": 750.00, "mass": 1000.00, "vol": 1000.00}, debug: bool = False) -> Planet:
        """
        name: str (English name of a planet in the Solar System)
        debug (bool): enables debug messages
        Returns a Planet (obj) by provided name
        """
        _planet = data.get_planet_data(name)
        #self.__class__._instances.append(weakref.proxy(self))

        # NOTE: keys from the dictionary object are added as class attributes to self
        for k in _planet.keys():
            print(f"INFO: adding attribute for planet {_planet['englishName']} ({k}) with value ({_planet[k]}) to {_planet['englishName']}") if debug else None
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
                # NOTE: ensure to ignore moons that equal None if any
                if moon == None:
                    print(f"INFO: the moon {moon} is not parseable, it will be skipped in plotting") if debug else None
                    continue    
                # NOTE: creates moon.Moon objects stored in planet.Planet.moonData[moon.Moon,...]            
                moonobj = Moon(moon['rel'], debug=debug)
                #print(f"DEBUG: {Moon._instances}") if debug else None
                if not hasattr(moonobj, 'id') or not hasattr(moonobj, 'semimajorAxis') or not hasattr(moonobj, 'semiminorAxis') or not hasattr(moonobj, 'equaRadius') or not hasattr(moonobj, 'meanRadius') or not hasattr(moonobj, 'vol') or not hasattr(moonobj, 'mass'):
                    print(f"INFO: the moon with relational URL {moon['rel']} is missing required attributes, it will be skipped in plotting") if debug else None
                    continue
                # TODO: do filtering based on attribute limits, in blender module...
                print(f"INFO: adding moon with relational URL {moon['rel']}") if debug else None
                self.moonData.append(moonobj)
        # NOTE: planets scale values default to 0
        self.scaleMassExp = 0.0 
        self.scaleSizeExp = 0.0 
        self.scaleDistExp = 0.0
        self.scaleVolExp  = 0.0
        # NOTE: unwrap dictionary values {'vol': {'volValue': n, 'volExponent': n} } for convenience
        self.volValue = self.vol['volValue']
        self.volExponent = self.vol['volExponent']
        self.massValue = self.mass['massValue']
        self.massExponent = self.mass['massExponent']
        # NOTE: calculate raw KG values for convenience, use format string to prevent scientific notation, which doesnt work well as inputs in blender.
        self.volumeRawKG = float( f"{float(self.volValue*(10**self.volExponent)):f}" )
        self.massRawKG = float( f"{float(self.massValue*(10**self.massExponent)):f}" )
        ############################################################################################################
        # NOTE: calculate distance from sun in AU                                                                  #
        # NOTE: calculate harmonic frequency value                                                                 #
        # NOTE: AU value for orbital harmonies set during scale to properly capture scaled AU and harmonic values  #
        # SOURCE km->au: https://www.wolframalpha.com/input/?i=1+km+in+AU                                          #
        # SOURCE au->km: https://www.wolframalpha.com/input/?i=1+AU+in+km                                          #        
        # 1.496*(10**(8-scale_exp)) -> 1 au in km (scaled)                                                         #
        # 6.685*(10**-(9-scale_exp)) -> 1 km in au (scaled)                                                        #     
        ############################################################################################################
        self.distanceFromSunInAU = float(f"{float(self.semimajorAxis*( 6.685 * (10**-float(9) ) )):f}")
        self.harmonicFrequency = float(f"{float((self.distanceFromSunInAU**3)/(self.sideralOrbit**2)):f}")        
        self.keys = list(_planet.keys()) + list(('semiminorAxis', 'volValue', 'volExponent', 'massValue', 'massExponent', 'volumeRawKG', 'massRawKG', 'distanceFromSunInAU','harmonicFrequency', 'scaleMassExp','scaleSizeExp','scaleDistExp', 'scaleVolExp'))
        self.__class__._instances.append(self) 

    def scale_distance(self, scale_exp: float = 4.2, debug: bool = False) -> Planet:
        """
        scale_exp: float (the exponent used to scale semiminor and semimajor axis axis/(10**scale_exp) )
        debug (bool): enables debug messages
        Returns a Planet (obj) with distance quantities scaled by [axis/(10**scale_exp)]
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
        self.massExponent = self.massExponent - (scale_exp)
        self.massRawKG = int( f"{int(self.massValue*(10**self.massExponent)):d}" )
        print(f"INFO: scaled values volExponent ({self.volExponent}) massExponent ({self.massExponent})") if debug else None
        return self

    def scale_vol(self, scale_exp: float = 8.5, debug: bool = False) -> Moon:
        """
        scale_exp: float (the exponent used to scale volumeRawKG value/(10**scale_exp) )
        debug (bool): enables debug messages
        Returns Moon (scaled mass quantities)"""
        print(f"INFO: unscaled values volExponent ({self.volExponent})") if debug else None
        self.scaleVolExp = scale_exp
        self.volExponent = self.volExponent - (scale_exp)
        self.volumeRawKG = int( f"{int(self.volValue*(10**self.volExponent)):d}" )
        print(f"INFO: scaled values volExponent ({self.volExponent})") if debug else None 
        return self
    
    #scale_size: float = 0.5,scale_mass: float = 8.5, scale_vol: float = 8.5, scale_dist: float = 4.2, debug: bool = False
    def scale_planet(self,scale_size: float = 0.5, scale_mass: float = 8.5, scale_vol: float = 8.5,  scale_dist: float = 3.2, do_moons: bool = False, moon_scales: dict = {"debug": False, "scale_mass": 8.5, "scale_vol": 8.5, "scale_dist": 4.2, "scale_size": 0.5}, debug: bool = False) -> Planet:
        """
        scale_size: float (the exponent used to scale meanRadius and equaRadius  'radius/(10**scale_exp)' )
        scale_mass: float (the exponent used to scale massRawKG 'quantity/(10**scale_exp)' )
        scale_vol: float (the exponent used to scale volumeRawKG 'quantity/(10**scale_exp)' )
        scale_dist: float (the exponent used to scale semiminor and semimajor axis 'axis/(10**scale_exp)' 
        do_moons: bool (scale moons aroundPlanet)
        moon_scales: dict (provide a dictionary of args for the Moon.scale_moon() function)
        debug (bool): enables debug messages
        Returns Planet (scaled size, mass and distance values)
        """
        self.meanRadius = self.meanRadius
        self.equaRadius = self.equaRadius
        self.englishName = self.englishName
        print(f"INFO: unscaled values for {self.englishName} meanRadius ({self.meanRadius}) equaRadius ({self.equaRadius}) semimajorAxis ({self.semimajorAxis}) semiminorAxis ({self.semiminorAxis})  volExponent ({self.volExponent}) volValueRawKG ({self.volValue*(10**self.volExponent)}) massExponent ({self.massExponent}) massRawKG ({self.massValue*(10**self.massExponent)})") if debug else None
        self.scaleDistExp = scale_dist 
        self.scaleMassExp = scale_mass 
        self.scaleSizeExp = scale_size
        self.scaleVolExp  = scale_vol  
        self.semimajorAxis = self.semimajorAxis/(10**scale_dist)
        self.semiminorAxis = self.semiminorAxis/(10**scale_dist)
        self.volExponent = self.volExponent - (scale_vol)
        self.massExponent = self.massExponent - (scale_mass)
        self.massRawKG = int( f"{int(self.massValue*(10**self.massExponent)):d}" )
        self.volumeRawKG = int( f"{int(self.volValue*(10**self.volExponent)):d}" )
        # NOTE: to address `OverflowError: Python int too large to convert to C int`, values which tend towards max will have their overage +100 subtracted `ctypes.c_uint(-1).value` 
        if self.massRawKG >= ctypes.c_uint(-1).value:
            amountOver = self.massRawKG - ctypes.c_uint(-1).value
            print(f"INFO: this planets mass in raw KG is too large to convert to a C int and will cause an overflow error, subtracting {amountOver+100}") if debug else None
            self.massRawKG = self.massRawKG - (amountOver + 100.00)
        if self.volumeRawKG >= ctypes.c_uint(-1).value:
            amountOver = self.volumeRawKG - ctypes.c_uint(-1).value
            print(f"INFO: this planets mass in raw KG is too large to convert to a C int and will cause an overflow error, subtracting {amountOver+100}") if debug else None
            self.volRawKG = self.volRawKG - (amountOver + 100.00)
        self.meanRadius = self.meanRadius / (10**(scale_size)) 
        self.equaRadius = self.equaRadius / (10**(scale_size))
        #self.distanceFromSunInAU = self.distanceFromSunInAU / (10**(scale_dist))
        # NOTE: you should scale moons with the planet accordingly
        # scale_size: float = 0.5,scale_mass: float = 8.5, scale_vol: float = 8.5, scale_dist: float = 4.2, debug: bool = False
        if do_moons:
            [i.scale_moon(debug=moon_scales['debug'], scale_mass=moon_scales['scale_mass'], scale_vol=moon_scales['scale_vol'], scale_dist=moon_scales['scale_dist'], scale_size=moon_scales['scale_size']) for i in self.moonData]

        print(f"INFO: scaled values for {self.englishName} meanRadius ({self.meanRadius}) equaRadius ({self.equaRadius}) semimajorAxis ({self.semimajorAxis}) semiminorAxis ({self.semiminorAxis}) volExponent ({self.volExponent}) volValueRawKG ({self.volValue*(10**self.volExponent)}) massExponent ({self.massExponent}) massRawKG ({self.massValue*(10**self.massExponent)})") if debug else None
        return self


    def attributes(self) -> list:
        """
        Returns list containing attributes defined on Planet object
        """
        return list(self.__dict__.keys())

    def inspect(self) -> dict:
        """
        Returns dict containing k->v for all attributes defined on Planet object, calls Moon.inspect on Moon objects
        """
        data = dict({k:v for k,v in self.__dict__.items()})
        moons = list(map(Moon.inspect, data['moonData']))
        data['moonData'] = moons
        return data

    def tostring(self) -> str:
        """
        Returns JSON str representing all attributes defined on Planet object, calls Moon.inspect on Moon objects 
        """
        data = dict({k:v for k,v in self.__dict__.items()})
        moons = list(map(Moon.inspect, data['moonData']))
        data['moonData'] = moons
        return str( 
            json.dumps(data, separators=(',',':'), indent=2)
        )

    def save(self, path: str = "/tmp"):
        """
        path: str (filesystem path where object will be saved)
        Serializes a planet object to the filesystem
        """
        pickle.dump(self, open(f"{path}/_planet_{self.englishName.replace(' ', '')}.pickle", "wb"))

    @classmethod
    def saveall(cls, path: str = "/tmp"):
        """
        path: str (filesystem path where object will be saved)
        Serializes all defubed planets object to the filesystem
        """
        [i.save(f"{path}") for i in cls._instances]

    @classmethod 
    def load(cls, path: str):
        pkls = glob.glob(f"{path}/_planet_*.pickle")
        [cls._instances.append(pickle.load(i)) for i in pkls]

    @classmethod
    def scale_planets(cls, scale_size: float = 0.5, scale_mass: float = 8.5, scale_vol: float = 8.5,  scale_dist: float = 3.2, do_moons: bool = False, moon_scales: dict = {"debug": False, "scale_mass": 8.5, "scale_vol": 8.5, "scale_dist": 4.2, "scale_size": 0.5}, debug: bool = False):
        """
        scale_size: float (the exponent used to scale meanRadius and equaRadius  'radius/(10**scale_exp)' )
        scale_mass: float (the exponent used to scale massRawKG  'mass/(10**scale_exp)' )
        scale_vol: float (the exponent used to scale volumeRawKG 'volume/(10**scale_exp)' )
        scale_dist: float (the exponent used to scale semiminor and semimajor axis 'axis/(10**scale_exp)' )
        do_moons: bool (scale moons aroundPlanet)
        moon_scales: dict (provide a dictionary of args for the Moon.scale_moon() function)
        debug (bool): enables debug messages
        Scales all defined planet objects by defined parameters (scaled size, mass and distance values)
        """
        [i.scale_planet(scale_size=scale_size, scale_mass=scale_mass, scale_vol=scale_vol, scale_dist=scale_dist,debug=debug) for i in cls._instances]
        if do_moons:
            [i.scale_moon(debug=moon_scales['debug'], scale_mass=moon_scales['scale_mass'], scale_vol=moon_scales['scale_vol'], scale_dist=moon_scales['scale_dist'], scale_size=moon_scales['scale_size']) for i in Moon._instances]

    @classmethod
    def byname(cls, name: str):
        """
        name: englishName of planet
        Selects planet object by name from instances of Planet class.
        """
        try:
            #return {i.englishName: i for i in cls._instances if i.englishName == name}, use a better data format
            data = [i for i in cls._instances if i.englishName == name]
            return data if len(data) > 1 else data[0]
        except IndexError:
            return None

    @classmethod
    def select(cls, name: str):
        """
        name: str (Planets english name)
        select Planet object by its english name
        """
        try:
            data = [i for i in cls._instances if i.englishName == name]
            return data if len(data) > 0 else data[0]
        except IndexError:
            return None

    @classmethod 
    def query(cls, attrib: str) -> dict:
        """
        attrib: attribute on Planet class to output
        debug (bool): enables debug messages
        Scales all defined planet objects by defined parameters (scaled size, mass and distance values)
        """
        try:
            return sorted({
                i.englishName: i.__getattribute__(attrib) for i in cls._instances
            }.items(), key=lambda x: x[1])
        except AttributeError:
            print(f"WARNING: an attribute named `{attrib}` does not exist")
            return None

    @classmethod
    def minmax(cls, attrib: str) -> tuple:
        """
        attrib: attribute on Planet class to output 
        debug (bool): enables debug messages 
        Find minimum and maximum values for an attribute across defined planet.Planet() objects 
        """
        mini = min([i for i in cls._instances], key=lambda i: i.__getattribute__(attrib))
        maxi = max([i for i in cls._instances], key=lambda i: i.__getattribute__(attrib))
        return (mini,maxi)

    @classmethod
    def min(cls, attrib: str) -> Planet:
        """
        attrib: attribute on Planet class to output 
        debug (bool): enables debug messages 
        Find minimum values for an attribute across defined planet.Planet() objects 
        Returns: Planet
        """
        return min([i for i in cls._instances], key=lambda i: i.__getattribute__(attrib))

    @classmethod
    def max(cls, attrib: str) -> Planet:
        """
        attrib: attribute on Planet class to evaluate
        Find Planet by maximum value for an attribute across all defined planet.Planet() objects 
        Returns: Planet
        """
        #return max([ i.__getattribute__(attrib) for i in cls._instances])
        return max([i for i in cls._instances], key=lambda i: i.__getattribute__(attrib))

    @classmethod
    def avg(cls, attrib: str):
        """
        attrib: attribute on Planet object to evaluate
        Find average value for an attribute across all defined planet.Planet() objects
        """
        return np.average(
            [i.__getattribute__(attrib) for i in cls._instances]
        )

    @classmethod
    def mean(cls, attrib: str):
        """
        attrib: attribute on Planet object to evaluate
        Find mean value for an attribute across all defined planet.Planet() objects
        """
        return np.mean(
            [i.__getattribute__(attrib) for i in cls._instances]
        )

    @classmethod
    def std(cls, attrib: str):
        """
        attrib: attribute on Planet object to evaluate
        Find standard deviation value for an attribute across all defined planet.Planet() objects
        """
        return np.std(
            [i.__getattribute__(attrib) for i in cls._instances]
        )

    @classmethod
    def var(cls, attrib: str):
        """
        attrib: attribute on Planet object to evaluate
        Find variance value for an attribute across all defined planet.Planet() objects
        """
        return np.var(
            [i.__getattribute__(attrib) for i in cls._instances]
        )

    @classmethod 
    def evaluate(cls, attrib: str, evalstr: str) -> list:
        """
        attrib: attribute on Planet class to output 
        evalstr: string representing `code` to be evaluated, the word `attrib` evaluatess to the attributes name, and the word `val` evaluates to the attributes value. eg: 'val/(10**5)' or 'val >= ctypes.c_uint(-1).value' or 'type(val)'
        debug (bool): enables debug messages 
        evaluate/assert conditions for an attribute across defined planet.Planet() objects  
        Returns: list
        """
        vals = []
        for i in cls._instances:
            val = i.__getattribute__(attrib)
            vals.append(
                (i.englishName, val, eval(evalstr))
            )
        return vals

    @classmethod 
    def make_system(cls, debug: bool = False):
        [cls(i,debug=debug) for i in cls._planets]