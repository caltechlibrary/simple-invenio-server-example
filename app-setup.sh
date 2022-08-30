#!/bin/sh

# Change the following value to the port used by the Flask app in the
# script run-app.sh
export PORT=5000

# The rest of this file should not need to be changed -------------------------

# The base name of the Python file that defines our app.
export FLASK_APP=myapp

# Quit this script if an error occurs.
set -o errexit

# Test if something is already running on the port and give a useful message.
if lsof -Pi :$PORT -sTCP:LISTEN -t > /dev/null; then
    echo "‼️  Port $PORT is occupied – maybe Flask is already running? ‼️"
    exit 1
fi

# In case the user runs this script from somewhere other than the directory
# where it's located, relocate ourselves to the script directory.
cd `dirname "$0"`

# Create the database. (Note: these "db" commands come from the Invenio-DB
# module, *not* Flask-migrate. The latter Flask module code is not used in
# Invenio, but if you are new to Invenio and don't know this, and you Google
# around for "flask db" commands, you encounter Flask-migrate. Ignore that.)
flask db init
flask db create

# Create a sample record in the database.
flask fixtures create-sample-record
