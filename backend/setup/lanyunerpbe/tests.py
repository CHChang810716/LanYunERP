from django.test import TestCase
import simplejson as json
from .models import InstrGroup, ManageGroup, Person, Property, User

userData = {
    'username': 'testuser',
    'password': 'testuserxxx',
    'email': 'testuser@testmail.com',
    'first_name': 'test',
    'last_name': 'user',
    'sn': '31YQ28',
    'sArYear': 2004
}
def create_user(test):
    response = test.client.post(
        path = '/lanyunerpbe/create_person', 
        data = userData,
        follow = True
    )
    test.assertEqual(response.status_code, 200)
    res = response.json()
    test.assertEqual(res['code'], 0)
    return res

def login(test):
    response = test.client.post(
        path = '/lanyunerpbe/login', 
        data = {
            'username': userData['username'],
            'password': userData['password']
        },
        follow = True
    )
    test.assertEqual(response.status_code, 200)
    res = response.json()
    test.assertEqual(res['code'], 0)
    return res

def logout(test):
    response = test.client.get(
        path = '/lanyunerpbe/logout', 
        follow = True
    )
    test.assertEqual(response.status_code, 200)
    res = response.json()
    test.assertEqual(res['code'], 0)
    return res

class TestPerson(TestCase):
    def test_hello_world(self):
        response = self.client.get('/lanyunerpbe/')
        self.assertEqual(response.status_code, 200)

    def test_person_normal_flow(self):
        # create user
        create_user(self)
        # login
        login(self)
        # get user info
        response = self.client.get(
            path = '/lanyunerpbe/person_info',
            follow = True
        )
        self.assertEqual(response.status_code, 200)
        res = response.json()
        self.assertEqual(res['code'], 0)
        data = res['data']
        shouldRetFields = [
            'sn', 'sArYear', 'email',
            'first_name', 'last_name',
            'username'
        ]
        for field in shouldRetFields:
            self.assertEqual(data[field], userData[field])

    def test_property_list(self):
        create_user(self)
        login(self)
        response = self.client.get(
            path = '/lanyunerpbe/property_list'
        )
        self.assertEqual(response.status_code, 200)
        res = response.json()
        self.assertEqual(res['code'], 1)
        logout(self)
        user = User.objects.get(username = userData['username'])
        person = Person.objects.get(authUser = user)
        person.canListProperties = True
        person.save()
        mg = ManageGroup.objects.create(
            name = '拉弦組'
        )
        ig = InstrGroup.objects.create(
            name = '二胡'
        )
        Property.objects.create(
            name = '二胡1',
            serialNum = 'asdf',
            mgroup = mg,
            igroup = ig,
            borrowedBy = person,
            activated = True
        )
        login(self)
        response = self.client.get(
            path = '/lanyunerpbe/property_list'
        )
        self.assertEqual(response.status_code, 200)
        res = response.json()
        self.assertEqual(res['code'], 0)
        self.assertEqual(len(res['data']), 1)
        self.assertEqual(res['data'][0]['borrowedBy'], 'user test')


    def test_person_list(self):
        create_user(self)
        login(self)
        response = self.client.get(
            path = '/lanyunerpbe/person_list'
        )
        self.assertEqual(response.status_code, 200)
        res = response.json()
        self.assertEqual(res['code'], 1)
        logout(self)
        user = User.objects.get(username = userData['username'])
        person = Person.objects.get(authUser = user)
        person.canActivateUser = True
        person.save()
        login(self)
        response = self.client.get(
            path = '/lanyunerpbe/person_list'
        )
        self.assertEqual(response.status_code, 200)
        res = response.json()
        self.assertEqual(res['code'], 0)
        self.assertEqual(len(res['data']), 1)
        self.assertEqual(res['data'][0]['name'], 'user test')

    def test_property_info(self):
        mg = ManageGroup.objects.create(
            name = '拉弦組'
        )
        ig = InstrGroup.objects.create(
            name = '二胡'
        )
        Property.objects.create(
            name = '二胡1',
            serialNum = 'asdf',
            mgroup = mg,
            igroup = ig,
            activated = True
        )
        create_user(self)
        login(self)
        response = self.client.get(
            path = '/lanyunerpbe/property_info',
            data = {
                'serialNum': 'asdf'
            }
        )
        self.assertEqual(response.status_code, 200)
        res = response.json()
        self.assertEqual(res['code'], 1)
        logout(self)
        user = User.objects.get(username = userData['username'])
        person = Person.objects.get(authUser = user)
        person.canListProperties = True
        person.save()
        login(self)
        response = self.client.get(
            path = '/lanyunerpbe/property_info',
            data = {
                'serialNum': 'asdf'
            }
        )
        self.assertEqual(response.status_code, 200)
        res = response.json()
        self.assertEqual(res['code'], 0)
        self.assertEqual(res['data']['serialNum'], 'asdf')

# Create your tests here.
