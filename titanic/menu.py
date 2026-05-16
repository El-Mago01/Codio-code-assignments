import ship_coordination_module as scm
import ship_data_handler as sdh

TOP_X = 10


def print_help_message(all_ships: list, args: int = 0) -> None:
    """
    prints the help message with all available commands
    :return:
    """
    print("Available commands:")
    for command in FUNCTIONS:
        print(command)
    print("")


FUNCTIONS = {
    "help": print_help_message,
    "show_countries": scm.print_all_countries_no_duplicates,
    "top_countries <top x countries>": scm.print_top_countries,
    "ship_by_type": scm.print_ships_by_types,
    "search_ship": scm.search_ship,
    "speed_histogram": scm.plot_speed_histogram,
    "map_current_location": scm.map_with_locations_of_ships,
}


def get_user_command() -> tuple:
    """
    Get correct user input. Don't accept any BS
    :return: a tuple (command, argument). Argument is provided with some
    commands
    """
    while True:
        int_arg = 0
        command = input("> ")
        split_command = command.split(" ")
        main_command = split_command[0]
        if main_command == "top_countries":
            # input indicates 'top_countries'. Now check the argument
            if len(split_command) > 2:
                print("Invalid number of arguments, should be 1.")
                continue
            if len(split_command) == 2:
                try:
                    int_arg = int(split_command[1])
                    return main_command + " <top x countries>", int_arg
                except ValueError:
                    print("Invalid argument, wrong type.")
                    continue
            elif len(split_command) == 1:
                # input indicating 'top_countries', but without argument
                return main_command + " <top x countries>", TOP_X
        elif main_command in FUNCTIONS:
            if len(split_command) > 1:
                print(
                    "Invalid number of arguments. Should be 1, you provided ",
                    len(split_command),
                )
                continue
            return main_command, -1
        else:
            print("Invalid command...")


def welcome_user():
    """
    Welcome the user
    """
    print("Welcome to the Ships CLI! Enter 'help' to view available commands.")


def main():
    """
    Fetch the json file with all ships.
    Ask for commands from the user.
    handle the commands in the right manner
    """
    ship_data = sdh.get_all_ship_data()
    if len(ship_data) == 0:
        print("No shipping data")
        return -1
    all_ships = ship_data
    welcome_user()
    while True:
        command, arg = get_user_command()
        if arg == -1:
            FUNCTIONS[command](all_ships)
        else:
            FUNCTIONS[command](all_ships, arg)


if __name__ == "__main__":
    main()
