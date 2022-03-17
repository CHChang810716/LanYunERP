from django.test import TestCase
import simplejson as json

class TestPerson(TestCase):
    def test_hello_world(self):
        response = self.client.get('/lanyunerpbe/')
        self.assertEqual(response.status_code, 200)

    def test_create_person_normal(self):
        response = self.client.post(
            path = '/lanyunerpbe/create_person', 
            data = {
                'username': 'testuser',
                'password': 'testuserxxx',
                'email': 'testuser@testmail.com',
                'first_name': 'test',
                'last_name': 'user',
                'sn': '31YQ28',
                'sArYear': 2004
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        res = response.json()
        self.assertEqual(res['code'], 0)

        response = self.client.post(
            path = '/lanyunerpbe/person_login', 
            data = {
                'username': 'testuser',
                'password': 'testuserxxx'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        res = response.json()
        print(res['msg'])
        self.assertEqual(res['code'], 0)

# Create your tests here.
