import database

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) Add new user.
4) Watch a movie.
5) View watched movies.
6) Add new movie.
7) Search for a movie.
8) Delete a movie.
9) Exit.

Your selection: """

welcome = "Welcome to the watchlist app!"

print(welcome)

database.create_tables()

while (user_input := input(menu)) != "9":
    if user_input == "1":
        name = input("Enter movie name: ")
        release_timestamp = input("Enter release timestamp: ")
        database.add_movie(name, release_timestamp)
    elif user_input == "2":
        movies = database.get_movies(upcoming=True)
        for movie in movies:
            movie_data = (movie[1], movie[2])
            print(f"{movie_data[0]} (on {movie_data[1]})")
    elif user_input == "3":
        username = input("Enter username: ")
        database.add_user(username)
    elif user_input == "4":
        username = input("Username: ")
        movie_id = input("Movie ID: ")
        database.watch_movie(username, movie_id)
    elif user_input == "5":
        username = input("Username: ")
        movies = database.get_watched_movies(username)
        for movie in movies:
            print(movie[1])
    elif user_input == "6":
        pass
    elif user_input == "7":
        search_term = input("Enter search term: ")
        movies = database.search_movies(search_term)
        for movie in movies:
            print(movie[1])
    elif user_input == "8":
        title = input("Enter movie title: ")
        database.delete_movie(title)
    else:
        print("Invalid input, please try again!")