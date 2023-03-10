"""
Search nearest locations of films
"""
import argparse
import folium
from geopy.geocoders import Nominatim
from haversine import haversine


def read_data(path: str, year_film: int) -> list:
    """
    reads data from file about films and return list of tuples with year and the place where it was filmed

    >>> print(read_data("locations.list", 2015)[1])
    ('2015', 'West Hills, California, USA')
    """
    with open(path, "r") as fff:
        file = fff.readlines()
    file = file[15:]
    year = ""
    year_location = []
    for jnd, film in enumerate(file):
        for ind, symb in enumerate(film):
            if symb == "(" and 48 <= ord(film[ind + 1]) <= 57 and 48 <= ord(film[ind + 2]) <= 57 and\
                48 <= ord(film[ind + 3]) <= 57 and 48 <= ord(film[ind + 4]) <= 57:
                year = film[ind + 1:ind + 5]
                break
        file[jnd] = file[jnd].replace("\t", "|")
        file[jnd] = file[jnd].replace("\n", "|")
        file[jnd] = file[jnd].split("|")
        if file[jnd][-2][-1] != ")" and year_film == int(year):
            year_location.append((year, file[jnd][-2]))
        elif year_film == int(year):
            year_location.append((year, file[jnd][-3]))
    return year_location[:80]


def get_locations(year_location: list) -> list:
    """
    gets locations of all films

    >>> get_locations([('2000', 'Montenegro')])
    [(42.9868853, 19.5180992)]
    """
    locations = []
    for tpl in year_location:
        geolocator = Nominatim(user_agent="get_location")
        tpl_split = tpl[1].split(",")
        flag = True
        for elm in tpl_split:
            try:
                location = geolocator.geocode(elm.strip())
                flag = False
                break
            except:
                continue
        if not flag and location is not None:
            locations.append((location.latitude, location.longitude))
        else:
            continue
    return locations


def distance(location: tuple, locations: list) -> list:
    """
    get distances from your location to every location of films

    >>> list(distance((53.0162014, -2.1812607), [(42.9868853, 19.5180992), (41.0671774, 29.0432713)]))
    [(1949.7846486566084, (42.9868853, 19.5180992)), (2682.981082694581, (41.0671774, 29.0432713))]
    """
    for loc in locations:
        try:
            yield (haversine(location, loc), loc)
        except:
            continue


def main():
    """
    """
    parser = argparse.ArgumentParser(description="argpars")

    parser.add_argument("year", type=int)
    parser.add_argument("latitude", type=float)
    parser.add_argument("longitude", type=float)
    parser.add_argument("path_dataset", type=str)
    args = parser.parse_args()

    location = (args.latitude, args.longitude)

    year_location = read_data(args.path_dataset, args.year)

    locations = get_locations(year_location)

    distances = list(distance(location, locations))

    distances = sorted(distances)

    map = folium.Map(tiles="Stamen Toner",
                location=list(location),
                zoom_start=3)

    for ind in range(10):
        map.add_child(folium.Marker(distances[ind][1],
                                    icon=folium.Icon()))

    map.add_child(folium.Marker(location,
                                icon=folium.Icon(color='red')))

    map.add_child(folium.LayerControl())

    map.save("map1.html")


if __name__ == "__main__":
    main()
