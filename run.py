import os

from api.app import app

host = os.environ.get('HOST', '0.0.0.0')
debug = True if os.environ.get('DEBUG', False) == 'True' else False
port = int(os.environ.get('PORT', 5000))

app.run(host=host, debug=debug, port=port)
