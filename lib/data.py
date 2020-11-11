
import requests as cURL
from urllib.parse import urljoin
import json

API_BASE = "https://api.le-systeme-solaire.net/rest/bodies/"
REQ_HEADERS = {
    'user-agent': 'SolarSystemModeler ()'
}

def get_planet_data(name):
    """
    name: str (The english name of a planet in the solar system) 
    Returns a python dict representing the returned JSON for planetary data, or None if the requested planet is not available
    """
    req = cURL.get(urljoin(API_BASE, name))
    try:
        planet = json.loads(req.text)
    except json.decoder.JSONDecodeError:
        print('planet does not exist...')
        planet = None
    finally:
        return planet

def get_moon_data(rel):
    """
    rel: str (The API URL to the english nae of a moon in the solar system. [eg. 'https://api.le-systeme-solaire.net/rest/bodies/lune'])
    Returns a python dict representing the returned JSON for moon data, or None if the requested planet if not available"""
    req = cURL.get(rel)
    try:
        moon = json.loads(req.text)
    except json.decoder.JSONDecodeError:
        print('moon does not exist...')
        moon = None
    finally:
        return moon
