#!/usr/bin/env bash -e

# Make sure this port number matches the value used in app-setup.sh.
PORT=5000

# Start it up.
FLASK_APP=myapp.py FLASK_DEBUG=1 flask run --debugger -p $PORT
