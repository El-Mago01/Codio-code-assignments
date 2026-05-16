"""
Analyzes the provided json with shipping data and accepts user commands
to get relevant data for the user.
"""
from threading import Thread
import os
import sys
import webbrowser
import socketserver
import http.server
import seaborn as sns
import folium
import matplotlib.pyplot as plt
import ship_data_handler as sdh

TOP_X = 10
OUTPUT_DIR = "static"


def pretty_print(types_of_ships_frequency):
    """
    Nicely print the types and their frequencies
    :param types_of_ships_frequency:
    :return:
    """
    print("The types of ships and the frequencies in our data")
    print(f"{"Type":20}Frequency")
    print("=====================================================")
    for ship_type in types_of_ships_frequency:
        print(f"{ship_type:20}{types_of_ships_frequency[ship_type]}")


def print_ships_by_types(all_ships: list) -> list:
    """
    Algortihm:
    1. Check the available types of ships in the data
    2. Create a dictionary of types of ships and their frequencies
    3. Print the types of ships and the frequencies
    :param all_ships:
    :param args:
    :return:
    """
    # 1. Check the available types of ships in the data
    types_of_ships = []
    for ship in all_ships:
        ship_type = ship["TYPE_SUMMARY"]
        types_of_ships.append(ship_type)
    available_types = set(types_of_ships)
    types_of_ships_frequency = {}
    for available_type in available_types:
        types_of_ships_frequency[available_type] = types_of_ships.count(
            available_type)
    pretty_print(types_of_ships_frequency)


def pretty_print_ships_found(ships_found, search_string):
    """
    Nicely print the found ships using the search string
    :param types_of_ships_frequency:
    :return:
    """
    print(f"Found {len(ships_found)} ships matching {search_string}")
    print(f"{"Ship ID":10}{"Ship Name":35}{"Ship Type":20}{"Destination":20}")
    print("==========================================================================")
    for ship in ships_found:
        try:
            if ship["DESTINATION"] is None:
                ship["DESTINATION"] = ""
            print(
                f'{
                    ship["SHIP_ID"]:10}{
                    ship["SHIPNAME"]:35}{
                    ship["TYPE_SUMMARY"]:20}{
                        ship["DESTINATION"]:20}')
        except (KeyError, TypeError):
            print(f"Could not print ship {ship['SHIP_ID']}, ship[{ship['SHIPNAME']}]")


def search_ship(all_ships: list) -> list:
    """
    searches for a shipname or part of the shipname  in the JSON using the search_string
    and 3 search variants expressed by match_type (int)
    :param search_string: the name or part of the shipname you want to search for
    :param match_type: the type of match you want to use (int)

    match_type 0 => not exact & case-insensitive
    match_type 1 => matching characters, but case-insensitive and stripped
    match_type 2 => exact match, and case-sensitive
    :return: a list with all the found ships
    """

    def get_valid_search_input():
        s_string = input("Please enter a search string: ")
        return s_string

    search_string = get_valid_search_input()
    ships_found = list(sdh.search_ship_name(search_string, all_ships))
    pretty_print_ships_found(ships_found, search_string)
    return ships_found


def plot_speed_histogram(all_ships: list) -> list:
    """
    Algortihm:
    1. fetch velocity data for all ships
    2. Create a speed histogram from this data
    3. ask for a filename and save as png
    :param all_ships:
    :param args:
    :return:
    """
    velocity = []
    for ship in all_ships:
        try:
            velocity.append(float(ship["SPEED"]))
        except KeyError:
            print(
                "No speed data for this ship",
                ship["SHIP_ID"],
                ship["SHIP_NAME"])
        except ValueError:
            print(
                "available velocity has not the right format for",
                ship["SHIP_ID"],
                ship["SHIPNAME"],
            )
    print(velocity)
    sns.set()
    sns.set_style("white")
    plt.figure(figsize=(8, 6))
    bins = [
        1,
        2,
        4,
        6,
        8,
        10,
        12,
        14,
        16,
        18,
        20,
        22,
        24,
        26,
        28,
        30,
        32,
        34,
        36,
        38,
        40,
    ]
    plt.hist(velocity, bins=bins, edgecolor="black", color="#108A99")
    plt.title("Histogram of speed of the ships", fontsize=14, weight="bold")
    plt.xlabel("Speed of the ships", fontsize=14)
    plt.xlabel("speed (knot)")
    plt.ylabel("frequency")
    plt.tight_layout()
    sns.despine()
    plt.show()
    OUTPUT_FILE = os.path.join(OUTPUT_DIR, "histogram.png")
    plt.savefig(OUTPUT_FILE)
    sys.stdout.flush()
    print("File histogram.png is created and stored in: ", OUTPUT_FILE)


