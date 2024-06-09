import configparser
import os
import sys
import csv
import time
from tqdm import tqdm
from tabulate import tabulate
from resource.login import Options
from db.model import MovieModel, UserModel      
from utils.openai_helper import OpenAIHelper
from services.account_service import AccountService

class MenuSystem():
    def __init__(self):
        self.openai_helper = OpenAIHelper()
        self.options = Options()
        self.movie_model = MovieModel()
        self.user_model = UserModel()
        self.account_service = AccountService()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def loading_percentage(self, total_time):
        for i in range(101):
            print(f'\rLoading... {i}%', end='')
            time.sleep(total_time / 100)
        print()  # For new line after completion



    def user_menu(self):
        print("##########################################")
        print("Welcome to Maver, the movie recommender AI")
        print("---Please login or register to continue---")
        print("##########################################")
        print()
        print("   1. Login")
        print("   2. Register")
        print("   3. Exit")
        print()
        print("##################################")
        print("##################################")

    def login_flow(self):
        while True:
            print("\n==== Login ====\n")
            username = input("Enter Username (or type 'exit' to quit): ").strip().title()
            
            if username == 'Admin':
                self.clear()
                print("\n----Admin Login is not allowed----.\n")
            elif username == 'Exit':
                self.clear()
                print("Exiting...")
                sys.exit()
            elif not self.account_service.validate_username(username):
                self.clear()
                print(f'\n{"-"*40}\nInvalid Username. Must be at least 5 characters long and can include letters, numbers, and underscores.\n{"-"*40}\n')
            else:
                password = self.account_service.get_password("Enter Password: ")
                print("\nAuthenticating...")
                self.loading_percentage(2)
                if self.account_service.login(username, password):
                    self.clear()
                    return username
                else:
                    self.clear()
                    print("\n==== Invalid Username or Password, Please Try Again ====\n")
            self.user_menu()

    def register_flow(self):
        while True:
            username = self.account_service.get_valid_username()
            email = self.account_service.get_valid_email()
            password = self.account_service.get_valid_password()
            if self.account_service.register(username, email, password):
                self.clear()
                return username
            else:
                print("Registration Failed, Please Try Again")
                self.user_menu()


        
    def main_menu(self, username):
        while True:
            print("\n##########################################")
            print("Welcome to Maver, the movie recommender AI")
            print("---Please Select an Option to Continue---")
            print("##########################################")
            print()
            print('   Logged in as: ' + username)
            print()
            print("   1. Get Movie Recommendation")
            print("   2. Generate Movie Idea")
            print("   3. Add a New Movie")
            print("   4. Rate a Movie")
            print("   5. Search Movies")
            print("   6. Manage Users")
            print("   7. View Movie Details")
            print("   8. Generate by region")
            print("   9. Generate Reports")
            print("   10. Toggle Auto-Login")
            print("   11. Exit")
            print()
            print("##################################")
            print("##################################")

            choice = input("\nEnter Option: ")

            if choice == '1':
                self.clear()
                self.recommendation_menu()
            elif choice == '2':
                self.clear()
                self.generate_movie_idea()
            elif choice == '3':
                self.clear()
                self.add_new_movie()
            elif choice == '4':
                self.clear()
                self.rate_movie()
            elif choice == '5':
                self.clear()
                self.search_movies()
            elif choice == '6':
                self.clear()
                self.manage_users()
            elif choice == '7':
                self.clear()
                self.view_movie_details()
            elif choice == '8':
                self.generate_by_region()
            elif choice == '9':
                self.clear()
                self.generate_reports()
            elif choice == '10':
                self.clear()
                self.account_service.toggle_auto_login(username)
            elif choice == '11':
                self.clear()
                self.account_service.logout(username)
                while True:
                    self.user_menu()
                    user_input = input("Enter Option: ")
                    if user_input == '1':
                        username = self.login_flow()
                        if username:
                            self.clear()
                            self.main_menu(username)
                    elif user_input == '2':
                        username = self.register_flow()
                        if username:
                            self.clear()
                            self.main_menu(username)
                    elif user_input == '3':
                        print("Goodbye!")
                        sys.exit()
                    else:
                        self.clear()
                        print("\n==== Invalid Option, Please Try Again ====\n")

                
           


    def recommendation_menu(self):
        while True:
            print("\n##########################################")
            print("Welcome to Maver, the movie recommender AI")
            print("---Please Select an Option to Continue---")
            print("##########################################")
            print()
            print("   1. Recommend Movies by Genre")
            print("   2. Recommend Movies by Rating")
            print("   3. Recommend Movies by Year")
            print("   4. Recommend Movies by Director")
            print("   5. Go Back")
            print()
            print("##################################")
            print("##################################")

            choice = input("\nEnter Option: ")

            if choice == '1':
                genre = input("Enter Genre: ")
                self.clear()
                print("Recommendation based on Genre: " + genre + "\n")
                recommendations = self.openai_helper.recommend_movies_by_genre(genre)
                print(recommendations)
            elif choice == '2':
                rating = input("Enter Rating: ")
                self.clear()
                print("Recommendation based on Rating: " + rating + "\n")
                recommendations = self.openai_helper.recommend_movies_by_rating(rating)
                print(recommendations)
            elif choice == '3':
                year = input("Enter Year: ")
                self.clear()
                print("Recommendation based on Year: " + year + "\n")
                recommendations = self.openai_helper.recommend_movies_by_year(year)
            elif choice == '4':
                director = input("Enter Director: ")
                self.clear()
                print("Recommendation based on Director: " + director + "\n")
                recommendations = self.openai_helper.recommend_movies_by_director(director)
                print(recommendations)
            elif choice == '5':
                self.clear()
                break

    def generate_movie_idea(self):
        while True:
            print("\n##########################################")
            print("Welcome to Maver, the movie recommender AI")
            print("---Please Select an Option to Continue---")
            print("##########################################")
            print()
            print("   1. Generate a movie plot based on genre")
            print("   2. Generate a movie plot based on random keywords")
            print("   3. Generate a movie plot based on current trends")
            print("   4. Go Back")
            print()
            print("##################################")
            print("##################################")

            choice = input("\nEnter Option: ")

            if choice == '1':
                genre = input("Enter Genre: ")
                self.clear()
                print("Generating movie plot based on genre: " + genre + "\n")
                plot = self.openai_helper.generate_movie_plot_based_on_genre(genre)
                print("Generated Plot:\n", plot)
            elif choice == '2':
                keywords = input("Enter Keywords: ")
                self.clear()
                print("Generating movie plot based on keywords: " + keywords + "\n")
                plot = self.openai_helper.generate_movie_plot_based_on_keywords(keywords)
                print("Generated Plot:\n", plot)
            elif choice == '3':
                self.clear()
                print("Generating movie plot based on trends\n")
                plot = self.openai_helper.generate_movie_plot_based_on_trends()
                print("Generated Plot:\n", plot)
            elif choice == '4':
                self.clear()
                break

    def add_new_movie(self):
        while True:
            print("\n##########################################")
            print("Welcome to Maver, the movie recommender AI")
            print("---Please Select an Option to Continue---")
            print("##########################################")
            print()
            print("   1. Enter movie details manually")
            print("   2. Upload a CSV file with movie details")
            print("   3. Go Back")
            print()
            print("##################################")
            print("##################################")
            
            choice = input("\nEnter Option: ")

            if choice == '1':
                self.clear()
                title = input("Enter Title (required): ")
                release_date = input("Enter Release Date (required, YYYY-MM-DD): ")
                genre = input("Enter Genre (required): ")
                description = input("Enter Description (optional): ") or None
                director = input("Enter Director (optional): ") or None
                rating = input("Enter Rating (optional): ") or None
                self.movie_model.add_new_movie(title, release_date, genre, description, director, rating)
                print("Movie added successfully\n")
            elif choice == '2':
                self.clear()
                print("Upload a CSV file with movie details\n")
                file_path = input("Enter file path: ")
                try:
                    with open(file_path, mode='r') as file:
                        csv_reader = csv.DictReader(file)
                        for row in csv_reader:
                            title = row.get('Title')
                            release_date = row.get('Release Date')
                            genre = row.get('Genre')
                            description = row.get('Description', None)
                            director = row.get('Director', None)
                            rating = row.get('Rating', None)

                            self.movie_model.add_new_movie(title, release_date, genre, description, director, rating)
                    print("Movies added successfully\n")
                except FileNotFoundError:
                    print("The specified file was not found.\n")
                except Exception as e:
                    print("An error occurred while reading the CSV file: ", e)
            elif choice == '3':
                self.clear()
                break

    def rate_movie(self):
        while True:
            print("\n##########################################")
            print("Welcome to Maver, the movie recommender AI")
            print("---Please Select an Option to Continue---")
            print("##########################################")
            print()
            print("   1. Rate a Movie")
            print("   2. Go Back")
            print()
            print("##################################")
            print("##################################")

            choice = input("\nEnter Option: ")

            if choice == '1':
                movies = self.movie_model.get_movie_title()
                if not movies:
                    print("\nThere are no movies available to rate.\n")
                    continue

                table = tabulate(movies, headers=['ID', 'Title'], tablefmt='pretty')
                print(table)
                movie_id = input("Enter Movie ID: ")
                if not movie_id.isdigit():
                    print("\nInvalid movie ID. Please try again.\n")
                    continue

                rating = input("Enter Rating (1-5): ")
                if not rating.isdigit() or not (1 <= int(rating) <= 10):
                    print("\nInvalid rating. Please try again.\n")
                    continue

                self.movie_model.rate_movie(int(movie_id), int(rating))
                print("Movie rated successfully\n")
            elif choice == '2':
                self.clear()
                break

    def search_movies(self):
        while True:
            print("\n##########################################")
            print("Welcome to Maver, the movie recommender AI")
            print("---Please Select an Option to Continue---")
            print("##########################################")
            print()
            print("   1. Search by Title")
            print("   2. Search by Genre")
            print("   3. Search by Year")
            print("   4. Search by Rating")
            print("   5. Search by Director")
            print("   6. Go Back")
            print()
            print("##################################")
            print("##################################")

            choice = input("\nEnter Option: ")

            if choice == '1':
                title = input("Enter Title: ").title()
                self.clear()
                print(f"Searching for movies with title: {title}\n")
                movies = self.movie_model.get_movies_by_title(title)
                if movies:
                    table = tabulate(movies, headers=['ID', 'Title', 'Release Date', 'Description', 'Director', 'Rating'], tablefmt='pretty')
                    print(table)
                else:
                    print("Movie not found\n")
            elif choice == '2':
                genre = input("Enter Genre: ").title()
                self.clear()
                print(f"Searching for movies with genre: {genre}\n")
                movies = self.movie_model.get_movies_by_genre(genre)
                if movies:
                    table = tabulate(movies, headers=['ID', 'Title', 'Release Date', 'Description', 'Director', 'Rating'], tablefmt='pretty')
                    print(table)
                else:
                    print("Movie not found\n")
            elif choice == '3':
                year = input("Enter Year: ")
                self.clear()
                print(f"Searching for movies released in year: {year}\n")
                movies = self.movie_model.get_movies_by_year(year)
                if movies:
                    table = tabulate(movies, headers=['ID', 'Title', 'Release Date', 'Description', 'Director', 'Rating'], tablefmt='pretty')
                    print(table)
                else:
                    print("Movie not found\n")
            elif choice == '4':
                rating = input("Enter Rating (N.N): ")
                self.clear()
                print(f"Searching for movies with rating: {rating}\n")
                movies = self.movie_model.get_movies_by_rating(rating)
                if movies:
                    table = tabulate(movies, headers=['ID', 'Title', 'Release Date', 'Description', 'Director', 'Rating'], tablefmt='pretty')
                    print(table)
                else:
                    print("Movie not found\n")
            elif choice == '5':
                director = input("Enter Director: ").title()
                self.clear()
                print(f"Searching for movies with director: {director}\n")
                movies = self.movie_model.get_movies_by_director(director)
                if movies:
                    table = tabulate(movies, headers=['ID', 'Title', 'Release Date', 'Description', 'Director', 'Rating'], tablefmt='pretty')
                    print(table)
                else:
                    print("Movie not found\n")
            elif choice == '6':
                self.clear()
                break

    def manage_users(self):
        while True:
            print("\n##########################################")
            print("Welcome to Maver, the movie recommender AI")
            print("---Please Select an Option to Continue---")
            print("##########################################")
            print()
            print("   1. View User Details")
            print("   2. Update User Details")
            print("   3. Delete User")
            print("   4. Go Back")
            print()
            print("##################################")
            print("##################################")

            choice = input("\nEnter Option: ")

            if choice == '1':
                username = input("Enter Username: ").title()
                self.clear()
                user = self.user_model.get_user_details(username)
                if user:
                    user = list(user)
                    user[-1] = user[-1].strftime('%Y-%m-%d')
                    table = tabulate([user], headers=['Username', 'Email', 'Created At'], tablefmt='pretty')
                    print(table)
                else:
                    print("User not found\n")
            elif choice == '2':
                email = input("Enter Email: ")
                password = input("Enter Password: ")
                username = input("Enter Username: ")
                self.user_model.update_user(username, email, password)
                print("User updated successfully\n")
            elif choice == '3':
                username = input("Enter Username: ").title()
                self.user_model.delete_user(username)
                print("User deleted successfully\n")
            elif choice == '4':
                self.clear()
                break

    def view_movie_details(self):
        while True:
            print("\n##########################################")
            print("Welcome to Maver, the movie recommender AI")
            print("---Please Select an Option to Continue---")
            print("##########################################")
            print()
            print("   1. View Movie Details")
            print("   2. Go Back")
            print()
            print("##################################")
            print("##################################")

            choice = input("\nEnter Option: ")

            if choice == '1':
                title = input("Enter Movie Title: ").title()
                self.clear()
                print("Viewing details for movie: " + title + "\n")
                movies = self.movie_model.get_movies_by_title(title)
                if movies:
                    table = tabulate(movies, headers=['ID', 'Title', 'Release Date', 'Rating'], tablefmt='pretty')
                    print(table)
                else:
                    print("Movie not found\n")
            elif choice == '2':
                self.clear()
                break

    def generate_reports(self):
        while True:
            print("\n##########################################")
            print("Welcome to Maver, the movie recommender AI")
            print("---Please Select an Option to Continue---")
            print("##########################################")
            print()
            print("   1. Generate User Report")
            print("   2. Generate Movie Report")
            print("   3. Generate User Movie Report")
            print("   4. Go Back")
            print()
            print("##################################")
            print("##################################")

            choice = input("\nEnter Option: ")

            if choice == '1':
                self.clear()
                print("Generating User Report\n")
                report = self.user_model.generate_user_report()
                print(report)
            elif choice == '2':
                self.clear()
                print("Generating Movie Report\n")
                report = self.movie_model.generate_movie_report()
                report = tabulate(report, headers=['ID', 'Title', 'Release Date', 'Description', 'Director', 'Rating'], tablefmt='pretty')
                print(report)
            elif choice == '3':
                self.clear()
                print("Generating User Movie Report\n")
                report = self.movie_model.generate_user_movie_report()
                print(report)
            elif choice == '4':
                self.clear()
                break

    def toggle_auto_login(self, username):
        self.account_service.toggle_auto_login(username)

