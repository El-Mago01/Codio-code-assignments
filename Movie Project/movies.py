import os
import statistics
import random

# Algorithm:
# =============================
# step 10: show the menu numbered from 1-8 and ask for input
# step 20: check that the provided input is a number from 1-8, if not, clear the screen and show the menu again.
# step 30: execute the desired CRUD function or analysis function
# step 40: show the results to screen
# step 50: ask for an enter to continue
# step 60: after enter is provided, start from 10 again.

def clear_screen():
    if os.name=='nt':
        os.system('cls')
    else:
        os.system('clear')

def is_float(string:str) -> bool:
    try:
        float(string)
    except ValueError:
        return False
    return True


def show_menu():
    menu_string = ("** ** ** ** ** My Movies Database ** ** ** ** ** \n\n"
                   "Menu: \n1. List movies\n2. Add movie\n3. Delete movie\n"
                   "4. Update movie\n5. Stats\n6. Random movie\n7. Search movie\n"
                   "8. Movies sorted by rating\n\n"
                   )
    correct_input_provided = False
    while correct_input_provided is False:
        clear_screen() # clears the screen
        print(menu_string)
        input_selection=input("Enter choice(1 - 8):")
        if input_selection.isnumeric() and (1 <= int(input_selection) <= 8):
            correct_input_provided = True
            input_selection=int(input_selection)
        if correct_input_provided == False:
            input("Input should be between 1-8. Press enter to continue")
    return input_selection

def list_movies(movies:dict):
    print(f"{len(movies)} movies in total")
    for movie in movies:
        print(f"{movie}: {movies[movie]}")

def get_correct_movie_input() -> tuple:
    correct_input_provided = False
    while correct_input_provided is False:
        movie = input("Enter movie name: ")
        rating = input("Enter new movie rating: ")
        if is_float(rating):
            correct_input_provided = True
            rating=float(rating)
        if correct_input_provided == False:
            input("Input provide valid input. Press enter to continue")
    return movie, rating, correct_input_provided

def add_movie(movies:dict) -> bool:
    movie, rating, correct_input_provided=get_correct_movie_input()
    if not correct_input_provided: # if correct input was provided (this should always be True
        print("Movie can not be added, wrong input")
        return False
    found_movies=search_movies(movies,movie,1)
    if len(search_movies(movies,movie,1))>0 :#search case-insensitive, but matching characters
        print(f"Movie {movie} is already stored")
        return False

    movies[movie] = float(rating)
    print(f"Movie {movie} successfully added")
    return True

def delete_movie(movies:dict, movie_to_delete:str) -> bool:
    try:
        movies.pop(movie_to_delete)
    except:
        print(f"Movie {movie_to_delete} doesn't exist!")
        return False
    return True

def update_movie(movies:dict) -> str:
    movie_to_update, new_rating, correct_input_provided = get_correct_movie_input()
    movies_found=search_movies(movies,movie_to_update,2)
    if len(movies_found) > 0: # in case there is an exact match already
        movies.update({movie_to_update: new_rating})
        return movie_to_update
    else:
        return ""

def max_min_rating_movie(movies: dict) -> tuple:
    min_rating = min(movies.values())
    max_rating = max(movies.values())
    worst_movie = ""
    best_movie = ""
    for movie in movies:
        if movies[movie] == min_rating:
            worst_movie+=movie + " + " # in case 2 movies have the worst rating
        if movies[movie] == max_rating:
            best_movie+=movie + " + " # in case 2 movies have the best rating
    if best_movie == "":
        best_movie = "Not found + "
    if worst_movie == "":
        worst_movie = "Not found + "
    return best_movie[0:-3],worst_movie[0:-3] # slicing to remove the + at the end

def show_stats(movies:dict):
    print("values: ", movies.values())
    average_rating=sum(movies.values())/len(movies)
    median_rating=statistics.median(list(movies.values()))
    print(f"Average rating: {average_rating}")
    print(f"Median rating: {median_rating}")
    print(f"Best movie: {max_min_rating_movie(movies)[0]}")
    print(f"Worst movie: {max_min_rating_movie(movies)[1]}")

def select_random_movie(movies:dict) -> tuple:
    #Your movie for tonight: Star Wars: Episode V, it's rated 8.7
    random_movie=random.choice(list(movies.keys()))
    print(f"Your movie for tonight: {random_movie}, it's rated {movies[random_movie]}")
    return random_movie, movies[random_movie]

def search_movies(movies:dict, search_string, match_type:int=0) -> tuple:
    # match_type 0 => not exact & case-insensitive
    # match_type 1 => matching characters, but case-insensitive
    # match_type 2 => exact match, and case-sensitive
    if match_type >2 or match_type<0:
        print(f"Coding error, match_type var out of bound. Value {match_type}")
        return "Coding Error", search_string, 0
    movies_found={}
    movies_names = movies.keys()
    for movie in movies_names:
        if ((search_string.lower() in movie.lower() and match_type == 0) or
                (search_string.lower() == movie.lower() and match_type == 1) or
                (search_string == movie and match_type == 2)):
            movies_found[movie]=movies[movie]
    return movies_found

def sort_by_rating(movies:dict) -> list:
    movie_list=movies.items()
    sorted_list=sorted(movie_list,key=lambda tup: tup[1], reverse = True) #sorts the list of tuples based on the rating (tup[1])
    print()
    for movie,rating in sorted_list:
        print(f"{movie}: {rating}")
    return sorted_list

def main():
    # Dictionary to store the movies and the rating
    movies = {
        "The Shawshank Redemption": 9.5,
        "Pulp Fiction": 8.8,
        "The Room": 3.6,
        "The Godfather": 9.2,
        "The Godfather: Part II": 9.0,
        "The Dark Knight": 9.0,
        "12 Angry Men": 8.9,
        "Everything Everywhere All At Once": 8.9,
        "Forrest Gump": 8.8,
        "Star Wars: Episode V": 8.7
    }
    no_interrupt=True
    while no_interrupt:
        menu_selection=show_menu()
        if menu_selection == 1:
            list_movies(movies)
        if menu_selection == 2:
            add_movie(movies)
        if menu_selection == 3:
            movie_to_delete = input("Enter movie name to delete: ")
            if delete_movie(movies,movie_to_delete):
                print(f"Movie {movie_to_delete} successfully deleted")
        if menu_selection == 4:
            updated_movie=update_movie((movies))
            if len(updated_movie) > 0:
                print(f"Movie {updated_movie} successfully updated")
            else:
                print(f"Movie doesn't exist!")
        if menu_selection == 5:
            show_stats(movies)
        if menu_selection == 6:
            select_random_movie(movies)
        if menu_selection == 7:
            search_string = input("\nEnter part of movie name:")
            found_movies = search_movies(movies,search_string, 0)
            for movie in found_movies:
                print (f"{movie}, {found_movies[movie]}")

        if menu_selection == 8:
            sort_by_rating(movies)
        input("\nPress enter to continue")

if __name__ == "__main__":
    main()
