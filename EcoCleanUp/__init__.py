# This script runs automatically when our `loginapp` module is first loaded,
# and handles all the setup for our Flask app.
from flask import Flask

app = Flask(__name__)

# Set the "secret key" that our app will use to sign session cookies. This can
# be anything.

app.secret_key = 'Example Secret Key (CHANGE THIS TO YOUR OWN SECRET KEY!)'

# Set up database connection.
from EcoCleanUp import connect
from EcoCleanUp import db
db.init_db(app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname,
           connect.dbport)

# Include all modules that define our Flask route-handling functions.
from EcoCleanUp import user
from EcoCleanUp import volunteer
from EcoCleanUp import leader
from EcoCleanUp import admin