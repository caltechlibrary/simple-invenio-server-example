#!/usr/bin/env bash -e

# The base name of the Python file that defines our app.
export FLASK_APP=myapp

# In case the user runs this script from somewhere other than the directory
# where it's located, relocate ourselves to the script directory.
cd `dirname "$0"`

# Delete the database.
flask db drop --yes-i-know
rm -f app.db
