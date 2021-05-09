# BlogZuri

Link: <a href="https://blogzuri.herokuapp.com/home" target="_blank">BlogZuri</a>

## Overview

This web application is a simple blog about life generally spanning from sex to wealth and beyond.

The main features that have currently been implemented are:

_-There are models for categories, post user and comments._<br>
_-Users can make a comment on a post_

## Quick Start
To get this project up and running locally on your computer:

1. Set up the Python development environment. We recommend using a Python virtual environment.
2. Assuming you have Python setup, run the following commands (if you're on Windows you may use py or py -3 instead of python to start Python): <br>

        pip3 install -r requirements.txt
        python3 manage.py makemigrations
        python3 manage.py migrate
        python3 manage.py collectstatic
        python3 manage.py test # Run the standard tests. These should all pass.
        python3 manage.py createsuperuser # Create a superuser
        python3 manage.py runserver
3. Open a browser to http://127.0.0.1:8000/admin/ to open the admin site
4. Create a few test objects of each type.
5. Open tab to http://127.0.0.1:8000 to see the main site, with your new objects.