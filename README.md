## zeus

A Twitter/X clone made in Python/Django.

### Installation (Mac-specific)

1. Clone the repo by running `git clone https://github.com/atbu/zeus.git`.
2. Ensure pip is installed. If it isn't, follow the guide here: https://pip.pypa.io/en/stable/installation
3. Create a virtual environment by running `virtualenv env --no-site-packages` then `source env/bin/activate` to activate.
4. Run `pip install django` to install Django to this virtual environment.
5. Run `python manage.py migrate` to migrate the database (the project uses sqlite3).
6. Run `python manage.py createsuperuser` to create a superuser account for yourself.
7. Run `python manage.py runserver` to run the server and visit `localhost:3000` (by default) to access the app.
