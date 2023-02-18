import argparse
import folium
from geopy.geocoders import Nominatim
from haversine import haversine, Unit


def read_data(path: str) -> list:
    """
    reads data from file about films and return list of tuples with year and the place where it was filmed

    >>> print(read_data("locations.list")[1])
    ('2015', 'Coventry, West Midlands, England, UK')
    """
    with open(path, "r") as fff:
        file = fff.readlines()
    file = file[15:]
    year = ""
    year_location = []
    for jnd, film in enumerate(file):
        for ind, symb in enumerate(film):
            if symb == "(" and 49 <= ord(film[ind + 1]) <= 57:
                year = film[ind + 1:ind + 5]
                break
        file[jnd] = file[jnd].replace("\t", "|")
        file[jnd] = file[jnd].replace("\n", "|")
        file[jnd] = file[jnd].split("|")
        if file[jnd][-2][-1] != ")":
            year_location.append((year, file[jnd][-2]))
        else:
            year_location.append((year, file[jnd][-3]))
    return year_location[:100]

# geolocator = Nominatim(user_agent="get_location")
# location = geolocator.geocode("Старі Кути")
# print(location.latitude)

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
        if not flag and location != None:
            locations.append((location.latitude, location.longitude))
        else:
            continue
    return locations


def distance(location: tuple, locations) -> list:
    """
    """
    distances = []
    for loc in locations:
        try:
            distances.append((haversine(location, loc), loc))
        except:
            continue
    return distances


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

    year_location = read_data(args.path_dataset)

    # year_location = [elm for elm in year_location if int(elm[0]) == args.year]

    locations = get_locations(year_location)

    distances = distance(location, locations)

    map = folium.Map(tiles="Stamen Terrain",
                location=[args.latitude, args.longitude],
                zoom_start=17)
    map.save("map.html")
    

if __name__ == "__main__":
    main()
    # import doctest
    # print(doctest.testmod())
    # print(haversine((49.83826, 24.02324), (53.0666687, -121.5166749)))
    pass
