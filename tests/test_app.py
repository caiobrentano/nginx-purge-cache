import json
import unittest

from api.app import app, db
from api.models import Base, Url, Host, Purge

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

        # propagate the exceptions to the test client
        self.client.testing = True
        Base.metadata.drop_all(bind=db.engine)
        Base.metadata.create_all(bind=db.engine)

        db.session.commit()

    def test_healthcheck(self):
        response = self.client.get('/healthcheck')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), 'OK')

    def test_post_url(self):
        url = 'http://domain.com/path/to/purge'
        user = 'someone else'
        response = self.client.post('/add', data={
            'url': url,
            'user': user
        })

        self.assertEqual(response.status_code, 201)

        # Check if it was saved on db
        db_url = db.session.query(Url).filter_by(url=url).first()
        self.assertEqual(db_url.url, url)
        self.assertEqual(db_url.created_by, user)

    def test_post_list_of_urls(self):
        url_1 = 'http://domain.com/path/to/purge_1'
        url_2 = 'http://domain.com/path/to/purge_2'
        user = 'someone else'
        response = self.client.post('/add',
            content_type='application/json',
            data=json.dumps({
                'url': [url_1, url_2],
                'user': user,
            }),
        )

        self.assertEqual(response.status_code, 201)

        # Check if it was saved on db
        db_urls = db.session.query(Url).filter(Url.url.in_([url_1, url_2])).all()

        for db_url in db_urls:
            self.assertIn(db_url.url, [url_1, url_2])
            self.assertEqual(db_url.created_by, user)

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
        response = self.client.post('/hosts/add', data={
            'hostname': hostname,
        })

        self.assertEqual(response.status_code, 201)

        # Check if it was saved on db
        db_host = db.session.query(Host).filter_by(hostname=hostname).first()
        self.assertEqual(db_host.hostname, hostname)

    def test_add_duplicated_host(self):
        hostname = 'myservername'

        # create a new host
        response = self.client.post('/hosts/add', data={
            'hostname': hostname,
        })

        # try to create the same host
        response = self.client.post('/hosts/add', data={
            'hostname': hostname,
        })

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_data(as_text=True), 'Duplicated host')

    def test_add_new_host_with_missing_information(self):
        # missing hostname
        response = self.client.post('/hosts/add', data={
            'hostname': ''
        })
        self.assertEqual(response.status_code, 500)

    def test_get_caches_pending_to_purge_for_a_host(self):
        ''' Get the list of urls to be purged by a specific host '''

        hostname = 'myservername'
        # these 2 urls should return on the GET below
        new_url_1 = 'http://domain.com/path/to/purge_1'
        new_url_2 = 'http://domain.com/path/to/purge_2'

        # this should not return on the GET because it was purged
        purged_url = 'http://domain.com/path/already_purge'

        db.session.add(Url(id=1, url=purged_url))
        db.session.add(Url(id=2, url=new_url_1))
        db.session.add(Url(id=3, url=new_url_2))
        db.session.add(Host(id=1, hostname=hostname))
        db.session.add(Purge(id=1, url_id=1, host_id=1))
        db.session.commit()

        response = self.client.get('/hosts/pending_purge', query_string={
            'hostname': hostname
        })

        self.assertEqual(response.status_code, 200)

        computed = json.loads(response.get_data(as_text=True))
        self.assertEqual(computed, [new_url_1, new_url_2])
        self.assertNotIn(purged_url, computed)

    # def test_get_caches_pending_to_purge_for_a_new_host(self):
    #     hostname = 'myservername_2'
    #
    #     response = self.client.get('/hosts/pending_purge', query_string={
    #         'hostname': hostname
    #     })
    #
    #     self.assertEqual(response.status_code, 200)

    def test_notify_purged_url(self):
        hostname = 'myservername'
        url = 'http://domain.com/path/to/purge'

        # Populate DB for test
        db.session.add(Url(id=1, url=url))
        db.session.add(Host(id=1, hostname=hostname))
        db.session.commit()

        response = self.client.post('/purge', data={
            'hostname': 'myservername',
            'url': 'http://domain.com/path/to/purge',
            'command_output': 'result_from_purge_command',
        })

        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
