import datetime
import psycopg2
import configparser



CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
);"""

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
);"""

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY(user_username) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);"""


INSERT_MOVIE = "INSERT INTO movies (title, release_timestamp) VALUES (%s, %s);"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"
INSERT_USER = "INSERT INTO users (username) VALUES (%s);"
INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_username, movie_id) VALUES (%s, %s);"
SELECT_WATCHED_MOVIES = """SELECT movies.* 
FROM movies
JOIN watched ON users.username = watched.user_username
JOIN movies ON watched.movie_id = movies.id
WHERE watched.user_username = %s;"""
SEARCH_MOVIE = "SELECT * FROM movies WHERE title LIKE %s;"
DELETE_MOVIE = "DELETE FROM movies WHERE title = %s;"


def get_connection():
    config = configparser.ConfigParser()
    config.read('config.ini')
    conn = psycopg2.connect(
        host=config['DATABASE']['host'],
        database=config['DATABASE']['database'],
        user=config['DATABASE']['username'],
        password=config['DATABASE']['password']
    )
    conn.set_session(autocommit=True)
    return conn



def create_tables():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_WATCHED_TABLE)

def add_movie(name, release_timestamp):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(INSERT_MOVIE, (name, release_timestamp))

def get_movies(upcoming=False):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            if upcoming:
                today_timestamp = datetime.datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
            else:
                cursor.execute(SELECT_ALL_MOVIES)
            return cursor.fetchall()
        
def add_user(username):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(INSERT_USER, (username,))

def watch_movie(username, movie_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(INSERT_WATCHED_MOVIE, (username, movie_id))

def get_watched_movies(username):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(SELECT_WATCHED_MOVIES, (username,))
            return cursor.fetchall()
    
def search_movies(search_term):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(SEARCH_MOVIE, (f'%{search_term}%',))
            return cursor.fetchall()

def delete_movie(title):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(DELETE_MOVIE, (title,))

