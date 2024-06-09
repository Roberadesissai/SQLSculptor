import datetime
import database

menu = """\nPlease select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies
4) Add watched movie
5) View watched movies.
6) Add user to the app.
7) Exit.

Your selection: """


def welcome():
    print(f"{'#'*40}\n  Welcome to the movie watchlist app!\n{'#'*40}\n\n")
    database.create_table()


def prompt_add_movie():
    title = input("Movie title: ")
    release_date = input("Release date (dd-mm-YYYY): ")
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()
    print('\n')

    database.add_movie(title, timestamp)

def print_movies_list(heading, movies):
    print(f"\n--- {heading} movies ---")
    for _id, title, release_timestamp in movies:
        movie_date = datetime.datetime.fromtimestamp(release_timestamp)
        human_date = movie_date.strftime("%b %d %Y")
        print(f"{_id}: {title} (on {human_date})")
    print("---- \n")

def prompt_watch_movie():
    username = input("Username: ")
    movie_title = input("movie ID: ")
    database.watch_movie(username, movie_title)


def prompt_show_watched_movies():
    username = input("Username: ")
    movies = database.get_watched_movies(username)
    if movies:
        print_movies_list("Watched", movies)
    else:
        print("That user has not watched any movies yet!")


def prompt_add_user():
    username = input("Username: ")
    database.add_user(username)


while (user_input := input(menu)) != "7":
    database.create_table()
    if user_input == "1":
        prompt_add_movie()
    elif user_input == "2":
        movies = database.get_movies(True)
        print_movies_list("Upcoming", movies)
    elif user_input == "3":
        movies = database.get_movies()
        print_movies_list("All", movies)
    elif user_input == "4":
        prompt_watch_movie()
    elif user_input == "5":
        prompt_show_watched_movies()
    elif user_input == "6":
        prompt_add_user()
    else:
        print("Invalid input, please try again!")

