from trello_app.models import UserProfile, User, Bank, Board, List, Card, Attachement, Token
from django.test import TestCase
from django.test import Client
import json
from django.db import IntegrityError


class TestViews(TestCase):
    def setUp(self):
        print "before run"

    def test_user_details_post_add_details(self):
        client = Client()
        json_payload = '{"username":"p","password" : "p","email":"p@gmail.com","firstname":"p",' \
                       '"lastname":"pp","is_superuser":"True", "alias":"p", "workplace_name":"my_test"}'

        response = client.post('/trello_app/api/v1/user/',data=json_payload, content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(UserProfile.objects.filter(alias='p').count(),1)
        self.assertEqual(User.objects.filter(username='p').count(), 1)
        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(data.get("status"), 200)
        self.assertEqual(data.get("message"), "successful")

    def test_exceptions_while_saving_user(self):
        client = Client()
        json_payload = '{"username":"p", "password":"p", "email":"p@gmail.com", "firstname":"p",' \
                           '"lastname":"pp", "is_superuser":"True", "alias":"p"}'
        response = client.post('/trello_app/api/v1/user/', data=json_payload, content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(data.get("message"), "expected keys are: [username, email,password,first_name, "
                                              "last_name, is_superuser, alias, workplace_name]")

        json_payload = '{"username":"p","password" : "p","email":"p@gmail.com","firstname":"p",' \
                           '"lastname":"pp","is_superuser":"True", "alias":"p","workplace_name":" "}'
        response = client.post('/trello_app/api/v1/user/', data=json_payload, content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(data.get("message"), "expected keys are: [username, email,password,first_name, "
                                              "last_name, is_superuser, alias, workplace_name]")

        self.assertEqual(data.get('status'),500)

    def test_get_token_successful(self):
        user = self.create_userprofile()
        client = Client()
        json_payload = '{"username":"rashi","password" : "password"}'
        response = client.post('/trello_app/api/v1/api-token-auth/', data=json_payload, content_type='application/json')
        data = json.loads(response.content)
        self.assertTrue(len(data.get('token')) > 1)

    def test_get_token_with_missing_credentials(self):
        self.create_userprofile()
        client = Client()
        json_payload = '{"password" : "password"}'
        response = client.post('/trello_app/api/v1/api-token-auth/', data=json_payload, content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(data.get('username'),["This field is required."])

    def test_get_profile_details(self):
        token = self.create_user_and_get_token()
        client = Client(HTTP_AUTHORIZATION="Token "+token)
        response = client.get('/trello_app/api/v1/user/1/', content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(data.get('username'),"rashi")
        self.assertEqual(data.get('status'), 200)
        self.assertEqual(data.get('alias'), "rashi")

    def test_get_profile_details_without_token(self):
        client = Client()
        response = client.get('/trello_app/api/v1/user/1/', content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(data.get('detail'),"Authentication credentials were not provided.")

    def test_post_bank_details(self):
        client = Client(HTTP_AUTHORIZATION="Token "+self.create_user_and_get_token())
        json_payload = '{"card_holder_name":"rashi","cvv" : "122","expiry_date":"2021-06"}'

        response = client.post('/trello_app/api/v1/bank_details/', data=json_payload, content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(data.get('status'),200)
        self.assertEqual(data.get('message'),"successfully saved")

        response_for_get = client.get('/trello_app/api/v1/bank_details/')
        data = json.loads(response_for_get.content)
        self.assertEqual(data.get('card_holder_name'),"rashi")
        self.assertEqual(data.get('status'), 200)

    def test_post_bank_details_with_incomplete_input(self):
        client = Client(HTTP_AUTHORIZATION="Token "+self.create_user_and_get_token())
        json_payload = '{"card_holder_name":"rashi","expiry_date":"2021-06"}'

        response = client.post('/trello_app/api/v1/bank_details/', data=json_payload, content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(data.get('status'), 500)

    def test_get_bank_details_when_no_bank_details_are_there(self):
        client = Client(HTTP_AUTHORIZATION="Token " + self.create_user_and_get_token())
        response = client.get('/trello_app/api/v1/bank_details/')
        data = json.loads(response.content)
        self.assertEqual(data.get('status'), 0)
        self.assertEqual(data.get('message'),'bank details not found')

    def test_get_bank_details_without_token(self):
        client = Client()
        response = client.get('/trello_app/api/v1/bank_details/')
        data = json.loads(response.content)
        self.assertEqual(data.get('detail'), "Authentication credentials were not provided.")

    def test_board_creation(self):
        client = Client(HTTP_AUTHORIZATION="Token "+self.create_user_and_get_token())
        json_payload = '{"title":"testing_board","created_at":"2021-06-01"}'
        response = client.post('/trello_app/api/v1/board/', data=json_payload, content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(data.get('status'), 200)
        self.assertEqual(data.get('message'), "successfully saved")

    def test_board_creation_with_incomplete_input(self):
        client = Client(HTTP_AUTHORIZATION="Token "+self.create_user_and_get_token())
        json_payload = '{"title":" "}'
        response = client.post('/trello_app/api/v1/board/', data=json_payload, content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(data.get('status'), 500)
        self.assertEqual(data.get('message'), 'expected key in JSON:["title"]')

    def test_list_creation_when_board_does_not_exist(self):
        client = Client(HTTP_AUTHORIZATION="Token "+self.create_user_and_get_token())
        json_payload = '{"title":"testing_list","created_at":"2021-06-01"}'
        response = client.post('/trello_app/api/v1/board/1/list/', data=json_payload, content_type='application/json')
        data = json.loads(response.content)
        self.assertEquals(data.get('message'),  'unknown error')   # we need to handle this case where board is not present
        self.assertEquals(data.get('status'), 500)

    def test_list_creation_when_board_is_present(self):
        client = Client(HTTP_AUTHORIZATION="Token "+self.create_user_and_get_token())
        json_payload = '{"title":"testing_board","created_at":"2021-06-01"}'
        response = client.post('/trello_app/api/v1/board/', data=json_payload, content_type='application/json')
        data = json.loads(response.content)     # board creation complete

        json_payload = '{"title":"testing_list","created_at":"2021-06-01"}'
        response = client.post('/trello_app/api/v1/board/' + str(data.get('id')) + '/list/', data=json_payload, content_type='application/json')
        data_for_post = json.loads(response.content)
        self.assertEquals(data_for_post.get('message'),  'successfully saved')
        self.assertEquals(data_for_post.get('status'), 200)

        response_for_get = client.get('/trello_app/api/v1/list_details/' + str(data_for_post.get('id')) + '/')
        data = json.loads(response_for_get.content)
        self.assertEquals(data.get('list_details').get('created_by_alias'), 'rashi')
        self.assertEquals(data.get('list_details').get('title'),'testing_list')

    def create_user_and_get_token(self):
        self.create_userprofile()
        client = Client()
        json_payload = '{"username":"rashi", "password" : "password"}'
        response = client.post('/trello_app/api/v1/api-token-auth/', data=json_payload, content_type='application/json')
        data = json.loads(response.content)
        return data.get('token')

    def create_userprofile(self):
        user_profile = UserProfile()
        user = User()
        user.username = "rashi"
        user.set_password("password")
        user.email = "rashi@gmail.com"
        user.first_name = "rashi"
        user.last_name = "dubey"
        user.save()
        user_profile.alias = "rashi"
        user_profile.workplace_name = "my_test"
        user_profile.user = user
        user_profile.save()
