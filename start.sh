#!/bin/bash

# create a new python virtual environment
python3 -m venv venv

# activate the virtual environment
source venv/bin/activate

# install the requirements
pip install -r requirements.txt

# run the django migrations
python manage.py migrate

# start the server
python manage.py runserver
