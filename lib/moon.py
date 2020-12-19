from __future__ import annotations  
import os, sys, weakref, pickle, glob, ctypes
sys.path.extend([os.path.join('../', 'lib')])
import data
from orbital import derive_semiminor_axis
import json
import utilz
import numpy as np

class Moon:
    """
        Container class which represents a Moon
        
    ...

    Class Attributes
    ----------------

    _instances: list 
        A list containing all defined instances of Moon objects
    _moons: list
    A list containing all known moon in the solar system
    _default_scale_data: dict 
        A nervous addition of the default scale dictionary to the class for convenienence =)!!
    _limits: dict 
        An artifact which may possibly used at some point which will control the limits of objects
        TODO: move this type of function/data to blender module, where limits of things will matter for plotting in 3 dimensions.


    Instance Attributes
    -------------------
    name: str
        The name of the Moon object
    default_scale_data: dict
        A dict storing scale exponents for each object type (default: see below..)
            {
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
                "moon": {
                    "debug": True, 
                    "scale_mass": 8.5
                }
            }
    alternativeName: str
        Alternative name of moon
    aroundPlanet: dict
        Dictionary containing keys 'moon' (the name of planet this moon orbits), 'rel' (relational link to the planet data source)
    aphelion: int
        The moons Aphelion in kilometers
    id: str
        The moons Identifier in https://api.le-systeme-solaire.net/en/
    name: str 
        The moons name in French =)
    englishName: str 
        The moons name in english
    isPlanet: bool
        False for all moon objects
    semimajorAxis: float 
        the semimajor axis of the orbital ellipse in kilometers
    semiminorAxis: float 
        the semimajor axis of the orbital ellipse in kilometers
    perihelion: int 
        the moons Perihelion in kilometers
    aphelion: int
        the moons Aphelion in kilometers
    eccentricity: float
        the eccentricty of the moons orbit
    inclination: int
        the moons orbital inclination in degrees (angle from orbital plane)
    mass: dict 
        the moons mass in kilograms (a dict containing a base (massValue) and exponent (massExponent) == massValue*10eMassExponent)
    vol: dict
        the moons volume in kilograms (a dict containing a base (volValue) and exponent (volExponent) == massValue*10eMassExponent)
    density: float
        the moons density in grams/centimeter^3
    gravity: float
        the moons average surface gravity meters/second^-2
    escape: float
        the moons escape speed, the speed required to overrule the pull of gravity and enter space
    meanRadius: float 
        the moons mean radius
    equaRadius: float
        the moons radius at the equator
    polarRadius: float
        the moons average radius at the poles
    flattening: float
        the moons oblateness
    dimension: str
        the bodies dimenions on 3 axis (generally blank from data source)
    sideralOrbit: float
        the moons orbital period (the time for 1 full revolution around the sun) in days
    sideralRotation: float 
        the moons axial rotational period in hours
    discoveredBy: str 
        the name of the person who "discovered" the moon
    discoveryDate: str 
        the date the moon was discovered
    axialTilt: str 
        the moons axial tilt
    scaleMassExp: int 
        when using scale_data param, the mass scale value will be stored here
    scaleSizeExp: float
        when using scale_data param, the size scale value will be stored here
    scaleDistExp: float
        when using scale_data param, the distance scale value will be stored here
    scaleVolExp: float
        when using scale_data param, the volume scale value will be stored here
    volValue: float
        the moons volume value
    volExponent: float
        the moons volume exponent
    massValue: float
        the moons mass value
    massExponent: float
        the moons mass exponent
    volumeRawKG: float
        the moons raw calculated floating point volume 
    massRawKG: float
       the moons raw calculated floating point mass
    distanceFromSunInAU: float
        the moons calculated distance from sun in AU
    harmonicFrequency: float
        the moons calculated harmonic frequency
    keys: list
        the list of attributes(keys) associated with the moon object

    
    debug : bool
        output informational messages (default: False)


    Instance Methods
    ----------------
    """

    _instances = []
    _moons = {
        "Adrast\u00e9e": {
            "englishName": "Adrastea",
            "id": "adrastee",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/adrastee"
        },
        "Aegir": {
            "englishName": "Aegir",
            "id": "aegir",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/aegir"
        },
        "Aitn\u00e9": {
            "englishName": "Aitne",
            "id": "aitne",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/aitne"
        },
        "Albiorix": {
            "englishName": "Albiorix",
            "id": "albiorix",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/albiorix"
        },
        "Amalth\u00e9e": {
            "englishName": "Amalthea",
            "id": "amalthee",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/amalthee"
        },
        "Anank\u00e9": {
            "englishName": "Ananke",
            "id": "ananke",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/ananke"
        },
        "Anth\u00e9": {
            "englishName": "Anthe",
            "id": "anthe",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/anthe"
        },
        "Aoed\u00e9": {
            "englishName": "Aoede",
            "id": "aoede",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/aoede"
        },
        "Arch\u00e9": {
            "englishName": "Arche",
            "id": "arche",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/arche"
        },
        "Ariel": {
            "englishName": "Ariel",
            "id": "ariel",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/ariel"
        },
        "Atlas": {
            "englishName": "Atlas",
            "id": "atlas",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/atlas"
        },
        "Autono\u00e9": {
            "englishName": "Autonoe",
            "id": "autonoe",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/autonoe"
        },
        "Bebhionn": {
            "englishName": "Bebhionn",
            "id": "bebhionn",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/bebhionn"
        },
        "Belinda": {
            "englishName": "Belinda",
            "id": "belinda",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/belinda"
        },
        "Bergelmir": {
            "englishName": "Bergelmir",
            "id": "bergelmir",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/bergelmir"
        },
        "Bestla": {
            "englishName": "Bestla",
            "id": "bestla",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/bestla"
        },
        "Bianca": {
            "englishName": "Bianca",
            "id": "bianca",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/bianca"
        },
        "Caliban": {
            "englishName": "Caliban",
            "id": "caliban",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/caliban"
        },
        "Callichore": {
            "englishName": "Kallichore",
            "id": "callichore",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/callichore"
        },
        "Callirrho\u00e9": {
            "englishName": "Callirrhoe",
            "id": "callirrhoe",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/callirrhoe"
        },
        "Callisto": {
            "englishName": "Callisto",
            "id": "callisto",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/callisto"
        },
        "Calypso": {
            "englishName": "Calypso",
            "id": "calypso",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/calypso"
        },
        "Cal\u00e9": {
            "englishName": "Kale",
            "id": "cale",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/cale"
        },
        "Carm\u00e9": {
            "englishName": "Carme",
            "id": "carme",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/carme"
        },
        "Carpo": {
            "englishName": "Carpo",
            "id": "carpo",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/carpo"
        },
        "Chald\u00e9n\u00e9": {
            "englishName": "Chaldene",
            "id": "chaldene",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/chaldene"
        },
        "Cord\u00e9lia": {
            "englishName": "Cordelia",
            "id": "cordelia",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/cordelia"
        },
        "Cor\u00e9": {
            "englishName": "Kore",
            "id": "core",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/core"
        },
        "Cressida": {
            "englishName": "Cressida",
            "id": "cressida",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/cressida"
        },
        "Cupid": {
            "englishName": "Cupid",
            "id": "cupid",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/cupid"
        },
        "Cyll\u00e8ne": {
            "englishName": "Cyllene",
            "id": "cyllene",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/cyllene"
        },
        "Daphnis": {
            "englishName": "Daphnis",
            "id": "daphnis",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/daphnis"
        },
        "Desd\u00e9mone": {
            "englishName": "Desdemona",
            "id": "desdemona",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/desdemona"
        },
        "Despina": {
            "englishName": "Despina",
            "id": "despina",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/despina"
        },
        "De\u00efmos": {
            "englishName": "Deimos",
            "id": "deimos",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/deimos"
        },
        "Dia": {
            "englishName": "Dia",
            "id": "dia",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/dia"
        },
        "Dion\u00e9": {
            "englishName": "Dione",
            "id": "dione",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/dione"
        },
        "Eir\u00e9n\u00e9": {
            "englishName": "Eirene",
            "id": "eirene",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/eirene"
        },
        "Encelade": {
            "englishName": "Enceladus",
            "id": "encelade",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/encelade"
        },
        "Epim\u00e9th\u00e9e": {
            "englishName": "Epimetheus",
            "id": "epimethee",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/epimethee"
        },
        "Erinom\u00e9": {
            "englishName": "Erinome",
            "id": "erinome",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/erinome"
        },
        "Erriapo": {
            "englishName": "Erriapus",
            "id": "erriapo",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/erriapo"
        },
        "Ersa": {
            "englishName": "Ersa",
            "id": "ersa",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/ersa"
        },
        "Euanth\u00e9": {
            "englishName": "Euanthe",
            "id": "euanthe",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/euanthe"
        },
        "Euk\u00e9lad\u00e9": {
            "englishName": "Eukelade",
            "id": "eukelade",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/eukelade"
        },
        "Euph\u00e9m\u00e9": {
            "englishName": "Eupheme",
            "id": "eupheme",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/eupheme"
        },
        "Euporie": {
            "englishName": "Euporie",
            "id": "euporie",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/euporie"
        },
        "Europe": {
            "englishName": "Europa",
            "id": "europe",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/europe"
        },
        "Eurydom\u00e9": {
            "englishName": "Eurydome",
            "id": "eurydome",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/eurydome"
        },
        "Farbauti": {
            "englishName": "Farbauti",
            "id": "farbauti",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/farbauti"
        },
        "Fenrir": {
            "englishName": "Fenrir",
            "id": "fenrir",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/fenrir"
        },
        "Ferdinand": {
            "englishName": "Ferdinand",
            "id": "ferdinand",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/ferdinand"
        },
        "Fornjot": {
            "englishName": "Fornjot",
            "id": "fornjot",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/fornjot"
        },
        "Francisco": {
            "englishName": "Francisco",
            "id": "francisco",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/francisco"
        },
        "Galat\u00e9e": {
            "englishName": "Galatea",
            "id": "galatee",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/galatee"
        },
        "Ganym\u00e8de": {
            "englishName": "Ganymede",
            "id": "ganymede",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/ganymede"
        },
        "Greip": {
            "englishName": "Greip",
            "id": "greip",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/greip"
        },
        "Halim\u00e8de": {
            "englishName": "Halimede",
            "id": "halimede",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/halimede"
        },
        "Harpalyk\u00e9": {
            "englishName": "Harpalyke",
            "id": "harpalyke",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/harpalyke"
        },
        "Hati": {
            "englishName": "Hati",
            "id": "hati",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/hati"
        },
        "Hermipp\u00e9": {
            "englishName": "Hermippe",
            "id": "hermippe",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/hermippe"
        },
        "Hers\u00e9": {
            "englishName": "Herse",
            "id": "herse",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/herse"
        },
        "Himalia": {
            "englishName": "Himalia",
            "id": "himalia",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/himalia"
        },
        "Hippocampe": {
            "englishName": "Hippocamp",
            "id": "hippocampe",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/hippocampe"
        },
        "Hyp\u00e9rion": {
            "englishName": "Hyperion",
            "id": "hyperion",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/hyperion"
        },
        "Hyrrokkin": {
            "englishName": "Hyrrokkin",
            "id": "hyrrokkin",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/hyrrokkin"
        },
        "H\u00e9g\u00e9mone": {
            "englishName": "Hegemone",
            "id": "hegemone",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/hegemone"
        },
        "H\u00e9lic\u00e9": {
            "englishName": "Helike",
            "id": "helice",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/helice"
        },
        "H\u00e9l\u00e8ne": {
            "englishName": "Helene",
            "id": "helene",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/helene"
        },
        "Ijiraq": {
            "englishName": "Ijiraq",
            "id": "ijiraq",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/ijiraq"
        },
        "Io": {
            "englishName": "Io",
            "id": "io",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/io"
        },
        "Iocast\u00e9": {
            "englishName": "Iocaste",
            "id": "iocaste",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/iocaste"
        },
        "Isono\u00e9": {
            "englishName": "Isonoe",
            "id": "isonoe",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/isonoe"
        },
        "Janus": {
            "englishName": "Janus",
            "id": "janus",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/janus"
        },
        "Japet": {
            "englishName": "Iapetus",
            "id": "japet",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/japet"
        },
        "Jarnsaxa": {
            "englishName": "Jarnsaxa",
            "id": "jarnsaxa",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/jarnsaxa"
        },
        "Juliette": {
            "englishName": "Juliet",
            "id": "juliet",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/juliet"
        },
        "Kalyk\u00e9": {
            "englishName": "Kalyke",
            "id": "kalyke",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/kalyke"
        },
        "Kari": {
            "englishName": "Kari",
            "id": "kari",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/kari"
        },
        "Kiviuq": {
            "englishName": "Kiviuq",
            "id": "kiviuq",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/kiviuq"
        },
        "La Lune": {
            "englishName": "Moon",
            "id": "lune",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/lune"
        },
        "Laom\u00e9die": {
            "englishName": "Laomedeia",
            "id": "laomedie",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/laomedie"
        },
        "Larissa": {
            "englishName": "Larissa",
            "id": "larissa",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/larissa"
        },
        "Loge": {
            "englishName": "Loge",
            "id": "loge",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/loge"
        },
        "Lysith\u00e9a": {
            "englishName": "Lysithea",
            "id": "lysithea",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/lysithea"
        },
        "L\u00e9da": {
            "englishName": "Leda",
            "id": "leda",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/leda"
        },
        "Mab": {
            "englishName": "Mab",
            "id": "mab",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/mab"
        },
        "Margaret": {
            "englishName": "Margaret",
            "id": "margaret",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/margaret"
        },
        "Mimas": {
            "englishName": "Mimas",
            "id": "mimas",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/mimas"
        },
        "Miranda": {
            "englishName": "Miranda",
            "id": "miranda",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/miranda"
        },
        "Mn\u00e9m\u00e9": {
            "englishName": "Mneme",
            "id": "mneme",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/mneme"
        },
        "Mundilfari": {
            "englishName": "Mundilfari",
            "id": "mundilfari",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/mundilfari"
        },
        "M\u00e9gaclit\u00e9": {
            "englishName": "Megaclite",
            "id": "megaclite",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/megaclite"
        },
        "M\u00e9thone": {
            "englishName": "Methone",
            "id": "methone",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/methone"
        },
        "M\u00e9tis": {
            "englishName": "Metis",
            "id": "metis",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/metis"
        },
        "Narvi": {
            "englishName": "Narvi",
            "id": "narvi",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/narvi"
        },
        "Na\u00efade": {
            "englishName": "Naiad",
            "id": "naiade",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/naiade"
        },
        "N\u00e9re\u00efde": {
            "englishName": "Nereid",
            "id": "nereide",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/nereide"
        },
        "N\u00e9so": {
            "englishName": "Neso",
            "id": "neso",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/neso"
        },
        "Ob\u00e9ron": {
            "englishName": "Oberon",
            "id": "oberon",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/oberon"
        },
        "Oph\u00e9lie": {
            "englishName": "Ophelia",
            "id": "ophelia",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/ophelia"
        },
        "Orthosie": {
            "englishName": "Orthosie",
            "id": "orthosie",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/orthosie"
        },
        "Paaliaq": {
            "englishName": "Paaliaq",
            "id": "paaliaq",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/paaliaq"
        },
        "Pall\u00e8ne": {
            "englishName": "Pallene",
            "id": "pallene",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/pallene"
        },
        "Pan": {
            "englishName": "Pan",
            "id": "pan",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/pan"
        },
        "Pandia": {
            "englishName": "Pandia",
            "id": "pandia",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/pandia"
        },
        "Pandore": {
            "englishName": "Pandora",
            "id": "pandore",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/pandore"
        },
        "Pasipha\u00e9": {
            "englishName": "Pasiphae",
            "id": "pasiphae",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/pasiphae"
        },
        "Pasith\u00e9e": {
            "englishName": "Pasithee",
            "id": "pasithee",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/pasithee"
        },
        "Perdita": {
            "englishName": "Perdita",
            "id": "perdita",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/perdita"
        },
        "Philophrosyne": {
            "englishName": "Philophrosyne",
            "id": "philophrosyne",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/philophrosyne"
        },
        "Phobos": {
            "englishName": "Phobos",
            "id": "phobos",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/phobos"
        },
        "Ph\u0153b\u00e9": {
            "englishName": "Phoebe",
            "id": "phoebe",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/phoebe"
        },
        "Pollux": {
            "englishName": "Polydeuces",
            "id": "pollux",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/pollux"
        },
        "Portia": {
            "englishName": "Portia",
            "id": "portia",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/portia"
        },
        "Praxidyk\u00e9": {
            "englishName": "Praxidike",
            "id": "praxidike",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/praxidike"
        },
        "Prom\u00e9th\u00e9e": {
            "englishName": "Prometheus",
            "id": "promethee",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/promethee"
        },
        "Prospero": {
            "englishName": "Prospero",
            "id": "prospero",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/prospero"
        },
        "Prot\u00e9e": {
            "englishName": "Proteus",
            "id": "protee",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/protee"
        },
        "Psamath\u00e9e": {
            "englishName": "Psamathe",
            "id": "psamathee",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/psamathee"
        },
        "Puck": {
            "englishName": "Puck",
            "id": "puck",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/puck"
        },
        "Rh\u00e9a": {
            "englishName": "Rhea",
            "id": "rhea",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/rhea"
        },
        "Rosalinde": {
            "englishName": "Rosalind",
            "id": "rosalind",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/rosalind"
        },
        "S/2003 J 10": {
            "englishName": "S/2003 J 10",
            "id": "s2003j10",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2003j10"
        },
        "S/2003 J 12": {
            "englishName": "S/2003 J 12",
            "id": "s2003j12",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2003j12"
        },
        "S/2003 J 16": {
            "englishName": "S/2003 J 16",
            "id": "s2003j16",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2003j16"
        },
        "S/2003 J 18": {
            "englishName": "S/2003 J 18",
            "id": "s2003j18",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2003j18"
        },
        "S/2003 J 19": {
            "englishName": "S/2003 J 19",
            "id": "s2003j19",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2003j19"
        },
        "S/2003 J 2": {
            "englishName": "S/2003 J 2",
            "id": "s2003j2",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2003j2"
        },
        "S/2003 J 23": {
            "englishName": "S/2003 J 23",
            "id": "s2003j23",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2003j23"
        },
        "S/2003 J 4": {
            "englishName": "S/2003 J 4",
            "id": "s2003j4",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2003j4"
        },
        "S/2003 J 9": {
            "englishName": "S/2003 J 9",
            "id": "s2003j9",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2003j9"
        },
        "S/2004 S 12": {
            "englishName": "S/2004 S 12",
            "id": "s2004s12",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2004s12"
        },
        "S/2004 S 13": {
            "englishName": "S/2004 S 13",
            "id": "s2004s13",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2004s13"
        },
        "S/2004 S 17": {
            "englishName": "S/2004 S 17",
            "id": "s2004s17",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2004s17"
        },
        "S/2004 S 7": {
            "englishName": "S/2004 S 7",
            "id": "s2004s7",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2004s7"
        },
        "S/2006 S 1": {
            "englishName": "S/2006 S 1",
            "id": "s2006s1",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2006s1"
        },
        "S/2006 S 3": {
            "englishName": "S/2006 S 3",
            "id": "s2006s3",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2006s3"
        },
        "S/2007 S 2": {
            "englishName": "S/2007 S 2",
            "id": "s2007s2",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2007s2"
        },
        "S/2007 S 3": {
            "englishName": "S/2007 S 3",
            "id": "s2007s3",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2007s3"
        },
        "S/2009 S 1": {
            "englishName": "S/2009 S 1",
            "id": "s2009s1",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2009s1"
        },
        "S/2010 J 1": {
            "englishName": "S/2010 J 1",
            "id": "s2010j1",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2010j1"
        },
        "S/2010 J 2": {
            "englishName": "S/2010 J 2",
            "id": "s2010j2",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2010j2"
        },
        "S/2011 J 2": {
            "englishName": "S/2011 J 2",
            "id": "s2011j2",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2011j2"
        },
        "S/2016 J 1": {
            "englishName": "S/2016 J 1",
            "id": "s2016j1",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2016j1"
        },
        "S/2017 J 1": {
            "englishName": "S/2017 J 1",
            "id": "s2017j1",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2017j1"
        },
        "S/2017 J 2": {
            "englishName": "S/2017 J 2",
            "id": "s2017j2",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2017j2"
        },
        "S/2017 J 3": {
            "englishName": "S/2017 J 3",
            "id": "s2017j3",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2017j3"
        },
        "S/2017 J 5": {
            "englishName": "S/2017 J 5",
            "id": "s2017j5",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2017j5"
        },
        "S/2017 J 6": {
            "englishName": "S/2017 J 6",
            "id": "s2017j6",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2017j6"
        },
        "S/2017 J 7": {
            "englishName": "S/2017 J 7",
            "id": "s2017j7",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2017j7"
        },
        "S/2017 J 8": {
            "englishName": "S/2017 J 8",
            "id": "s2017j8",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2017j8"
        },
        "S/2017 J 9": {
            "englishName": "S/2017 J 9",
            "id": "s2017j9",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/s2017j9"
        },
        "Sao": {
            "englishName": "Sao",
            "id": "sao",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/sao"
        },
        "Setebos": {
            "englishName": "Setebos",
            "id": "setebos",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/setebos"
        },
        "Siarnaq": {
            "englishName": "Siarnaq",
            "id": "siarnaq",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/siarnaq"
        },
        "Sinop\u00e9": {
            "englishName": "Sinope",
            "id": "sinope",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/sinope"
        },
        "Skathi": {
            "englishName": "Skathi",
            "id": "skathi",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/skathi"
        },
        "Skoll": {
            "englishName": "Skoll",
            "id": "skoll",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/skoll"
        },
        "Spond\u00e9": {
            "englishName": "Sponde",
            "id": "sponde",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/sponde"
        },
        "Stephano": {
            "englishName": "Stephano",
            "id": "stephano",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/stephano"
        },
        "Surtur": {
            "englishName": "Surtur",
            "id": "surtur",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/surtur"
        },
        "Suttungr": {
            "englishName": "Suttungr",
            "id": "suttungr",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/suttungr"
        },
        "Sycorax": {
            "englishName": "Sycorax",
            "id": "sycorax",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/sycorax"
        },
        "Tarqeq": {
            "englishName": "Tarqeq",
            "id": "tarqeq",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/tarqeq"
        },
        "Tarvos": {
            "englishName": "Tarvos",
            "id": "tarvos",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/tarvos"
        },
        "Tayg\u00e9t\u00e9": {
            "englishName": "Taygete",
            "id": "taygete",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/taygete"
        },
        "Thalassa": {
            "englishName": "Thalassa",
            "id": "thalassa",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/thalassa"
        },
        "Thelxino\u00e9": {
            "englishName": "Thelxinoe",
            "id": "thelxinoe",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/thelxinoe"
        },
        "Thrymr": {
            "englishName": "Thrymr",
            "id": "thrymr",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/thrymr"
        },
        "Thyon\u00e9": {
            "englishName": "Thyone",
            "id": "thyone",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/thyone"
        },
        "Th\u00e9b\u00e9": {
            "englishName": "Thebe",
            "id": "thebe",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/thebe"
        },
        "Th\u00e9misto": {
            "englishName": "Themisto",
            "id": "themisto",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/themisto"
        },
        "Titan": {
            "englishName": "Titan",
            "id": "titan",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/titan"
        },
        "Titania": {
            "englishName": "Titania",
            "id": "titania",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/titania"
        },
        "Trinculo": {
            "englishName": "Trinculo",
            "id": "trinculo",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/trinculo"
        },
        "Triton": {
            "englishName": "Triton",
            "id": "triton",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/triton"
        },
        "T\u00e9lesto": {
            "englishName": "Telesto",
            "id": "telesto",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/telesto"
        },
        "T\u00e9thys": {
            "englishName": "Tethys",
            "id": "tethys",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/tethys"
        },
        "Umbriel": {
            "englishName": "Umbriel",
            "id": "umbriel",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/umbriel"
        },
        "Val\u00e9tudo": {
            "englishName": "Valetudo",
            "id": "valetudo",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/valetudo"
        },
        "Ymir": {
            "englishName": "Ymir",
            "id": "ymir",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/ymir"
        },
        "\u00c9g\u00e9on": {
            "englishName": "Aegaeon",
            "id": "egeon",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/egeon"
        },
        "\u00c9lara": {
            "englishName": "Elara",
            "id": "elara",
            "rel": "https://api.le-systeme-solaire.net/rest/bodies/elara"
        }
    }

    _default_scale_data = {
                "moon": {
                    "debug": False,
                    "scale_mass": 8.5,
                    "scale_vol": 8.5,
                    "scale_dist": 4.2,
                    "scale_size": 0.5
                }
            }

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
            }
    }

    def __init__(self, rel: str, scale_data: dict = None,debug: bool = False):
        """
        Returns an object of class moon.Moon 

        Parameters
        ----------

        rel: str 
            relational url of a moon within data source (https://api.le-systeme-solaire.net/en/)
        scale_data: dict
            A dict which overrides any default settings with user provided settings (default: see below for format..)
            {
                "moon": {
                    "debug": True, 
                    "scale_mass": 8.5
                }
            }
        debug (bool): output useful debugging information
        """
        self.default_scale_data = {
            "moon": {
                "debug": False, 
                "scale_mass": 8.5, 
                "scale_vol": 8.5, 
                "scale_dist": 4.2, 
                "scale_size": 0.5
            }
        }
        self.user_scale_data = self.default_scale_data if scale_data == None else utilz.merge_attributes(self.default_scale_data, scale_data)
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
        self.semimajorAxis = float(self.semimajorAxis)
        self.volValue = self.vol['volValue']
        self.volExponent = self.vol['volExponent']
        self.massValue = self.mass['massValue']
        self.massExponent = self.mass['massExponent']
        self.volumeRawKG = float( f"{float(self.volValue*(10**self.volExponent)):f}" )
        self.massRawKG = float( f"{float(self.massValue*(10**self.massExponent)):f}" )
        self.keys = list(_moon.keys()) + list(('volValue', 'volExponent', 'massValue', 'massExponent', 'volumeRawKG', 'massRawKG', 'scaleMassExp','scaleSizeExp','scaleDistExp', 'scaleVolExp'))
        # NOTE: some moons may have no equaRadius data (see jupiter), in these cases fall back to setting radius by meanRadius value
        if self.equaRadius == 0:
            self.equaRadius = self.meanRadius
        if self.englishName == "":
            self.englishName = self.name
        self.__class__._instances.append(self) 

    # Scaling functions
    def scale_distance(self, scale_data: dict = None, debug: bool = False) -> Moon:
        """
        Returns a moon object with scaled distance values (semimajorAxis, semiminorAxis)
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
        self.scaleDistExp  = scale_data['moon']['scale_dist'] 
        self.semimajorAxis = self.semimajorAxis/(10**float(self.scaleDistExp))
        self.semiminorAxis = self.semiminorAxis/(10**float(self.scaleDistExp))
        print(f"INFO: {self.englishName} scaled with [values/(10**{self.scaleDistExp})] [semimajorAxis -> {self.semimajorAxis}] [semiminorAxis -> {self.semiminorAxis}]") if debug else None
        return self

    def scale_mass(self, scale_data: dict = None, debug: bool = False) -> Moon:
        """
        Returns a moon object with scaled calculated mass value (massRawKG)
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
        self.scaleMassExp = scale_data['moon']['scale_mass']
        self.massExponent = self.massExponent - (self.scaleMassExp)
        self.massRawKG = float( f"{float(self.massValue*(10**self.scaleMassExp)):f}" )
        print(f"INFO: {self.englishName} scaled with [values/(10**{self.scaleMassExp})] [mass ->{self.massRawKG}]") if debug else None
        return self

    def scale_vol(self, scale_data: dict = None, debug: bool = False) -> Moon:
        """
        Returns a moon object with scaled calculated volume value (volumeRawKG)
        standard scaling is performed by the function f(x) = x/(10**scaleExponent)

        Parameters
        ----------

        scale_data: dict (dictionary of overrides for default scale_data)
        output informational messages (default: False)
        """
        scale_data = self.default_scale_data if scale_data == None else utilz.merge_attributes(self.default_scale_data, scale_data)
        print(f"INFO: {self.englishName} raw values [volume -> {self.volumeRawKG}]") if debug else None
        self.scaleVolExp = scale_data['moon']['scale_vol']
        self.volExponent = self.volExponent - (self.scaleVolExp)
        self.volumeRawKG = float( f"{float(self.volValue*(10**self.scaleVolExp)):f}" )
        print(f"INFO: {self.englishName} scaled with [values/(10**{self.scaleVolExp})] [volume -> {self.volumeRawKG}]") if debug else None 
        return self
    
    def scale_moon(self, scale_data: dict = None, debug: bool = False) -> Moon:
        """
        Returns a moon object with scaled distance, size, calculated mass & volume values (equaRadius, meanRadius, massRawKG, volumeRawKG, semimajorAxis, semiminorAxis)
        standard scaling is performed by the function f(x) = x/(10**scaleExponent)

        Parameters
        ----------

        scale_data: dict (dictionary of overrides for default scale_data)
        output informational messages (default: False)
        """
        scale_data = self.default_scale_data if scale_data == None else utilz.merge_attributes(self.default_scale_data, scale_data)
        self.meanRadius = self.meanRadius
        
        
        self.scaleDistExp = scale_data['moon']['scale_dist']
        self.scaleMassExp = scale_data['moon']['scale_mass'] 
        self.scaleSizeExp = scale_data['moon']['scale_size']
        self.scaleVolExp  = scale_data['moon']['scale_vol']
        self.semimajorAxis = self.semimajorAxis/(10**self.scaleDistExp)
        self.semiminorAxis = self.semiminorAxis/(10**self.scaleDistExp)
        self.volExponent = self.volExponent - (self.scaleVolExp)
        self.massExponent = self.massExponent - (self.scaleMassExp)
        self.massRawKG = float( f"{float(self.massValue*(10**self.scaleMassExp)):f}" )
        self.volumeRawKG = float( f"{float(self.volValue*(10**self.scaleVolExp)):f}" )
        self.meanRadius = self.meanRadius / (10**(self.scaleSizeExp)) 
        self.equaRadius = self.equaRadius / (10**(self.scaleSizeExp))
        print(f"INFO: {self.englishName} scaled values [meanRadius -> {self.meanRadius}] [equaRadius -> {self.equaRadius}] [semimajorAxis -> {self.semimajorAxis}] [semiminorAxis -> {self.semiminorAxis}]  [volValueRawKG -> {self.volumeRawKG}] [massRawKG -> {self.massRawKG}]") if debug else None
        return self


    def attributes(self) -> list:
        """
        Returns list containing attributes defined on Moon object
        """
        return list(self.__dict__.keys())

    def inspect(self) -> dict:
        """
        Returns dict containing all attributes, attribute values defined on Moon object 
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
        Serializes a Planet object to the filesystem in python pickle format 

        Parameters
        ----------

        path: str
            str filesystem path where object will be saved

        """
        pickle.dump(self, open(f"{path}/_moon_{self.englishName.replace(' ','_')}.pickle", "wb"))

    @classmethod
    def scale_moons(cls, scale_data: dict = None, debug: bool = False):
        """
        Returns a list of moon objects with scaled distance, size, calculated mass & volume values (equaRadius, meanRadius, massRawKG, volumeRawKG, semimajorAxis, semiminorAxis)
        standard scaling is performed by the function f(x) = x/(10**scaleExponent)

        Parameters
        ----------

        scale_data: dict 
            dictionary of overrides for default scale_data
        debug: bool
            output informational messages (default: False)
        """
        scale_data = cls._default_scale_data if scale_data == None else utilz.merge_attributes(cls._default_scale_data, scale_data)
        return [i.scale_moon(scale_data=scale_data,debug=debug) for i in cls._instances]

    @classmethod
    def byname(cls, name: str):
        """
        Selects moon object by name from instances of Moon class.
        
        Parameters
        ----------        
        
        name: str
            english name of Moon
        
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
        Selects a moon object by its english name

        Parameters
        ----------        
                
        name: str 
            moons english name

        """
        try:
            data = [i for i in cls._instances if i.englishName == name]
            return data if len(data) > 0 else data[0]
        except IndexError:
            return None

    @classmethod 
    def vals(cls, attrib: str) -> list: 
        """
        Returns list of values corresponding to requested attribute across defined moon.Moon objects 

        Parameters
        ----------

        attrib: str 
            attribute on Moon class to output
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
        return round(float( 
            (end-start)*(value-min(data))/(max(data)-min(data))+start
            ),precision) 

    @classmethod 
    def query(cls, attrib: str) -> dict:
        """
        Returns sorted dictionary containing key -> englishName (as label) and value -> attribute value for specified attribute 

        Parameters
        ----------

        attrib: str
            attribute on Planet class to outpu
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
        pkls = glob.glob(f"{path}/_moon_*.pickle")
        [cls._instances.append(pickle.load(i)) for i in pkls]

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
    def min(cls, attrib: str) -> Moon:
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
    def max(cls, attrib: str) -> Moon:
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
