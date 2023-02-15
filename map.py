import argparse
import folium
from geopy.geocoders import Nominatim
from haversine import haversine, Unit
from geopy import GeocodeUnavailable


def read_data(path: str) -> list:
    """
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
    return year_location


def main():
    """
    """
    parser = argparse.ArgumentParser(description="argpars")

    parser.add_argument("year", type=str)
    parser.add_argument("latitude", type=str)
    parser.add_argument("longitude", type=str)
    parser.add_argument("path_dataset", type=str)
    args = parser.parse_args()
    
    year_location = read_data(args.path_dataset)
    year_location = [elm for elm in year_location if elm[0] == args.year]

    map = folium.Map(tiles="Stamen Terrain",
                location=[args.latitude, args.longitude],
                zoom_start=17)
    map.save("map.html")
    

if __name__ == "__main__":
    main()
