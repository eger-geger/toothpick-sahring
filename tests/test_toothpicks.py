import os
import json
import unittest
from datetime import datetime
from flask_fixtures import FixturesMixin
from toothpick_sharing import Service

service = Service(__name__, os.path.dirname(__file__))
service.app.testing = True

class ToothpicksResourceTests(unittest.TestCase, FixturesMixin):

    fixtures = ['default.yaml']
    app = service.app
    db = service.db

    def setUp(self):
        self.app = service.app.test_client()

    def post_json(self, path, data=None):
        response = self.app.post(path, data=json.dumps(data), content_type='application/json')
        return response, parse_json(response)

    def get_json(self, path):
        response = self.app.get(path)
        return response, parse_json(response)

    def test_get_all_toothpicks(self):
        response, payload = self.get_json('/api/toothpicks')

        self.assertEqual(response.status_code, 200)

        self.assertCountEqual(payload, [
            {'id': 1, 'owners': [
                {
                    'user': {'id': 3, 'name': 'Hugh Jackman'},
                    'since': '2018-01-15T00:00:00'
                },
                {
                    'user': {'id': 1, 'name': 'Jack Daniels'},
                    'since': '2018-01-01T00:00:00'
                }
            ]},
            {'id': 2, 'owners': [
                {
                    'since': '2018-01-10T00:00:00',
                    'user': {'id': 2, 'name': 'Pamela Anderson'}
                },
                {
                    'since': '2018-01-01T00:00:00',
                    'user': {'id': 1, 'name': 'Jack Daniels'}
                }
            ]},
            {'id': 3, 'owners': [
                {
                    'user': {'id': 1, 'name': 'Jack Daniels'},
                    'since': '2018-01-20T00:00:00'
                },
                {
                    'user': {'id': 2, 'name': 'Pamela Anderson'},
                    'since': '2018-01-10T00:00:00'
                }
            ]}
        ])

    def test_get_toothpick_by_id(self):
        response, payload = self.get_json('/api/toothpicks/1')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(payload, {
            'id': 1, 'owners': [
                {
                    'user': {'id': 3, 'name': 'Hugh Jackman'},
                    'since': '2018-01-15T00:00:00'
                },
                {
                    'user': {'id': 1, 'name': 'Jack Daniels'},
                    'since': '2018-01-01T00:00:00'
                }
            ]}
        )

    def test_get_toothpick_by_wrong_id(self):
        response, payload = self.get_json('/api/toothpicks/99')

        self.assertEqual(response.status_code, 404)
        self.assertIn('message', payload)
        self.assertIn('Toothpick with id=<99> not found.', payload['message'])

    def test_add_new_toothpick(self):
        response, payload = self.post_json('/api/toothpicks')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(payload, {'id': 4, 'owners': []})
        self.assertIn(payload, parse_json(self.app.get('/api/toothpicks')))
        self.assertEqual(payload, parse_json(self.app.get('/api/toothpicks/4')))

    def test_change_toothpick_owner(self):
        first_response, first_payload = self.post_json('/api/toothpicks/1/owners/1')

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(first_payload, {
            'id': 1,
            'owners': [
                {
                    'user': {'id': 1, 'name': 'Jack Daniels'},
                    'since': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
                },
                {
                    'user': {'id': 3, 'name': 'Hugh Jackman'},
                    'since': '2018-01-15T00:00:00'
                },
                {
                    'user': {'id': 1, 'name': 'Jack Daniels'},
                    'since': '2018-01-01T00:00:00'
                }
            ]}
        )

        second_response, second_payload = self.post_json('/api/toothpicks/1/owners/1')

        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(second_payload, first_payload)

    def test_change_toothpick_owner_unknown_user(self):
        response, payload = self.post_json('/api/toothpicks/1/owners/99')

        self.assertEqual(response.status_code, 404)
        self.assertIn('message', payload)
        self.assertIn('User with id=<99> not found.', payload['message'])

    def test_change_toothpick_owner_unknown_toothpick(self):
        response, payload = self.post_json('/api/toothpicks/99/owners/1')

        self.assertEqual(response.status_code, 404)
        self.assertIn('message', payload)
        self.assertIn('Toothpick with id=<99> not found.', payload['message'])
    

def parse_json(response):
    return json.loads(response.data.decode())
