import pytest
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
from config.config import db_config


@contextmanager
def get_db_connection(env):
    try:
        connection = mysql.connector.connect(**db_config[env])
        yield connection
    except Error as e:
        print(f"Error: {e}")
        raise e


@pytest.fixture
def app_env():
    return 'local'    # ALWAYS USE LOCAL


@pytest.fixture
def db_env():
    return 'gamedev'  # ALWAYS USE GAMEDEV


@pytest.fixture
def user_id():
    return 79


@pytest.fixture
def db_connection(db_env):
    with get_db_connection(db_env) as conn:
        yield conn
