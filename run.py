import os

from api.app import app

debug = True if os.environ.get('DEBUG', False) == 'True' else False
port = int(os.environ.get('PORT', 5000))
app.run(debug=debug, port=port)
