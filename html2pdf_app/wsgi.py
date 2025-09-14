# wsgi.py
from app import app

# Pour gunicorn/uwsgi
application = app
