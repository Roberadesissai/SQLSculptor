import datetime
import database
import database

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies.
4) watch a movie.
5) view watched movies.
6) Exit.

Enter your choice: """


def welcome():
    print(f"{'#'*40}\n  Welcome to the movie watchlist app!\n{'#'*40}\n\n")
    database.create_table()

def prompt_add_movie():
    title = input("Movie title: ")
    release_date = input("Release date (dd-mm-YYYY): ")
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()

    database.add_movie(title, timestamp)

def print_movies_list(heading, movies):
    print(f"\n-- {heading} movies --")
    for movie in movies:
        movie_date = datetime.datetime.fromtimestamp(movie[1])
        human_date = movie_date.strftime("%b  %d %Y")
        print(f"{movie[0]} (on {human_date})")
    print("---- \n")




if __name__ == "__main__":
    welcome()
    while (user_input := input(menu)) != "6":
        if user_input == "1":
            prompt_add_movie()
        elif user_input == "2":
            movies = database.get_movies(True)
            print_movies_list("Upcoming",movies)
        elif user_input == "3":
            movies = database.get_movies()
            print_movies_list("All", movies)
        elif user_input == "4":
            pass
        elif user_input == "5":
            pass
        else:
            print("Invalid input, please try again!")

