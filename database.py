import sqlite3

DATABASE = "feedback.db"


def get_connection():
    return sqlite3.connect(DATABASE)