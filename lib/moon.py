from __future__ import annotations  
import os, sys, weakref, pickle, glob, ctypes
sys.path.extend([os.path.join('.', 'lib')])
import data
from orbital import derive_semiminor_axis
import json
import numpy as np

class Moon:
    _instances = []

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
            print(f"WARNING: the moon with relational URL {rel} was not available due to some parsing error, it will be skipped in plotting") if debug else None
            return None
        # NOTE: some moons have null (None) values for `mass` and/or `vol`
        if _moon['mass'] == None or _moon['vol'] == None:
            print(f"WARNING: the moon with relational URL {rel} has `None` mass or volume values, it will be skipped in plotting") if debug else None
            return None
        for k in _moon.keys():
            print(f"INFO: adding attribute for moon {_moon['englishName']} around {_moon['aroundPlanet']['planet']} ({k}) with value ({_moon[k]})") if debug else None
            setattr(self, k,  _moon[k])
        self.vol = self.vol 
        self.mass = self.mass 
        self.englishName = self.englishName
        self.name = self.name
        self.scaleMassExp = 0.0 
        self.scaleSizeExp = 0.0 
        self.scaleDistExp = 0.0
        self.scaleVolExp = 0.0
        self.semiminorAxis = round(derive_semiminor_axis(self))
        self.volValue = self.vol['volValue']
        self.volExponent = self.vol['volExponent']
        self.massValue = self.mass['massValue']
        self.massExponent = self.mass['massExponent']
        self.volumeRawKG = int( f"{int(self.volValue*(10**self.volExponent)):d}" )
        self.massRawKG = int( f"{int(self.massValue*(10**self.massExponent)):d}" )
        self.keys = list(_moon.keys()) + list(('volValue', 'volExponent', 'massValue', 'massExponent', 'volumeRawKG', 'massRawKG', 'scaleMassExp','scaleSizeExp','scaleDistExp', 'scaleVolExp'))
        # NOTE: some moons may have no equaRadius data (see jupiter), in these cases fall back to setting radius by meanRadius value
        if self.equaRadius == 0:
            self.equaRadius = self.meanRadius
        if self.englishName == "":
            self.englishName = self.name
        self.__class__._instances.append(self) 

    def scale_distance(self, scale_exp: float = 2.2, debug: bool = False) -> Moon:
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

    def scale_mass(self, scale_exp: float = 8.5, debug: bool = False) -> Moon:
        """
        scale_exp: float (the exponent used to scale massRawKG value/(10**scale_exp) )
        debug (bool): enables debug messages
        Returns Moon (scaled mass quantities)"""
        print(f"INFO: unscaled values massExponent ({self.massExponent})") if debug else None
        self.scaleMassExp = scale_exp
        self.massExponent = self.massExponent - (scale_exp)
        self.massRawKG = int( f"{int(self.massValue*(10**self.massExponent)):d}" )
        print(f"INFO: scaled values massExponent ({self.massExponent})") if debug else None 
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
    
    def scale_moon(self,scale_size: float = 0.5,scale_mass: float = 8.5, scale_vol: float = 8.5, scale_dist: float = 2.2, debug: bool = False) -> Moon:
        """
        scale_size: float (the exponent used to scale meanRadius and equaRadius  'radius/(10**scale_exp)' )
        scale_mass: float (the exponent used to scale massRawKG and volumeRawKG 'mass/(10**scale_exp)' )
        scale_vol: float (the exponent used to scale volumeRawKG 'vol/(10**scale_exp)' )
        scale_dist: float (the exponent used to scale semiminor and semimajor axis 'axis/(10**scale_exp)' )
        debug (bool): enables debug messages
        Returns Moon (scaled size, mass and distance quantities)
        """
        self.meanRadius = self.meanRadius
        print(f"INFO: unscaled values meanRadius ({self.meanRadius}) equaRadius ({self.equaRadius}) semimajorAxis ({self.semimajorAxis}) semiminorAxis ({self.semiminorAxis}) volExponent ({self.volExponent}) volValueRawKG ({self.volValue*(10**self.volExponent)}) massExponent ({self.massExponent}) massRawKG ({self.massValue*(10**self.massExponent)})") if debug else None
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
            print(f"{self.massRawKG} is larger than {ctypes.c_uint(-1).value}, subtracting {amountOver+100} from value") if debug else None
            self.massRawKG = self.massRawKG - (amountOver + 100.00)
        if self.volumeRawKG >= ctypes.c_uint(-1).value:
            amountOver = self.volumeRawKG - ctypes.c_uint(-1).value
            print(f"{self.volumeRawKG} is larger than {ctypes.c_uint(-1).value}, subtracting {amountOver+100} from value") if debug else None
            self.volRawKG = self.volRawKG - (amountOver + 100.00)
        self.meanRadius = self.meanRadius / (10**(scale_size)) 
        self.equaRadius = self.equaRadius / (10**(scale_size))
        print(f"INFO: scaled values meanRadius ({self.meanRadius}) equaRadius ({self.equaRadius}) semimajorAxis ({self.semimajorAxis}) semiminorAxis ({self.semiminorAxis}) volExponent ({self.volExponent}) volValueRawKG ({self.volValue*(10**self.volExponent)}) massExponent ({self.massExponent}) massRawKG ({self.massValue*(10**self.massExponent)})") if debug else None
        return self


    def attributes(self) -> list:
        """
        Returns list containing attributes defined on Moon object
        """
        return list(self.__dict__.keys())

    def inspect(self) -> dict:
        """
        Returns dict containing all attributes, attribute values defined on Planet object 
        """
        #return dict({k:v for k,v in zip(list(self.__dict__.values())[-1], list(self.__dict__.values())[0:-2])})
        return dict({k:v for k,v in self.__dict__.items()})
        #return list(zip(list(self.__dict__.values())[-1], list(self.__dict__.values())[0:-2]))

    def tostring(self) -> str:
        """
        Returns JSON str representing all attributes defined on Moon object
        """
        data = dict({k:v for k,v in self.__dict__.items()})
        return str( 
            json.dumps(data, separators=(',',':'), indent=2)
        )

    def save(self, path: str = "/tmp"):
        """
        path: str (filesystem path where object will be saved)
        Serializes a moon object to the filesystem
        """
        pickle.dump(self, open(f"{path}/_moon_{self.englishName.replace(' ','_')}.pickle", "wb"))

    @classmethod
    def scale_moons(cls, scale_size: float = 0.5, scale_mass: float = 8.5, scale_vol: float = 8.5, scale_dist: float = 2.2, debug: bool = False):
        """
        scale_size: float (the exponent used to scale meanRadius and equaRadius  'radius/(10**scale_exp)' )
        scale_mass: float (the exponent used to scale massRawKG 'quantity/(10**scale_exp)' )
        scale_vol: float (the exponent used to scale volumeRawKG 'quantity/(10**scale_exp)' )
        scale_dist: float (the exponent used to scale semiminor and semimajor axis 'axis/(10**scale_exp)' 
        debug: bool (print informational messages)
        Scales all moon objects to specified parameters
        """
        [i.scale_moon(scale_size=scale_size, scale_vol=scale_vol, scale_mass=scale_mass, scale_dist=scale_dist,debug=debug) for i in cls._instances]

    @classmethod
    def byname(cls, name: str):
        """
        name: englishName of Moon
        Selects moon object by name from instances of Planet class.
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
        name: str (moons english name)
        select moon object by its english name
        """
        try:
            data = [i for i in cls._instances if i.englishName == name]
            return data if len(data) > 0 else data[0]
        except IndexError:
            return None

    @classmethod 
    def query(cls, attrib: str) -> dict:
        """
        attrib: attribute on Moon class to output
        debug (bool): enables debug messages
        Query values for speicifed parameter across all defined moon.Moon() objects
        """
        try:
            return sorted({
                i.englishName: i.__getattribute__(attrib) for i in cls._instances
            }.items(), key=lambda x: x[1])
        except AttributeError:
            print(f"WARNING: an attribute named `{attrib}` does not exist")
            return None


    @classmethod
    def saveall(cls, path: str = "/tmp"):
        """
        path: str (filesystem path where object will be saved)
        Serializes all defubed planets object to the filesystem
        """
        [i.save(f"{path}") for i in cls._instances]

    @classmethod 
    def load(cls, path: str):
        """
        path: str (filesystem path where the object will be loaded from)
        """
        pkls = glob.glob(f"{path}/_moon_*.pickle")
        [cls._instances.append(pickle.load(i)) for i in pkls]

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
    def min(cls, attrib: str) -> Moon:
        """
        attrib: attribute on Moon object to evaluate 
        debug (bool): enables debug messages 
        Find minimum values for an attribute across defined moon.Moon() objects 
        Returns: Moon
        """
        return min([i for i in cls._instances], key=lambda i: i.__getattribute__(attrib))

    @classmethod
    def max(cls, attrib: str) -> Moon:
        """
        attrib: attribute on Moon object to evaluate 
        debug (bool): enables debug messages 
        Find maximum values for an attribute across defined planet.Planet() objects 
        Returns: Moon
        """
        return max([i for i in cls._instances], key=lambda i: i.__getattribute__(attrib))

    @classmethod
    def mean(cls, attrib: str):
        """
        attrib: attribute on Moon object to evaluate
        Find mean value for an attribute across all defined planet.Planet() objects
        """
        return np.mean(
            [i.__getattribute__(attrib) for i in cls._instances]
        )

    @classmethod
    def std(cls, attrib: str):
        """
        attrib: attribute on Moon object to evaluate
        Find standard deviation value for an attribute across all defined moon.Moon() objects
        """
        return np.std(
            [i.__getattribute__(attrib) for i in cls._instances]
        )

    @classmethod
    def var(cls, attrib: str):
        """
        attrib: attribute on Moon object to evaluate
        Find variance value for an attribute across all defined moon.Moon() objects
        """
        return np.var(
            [i.__getattribute__(attrib) for i in cls._instances]
        )

    @classmethod 
    def evaluate(cls, attrib: str, evalstr: str) -> list:
        """
        attrib: attribute on Moon class to evaluate 
        evalstr: string representing `code` to be evaluated, the word `attrib` evaluatess to the attributes name, and the word `val` evaluates to the attributes value. eg: 'val/(10**5)' or 'val >= ctypes.c_uint(-1).value' or 'type(val)'
        debug (bool): enables debug messages 
        evaluate/assert conditions for an attribute across defined planet.Planet() objects  
        Returns: list of tuples (object.englishName, object.initialValue, evaluatedData)
        """
        vals = []
        for i in cls._instances:
            val = i.__getattribute__(attrib)
            vals.append(
                (i.englishName, val, eval(evalstr))
            )
        return vals
