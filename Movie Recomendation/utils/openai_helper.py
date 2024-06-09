import os
import requests
import configparser
from PIL import Image
from io import BytesIO
from openai import OpenAI



class OpenAIHelper:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.api_key = config['openai']['openai_key']
        self.omdb_api_key = config['amdbapi']['amdbapi_key']
        self.client = OpenAI(api_key=self.api_key)

    def get_movies_recommendation(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a movie recommender AI called Maver."},
                {"role": "user", "content": prompt}
                ]
            )
        return response.choices[0].message.content
    

    def recommend_movies_by_genre(self, genre):
        prompt = f"""
        I can help you find movies to watch based on your genre preferences.
        Please provide a list top 3 Movie titles in the genre "{genre}" in the form of a Python list, e.g., ["Movie1", "Movie2", "Movie3"] headers=['ID', 'Title', 'Genre', 'Release Date', 'Rating'].
        Provide the answer only without any explanation.
        """
        movies = self.get_movies_recommendation(prompt)
        movies = movies.replace('[','').replace(']','').replace('"','').split(',')
        for movie in movies:
            self.print_movies(movie)
        return None
    
    def recommend_movies_by_rating(self, rating):
        prompt = f"""
        I can help you find movies to watch based on your rating preferences.
        Please provide a list top 3 Movie titles with a rating of {rating} in the form of a Python list, e.g., ["Movie1", "Movie2", "Movie3"].
        Provide the answer only without any explanation.
        """
        movies = self.get_movies_recommendation(prompt)
        movies = movies.replace('[','').replace(']','').replace('"','').split(',')
        for movie in movies:
            self.print_movies(movie)
        return None
   
    
    def recommend_movies_by_year(self, year):
        prompt = f"""
        I can help you find movies to watch based on the release year.
        Please provide a list top 3 Movie titles released in {year} in the form of a Python list, e.g., ["Movie1", "Movie2", "Movie3"].
        Provide the answer only without any explanation.
        """
        movies = self.get_movies_recommendation(prompt)
        movies = movies.replace('[','').replace(']','').replace('"','').split(',')
        for movie in movies:
            self.print_movies(movie)
        return None
    
    def recommend_movies_by_director(self, director):
        prompt = f"""
        I can help you find movies to watch based on the director.
        Please provide a list top 3 Movie titles directed by {director} in the form of a Python list, e.g., ["Movie1", "Movie2", "Movie3"].
        Provide the answer only without any explanation.
        """
        movies = self.get_movies_recommendation(prompt)
        movies = movies.replace('[','').replace(']','').replace('"','').split(',')
        for movie in movies:
            self.print_movies(movie)
        return None
    
    def recommend_movies_by_actors(self, actors):
        prompt = f"""
        I can help you find movies to watch based on the actors.
        Please provide a list top 3 Movie titles starring {actors} in the form of a Python list, e.g., ["Movie1", "Movie2", "Movie3"].
        Provide the answer only without any explanation.
        """
        movies = self.get_movies_recommendation(prompt)
        movies = movies.replace('[','').replace(']','').replace('"','').split(',')
        for movie in movies:
            self.print_movies(movie)
        return None
    
    def recommend_movies_by_title(self, title):
        prompt = f"""
        I can help you find movies to watch based on the title.
        Please provide a list of  movie titles similar to {title} in the form of a Python list, e.g., ["Movie1", "Movie2", "Movie3"].
        Provide the answer only without any explanation.
        """
        movies = self.get_movies_recommendation(prompt)
        movies = movies.replace('[','').replace(']','').replace('"','').split(',')
        for movie in movies:
            self.print_movies(movie)
        return None
    
    def generate_movie_plot_based_on_genre(self, genre):
        prompt = f"""
        I can help you generate a movie plot based on {genre} genre.
        Please provide a list top 3 Movie titles in the genre "{genre}" in the form of a Python list, e.g., ["Movie1", "Movie2", "Movie3"].    
        """
        movies = self.get_movies_recommendation(prompt)
        movies = movies.replace('[','').replace(']','').replace('"','').split(',')
        for movie in movies:
            self.print_movies(movie)
        return None
    
    
    def generate_movie_plot_based_on_keywords(self, keywords):
        prompt = f"""
        I can help you generate a movie plot based on random keywords.
        Please provide a list of random keywords "{keywords}"in the form of a Python list, e.g., ["keyword1", "keyword2", "keyword3"].
        """
        movies = self.get_movies_recommendation(prompt)
        movies = movies.replace('[','').replace(']','').replace('"','').split(',')
        for movie in movies:
            self.print_movies(movie)
        return None
    
    
    def generate_movie_plot_based_on_trends(self):
        prompt = f"""
        I can help you generate a movie plot based on the current trends.
        Please provide a list top 3 Movie titles that are trending in the form of a Python list, e.g., ["Movie1", "Movie2", "Movie3"].
        """
        movies = self.get_movies_recommendation(prompt)
        movies = movies.replace('[','').replace(']','').replace('"','').split(',')
        for movie in movies:
            self.print_movies(movie)
        return None



    
    def get_movie_details(self, movie_name):
        url = f"http://www.omdbapi.com/?apikey={self.omdb_api_key}&t={movie_name}"
        response = requests.get(url)
        return response.json()
    
    def print_movies(self, movies):
        try:
            print('\n---------------------------------------------')
            movie_details = self.get_movie_details(movies)
            print("\nTitle: ", movie_details['Title'])
            print("Year: ", movie_details['Year'])
            print("Genre: ", movie_details['Genre'])
            print("Rating: ", movie_details['imdbRating'])
            print("Director: ", movie_details['Director'])
            print("Actors: ", movie_details['Actors'])
            print("Plot: ", movie_details['Plot'])
            print('\n---------------------------------------------')
           
            if movie_details['Poster'] != 'N/A' and movie_details['Poster'] != None and movie_details['Poster'] != '':
                response = requests.get(movie_details['Poster'])
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    if not os.path.exists('images'):
                        os.makedirs('images')
                    img.save(f"images/{movie_details['Title'].replace(':', '')}.jpg", 'JPEG')
                    print("\nPoster saved successfully in images folder as ", movie_details['Title'].replace(':', '') + ".jpg")
                else:
                    print("\nFailed to save poster")
            else:
                print("\nNo Poster available")
        except Exception as e:
            print("\nError: ", e)
        return None


    

    

if __name__ == '__main__':
    openai_helper = OpenAIHelper()
    openai_helper.recommend_movies_by_year(2010)
  








    