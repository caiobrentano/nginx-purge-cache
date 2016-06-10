import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'api.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = True

NGINX_CACHE_PATH = os.environ.get('NGINX_CACHE_PATH', '/path/to/nginx/cache')
DELETE_TMPLT = ("grep -ra '{path}' "
                + NGINX_CACHE_PATH +
                " | sed 's/\:/ /'"
                " | awk '{print $1}'"
                " | xargs rm")

API_URL = os.environ.get('API_URL', 'http://localhost:5000')
