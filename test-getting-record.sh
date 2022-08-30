#!/usr/bin/env bash

# Make sure this port number matches the value used in run-app.sh.
PORT=5000

# Try to fetch the test record and print it.
curl -s http://localhost:$PORT/myrecords/1 | python -m json.tool
echo ""
