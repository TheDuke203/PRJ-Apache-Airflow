import csv
import hashlib
import os
dag_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))


# List of station names to gather info for used only for searching.
interest_stations = [
    "AAP",
    "AWM",
    "BFR",
    "BTN",
    "CBG",
    "CMB",
    "CTK",
    "ELY",
    "FPK",
    "FXN",
    "GTW",
    "HIT",
    "HRH",
    "HUN",
    "KGX",
    "KLN",
    "LET",
    "LTP",
    "PBO",
    "PBR",
    "RDH",
    "RYS",
    "STH",
    "STP",
    "SVG",
    "WBC",
    "WGC",
    "ZFD",
]

"""
name, hash,(latitude, longitude)
"""
def get_station_info():
    """
    Returns:
    name, hash,(latitude, longitude)
    """
    stations_info = {}

    # Read CSV file containing station information
    csv_file = csv.reader(open(os.path.join(dag_dir, "Constants", "data", "stations.csv"), "r"))
    next(csv_file, None)
    for row in csv_file:
        stations_info.update(
            {row[3]: [row[0], hash_coordinates(row[1], row[2]), (row[1], row[2])]}
        )

    return stations_info


def tiploc_crs():
    
    tiploc_crs = {}
    
    csv_file = csv.reader(open(os.path.join(dag_dir, "Constants", "data", "cif_tiplocs.csv"), "r"))
    next(csv_file, None)
    for row in csv_file:
        tiploc_crs.update(
            {row[1]: row[0]}
        )

    # stations info format: station name = crs, (latitude, longitude)
    return tiploc_crs

def name_crs():
    tiploc_crs = {}
    
    csv_file = csv.reader(open(os.path.join(dag_dir, "Constants", "data", "cif_tiplocs.csv"), "r"))
    next(csv_file, None)
    for row in csv_file:
        if len(row[0]) > 0:
            tiploc_crs.update(
                {row[2].lower(): row[0]}
            )

    # stations info format: station name = crs, (latitude, longitude)
    return tiploc_crs

def hash_coordinates(lat, long):
    coords = f"{float(lat):.3f},{float(long):.3f}"
    hash = int(hashlib.md5(coords.encode()).hexdigest(), 16)
    return hash % (10**8)