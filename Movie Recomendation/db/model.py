from db.database import Database

class UserModel:
    def __init__(self):
        self.db = Database()

    def get_user(self, username):
        query = 'SELECT * FROM users WHERE username = %s'
        return self.db.fetch_one(query, (username,))
    
    def create_user(self, username, email, password):
        query = 'INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING user_id'
        user_id = self.db.execute_query(query, (username, email, password))
        return user_id

    def update_user(self, username, email, password):
        query = 'UPDATE users SET email = %s, password = %s WHERE username = %s'
        return self.db.execute_query(query, (email, password, username))
    
    def delete_user(self, username):
        query = 'DELETE FROM users WHERE username = %s'
        return self.db.execute_query(query, (username,))
    
    def get_user_details(self, username):
        query = 'SELECT username, email, created_at FROM users WHERE username = %s'
        return self.db.fetch_one(query, (username,))
    
    def generate_user_report(self):
        query = 'SELECT * FROM users'
        return self.db.fetch_all(query)
    

    
class MovieModel:
    def __init__(self):
        self.db = Database()

    def generate_user_movie_report(self):
        query = '''
            SELECT u.username, m.title, ur.rating, ur.rating_date
            FROM users u
            JOIN user_ratings ur ON u.user_id = ur.user_id
            JOIN movies m ON ur.movie_id = m.movie_id
        '''
        return self.db.fetch_all(query)
    
    def get_movie_genres(self):
        query = 'SELECT DISTINCT genre FROM movie_genres'
        return self.db.fetch_all(query)
    
    def get_movie_genre(self, movie_id):
        query = 'SELECT genre FROM movie_genres WHERE movie_id = %s'
        return self.db.fetch_one(query, (movie_id,))
    
    def generate_movie_report(self):
        query = 'SELECT * FROM movies'
        return self.db.fetch_all(query)

    def get_movie_title(self):
        query = 'SELECT movie_id, title FROM movies'
        return self.db.fetch_all(query)

    def get_movie_by_id(self, movie_id):
        query = 'SELECT * FROM movies WHERE movie_id = %s'
        return self.db.fetch_one(query, (movie_id,))
    
    def get_movies_by_genre(self, genre):
        query = '''
            SELECT m.* FROM movies m
            JOIN movie_genres mg ON m.movie_id = mg.movie_id
            WHERE mg.genre = %s
        '''
        return self.db.fetch_all(query, (genre,))
    
    def get_all_movies(self):
        query = 'SELECT * FROM movies'
        return self.db.fetch_all(query)
    
    def get_movies_by_title(self, title):
        query = 'SELECT * FROM movies WHERE title ILIKE %s'
        return self.db.fetch_all(query, (f'%{title}%',))
    
    def get_movies_by_year(self, release_year):
        query = 'SELECT * FROM movies WHERE release_date = %s'
        return self.db.fetch_all(query, (release_year,))
    
    def get_movies_by_rating(self, rating):
        query = 'SELECT * FROM movies WHERE rating = %s'
        return self.db.fetch_all(query, (rating,))
    
    def get_movies_by_director(self, director):
        query = 'SELECT * FROM movies WHERE director = %s'
        return self.db.fetch_all(query, (director,))
    
    def add_new_movie(self, title, release_date=None, genre=None, description=None, director=None, rating=None):
        query = 'INSERT INTO movies (title, release_date, genre, description, director, rating) VALUES (%s, %s, %s, %s, %s, %s) RETURNING movie_id'
        movie_id = self.db.execute_query(query, (title, release_date, genre, description, director, rating))
        
        if genre:
            self.db.execute_query('''
                INSERT INTO movie_genres (movie_id, genre) VALUES (%s, %s)
            ''', (movie_id, genre))

        return movie_id

    def update_movie(self, movie_id, title=None, release_date=None, genre=None, description=None, director=None, rating=None):
        query = 'UPDATE movies SET title = %s, release_date = %s, genre = %s, description = %s, director = %s, rating = %s WHERE movie_id = %s'
        self.db.execute_query(query, (title, release_date, genre, description, director, rating, movie_id))
    
    def delete_movie(self, movie_id):
        query = 'DELETE FROM movies WHERE movie_id = %s'
        self.db.execute_query(query, (movie_id,))

    def rate_movie(self, movie_id, rating):
        query = 'UPDATE movies SET rating = %s WHERE movie_id = %s'
        self.db.execute_query(query, (rating, movie_id))


if __name__ == '__main__':
    user_model = UserModel()
    movie_model = MovieModel()
    print(user_model.get_user('roberadesissa'))
