from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse

from api import models
from api.models import Url
from common import utils

app = Flask(__name__)
app.config.from_object('settings')

db = SQLAlchemy(app)

logger = utils.get_logger(__name__)

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    """ Retuns OK if the API is running """
    logger.info('healthcheck')
    return 'OK'

@app.route('/add', methods=['POST'])
def add_url():
    """ Saves a URL to be purged """
    param_url = request.form.get('url')
    param_user = request.form.get('user', 'unknown')

    parsed = urlparse(param_url)
    if not parsed.scheme or not parsed.netloc:
        return 'Malformed url', 500

    url = Url(url=param_url, created_by=param_user)
    db.session.add(url)
    db.session.commit()

    return '', 201

@app.route('/check', methods=['GET'])
def check_url():
    """ Retrieves the status of a URL previously registered to be purged """
    param_url = request.args.get('url')

    response = []
    urls = db.session.query(Url).filter_by(url=param_url).all()
    for url in urls:
        response.append({
            'url': url.url,
            'created_by': url.created_by
        })

    return jsonify(response)
