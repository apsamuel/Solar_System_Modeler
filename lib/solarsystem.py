import os, sys

LIB_HOME='/Users/photon/DevOps/Projects/Solar_System_Model'
os.chdir(LIB_HOME)
sys.path.extend([os.path.join('.', 'lib')])
from sun import Sun  
from planet import Planet
from moon import Moon
import utilz
print(f"loaded ok..")

class SolarSystem:
    """
    Container class which represents a Solar System 

    ...

    Class Attributes
    ----------------

    _objects : list 
        A list containing all created objects contained in solar system
    _planets : list
        A list containing all planet objects contained in the solar system
    _suns: list
        A list containing all sun objects contained in the solar system 
    _instances: list 
        A list containing the SolarSystem object itself, this should always contain 1 item per instantiated SolarSystem
    _default_scale_data: dict 
        A nervous addition of the default scale dictionary to the class for convenienence =)!!

    Instance Attributes
    -------------------
    name: str
        The name of the SolarSystem object (default: 'SolarSystem') 
    sun: sun.Sun 
        The sun component of the solar system object 
    planets: list(planet.Planet,...)
        The planets associated with the solar system object 
    moons: list(moon.Moon,...)
        The moons associated with the solar system object

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
    
    debug : bool
        output informational messages (default: False)


    Class Methods
    -------------- 

    @scale_solar_systems(scale_data: dict = None, debug: bool = False): 
        Scales all objects in SolarSystem by scale_data (defaults to using SolarSystem._default_scale_data)
    @attributes() -> list:
        Returns attributes available on the SolarSystem class
    @vals(objtype: str = 'planets', attr: str = 'englishName', labeled=True) -> dict|list:
        Returns a list of values for attribute across all defined object types. The labeled option coerces the data type to a dict, where each value is labeled with it's owners `englishName`
    @byvalue(objtype: str = 'objects', attr: str = 'englishName', eval_string = 'val == Earth', debug=False) -> list(obj)
        Returns a list of objects meeting criteria (eval_string is true)
        preset variables are
            attr: the attribute name
            val: the attribute value
            example(s): 
                SolarSystem.byvalue(attr='englishName', eval_string='val == "Earth"')
    @min(objtype: str = 'objects', attr: str = 'englishName', debug=False):
        Returns the object with minimum value across all defined objects for specified attr (attribute). This works best for attributes with numeric values.
    @max(objtype: str = 'objects', attr: str = 'englishName', debug=False):
        Returns the object with maximum value across all defined objects for specified attr (attribute). This works best for attributes with numeric values.
    @minmax(objtype: str = 'objects', attr: str = 'englishName', debug=False):
        Returns a tuple object with (min(Object), max(Object)) values across all defined objects for specified attr (attribute). This works best for attributes with numeric values.

    Instance Methods
    ----------------
    scale_solar_system(scale_data: dict = None, debug: bool = False) -> SolarSystem: 
            Scales all objects in SolarSystem by scale_data (defaults to using SolarSystem._default_scale_data)
    """
    _objects = []
    _planets = [] 
    _suns = [] 
    _moons = []
    _instances = []
    _default_scale_data = {
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

    def __init__(self, name: str = "SolarSystem", scale_data: dict = None, debug: bool = False):
        """
        Constructs a SolarSystem object containing planets, moons, and sun(s)

        Parameters
        ----------

        name : str 
            The name of the SolarSystem object (default: 'SolarSystem')
        scale_data: dict 
            A dict containing exponents for standard scaling of objects (default: self.default_scale_data), this works by overriding built-in defaults, therefore, the full dictionary definition does not need to be specified. (default: see below)
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
        debug: bool
            Output useful debugging information
        """
        self.name = name
        self.default_scale_data = {
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
        # merge in any user provided scale data
        self.user_scale_data = self.default_scale_data if scale_data == None else utilz.merge_attributes(self.default_scale_data, scale_data)
        sun = Sun(debug=debug) 
        self.__class__._objects.append(sun)
        self.sun = sun 
        self.planets = Planet.make_planets(debug=debug) 
        self.__class__._objects.extend(self.planets)
        self.moons = utilz.flatten([i.moonData for i in self.planets])
        self.__class__._objects.extend(self.moons)
        self.__class__._instances.append(self)
        self.__class__._suns.append(self.sun)
        self.__class__._planets.extend(self.planets)
        self.__class__._moons.extend(self.moons)
        self.__class__._objects.append(self.sun)


    def scale_solar_system(self, scale_data: dict = None, debug: bool = False):
        """
        Scales all objects contained within a SolarSystem (planets, moons, and sun(s))

        Parameters
        ----------

        scale_data : dict 
            A dict containing exponents for standard scaling of objects (default: self.default_scale_data), this works by overriding built-in defaults, therefore, the full dictionary definition does not need to be specified. (default: see below)
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
        debug : bool
            Output useful debugging information
        """
        scale_data = self.default_scale_data if scale_data == None else utilz.merge_attributes(self.default_scale_data, scale_data)
        [i.scale_planet(scale_data=scale_data, debug=debug, do_moons=True) for i in self.planets] 
        self.sun.scale_sun(debug=debug)

    @classmethod
    def scale_solar_systems(cls, scale_data: dict = None, debug: bool = False):
        """
        Scales all objects defined, careful with this if you defined several SolarSystems, it will scale _ACROSS_ each SolarSystem container.

        Parameters
        ----------

        scale_data : dict 
            A dict containing exponents for standard scaling of objects (default: self.default_scale_data), this works by overriding built-in defaults, therefore, the full dictionary definition does not need to be specified. (default: see below)
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
        debug : bool
            Output useful debugging information
        """
        scale_data = cls._default_scale_data if scale_data == None else utilz.merge_attributes(cls._default_scale_data, scale_data)
        #scale planets and moons 
        [i.scale_planet(scale_data=scale_data, debug=debug, do_moons=True) for i in cls._planets]
        #scale sun 
        sun = cls._suns[0]
        sun.scale_sun(debug=True)


    @classmethod 
    def attributes(cls) -> list: 
        """
        Returns a list of non-internal attributes defined on SolarSystem class
        """
        return [i for i in cls.__dict__.keys() if i.startswith('_')]

    @classmethod 
    def vals(cls, objtype: str = 'planets', attr: str = 'englishName', labeled=True):
        """
        Returns list or dict (labeled list) of atrribute values for requested object type. 
 
        Parameters
        ----------

        objtype: str
            specify the type of object to validate values across, valid values are:
                planets: all defined planets 
                moons: all defined moons
                suns: all defined suns 
                objects: all defined objects
        attr: str
            specify the object attribute to be validated
        labeled: bool
            when True, instead of returning a list of raw values, it returns a labeled list, a dict ({'label':value, ...})
       
        """
        try: 
            if labeled:
                return { i.englishName: i.__getattribute__(attr) for i in cls.__dict__[f"_{objtype}"]}
            else:
                return sorted([i.__getattribute__(attr) for i in cls.__dict__[f"_{objtype}"] ])
        except AttributeError:
            print(f"WARNING: an attribute named `{attr}` does not exist")



    @classmethod
    def byvalue(cls, objtype: str = 'objects', attr: str = 'englishName', eval_string = 'val == "Earth"', debug=False):
        """
        Returns list of objects which meet the specified criteria
 
        Parameters
        ----------

        objtype: str
            specify the type of object to validate values across, valid values are:
                planets: all defined planets 
                moons: all defined moons
                suns: all defined suns 
                objects: all defined objects
        attr: str
            specify the object attribute to be validated
        
        eval_string: str
            An expression which when evaluates to true, objects meeting the criteria are returned. 
                Available variables:
                    val: attribute value
                    attr:  attribute name
            ex: eval_string='val >= 10e8' #return objects with a val greater than or equal to 1000000000.00

        """
        vals = []
        try:
            data = cls.__dict__[f"_{objtype}"]
            if len(data) > 0:
                for i in data:
                    val = i.__getattribute__(attr)
                    print(f"INFO: found attribute {attr} with value {val}") if debug else None
                    if (eval(eval_string)):
                        vals.append(i)
            return vals
        except IndexError:
            return None

    @classmethod
    def min(cls, objtype: str = 'objects', attr: str = 'englishName', debug=False):
        """
        Returns the object with the minimum value across all specified defined objects
 
        Parameters
        ----------

        objtype: str
            specify the type of object to validate values across, valid values are:
                planets: all defined planets 
                moons: all defined moons
                suns: all defined suns 
                objects: all defined objects
        attr: str
            specify the object attribute to be validated
        """
        try:
            return min(
                [i for i in cls.__dict__[f"_{objtype}"] ], key=lambda i: i.__getattribute__(attr)
                )
        except AttributeError:
            print(f"WARNING: an attribute named `{attr}` does not exist")
            return None

    @classmethod
    def max(cls, objtype: str = 'objects', attr: str = 'englishName', debug=False):
        """
        Returns the object with the maximum value across all specified defined objects
 
        Parameters
        ----------

        objtype: str
            specify the type of object to validate values across, valid values are:
                planets: all defined planets 
                moons: all defined moons
                suns: all defined suns 
                objects: all defined objects
        attr: str
            specify the object attribute to be validatede
        """
        try:
            return max(
                [i for i in cls.__dict__[f"_{objtype}"] ], key=lambda i: i.__getattribute__(attr)
                )
        except AttributeError:
            print(f"WARNING: an attribute named `{attr}` does not exist")
            return None

    @classmethod
    def minmax(cls, objtype: str = 'planets', attr: str = 'englishName', debug=False) -> tuple:
        """
        Returns a tuple containing (min(object), max(object)) across all specified defined objects
 
        Parameters
        ----------

        objtype: str
            specify the type of object to validate values across, valid values are:
                planets: all defined planets 
                moons: all defined moons
                suns: all defined suns 
                objects: all defined objects
        attr: str
            specify the object attribute to be validated
        """
        try:
            return ( min([i for i in cls.__dict__[f"_{objtype}"] ], key=lambda i: i.__getattribute__(attr)),max([i for i in cls.__dict__[f"_{objtype}"] ], key=lambda i: i.__getattribute__(attr)) )
        except AttributeError:
            print(f"WARNING: an attribute named `{attr}` does not exist")
            return None

