import json
import os
import unittest
import tempfile

from api.app import app, db
from api.models import Base, Url, Host

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

        # propagate the exceptions to the test client
        self.client.testing = True
        Base.metadata.drop_all(bind=db.engine)
        Base.metadata.create_all(bind=db.engine)

        db.session.add(Host(hostname='host1'))
        db.session.add(Host(hostname='host2'))
        db.session.commit()

    def test_healthcheck(self):
        response = self.client.get('/healthcheck')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), 'OK')

    def test_post_url(self):
        url = 'http://domain.com/path/to/purge'
        response = self.client.post('/add', data={
            'url': url
        })
        self.assertEqual(response.status_code, 201)

        # Check if it was saved on db
        db_url = db.session.query(Url).filter_by(url=url).first()
        self.assertEqual(db_url.url, url)

    def test_post_invalid_url(self):
        response = self.client.post('/add', data={
            'url': '/path/to/."invalid"/../url'
        })
        self.assertEqual(response.status_code, 500)

    def test_check_url(self):
        url = 'http://domain.com/path/to/purge'
        db.session.add(Url(url=url))
        db.session.commit()

        response = self.client.get('/check', query_string={
            'url': url
        })

        self.assertEqual(response.status_code, 200)

    def test_check_url_not_found(self):
        response = self.client.get('/check', query_string={
            'url': 'http://domain/path'
        })

        self.assertEqual(response.status_code, 200)

        computed = json.loads(response.get_data(as_text=True))
        self.assertEqual(computed, [])

    def test_add_new_host(self):
        hostname = 'myservername'
        ip = '1.1.1.1'
        response = self.client.post('/hosts/add', data={
            'hostname': hostname,
            'ip': ip
        })

        self.assertEqual(response.status_code, 201)

        # Check if it was saved on db
        db_host = db.session.query(Host).filter_by(hostname=hostname, ip=ip).first()
        self.assertEqual(db_host.hostname, hostname)

    def test_add_new_host_with_missing_information(self):
        # missing hostname
        response = self.client.post('/hosts/add', data={
            'ip': '1.1.1.1'
        })
        self.assertEqual(response.status_code, 500)

        # missing ip
        response = self.client.post('/hosts/add', data={
            'hostname': 'myservername'
        })
        self.assertEqual(response.status_code, 500)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
