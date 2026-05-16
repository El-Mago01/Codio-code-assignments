import json
import os

STORAGE_PATH = "storage"
JSON_FILE = "ships_data.json"

def get_all_ship_data():
    """
    opens the titanic data json file and returns it as a dictionary
    :return: dictionary with titanic dictionary
    """
    json_path = os.path.join(STORAGE_PATH, JSON_FILE)
    print("opening ship data json file")
    try:
        with open(json_path) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error, could not open data file {json_path}")
        data = {}
    if "data" not in data:
        print("No ship data found, please check the path of the json file")
        return data
    return data["data"]


def search_ship_name(search_string: str, all_ships) -> list:
    ships_found = []
    for ship in all_ships:
        if search_string.lower() in ship["SHIPNAME"].lower():
            ships_found.append(ship)
    return ships_found
