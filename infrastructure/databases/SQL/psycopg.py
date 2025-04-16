import psycopg2 as psycopg
from psycopg import OperationalError
from config.env import env


class PsycopgSqlDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PsycopgSqlDB, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        try:
            self.connection = psycopg.connect(dsn=env.sql_db_uri)
            self.cursor = self.connection.cursor()
        except OperationalError as e:
            print(f"Error connecting to the database: {e}")
            raise

    def get_connection(self):
        if self.connection.closed:
            self.initialize()
        return self.connection

    def get_cursor(self):
        if self.cursor.connection.closed:
            self.initialize()
        return self.cursor

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self._instance = None

    def get_db(self):
        return self._instance

    def __del__(self):
        self.close()
        self._instance = None
