import psycopg2
import configparser

class Database:
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

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.lastrowid

    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()
