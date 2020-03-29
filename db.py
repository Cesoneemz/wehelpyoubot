# import sqlite3
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']


def connect_to_database():
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    return connection, cursor


def connect(function):
    def wrapper(*args, **kwargs):
        try:
            connection, cursor = connect_to_database()
            result = function(cursor, *args, **kwargs)
            connection.commit()
            connection.close()
        except Exception as e:
            result = str(e)

        return result

    return wrapper
