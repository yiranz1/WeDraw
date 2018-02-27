from __future__ import unicode_literals
from django.contrib.auth.models import User

# Create your models here.
from django.db import models
from channels import Group
import datetime
import json
from django.db.models import Max
from django.template.loader import get_template
from django.shortcuts import render

jsonDec = json.decoder.JSONDecoder()

DEFAULT_CONTROLLER_ID = 0
DEFAULT_ROOM_LABLE = "000"

class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)
    host = models.CharField(max_length = 250,default = "",blank = True)
    # max number of players in one room
    max_number = models.IntegerField(default = 3)
    # number of current player in room
    current_player = models.IntegerField(default = 0)
    in_game = models.BooleanField(default = False)
    last_changed = models.DateTimeField(auto_now = True)

    # get the current users in the room
    @staticmethod
    def users_join_room(self):  
        users = []
        # get User queryset from get_curr_user_list
        # and append them to user_list
        user_list = self.get_curr_user_list(self)
        user = User.objects.filter(userprofile__in=user_list)
        for i in range(len(user)):
            users.append(user[i].username)
       
        return users

    # Retruns all recent additions and deletions
    @staticmethod
    def get_changes(time="1970-01-01T00:00+00:00"):       
        return Room.objects.filter(last_changed__gt=time).distinct()

    @staticmethod
    def get_changes_host(host, time="1970-01-01T00:00+00:00"):       
        return Room.objects.filter(host = host,last_changed__gt=time).distinct()

    @staticmethod
    def get_max_time():
        return Room.objects.all().aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"

    @staticmethod
    def get_max_time_host(host):
        room = Room.objects.filter(host = host).distinct()
        return room.aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"
    
    # change the host of the room    
    @staticmethod
    def change_host(self):
        user_list = self.get_curr_user_list(self)
        user = User.objects.filter(userprofile__in=user_list)
        if len(user) != 0:
            self.host = user[0].username
            
            self.save()
            return self.host

    # get the drawer of the game
    @staticmethod
    def is_drawer(self):  
        # get User queryset from get_curr_user_list
        # and append them to user_list
        host = self.host
        drawer = host

        return drawer

    def __unicode__(self):
        return self.label

    # get current user list in the room
    @staticmethod
    def get_curr_user_list(self):
        user_list = UserProfile.objects.filter(room = self).order_by('join_room_time')
        return user_list        

    # return user-score as a dictionary
    @staticmethod
    def userscore(self):
        user_score = {}
       
        user_list = self.get_curr_user_list(self)

        for user in user_list:
            user_score[user.user.username] = user.score
            
        return user_score

    # Check whether the room is full
    @staticmethod
    def room_is_full(self):      
        if self.current_player > self.max_number:
            return True
        else:
            return False

    # Generates the HTML-representation of a room.
    @property
    def html(self):
        template = get_template('room.html')
        context = {"label":self.label,"id":self.id}
        # there is an empty line at the top, have to eliminate it
        return template.render(context).replace("\n","")


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    score = models.IntegerField(default=0,blank=True)
    time = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room,
                             on_delete=models.SET_NULL,
                             null=True,
                             default=DEFAULT_ROOM_LABLE)

    status = models.IntegerField(default = 0)
    join_room_time = models.DateTimeField(default=datetime.datetime.fromtimestamp(0.0),
                                          auto_now=False,
                                          auto_now_add=False,
                                          blank=True)
    
    # If user made a correct guess, his guess status is True, thus
    # prevent him from accumulating his score.
    guess_status = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username

    @staticmethod
    def get_score(self):
        return self.score

    @staticmethod
    def add_score(self):
        self.score += 3
        self.save()
        return self.score

    # old profile first
    class Meta:
        ordering = ['time']

class Controller(models.Model):
    # These 3 integer field are all index starting from 0
    curr_round_number = models.IntegerField(default=0,blank=True)
    # The game will end in 1 round in default
    max_round_number = models.IntegerField(default=1,blank=True)
    curr_turn_number = models.IntegerField(default=0,blank=True)

    # The game will be performed between 2 users in default
    player_number = models.IntegerField(default=2,blank=True)
    player_list = models.CharField(max_length=4200,blank=True,null=True)

    room = models.ForeignKey(Room,
                             null=True,
                             default=DEFAULT_ROOM_LABLE)
    # This field record the word selected for each turn
    selected_word = models.CharField(max_length = 30)
    
    def __str__(self):
        return self.room.label

    # # getters
    @staticmethod
    def get_curr_user_list(self):
        list = json.loads(self.player_list)
        return list
    #
    @staticmethod

    def get_curr_painter(self):
        if self.curr_round_number == self.max_round_number:
            return "Game Over"
        else:
            list = json.loads(self.player_list)
            user_pk = list[self.curr_turn_number]["fields"]['user']
            curr_painter = User.objects.get(pk=user_pk)
            return curr_painter
    #
    @staticmethod
    def get_next_painter(self):
        list = json.loads(self.player_list)
        self.curr_turn_number += 1

        if self.curr_turn_number == self.player_number:
            self.curr_turn_number = (self.curr_turn_number) % (self.player_number)
            self.curr_round_number += 1
            if self.curr_round_number == self.max_round_number:
                # self.curr_turn_number = 0
                # self.curr_round_number = 0
                
                self.save()
                return "Game Over"
            else:
                user_pk = list[self.curr_turn_number]["fields"]['user']
                curr_painter = User.objects.get(pk=user_pk)
                self.save()
                
                return curr_painter
        else:
            self.curr_turn_number = (self.curr_turn_number)%(self.player_number)
            user_pk = list[self.curr_turn_number]["fields"]['user']
            curr_painter = User.objects.get(pk=user_pk)
            self.save()
            
            return curr_painter


class tableword(models.Model):
    wordId = models.IntegerField(primary_key = True)
    wordfield = models.CharField(max_length=30)
    word = models.CharField(max_length=30)
    hint1 = models.CharField(max_length=30)
    hint2 = models.CharField(max_length=30)
    hint3 = models.CharField(max_length=30)
