
import requests as cURL
from urllib.parse import urljoin
import json

API_BASE = "https://api.le-systeme-solaire.net/rest/bodies/"
REQ_HEADERS = {
    'user-agent': 'SolarSystemModeler ()'
}

def get_planet_data(name: str, debug: bool = False) -> dict:
    """
    name: str (The english name of a planet in the solar system) 
    debug: bool (enables debug messages)
    Returns a python dict representing the returned JSON for planetary data, or None if the requested planet is not available
    """
    req = cURL.get(urljoin(API_BASE, name))
    print(f"""
    req data: {req.text}
    req status: {req.status_code}
    """) if debug else None
    try:
        planet = json.loads(req.text)
    except json.decoder.JSONDecodeError:
        print(f"INFO: planet with name {name} does not exist...") if debug else None
        planet = None
    finally:
        return planet

def get_moon_data(rel: str, debug: bool = False) -> dict:
    """
    rel: str (The API URL to the english nae of a moon in the solar system. [eg. 'https://api.le-systeme-solaire.net/rest/bodies/lune'])
    debug: bool (enables debug messages)
    Returns a python dict representing the returned JSON for moon data, or None if the requested planet if not available"""
    req = cURL.get(rel)
    print(f"""
    req data: {req.text}
    req status: {req.status_code}
    """) if debug else None
    try:
        moon = json.loads(req.text)
    except json.decoder.JSONDecodeError:
        moon = None
    finally:
        return moon

def get_sun_data(debug: bool = False) -> dict:
    """
    debug: bool ()
    Returns a python dict representing the returned JSON for sun (sol) data, or None if the requested star if not available"""
    req = cURL.get("https://api.le-systeme-solaire.net/rest/bodies/sun")
    print(f"""
    req data: {req.text}
    req status: {req.status_code}
    """) if debug else None
    try:
        sun = json.loads(req.text)
    except json.decoder.JSONDecodeError:
        sun = None
    finally:
        return sun

def get_body_data(ident: str) -> dict:
    """
    ident: str (arbitrary celestial body ID value from SolarSystem Open Data)
    Returns: dictionary containg arbitrary body by ID.
    """
    req = cURL.get(urljoin(API_BASE, ident))
    try:
        obj = json.loads(req.text)
    except json.decoder.JSONDecodeError:
        obj = None 
    finally:    
        return obj

def getknowncount(ident: str) -> int:
    """
    ident: str (known counts available in database for referenced object)
    returns int containing count for referenced category of celestial objects
    Returns: int
    """
    req = cURL.get(urljoin("https://api.le-systeme-solaire.net/rest/knowncount/", ident))
    try:
        obj = json.loads(req.text)['knownCount']
    except json.decoder.JSONDecodeError:
        obj = None 
    finally:    
        return obj

def getknown() -> dict:
    """
    Queries database for knowncount by category
    Returns: dict
    """
    req = cURL.get("https://api.le-systeme-solaire.net/rest/knowncount")
    try:
        obj = json.loads(req.text).get('knowncount',None)
    except json.decoder.JSONDecodeError:
        obj = None 
    finally:    
        return obj

def getbodies() -> list:
    """
    Returns: dict
    """
    req = cURL.get("https://api.le-systeme-solaire.net/rest/bodies")
    try:
        obj = json.loads(req.text)
        obj = obj['bodies']
    except json.decoder.JSONDecodeError:
        obj = None 
    finally:    
        return obj

def findbodies(attrib: str, val) -> list:
    """
    attrib: str (attribute name)
    val: str (attribute value)
    Return all known bodies as dictionary
    Returns: dict
    """
    req = cURL.get("https://api.le-systeme-solaire.net/rest/bodies")
    try:
        obj = json.loads(req.text)
        obj = obj['bodies']
        obj = [i for i in obj if i[attrib] == val]
    except json.decoder.JSONDecodeError:
        obj = None 
    finally:    
        return obj


def getknowntypes() -> list:
    """
    Return known categories of bodies
    Returns: list 
    """
    req = cURL.get("https://api.le-systeme-solaire.net/rest/knowncount")
    try:
        obj = json.loads(req.text)
        obj = obj['knowncount']
        obj = [i['id'] for i in obj]
    except json.decoder.JSONDecodeError:
        obj = None 
    finally:    
        return obj

