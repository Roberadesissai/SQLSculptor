import psycopg2
import configparser

class CreateTables():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.connection = psycopg2.connect(
            host=config['database']['host'],
            port=config['database']['port'],
            user=config['database']['username'],
            database=config['database']['database'],
            password=config['database']['password']
        )

        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                movie_id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                release_date DATE,
                genre VARCHAR(50),
                description TEXT,
                director VARCHAR(100),
                rating NUMERIC(2, 1)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_ratings (
                rating_id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(user_id),
                movie_id INT REFERENCES movies(movie_id),
                rating INT CHECK (rating >= 1 AND rating <= 5),
                rating_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movie_genres (
                movie_id INT REFERENCES movies(movie_id),
                genre VARCHAR(50),
                PRIMARY KEY (movie_id, genre)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                preference_id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(user_id),
                genre VARCHAR(50)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_watchlist (
                watchlist_id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(user_id),
                movie_id INT REFERENCES movies(movie_id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                recommendation_id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(user_id),
                movie_id INT REFERENCES movies(movie_id),
                score NUMERIC(3, 2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.connection.commit()
        self.cursor.close()
        self.connection.close()

if __name__ == '__main__':
    create_tables = CreateTables()
    create_tables.create_tables()
