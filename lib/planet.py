from __future__ import annotations
import os, sys, weakref, pickle, glob, ctypes
sys.path.extend([os.path.join('.', 'lib')])
import data
import utilz
from orbital import derive_semiminor_axis
from moon import Moon
import json
import numpy as np



class Planet:
    """
        Container class which represents a Planet

    ...

    Class Attributes
    ----------------

    _instances: list 
        A list containing all defined instances of Planet objects
    _default_scale_data: dict 
        A nervous addition of the default scale dictionary to the class for convenienence =)!!
    _planets: list
        A list of known and recognized planets in the solar system (there are 8!, and no pluto is not one)

    Instance Attributes
    -------------------
    name: str
        The name of the Planet object
    default_scale_data: dict
        A dict storing scale exponents for each object type (default: see below..)
            {
                "sun": {
                    "debug": False, 
                    "scale_mass": 8.5, 
                    "scale_vol": 8.5, 
                    "scale_dist": 4.2, 
                    "scale_size": 0.5
                },
                "planet": {
                    "debug": False, 
                    "scale_mass": 8.5, 
                    "scale_vol": 8.5, 
                    "scale_dist": 3.2, 
                    "scale_size": 0.5
                },
                "moon": {
                    "debug": False, 
                    "scale_mass": 8.5, 
                    "scale_vol": 8.5, 
                    "scale_dist": 4.2, 
                    "scale_size": 0.5
                }
            }
    user_scale_data: dict
        A dict which overrides any default settings with user provided settings (default: see below for format..)
            {
                "sun": {
                    "debug": True, 
                    "scale_mass": 9.5, 
                    "scale_vol": 9.5, 
                    "scale_dist": 2.2, 
                    "scale_size": 1.5
                },
                "planet": {
                    "scale_size": 0.5
                },
                "moon": {
                    "debug": True, 
                    "scale_mass": 8.5
                }
            }
    alternativeName: str
        Alternative name of planet
    aroundPlanet: 
        ...
    aphelion: int
        The planets Aphelion in kilometers
    id: str
        The planets Identifier in https://api.le-systeme-solaire.net/en/
    name: str 
        The planets name in French =)
    englishName: str 
        The planets name in english
    isPlanet: bool
        True for all planet objects
    moons: list(dict)
        list of all known moons associated with planet object
    semimajorAxis: float 
        the semimajor axis of the orbital ellipse
    perihelion: int 
        the planets Perihelion in kilometers
    aphelion: int
        the planets Aphelion in kilometers
    eccentricity: float
        the eccentricty of the planets orbit
    inclination: int
        the planets orbital inclination in degrees (angle from orbital plane)
    mass: dict 
        the planets mass in kilograms (a dict containing a base (massValue) and exponent (massExponent) == massValue*10eMassExponent)
    vol: dict
        the planets volume in kilograms (a dict containing a base (volValue) and exponent (volExponent) == massValue*10eMassExponent)
    density: float
        the planets density in grams/centimeter^3
    gravity: float
        the planets average surface gravity meters/second^-2
    escape: float
        the planets escape speed, the speed required to overrule the pull of gravity and enter space
    meanRadius: float 
        the planets mean radius
    equaRadius: float
        the planets radius at the equator
    polarRadius: float
        the planets average radius at the poles
    flattening: float
        the planets oblateness
    dimension: str
        the bodies dimenions on 3 axis (generally blank from data source)
    sideralOrbit: float
        the planets orbital period (the time for 1 full revolution around the sun) in days
    sideralRotation: float 
        the planets axial rotational period in hours
    aroundPlanet: bool
        the nearest planet to <body>, generally blank for planets
    discoveredBy: str 
        the name of the person who "discovered" the planet
    discoveryDate: str 
        the date the planet was discovered
    axialTilt: str 
        the planets axial tilt
    semiminorAxis: float 
        the semimajor axis of the orbital ellipse
    moonData: list
        a list of moons orbiting the planet
    scaleMassExp: int 
        when using scale_data param, the mass scale value will be stored here
    scaleSizeExp: float
        when using scale_data param, the size scale value will be stored here
    scaleDistExp: float
        when using scale_data param, the distance scale value will be stored here
    scaleVolExp: float
        when using scale_data param, the volume scale value will be stored here
    volValue: float
        the planets volume value
    volExponent: float
        the planets volume exponent
    massValue: float
        the planets mass value
    massExponent: float
        the planets mass exponent
    volumeRawKG: float
        the planets raw calculated floating point volume 
    massRawKG: float
       the planets raw calculated floating point mass
    distanceFromSunInAU: float
        the planets calculated distance from sun in AU
    harmonicFrequency: float
        the planets calculated harmonic frequency
    keys: list
        the list of attributes(keys) associated with the planet object

    
    debug : bool
        output informational messages (default: False)


    Class Methods
    -------------- 



    Instance Methods
    ----------------
    """

    _default_scale_data = {
        "planet": {
            "debug": False,
            "scale_mass": 8.5,
            "scale_vol": 8.5,
            "scale_dist": 3.2,
            "scale_size": 0.5
        },
        "moon": {
            "debug": False,
            "scale_mass": 8.5,
            "scale_vol": 8.5,
            "scale_dist": 4.2,
            "scale_size": 0.5
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
    def __init__(self, name: str, scale_data: dict = None, debug: bool = False) -> Planet:
        """
        Returns an object of class planet.Planet 

        Parameters
        ----------

        name: str
            English name of a planet in the Solar System
        scale_data: dict
            A dict which overrides any default settings with user provided settings (default: see below for format..)
            {
                "planet": {
                    "scale_size": 0.5
                },
                "moon": {
                    "debug": True, 
                    "scale_mass": 8.5
                }
            }
        debug (bool): output useful debugging information
        """
        self.default_scale_data = {
            "planet": {
                "debug": False,
                "scale_mass": 8.5,
                "scale_vol": 8.5,
                "scale_dist": 3.2,
                "scale_size": 1.5
            },
            "moon": {
                "debug": False,
                "scale_mass": 8.5,
                "scale_vol": 8.5,
                "scale_dist": 4.2,
                "scale_size": 1.5
            }
        }
        self.user_scale_data = self.default_scale_data if scale_data == None else utilz.merge_attributes(self.default_scale_data, scale_data)
        _planet = data.get_planet_data(name)

        for k in _planet.keys():
            print(f"INFO: adding attribute for planet {_planet['englishName']} ({k}) with value ({_planet[k]}) to {_planet['englishName']}") if debug else None
            setattr(self, k,  _planet[k])

        self.semiminorAxis = round(derive_semiminor_axis(self))
        self.semimajorAxis = float(self.semimajorAxis)
        # NOTE: hack to avoid IDE errors, key is dynamically set from returned `planet` JSON object
        self.moons = self.moons
        self.vol = self.vol
        self.mass = self.mass
        self.sideralOrbit = self.sideralOrbit
        if self.moons == None:
            self.moonData = []
        else:
            self.moonData = []
            
            for moon in self.moons:
                if moon == None:
                    print(f"INFO: the moon {moon} is not parseable, it will be skipped in plotting") if debug else None
                    continue              
                moonobj = Moon(moon['rel'], debug=debug)
                if not hasattr(moonobj, 'id') or not hasattr(moonobj, 'semimajorAxis') or not hasattr(moonobj, 'semiminorAxis') or not hasattr(moonobj, 'equaRadius') or not hasattr(moonobj, 'meanRadius') or not hasattr(moonobj, 'vol') or not hasattr(moonobj, 'mass'):
                    print(f"INFO: the moon with relational URL {moon['rel']} is missing required attributes, it will be skipped in plotting") if debug else None
                    continue
                # TODO: do filtering based on attribute limits, in blender module...
                print(f"INFO: adding moon with relational URL {moon['rel']}") if debug else None
                self.moonData.append(moonobj)

        # scales are zeroed on initialization and updated when scale_planets, or scale_planet is called against the object
        self.scaleMassExp = 0.0 
        self.scaleSizeExp = 0.0 
        self.scaleDistExp = 0.0
        self.scaleVolExp  = 0.0

        # mass and volume values
        self.volValue = self.vol['volValue']
        self.volExponent = self.vol['volExponent']
        self.massValue = self.mass['massValue']
        self.massExponent = self.mass['massExponent']
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

    def scale_distance(self, scale_data: dict = None, debug: bool = False) -> Planet:
        """
        Returns a planet object with scaled distance values (semimajorAxis, semiminorAxis)
        standard scaling is performed by the function f(x) = x/(10**scaleExponent)

        Parameters
        ----------

        scale_data: dict 
            dictionary of overrides for default scale_data
        debug: bool
            output informational messages (default: False)
        """
        scale_data = self.default_scale_data if scale_data == None else utilz.merge_attributes(self.default_scale_data, scale_data)
        print(f"INFO: {self.englishName} raw values [semimajorAxis -> {self.semimajorAxis}] [semiminorAxis -> ({self.semiminorAxis}]") if debug else None
        self.scaleDistExp  = scale_data['planet']['scale_dist'] 
        self.semimajorAxis = float(self.semimajorAxis/(10**self.scaleDistExp))
        self.semiminorAxis = float(self.semiminorAxis/(10**self.scaleDistExp))
        print(f"INFO: {self.englishName} scaled with [values/(10**{self.scaleDistExp})] [semimajorAxis -> {self.semimajorAxis}] [semiminorAxis -> {self.semiminorAxis}]") if debug else None
        return self

    def scale_mass(self, scale_data: dict = None, debug: bool = False) -> Planet:
        """
        Returns a planet object with scaled calculated mass value (massRawKG)
        standard scaling is performed by the function f(x) = x/(10**scaleExponent)

        Parameters
        ----------

        scale_data: dict 
            (dictionary of overrides for default scale_data)
        debug: bool
            output informational messages (default: False)
        """
        scale_data = self.default_scale_data if scale_data == None else utilz.merge_attributes(self.default_scale_data, scale_data)
        print(f"INFO: {self.englishName} raw values [mass -> {self.massRawKG}]") if debug else None
        self.scaleMassExp = scale_data['planet']['scale_mass']
        self.massExponent = self.massExponent - (self.scaleMassExp)
        self.massRawKG = float( f"{float(self.massValue*(10**self.scaleMassExp)):f}" )
        print(f"INFO: {self.englishName} scaled with [values/(10**{self.scaleMassExp})] [mass ->{self.massRawKG}]") if debug else None
        return self

    def scale_vol(self, scale_data: dict = None, debug: bool = False) -> Moon:
        """
        Returns a planet object with scaled calculated volume value (volumeRawKG)
        standard scaling is performed by the function f(x) = x/(10**scaleExponent)

        Parameters
        ----------

        scale_data: dict (dictionary of overrides for default scale_data)
        output informational messages (default: False)
        """
        scale_data = self.default_scale_data if scale_data == None else utilz.merge_attributes(self.default_scale_data, scale_data)
        print(f"INFO: {self.englishName} raw values [volume -> {self.volumeRawKG}]") if debug else None
        self.scaleVolExp = scale_data['planet']['scale_vol']
        self.volExponent = self.volExponent - (self.scaleVolExp)
        self.volumeRawKG = float( f"{float(self.volValue*(10**self.scaleVolExp)):f}" )
        print(f"INFO: {self.englishName} scaled with [values/(10**{self.scaleVolExp})] [volume -> {self.volumeRawKG}]") if debug else None 
        return self
    
    def scale_planet(self,scale_data: dict = None, do_moons: bool = False, debug: bool = False) -> Planet:
        """
        Returns a planet object with scaled distance, size, calculated mass & volume values (equaRadius, meanRadius, massRawKG, volumeRawKG, semimajorAxis, semiminorAxis)
        standard scaling is performed by the function f(x) = x/(10**scaleExponent)

        Parameters
        ----------

        scale_data: dict (dictionary of overrides for default scale_data)
        output informational messages (default: False)
        """
        scale_data = self.default_scale_data if scale_data == None else utilz.merge_attributes(self.default_scale_data, scale_data)
        self.meanRadius = self.meanRadius
        self.equaRadius = self.equaRadius
        self.englishName = self.englishName
        print(f"INFO: {self.englishName} raw values [meanRadius -> {self.meanRadius}] [equaRadius -> {self.equaRadius}] [semimajorAxis -> {self.semimajorAxis}] [semiminorAxis -> {self.semiminorAxis}]  [volValueRawKG -> {self.volumeRawKG}] [massRawKG -> {self.massRawKG}]") if debug else None
        self.scaleDistExp = scale_data['planet']['scale_dist'] 
        self.scaleMassExp = scale_data['planet']['scale_mass'] 
        self.scaleSizeExp = scale_data['planet']['scale_size']
        self.scaleVolExp  = scale_data['planet']['scale_vol']
        self.semimajorAxis = self.semimajorAxis/(10**self.scaleDistExp)
        self.semiminorAxis = self.semiminorAxis/(10**self.scaleDistExp)
        self.volExponent = self.volExponent - (self.scaleVolExp)
        self.massExponent = self.massExponent - (self.scaleMassExp)
        self.massRawKG = float( f"{float(self.massValue*(10**self.scaleMassExp)):f}" )
        self.volumeRawKG = float( f"{float(self.volValue*(10**self.scaleVolExp)):f}" )

        self.meanRadius = self.meanRadius / (10**(self.scaleSizeExp)) 
        self.equaRadius = self.equaRadius / (10**(self.scaleSizeExp))
        #self.distanceFromSunInAU = self.distanceFromSunInAU / (10**(scale_dist))
        # NOTE: you should scale moons with the planet accordingly
        # scale_size: float = 0.5,scale_mass: float = 8.5, scale_vol: float = 8.5, scale_dist: float = 4.2, debug: bool = False
        if do_moons:
            [i.scale_moon(scale_data = scale_data, debug=debug) for i in self.moonData]

        print(f"INFO: {self.englishName} scaled values [meanRadius -> {self.meanRadius}] [equaRadius -> {self.equaRadius}] [semimajorAxis -> {self.semimajorAxis}] [semiminorAxis -> {self.semiminorAxis}]  [volValueRawKG -> {self.volumeRawKG}] [massRawKG -> {self.massRawKG}]") if debug else None
        return self


    def attributes(self) -> list:
        """
        Returns a list containing attributes defined on a Planet object
        """
        return list(self.__dict__.keys())

    def inspect(self) -> dict:
        """
        Returns dict containing k->v for all attributes defined on Planet object (recursively calls Moon.inspect on contained Moon objects)
        """
        data = dict({k:v for k,v in self.__dict__.items()})
        moons = list(map(Moon.inspect, data['moonData']))
        data['moonData'] = moons
        return data

    def tostring(self) -> str:
        """
        Returns JSON formatted str representing all attributes defined on Planet object (recursively calls Moon.inspect on contained Moon objects)
        """
        data = dict({k:v for k,v in self.__dict__.items()})
        moons = list(map(Moon.inspect, data['moonData']))
        data['moonData'] = moons
        return str( 
            json.dumps(data, separators=(',',':'), indent=2)
        )

    def save(self, path: str = "/tmp"):
        """
        Serializes a Planet object to the filesystem in python pickle format 

        Parameters
        ----------

        path: str
            str filesystem path where object will be saved

        """
        pickle.dump(self, open(f"{path}/_planet_{self.englishName.replace(' ', '')}.pickle", "wb"))

    @classmethod
    def saveall(cls, path: str = "/tmp"):
        """
        Serializes all defined Planet objects to the filesystem in python pickle format 

        Parameters
        ----------

        path: str
            filesystem path where object will be saved

        """
        [i.save(f"{path}") for i in cls._instances]

    @classmethod 
    def load(cls, path: str):
        """
        Loads all serialized objects from filesystem at specified path 

        Parameters
        ----------

        path: str 
            filesystem path where objects to be loaded were saved
        """
        pkls = glob.glob(f"{path}/_planet_*.pickle")
        [cls._instances.append(pickle.load(i)) for i in pkls]

    @classmethod
    def scale_planets(cls, scale_data: dict = None, do_moons: bool = True, debug: bool = False):
        """
        Scales all defined planets to scales specified by scale_data 

        Parameters
        ----------

        scale_data: dict 
            A dictionary 
        do_moons: bool 
            scale moons aroundPlanet
        moon_scales: dict 
            provide a dictionary of args for the Moon.scale_moon() function
        debug (bool): 
            enables debug messages
        """
        scale_data = cls._default_scale_data if scale_data == None else utilz.merge_attributes(cls._default_scale_data, scale_data)
        [i.scale_planet(scale_data=scale_data, debug=debug) for i in cls._instances]
        if do_moons:
            [i.scale_moon(scale_data=scale_data, debug=debug) for i in Moon._instances]

    @classmethod
    def byname(cls, name: str):
        """
        Return a planet object by its english name

        Parameters
        ----------

        name: str
            englishName of planet
        """
        try:
            data = [i for i in cls._instances if i.englishName == name]
            return data if len(data) > 1 else data[0]
        except IndexError:
            return None

    @classmethod
    def select(cls, name: str):
        """
        Umm, yea, does the same thing as by name... 

        TODO: refit this function to be more general, get object by attribute == value

        Parameters
        ----------

        name: str (Planets english name)

        """
        try:
            data = [i for i in cls._instances if i.englishName == name]
            return data if len(data) > 0 else data[0]
        except IndexError:
            return None

    @classmethod 
    def query(cls, attrib: str) -> dict:
        """
        Returns sorted dictionary containing key -> englishName (as label) and value -> attribute value for specified attribute 

        Parameters
        ----------

        attrib: str
            attribute on Planet class to output

        """
        try:
            return sorted({
                i.englishName: i.__getattribute__(attrib) for i in cls._instances
            }.items(), key=lambda x: x[1])
        except AttributeError:
            print(f"WARNING: an attribute named `{attrib}` does not exist")
            return None

    @classmethod 
    def vals(cls, attrib: str) -> list: 
        """
        Returns list of values corresponding to requested attribute across defined planet.Planet objects 

        Parameters
        ----------

        attrib: str 
            attribute on Planet class to output

        """
        try:
            return sorted([i[-1] for i in cls.query(attrib)])
        except AttributeError:
            print(f"WARNING: an attribute named `{attrib}` does not exist")
            return None

    @classmethod 
    def normalize_attribs(cls, attrib: str, start = 1, end = 10, precision=5):
        """
        Returns normalized values for specified attribute across defined planet.Planet objects 

        Parameters
        ----------

        attrib: str 
            attribute on Planet class to calculate
        start: int 
            minimum value of scaled range to calculate
        end : int
            maximum value of scaled range to calculate         
        precision: int 
            precision of floating point numbers

        """
        data = cls.vals(attrib)
        return [ round(float( (end-start)*(i-min(data))/(max(data)-min(data))+start),precision)  for i in data]

    @classmethod 
    def normalize_attrib(cls, attrib: str, value, start = 1, end = 10, precision=5):
        """
        Returns normalized value for specified attribute across all defined planet.Planet objects 

        Parameters
        ----------

        attrib: str 
            attribute on Planet class to output

        """
        data = cls.vals(attrib)
        print(f"numerator: {(end-start)*(value-min(data))}")
        print(f"denominator: {(max(data)-min(data))+start}")
        try: 
            return round(float( 
                (end-start)*(value-min(data))/(max(data)-min(data))+start
                ),precision) 
        except ZeroDivisionError:
            print(f"WARNING: division by zero, did you define enough planet objects to normalize an attribute across a range?")
            return round(float( 
                (end-start)*(value-min(data))/(max(data)-min(data))+start
                ),precision)     


    @classmethod
    def minmax(cls, attrib: str) -> tuple:
        """
        Returns a tuple containing the (min(object),max(object)) validated by provided attribute across all defined Planet objects

        Parameters
        ----------

        attrib: str
            attribute on Planet class to output 
        debug: bool
            enables debug messages 
        """
        mini = min([i for i in cls._instances], key=lambda i: i.__getattribute__(attrib))
        maxi = max([i for i in cls._instances], key=lambda i: i.__getattribute__(attrib))
        return (mini,maxi)

    @classmethod
    def min(cls, attrib: str) -> Planet:
        """
        Returns a min(object) validated by provided attribute across all defined Planet objects

        Parameters
        ----------

        attrib: str
            attribute on Planet class to output 
        debug: bool
            enables debug messages 
        """
        return min([i for i in cls._instances], key=lambda i: i.__getattribute__(attrib))

    @classmethod
    def max(cls, attrib: str) -> Planet:
        """
        Returns a max(object) validated by provided attribute across all defined Planet objects

        Parameters
        ----------

        attrib: str
            attribute on Planet class to output 
        debug: bool
            enables debug messages t
        """
        return max([i for i in cls._instances], key=lambda i: i.__getattribute__(attrib))

    @classmethod
    def avg(cls, attrib: str):
        """
        Returns a avg(object) validated by provided attribute across all defined Planet objects

        Parameters
        ----------

        attrib: str
            attribute on Planet class to output 
        debug: bool
            enables debug messages t
        """
        return np.average(
            [i.__getattribute__(attrib) for i in cls._instances]
        )

    @classmethod
    def mean(cls, attrib: str):
        """
        Returns a mean(object) validated by provided attribute across all defined Planet objects

        Parameters
        ----------

        attrib: str
            attribute on Planet class to output 

        """
        return np.mean(
            [i.__getattribute__(attrib) for i in cls._instances]
        )

    @classmethod
    def std(cls, attrib: str):
        """
        Returns a std(object) validated by provided attribute across all defined Planet objects

        Parameters
        ----------

        attrib: str
            attribute on Planet class to output 

        """
        return np.std(
            [i.__getattribute__(attrib) for i in cls._instances]
        )

    @classmethod
    def var(cls, attrib: str):
        """
        Returns a var(object) validated by provided attribute across all defined Planet objects

        Parameters
        ----------

        attrib: str
            attribute on Planet class to output 

        """
        return np.var(
            [i.__getattribute__(attrib) for i in cls._instances]
        )

    @classmethod 
    def evaluate(cls, attrib: str, evalstr: str) -> list:
        """
        evaluate/assert conditions for an attribute across defined planet.Planet() objects  

        Parameters
        ----------

        attrib: str
            attribute on Planet class to output 
        evalstr: string 
            representing `code` to be evaluated, the word `attrib` evaluatess to the attributes name, and the word `val` evaluates to the attributes value. eg: 'val/(10**5)' or 'val >= ctypes.c_uint(-1).value' or 'type(val)'
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
    def make_planets(cls, debug: bool = False):
        """
        Create all known planets in the solar system (makes moons also)

        Parameters
        ----------

        debug: bool
            print info messages
        """
        return [cls(i,debug=debug) for i in cls._planets]