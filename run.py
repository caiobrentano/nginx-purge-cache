import os

from api.app import app

debug = True if os.environ.get('DEBUG', False) == 'True' else False
app.run(debug=debug)
