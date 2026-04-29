import os
from pathlib import Path
from bs4 import BeautifulSoup
import requests

MOVIES="_static/mago_favorite_movies.html"

def load_html_file(file_path):
    with open(file_path, "r") as handle:
        return handle.read()
    
def write_to_new_html_file(html_file, content):
    with open(html_file, "w") as f:
        f.write(content)
        print(f'File stored in:{Path(__file__).parent.joinpath(f.name)}')


def scrape_for_flags(country: str) -> str:
    """
    Scrapes websites to obtain the country flags for a given country.
    """
    print(f"Scraping for country: {country}")
    SCRAPING_URL="https://flagsapi.com/"
    res= requests.get(SCRAPING_URL, timeout=5)
    print(f"Response for {country}: {res.status_code}")
    if res.status_code == 200:
        soup=BeautifulSoup(res.content, "html.parser")
        tags=soup.find_all('div', class_='item_country cell small-4 medium-2 large-2')
        for tag in tags:
            element=tag.text.splitlines()
            if element[2].strip().lower() == country.strip().lower():
                print(f"Found country: {element[1]}, {element[2]}")
                return element[1].strip().upper()
    return "BE"

def generate_grid(movies: list): #A list of tuples with the movies 
    """
    Generates a grid with the movies in the MOVIES file.
    """
    grid=""

    for movie in movies:
        if movie[7] is not None: # if there is a country for the movie
            countries=movie[7].split(",") # in case there are multiple countries for a movie, we take both countries
            country_codes=[]
            for country in countries:
                country_codes.append(scrape_for_flags(country))
        grid+=f"""
            <li>
            <div class="movie">
                <a href="https://www.imdb.com/title/{movie[1]}/" target="_blank">
                <img class="movie-poster" title="{movie[6]}" src="{movie[5]}" alt="{movie[2]} poster">
                </a>
                """
        for country_code in country_codes:
            grid+=f"""
                <img class="flag" src="https://flagsapi.com/{country_code.upper()}/shiny/64.png" alt="{country_code.upper()} flag">
                """
        grid+=f"""
                <div class="movie-title">{movie[2]}</div>
                <div class="movie-year">{movie[3]}</div>
                <div class="movie-rating">IMDB-Rating: {movie[4]}</div>
                </div>
                </li>
            """
    return grid
         
    
def generate_website(movies, username):
    """
    Generates a website with the movies in the MOVIES file.
    """  
    PAGE_TITLE=f"{username}'s Favorite Films and Series"
    MOVIES=f"_static/{username}_favorite_movies.html"
    TEMPLATE="_static/index_template.html"
    _TITLE_="__TEMPLATE_TITLE__"
    _MOVIE_GRID_="__TEMPLATE_MOVIE_GRID__"
    content=load_html_file(TEMPLATE)
    content=content.replace(_TITLE_, PAGE_TITLE) 
    content=content.replace(_MOVIE_GRID_, generate_grid(movies)) # we take the country of the first movie, but it should be the same for all movies of the user
    write_to_new_html_file(MOVIES, content)   