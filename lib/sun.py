from __future__ import annotations  
import os, sys, weakref, pickle, glob, ctypes
sys.path.extend([os.path.join('../', 'lib')])
import data
import utilz
from orbital import derive_semiminor_axis
import json
import numpy as np

class Sun:
    _instances = []

    def __init__(self, name: str = "sun",scale_data: dict = None, debug: bool = False):
        """
        name (str): 
        debug (bool): enables debug messages
        Returns a Moon (obj) by provided name
        Pro Tip: Moon objects are created when a Planet object is instantiated and has natural satellites, Planet.sunData[*].Moon
        """
        self.default_scale_data = {
            "sun": {
                "debug": False,
                "scale_mass": 8.5,
                "scale_vol": 8.5,
                "scale_dist": 3.2,
                "scale_size": 1.5
            }
        }
        self.user_scale_data = self.default_scale_data if scale_data == None else utilz.merge_attributes(self.default_scale_data, scale_data)
        _sun = data.get_sun_data()
        NoneType = type(None)
        # NOTE: some suns have poorly formatted JSON strings and will be skipped
        if isinstance(_sun, NoneType): 
            print(f"WARNING: the sun was not available due to some parsing error, it will be skipped in plotting") if debug else None
            return None
        # NOTE: some suns have null (None) values for `mass` and/or `vol`
        if _sun['mass'] == None or _sun['vol'] == None:
            print(f"WARNING: the sun with relational URL {rel} has `None` mass or volume values, it will be skipped in plotting") if debug else None
            return None
        for k in _sun.keys():
            print(f"INFO: adding attribute for sun {_sun['englishName']}  ({k}) with value ({_sun[k]})") if debug else None
            setattr(self, k,  _sun[k])
        self.vol = self.vol 
        self.mass = self.mass 
        self.englishName = self.englishName
        self.name = self.name
        self.scaleMassExp = 0.0 
        self.scaleSizeExp = 0.0 
        self.scaleDistExp = 0.0
        self.scaleVolExp = 0.0
        self.massValue = self.mass['massValue']
        self.massExponent = self.mass['massExponent']
        self.massRawKG = float( f"{float(self.massValue*(10**self.massExponent)):f}" )
        self.keys = list(_sun.keys()) + list(('massValue', 'massExponent',  'massRawKG', 'scaleMassExp','scaleSizeExp','scaleDistExp', 'scaleVolExp'))
        # NOTE: some suns may have no equaRadius data (see jupiter), in these cases fall back to setting radius by meanRadius value
        if self.equaRadius == 0:
            self.equaRadius = self.meanRadius
        if self.englishName == "":
            self.englishName = self.name
        self.__class__._instances.append(self) 

    def scale_mass(self, scale_data: dict = None, debug: bool = False) -> Sun:
        """
        scale_exp: float (the exponent used to scale massRawKG value/(10**scale_exp) )
        debug (bool): enables debug messages
        Returns Moon (scaled mass quantities)
        """
        self.user_scale_data = self.default_scale_data if scale_data == None else utilz.merge_attributes(self.default_scale_data, scale_data)
        print(f"INFO: unscaled values massExponent ({self.massExponent})") if debug else None
        self.scaleMassExp = scale_data['sun']['scale_mass']
        self.massExponent = self.massExponent - (self.scaleMassExp)
        self.massRawKG = int( f"{int(self.massValue*(10**self.massExponent)):d}" )
        print(f"INFO: scaled values massExponent ({self.massExponent})") if debug else None 
        return self
    
    def scale_sun(self, scale_data: dict = None, debug: bool = False) -> Sun:
        """
        scale_size: float (the exponent used to scale meanRadius and equaRadius  'radius/(10**scale_exp)' )
        scale_mass: float (the exponent used to scale massRawKG and volumeRawKG 'mass/(10**scale_exp)' )
        scale_vol: float (the exponent used to scale volumeRawKG 'vol/(10**scale_exp)' )
        debug (bool): enables debug messages
        Returns Moon (scaled size, mass and distance quantities)
        """
        self.user_scale_data = self.default_scale_data if scale_data == None else utilz.merge_attributes(self.default_scale_data, scale_data)
        self.meanRadius = self.meanRadius
        print(f"INFO: {self.englishName} raw values  [meanRadius {self.meanRadius}] [equaRadius {self.equaRadius}] [massExponent {self.massExponent}] [massRawKG {self.massRawKG}]") if debug else None
        #print(f"INFO: {self.englishName} raw values [meanRadius -> {self.meanRadius}] [equaRadius -> {self.equaRadius}] [semimajorAxis -> {self.semimajorAxis}] [semiminorAxis -> {self.semiminorAxis}] [volValueRawKG -> {self.volumeRawKG}] [massRawKG -> {self.massRawKG}]") if debug else None
        self.scaleMassExp = self.user_scale_data['sun']['scale_mass'] 
        self.scaleSizeExp = self.user_scale_data['sun']['scale_size']
        self.massExponent = self.massExponent - (self.scaleMassExp)
        self.massRawKG = float( f"{int(self.massValue*(10**self.massExponent)):d}" )
        # NOTE: to address `OverflowError: Python int too large to convert to C int`, values which tend towards max will have their overage +100 subtracted `ctypes.c_uint(-1).value` 
        #if self.massRawKG >= ctypes.c_uint(-1).value:
        #    amountOver = self.massRawKG - ctypes.c_uint(-1).value
        #    print(f"{self.massRawKG} is larger than {ctypes.c_uint(-1).value}, subtracting {amountOver+100} from value") if debug else None
        #    self.massRawKG = self.massRawKG - (amountOver + 100.00)
        self.meanRadius = self.meanRadius / (10**(self.scaleSizeExp)) 
        self.equaRadius = self.equaRadius / (10**(self.scaleSizeExp))
        print(f"INFO: {self.englishName} scaled values  [meanRadius {self.meanRadius}] [equaRadius {self.equaRadius}] [massExponent {self.massExponent}] [massRawKG {self.massRawKG}]") if debug else None
        #print(f"INFO: scaled values meanRadius ({self.meanRadius}) equaRadius ({self.equaRadius}) massExponent ({self.massExponent}) massRawKG ({self.massValue*(10**self.massExponent)})") if debug else None
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
        Serializes a sun object to the filesystem
        """
        pickle.dump(self, open(f"{path}/_sun_{self.englishName.replace(' ','_')}.pickle", "wb"))

    @classmethod
    def byname(cls, name: str):
        """
        name: englishName of Moon
        Selects sun object by name from instances of Planet class.
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
        name: str (suns english name)
        select sun object by its english name
        """
        try:
            data = [i for i in cls._instances if i.englishName == name]
            return data if len(data) > 0 else data[0]
        except IndexError:
            return None

    @classmethod 
    def load(cls, path: str):
        """
        path: str (filesystem path where the object will be loaded from)
        """
        pkls = glob.glob(f"{path}/_sun_*.pickle")
        [cls._instances.append(pickle.load(i)) for i in pkls]

    @classmethod 
    def evaluate(cls, attrib: str, evalstr: str) -> list:
        """
        attrib: attribute on Sun class to evaluate 
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
