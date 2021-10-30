#!/bin/bash

python3 app/worker.py &

FLASK_APP="run.py" flask run
