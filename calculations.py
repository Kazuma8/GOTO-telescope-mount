from skyfield.api import Star, load
from skyfield.data import hipparcos


def hipparcos_search(hip_number):

    with load.open(hipparcos.URL) as f:
        df = hipparcos.load_dataframe(f)

    star = Star.from_dataframe(df.loc[hip_number])
    ra, dec = observe(star)
    return ra, dec


def observe(target):

    planets = load('de421.bsp')
    earth = planets['earth']

    if target in planets:
        target = planets[str(target)]

    ts = load.timescale()
    t = ts.now()
    astrometric = earth.at(t).observe(target)
    ra, dec, distance = astrometric.radec('date')
    return ra, dec

if __name__ == "__main__":
    #print(hipparcos_search(87937))
    print(observe("mars"))