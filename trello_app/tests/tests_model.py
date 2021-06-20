from django.test import TransactionTestCase
from trello_app.models import UserProfile, User, Bank, Board, List, Card, Attachement, Token
from django.db import IntegrityError
from datetime import datetime


class TestModels(TransactionTestCase):

    def test_user_profile_creation_without_user(self):
        with self.assertRaises(IntegrityError):
            UserProfile.objects.create(alias='dd', workplace_name='dd_name')

    def test_user_profile_creation_with_user(self):
        user_profile = self.getUserProfile()
        self.assertEqual(user_profile.alias, "dd")
        self.assertEqual(user_profile.workplace_name, "dd_name")
        self.assertEqual(user_profile.user.username, "username")
        self.assertEqual(user_profile.user.email, "ff@gmail.com")
        self.assertEqual(user_profile.user.first_name, "gname")
        self.assertEqual(user_profile.user.last_name, "jlastemn")

    def test_token_creation(self):
        user = self.getUser()
        self.assertEqual(Token.objects.count(), 1)

    def test_creation_of_board(self):
        user_profile = self.getUserProfile()
        curr_time = datetime.now()
        board = Board.objects.create(user_profile=user_profile, title="checking_title", created_at=curr_time)
        self.assertEqual(board.title, "checking_title")
        self.assertEqual(board.created_at, curr_time)

    def test_exceptions_while_creating_board(self):
        user_profile = self.getUserProfile()
        with self.assertRaises(IntegrityError):
            curr_time = datetime.now()
            Board.objects.create(title="checking_title")
        with self.assertRaises(IntegrityError):
            curr_time = datetime.now()
            Board.objects.create(user_profile=user_profile)

    def test_creation_of_list(self):
        user_profile = self.getUserProfile()
        board = Board.objects.create(user_profile=user_profile, title="checking_title", created_at=datetime.now())
        lst = List.objects.create(created_by=user_profile, board=board, title="lst_title",created_at=datetime.now())
        self.assertEqual(lst.title, "lst_title")
        self.assertEqual(lst.board.title, "checking_title")
        self.assertEqual(user_profile.user.email, "ff@gmail.com")
        self.assertEqual(lst.created_by.alias, "dd")

    def test_exceptions_while_creating_list(self):
        user_profile = self.getUserProfile()
        board = Board.objects.create(user_profile=user_profile, title="checking_title", created_at=datetime.now())

        with self.assertRaises(IntegrityError):
            List.objects.create(created_by=user_profile, board=board, title="lst_title")

        with self.assertRaises(IntegrityError):
            List.objects.create(board=board, title="lst_title",created_at=datetime.now())

        with self.assertRaises(IntegrityError):
            List.objects.create(title="lst_title", created_by=user_profile, created_at=datetime.now())


    def test_creation_of_card(self):
        user_profile = self.getUserProfile()
        board = Board.objects.create(user_profile=user_profile, title="checking_title", created_at=datetime.now())
        lst = List.objects.create(created_by=user_profile, board=board, title="lst_title",created_at=datetime.now())
        card = Card.objects.create(list=lst, created_by=user_profile, created_at=datetime.now(), title='title for card',
                                   description="this is my special card", due_date=datetime.now(), position=1)
        self.assertEqual(card.title, "title for card")
        self.assertEqual(card.description, "this is my special card")
        self.assertEqual(card.list.title, "lst_title")
        self.assertEqual(card.created_by.alias, "dd")
        self.assertEqual(user_profile.user.email, "ff@gmail.com")

    def test_exceptions_while_creating_card(self):
        user_profile = self.getUserProfile()
        board = Board.objects.create(user_profile=user_profile, title="checking_title", created_at=datetime.now())
        lst = List.objects.create(created_by=user_profile, board=board, title="lst_title",created_at=datetime.now())

        with self.assertRaises(IntegrityError):
            Card.objects.create(list=lst, created_by=user_profile, title = 'title for card',
                                description = "this is my special card")
        with self.assertRaises(IntegrityError):
            Card.objects.create(list=lst, created_by=user_profile, title = 'title for card', position = 1)
        with self.assertRaises(IntegrityError):
            Card.objects.create(list=lst, created_by=user_profile,
                                description = "this is my special card",position = 1)
        with self.assertRaises(IntegrityError):
            Card.objects.create(list=lst, title = 'title for card',
                                description = "this is my special card",position = 1)
        with self.assertRaises(IntegrityError):
            Card.objects.create(created_by=user_profile, title = 'title for card',
                                description = "this is my special card",position = 1)

    def test_bank_details(self):
        user_profile = self.getUserProfile()
        bank = Bank.objects.create(user_profile=user_profile, card_holder_name="rashi", cvv=488, expiry_date=datetime.now())
        self.assertEqual(user_profile.user.email, "ff@gmail.com")
        self.assertEqual(bank.card_holder_name, "rashi")
        self.assertEqual(bank.cvv, 488)

    def test_exceptions_while_creating_bank_details(self):
        user_profile = self.getUserProfile()
        with self.assertRaises(IntegrityError):
            Bank.objects.create(card_holder_name="rashi", cvv=488)
        with self.assertRaises(IntegrityError):
            Bank.objects.create(user_profile=user_profile, cvv=488)
        with self.assertRaises(IntegrityError):
            Bank.objects.create(card_holder_name="rashi", user_profile=user_profile)

    def test_attachement(self):
        user_profile = self.getUserProfile()
        board = Board.objects.create(user_profile=user_profile, title="checking_title", created_at=datetime.now())
        lst = List.objects.create(created_by=user_profile, board=board, title="lst_title",created_at=datetime.now())
        card = Card.objects.create(list=lst, created_by=user_profile, created_at=datetime.now(), title='title for card',
                                   description="this is my special card", due_date=datetime.now(),position=1)
        attachements = Attachement.objects.create(card=card, user_profile=user_profile,
                                                  link="https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp",
                                                  attached_at=datetime.now())
        self.assertEqual(user_profile.user.email, "ff@gmail.com")
        self.assertEqual(attachements.link, "https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp")
        self.assertEqual(attachements.card.description, "this is my special card")

    def test_exception_while_adding_attachements(self):
        user_profile = self.getUserProfile()
        board = Board.objects.create(user_profile=user_profile, title="checking_title", created_at=datetime.now())
        lst = List.objects.create(created_by=user_profile, board=board, title="lst_title", created_at=datetime.now())
        card = Card.objects.create(list=lst, created_by=user_profile, created_at=datetime.now(), title='title for card',
                                   description="this is my special card", due_date=datetime.now(), position=1)
        with self.assertRaises(IntegrityError):
            Attachement.objects.create(user_profile=user_profile,
                                    link="https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp",)
        with self.assertRaises(IntegrityError):
            Attachement.objects.create(card=card,
                                    link="https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp",)
        with self.assertRaises(IntegrityError):
            Attachement.objects.create(card=card, user_profile=user_profile)

    def getUser(self):
        user = User()
        user.username = "username"
        user.set_password("password")
        user.email = "ff@gmail.com"
        user.first_name = "gname"
        user.last_name = "jlastemn"
        user.save()
        return user

    def getUserProfile(self):
        up = UserProfile.objects.create(user=self.getUser(), alias='dd', workplace_name='dd_name')
        return up
