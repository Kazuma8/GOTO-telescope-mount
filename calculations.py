from skyfield.api import Star, load, Loader
from skyfield.data import hipparcos
from contextlib import closing
import datetime

load = Loader(r'./data')

def hipparcos_search(hip_number):

    with load.open(hipparcos.URL) as f:
        df = hipparcos.load_dataframe(f)
    
    star = Star.from_dataframe(df.loc[hip_number])

    ra, dec = calculate_ra_dec(star)
    return ra, dec


def calculate_ra_dec(target): #can parse class star, or planet as string

    planets_names = ['mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']
    large_planet_moon_ratio = ['mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']

    planets = load('de440.bsp')
    earth = planets['earth']

    if target in planets_names:
        if target in large_planet_moon_ratio: #if planet only has barycentre data
            target = target + ' barycenter'
        target = planets[target] #target is now planet location data

    ts = load.timescale()
    t = ts.now()
    apparent = earth.at(t).observe(target).apparent()
    ra, dec, distance = apparent.radec('date')

    closing('de440.bsp')

    return ra, dec


if __name__ == "__main__":
    #print(hipparcos_search(87937))
    print(calculate_ra_dec("mars"))

