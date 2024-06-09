from utils.openai_helper import OpenAIHelper

class MovieServie:
    def __init__(self):
        self.openai_helper = OpenAIHelper()

    def recommend_movies_by_genre(self, genre):
        movies = self.openai_helper.recommend_movies_by_genre(genre)
        movies = movies.replace('[','').replace(']','').replace('"','').split(',')
        for movie in movies:
            self.openai_helper.print_movies(movie)
       

    def recommend_movies_by_title(self, title):
        movies = self.openai_helper.get_movies_recomendation(title)
        movies = movies.replace('[','').replace(']','').replace('"','').split(',')
        for movie in movies:
            self.openai_helper.print_movies(movie)
        
    def recommend_movies_by_year(self, year):
        movies = self.openai_helper.get_movies_recomendation(year)
        movies = movies.replace('[','').replace(']','').replace('"','').split(',')
        for movie in movies:
            self.openai_helper.print_movies(movie)
       
    
    def recommend_movies_by_rating(self, rating):
        movies = self.openai_helper.get_movies_recomendation(rating)
        movies = movies.replace('[','').replace(']','').replace('"','').split(',')
        for movie in movies:
            self.openai_helper.print_movies(movie)
        

    def recommend_movies_by_actor(self, actor):
        movies = self.openai_helper.get_movies_recomendation(actor)
        movies = movies.replace('[','').replace(']','').replace('"','').split(',')
        for movie in movies:
            self.openai_helper.print_movies(movie)
        

    def recommend_movies_by_director(self, director):
        movies = self.openai_helper.get_movies_recomendation(director)
        movies = movies.replace('[','').replace(']','').replace('"','').split(',')
        for movie in movies:
            self.openai_helper.print_movies(movie)
        