def start_socket_server():
    """
    Start the socket server to listen to port 8000 on localhost so that it
    can show automatically the html file with the ship location information
    as soon as it is generated
    :return:
    """
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()


def map_with_locations_of_ships(all_ships: list):
    """
    Algorithm
    1. From the ships data get all the ship locations, i.e. the latitude
    and longitude
    3. Use plot_map_current_location function to draw the map with the current
    locations,
    4. Generate a html file with a map showing those locations
    5. Start a local host socket_server to show this web-page
    """
    output_html = os.path.join(OUTPUT_DIR, "ships_locations.html")
    this_map = plot_map_current_location(all_ships)
    this_map.save(output_html)

    print(f"File saved to {output_html}. Open it in browser to see the map.")
    open_in_browser = input("Do you want to see it in the browser? (y/n)")

    if open_in_browser.lower() == "y" or open_in_browser.lower() == "yes":
        print("Starting new thread to open localhost:8000")
        try:
            start_socket_server()
            thread = Thread(target=start_socket_server)
            thread.start()
        except KeyboardInterrupt:
            print("Ship location tracking stopped")
            thread.do_run = False
        except OSError:
            print("Ship location tracking stopped")
            thread.do_run = False

        print("Thread started")
        webbrowser.open("http://localhost:8000/" + output_html, new=2)
        # print("Browser should be opening now.")
    # input("Press Enter to continue...")


def plot_map_current_location(all_ships: list):
    """
    The following code is based upon the use of folium library,
    see also the following excellent Video:
    https://www.youtube.com/watch?v=j8tGVhaciNo

    Initialize the location_map from it's starting location, ie. Amsterdam, Netherlands
    together with the zoom level. Adjust
    this level to show the whole US.
    Store this as m, which will be our map visualization.
    """
    m = folium.Map(
        location=[52.3730796, 4.8924534], zoom_start=3
    )  # Starting from the center of the world.

    for ship in all_ships:
        # For each ship:

        # Get the coordinates for the longitude and latitude for both the
        # origin and destination
        location = [float(ship["LAT"]), float(ship["LON"])]

        # Build location point on the map
        folium.Marker(
            location,
            popup=ship["SHIPNAME"],
            icon=folium.Icon(
                prefix="fa",
                icon="ship")).add_to(m)
    return m


def get_all_countries_no_duplicates(all_ships) -> set:
    """
    Derives all the available countries without duplicates as a set
    :param all_ships:
    :return: a set of countries without duplicates
    """
    countries = set(ship["COUNTRY"] for ship in all_ships)
    return countries


def get_all_countries(all_ships) -> list:
    """
    Derives all the available countries in the dictionary as a list. This
    list will contain duplicates
    :param all_ships:
    :return: list
    """
    countries = list(ship["COUNTRY"] for ship in all_ships)
    return countries


def frequency_of_countries(all_ships: list) -> list:
    """
    returns a list with tuples holding the available countries in the json file and
    the frequency per country
    :param all_ships: All ships in the json file
    :return:
    """
    all_countries = get_all_countries(all_ships)
    country_frequency = {}
    for country in all_countries:
        freq = all_countries.count(country)
        country_frequency[country] = freq
    sorted_countries_frequency = sorted(
        country_frequency.items(), key=lambda x: x[1], reverse=True
    )
    return sorted_countries_frequency


def print_top_countries(all_ships, top: int = 10):
    """
    print the top X countries and their frequencies in the json file.
    If X is not provided, 10 is chosen.
    """
    freq_of_countries = frequency_of_countries(all_ships)

    for place in range(top):
        print(
            f"{place + 1:4}. {freq_of_countries[place][0]:25} - {freq_of_countries[place][1]}"
        )


def print_all_countries_no_duplicates(all_ships) -> set:
    """
    Prints all the countries without duplicates as a list
    :param all_ships:
    :return: all countries without duplicates
    """
    all_countries = get_all_countries_no_duplicates(all_ships)
    print("There are ", len(all_countries), "countries (without duplicates).")
    for country in all_countries:
        print(country)
    return all_countries
