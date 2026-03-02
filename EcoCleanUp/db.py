

from flask import Flask, g
import psycopg2
import psycopg2.extras

# Database connection parameters (set when calling `init_db`).
connection_params = {}

def init_db(app: Flask, user: str, password: str, host: str, database: str,
            port: int = 5432, autocommit: bool = True):
    
    # Save connection details.
    connection_params['user'] = user
    connection_params['password'] = password
    connection_params['host'] = host
    connection_params['database'] = database
    connection_params['port'] = port
    connection_params['autocommit'] = autocommit

    # Register `close_db()` to run every time the application context is torn
    # down at the end of a Flask request, ensuring that any database connection
    # using during that request gets closed.
    app.teardown_appcontext(close_db)

def get_db():
    
    #if 'db' not in g:
        #g.db = psycopg2.connect(**connection_params)
    
    if 'db' not in g:
        conn = psycopg2.connect(
            user=connection_params['user'],
            password=connection_params['password'],
            host=connection_params['host'],
            dbname=connection_params['database'],
            port=connection_params['port']
        )
        conn.autocommit = connection_params.get('autocommit', True)
        g.db = conn

    return g.db

def get_cursor():
    
    return get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def close_db(exception = None):
    
    # Get the database connection from the current application context (the one
    # that's being torn down), or `None` if there is no connection.
    db = g.pop('db', None)
    
    if db is not None:
        db.close()