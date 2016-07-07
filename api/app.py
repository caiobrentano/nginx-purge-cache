import sqlalchemy

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse

from api import models
from api.models import Url, Host, Purge
from common import utils

app = Flask(__name__)
app.config.from_object('settings')

db = SQLAlchemy(app)

logger = utils.get_logger(__name__)

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    ''' Retuns OK if the API is running '''
    logger.info('healthcheck')
    return 'OK'

@app.route('/add', methods=['POST'])
def add_url():
    ''' Saves a URL to be purged '''
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
    ''' Retrieves the status of a URL previously registered to be purged '''
    param_url = request.args.get('url')

    response = []
    urls = db.session.query(Url).filter_by(url=param_url).all()
    for url in urls:
        response.append({
            'url': url.url,
            'created_by': url.created_by
        })

    return jsonify(response)

@app.route('/purge', methods=['POST'])
def purge_url():
    ''' Notify that an URL was purged by a host '''

    param_url = request.form.get('url')
    param_hostname = request.form.get('hostname')
    param_cmd_output = request.form.get('command_output')

    url = db.session.query(Url).filter(Url.url == param_url).first()
    host = db.session.query(Host).filter(Host.hostname == param_hostname).first()

    if not url:
        return 'URL not found', 500

    if not host:
        return 'Host not found', 500

    purge = Purge(url_id=url.id,
                  host_id=host.id,
                  command_output=param_cmd_output)

    db.session.add(purge)
    db.session.commit()

    return '', 201

@app.route('/hosts/add', methods=['POST'])
def add_host():
    ''' Register a new host in database '''
    hostname = request.form.get('hostname')
    ip = request.form.get('ip')

    if not hostname or not ip:
        return 'Missing information', 500

    host = Host(hostname=hostname, ip=ip)
    db.session.add(host)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return 'Duplicated host', 500

    return '', 201

@app.route('/hosts/pending_purge', methods=['GET'])
def get_host_pending_purge():
    ''' Returns a list with all URLs not yet purged for a specific hostname '''
    hostname = request.args.get('hostname')

    # Get host id
    host = db.session.query(Host).filter_by(hostname=hostname).first()
    # Get all urls id that the host already purged
    subquery = db.session.query(Purge.url_id).filter(Purge.host_id == host.id)

    response = []
    for url in db.session.query(Url).filter(~Url.id.in_(subquery)):
        response.append(url.url)

    return jsonify(response)
