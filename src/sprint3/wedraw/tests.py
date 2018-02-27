from django.test import TestCase, Client
from wedraw.models import *
from django.core.urlresolvers import reverse
from django.core import serializers


class WedrawTest(TestCase):

    def test_login(self):   # Tests that a GET request to /shared-todo-list/
        client = Client()       # results in an HTTP 200 (OK) response.
        response = client.get('/wedraw/login')
        self.assertEqual(response.status_code, 200)
    def test_signup(self):   # Tests that a GET request to /shared-todo-list/
        client = Client()       # results in an HTTP 200 (OK) response.
        response = client.get('/wedraw/signup/')
        self.assertEqual(response.status_code, 200)


class RoomModelsTest(TestCase):

    def test_add_room(self):
        self.assertTrue(Room.objects.all().count() == 0)
        new_room = Room(id = 1,label = "room1", host = "user1", max_number = 3)
        new_room.save()
        self.assertTrue(Room.objects.all().count() == 1)
        self.assertIsNotNone(Room.objects.filter(label='room1'))
    def test_room_is_full(self):
        new_room2 = Room(id = 1,label = "room1", host = "user1", max_number = 3, current_player=4)
        new_room2.save()
        self.assertTrue(Room.room_is_full(new_room2))
    def test_getcurrentUserList(self):
        new_room2 = Room(id = 1,label = "room1", host = "user1", max_number = 3, current_player=4)
        new_room2.save()
        self.assertIsNotNone(Room.get_curr_user_list(new_room2))


class UserProfileModelsTest(TestCase):
    def test_add_userProfile(self):
        self.assertTrue(UserProfile.objects.all().count() == 0)
        new_user = User.objects.create_user(username = "nameTest", \
                                        password = "passwordTest",)
        new_user.save()
        new_room = Room(id = 1,label = "room1", host = "user1", max_number = 3)
        new_room.save()
        new_userProfile = UserProfile(user = new_user, score = 3, room = new_room,
                                        status = 0, guess_status = False)
        new_userProfile.save()
        self.assertTrue(UserProfile.objects.all().count() == 1)
        self.assertTrue(UserProfile.objects.filter(user = new_user))
    def test_get_add_score(self):
        new_user = User.objects.create_user(username = "nameTest", \
                                        password = "passwordTest",)
        new_user.save()
        new_room = Room(id = 1,label = "room1", host = "user1", max_number = 3)
        new_room.save()
        new_userProfile = UserProfile(user = new_user, score = 3, room = new_room,
                                        status = 0, guess_status = False)
        new_userProfile.save()
        self.assertTrue(UserProfile.get_score(new_userProfile) == 3)
        self.assertTrue(UserProfile.add_score(new_userProfile) == 6)


class PageTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('user1', password='passw1')
        self.client.login(username='user1', password='passw1')

    def test_login(self):
        self.assertTrue(self.user.is_authenticated())

    def test_home(self):
        self.client.login(username='user1', password='passw1')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

class ControllerTestCasw(TestCase):
    # user1 = User.objects.create_user(username = "user1",password="pwd1")
    # user2 = User.objects.create_user(username="user2", password="pwd2")
    def setUp(self):
        self.room_default = Room.objects.create(label = "000")
        self.room1 = Room(id=2, label="room1", host="user1", max_number=3)

        self.user1 = User.objects.create_user(username = "user1",password="pwd1")
        self.user2 = User.objects.create_user(username="user2", password="pwd2")
        self.user3 = User.objects.create_user(username="user3", password="pwd3")
        # user joins as order : user3,user2,user1
        self.profile3 = UserProfile.objects.create(user=self.user3, room=self.room1)
        self.profile2 = UserProfile.objects.create(user=self.user2, room=self.room1)
        self.profile1 = UserProfile.objects.create(user=self.user1, room=self.room1)

        self.player_list = UserProfile.objects.filter(room=self.room1).order_by('join_room_time')
        self.player_number = len(self.player_list)
        self.player_list_json = serializers.serialize('json', self.player_list)

        self.controller = Controller.objects.create(curr_round_number=0,
                                               max_round_number=2,
                                               curr_turn_number=0,
                                               player_number=self.player_number,
                                               player_list=self.player_list_json,
                                               room=self.room1)

    def test_get_curr_user_list(self):
        self.assertEqual(3,len(self.controller.get_curr_user_list(self.controller)))

    def test_get_curr_painter(self):
        self.assertEqual(self.user3, self.controller.get_curr_painter(self.controller))
        self.assertNotEqual(self.user2,self.controller.get_curr_painter(self.controller))
        self.assertNotEqual(self.user1,self.controller.get_curr_painter(self.controller))

    def test_get_next_painter(self):
        # now it's user2 for the 1st round
        self.assertEqual(self.user2, self.controller.get_next_painter(self.controller))
        self.assertNotEqual(self.user3,self.controller.get_curr_painter(self.controller))
        self.assertNotEqual(self.user1,self.controller.get_curr_painter(self.controller))

        # now it's user1 for the 1st round
        self.assertEqual(self.user1, self.controller.get_next_painter(self.controller))

        # now it's user3 for the 2nd round
        self.assertEqual(self.user3, self.controller.get_next_painter(self.controller))

        # now it's user2 for the 2nd round
        self.assertEqual(self.user2, self.controller.get_next_painter(self.controller))

        # now it's user1 for the 2nd round
        self.assertEqual(self.user1, self.controller.get_next_painter(self.controller))

        # now it's Game Over
        self.assertEqual("Game Over", self.controller.get_next_painter(self.controller))
