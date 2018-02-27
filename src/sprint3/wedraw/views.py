from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from wedraw.models import *
from wedraw.forms import *
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect

import datetime
import time
from random import randint
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from haikunator import Haikunator
import json
from django.core import serializers


current_milli_time = lambda: int(round(time.time()))
# haikunator is used to generate random room names
haikunator = Haikunator()

@login_required
def home(request):    
    rooms = Room.objects.order_by("label")
    return render(request,'wedraw/home.html', {'rooms':rooms})

# Action for creating a new room
@login_required
def new_room(request):
    """
    Randomly create a new room, and redirect to it.
    """
    new_room = None
    while not new_room:
        label = haikunator.haikunate()

        if Room.objects.filter(label=label).exists():
            continue
            
        # create a new room with label and host being the request user
        new_room = Room.objects.create(label=label, host = request.user.username)
        new_room.save()
    return redirect(join_room, label=label)

# Action for join the room. If a user click the link to the room,
# then he is lead to the room page to wait for the host begining
# the game
@login_required
def join_room(request, label):
    try:
        rooms = Room.objects.get(label = label)
    except:
        return redirect('home')

    # If game already begins, do not let other users join this room
    if rooms.in_game:
        return redirect('home')

    profile = get_object_or_404(UserProfile, user = request.user)

    users_profile_list = rooms.get_curr_user_list(rooms)
    if profile not in users_profile_list:
        # This user hasn't been added to the room yet.

        #TODO: check weather room needs this fields
        rooms.current_player += 1
        rooms.save()
        
        # if the room is full of users, current user can't join that room
        # redirect the user back to home page
        
        if rooms.room_is_full(rooms) :
            
            rooms.current_player -=1
            rooms.save()
            return redirect('home')

        profile.room = rooms
        
        profile.score = 0
        time = float(current_milli_time())
        profile.join_room_time = datetime.datetime.fromtimestamp(time)
        profile.save()
        
    else:
        profile.score = 0
        profile.save()
        # This hadle the situation that player rejoin/refresh the waiting page

    users = rooms.users_join_room(rooms)
    users_profile_list = rooms.get_curr_user_list(rooms)
    
    context = {'room': rooms,'users':users,'userprofile':profile}
    
    # if the room is not full let him join that room
   
    return render(request, "wedraw/gameroom.html", context)


@login_required
def checkInRoom(request, label):
    try:
        rooms = Room.objects.get(label = label)
    except:
        return redirect('home')

    profile = get_object_or_404(UserProfile, user = request.user)

    # TODO: VERY IMPORTANT: make sure room.getxxxx can filter right users
    users_profile_list = rooms.get_curr_user_list(rooms)
    if profile not in users_profile_list:
        return HttpResponse("false")
    else :
        return HttpResponse("true")

# Action for leave the rooms.
# When user leaves the room, set his foreign key to default
# and redirect him to the home page
@login_required
def leave_room(request,label):
    default_room = get_object_or_404(Room, label="000")
    rooms = get_object_or_404(Room, label=label)
    rooms.current_player -= 1
    rooms.save()
    # get the profile of the user specified
    profile = get_object_or_404(UserProfile, user = request.user)
    profile.room = default_room
    profile.save()
    # If the host left the room, change the room host
    if request.user.username == rooms.host:
        rooms.change_host(rooms)

    user_list = rooms.get_curr_user_list(rooms)
    # If the last user left the room, delete the room instance
    if (len(user_list) == 0):
        Room.objects.filter(label=rooms.label).delete()
    return redirect('home')

@login_required
@transaction.atomic
# Returns all recent changes to the database, as JSON
# Action for all room changes
def get_changes(request, time="1970-01-01T00:00+00:00"):
    max_time = Room.get_max_time()
    rooms = Room.get_changes(time)
    context = {"max_time":max_time, "rooms":rooms} 
    return render(request, 'rooms.json', context, content_type='application/json')

@login_required
@transaction.atomic
# Returns all recent changes to the database, as JSON
# Action for all room host changes
def get_changes_host(request, label, time="1970-01-01T00:00+00:00"):
    if time == 'undefined':
        time = "1970-01-01T00:00+00:00"

    room = get_object_or_404(Room, label = label)
    host = room.host
    
    max_time = Room.get_max_time_host(host) 
       
    context = {"max_time":max_time,"host":host} 
    return render(request, 'hosts.json', context, content_type='application/json')

# Action when user made a correct guess
@login_required
def add_score(request):
    if request.method == 'POST':
        user = request.user
        profile = get_object_or_404(UserProfile, user = request.user)

        # Add 3 points for that user and save his profile
        profile.add_score(profile)
        profile.save()

        context = {'username':user.username,'score':profile.score}
        return render(request,'wedraw/score.json',context, content_type = 'application/json')
    else:
        return HttpResponse("no permission")
# Action for getting the current painter
@login_required
def get_curr_painter(request):
    userprofile = get_object_or_404(UserProfile, user = request.user)
    room = userprofile.room
    controller = get_object_or_404(Controller, room = room)
    curr_paiter = controller.get_curr_painter(controller)
    if curr_paiter == "Game Over":
        room.in_game = False
        room.save()
        return redirect(game_result)
    else:
        return HttpResponse(curr_paiter.username == request.user.username)

# Action for start a new turn    
@login_required
def new_turn(request):
    if request.method == 'POST':
        userprofile = get_object_or_404(UserProfile, user = request.user)
        room = userprofile.room

        controller = get_object_or_404(Controller, room = room)

        list = controller.get_curr_user_list(controller)

        next_user = controller.get_next_painter(controller)

        if next_user == "Game Over":
            room.in_game = False
            room.save()
            return redirect(game_result)
        else:
            return HttpResponse(next_user.username == request.user.username)
    else:
        return HttpResponse("no permission")
# Action for get the game result
@login_required

def game_result(request):
    userprofile = get_object_or_404(UserProfile, user = request.user)
    room = userprofile.room
    profiles = UserProfile.objects.filter(room = room)
    
    
    user_score = room.userscore(room)
    response_data = {}
    users = []
    scores = []
    # find the user who has the highest score
    winner = max(user_score,key =user_score.get)

    # get the users and their scores
    for profile in profiles:
        users.append(profile.user.username)
        scores.append(profile.score)

    # return as a dictionary
    response_data['user'] = users
    response_data['score'] = scores
    response_data['winner'] = winner

    return HttpResponse(json.dumps(response_data), content_type="application/json")

# Action for guesser page. Render the guessing html for guesser
@login_required

def guesser_page(request,label):
    # get the game room
    room = get_object_or_404(Room, label = label)
    userprofile = get_object_or_404(UserProfile, user = request.user)

    # If it's not the first round, then the user's guess status might be 
    # True. So in the new round, we need to set this status back to False
    if userprofile.guess_status:
        userprofile.guess_status = False
        userprofile.save()
    # get all users' profile in that game room
    user_list = room.get_curr_user_list(room)

    # get the controller and the current painter
    controller = get_object_or_404(Controller, room=room)
    current_painter = controller.get_curr_painter(controller)
    
    context = {'room':room,'users':user_list,'painter':current_painter}
    return render(request, 'wedraw/game_guesser.html', context)

# Action for drawer page
@login_required

def drawer_page(request,label):
    # get the game room and all users' profile in that room
    room = get_object_or_404(Room,label = label)    
    user_list = room.get_curr_user_list(room)

    context = {'room':room,'users':user_list}
    return render(request, 'wedraw/game_drawer.html', context)

@login_required
def getwordsInfo(request):
    
    context = {}
    count = len(tableword.objects.all())
    userprofile = get_object_or_404(UserProfile, user = request.user)
    room = userprofile.room
    controller = get_object_or_404(Controller, room = room)

    if count > 0 :
        random_index = randint(0, count-1) # should change to count in python 3 
        randomWord = tableword.objects.all()[random_index]
        controller.selected_word = randomWord.word
        controller.save()
        context = {'word': randomWord.word,'hint1':randomWord.hint1,'hint2':randomWord.hint2,'hint3':randomWord.hint3}

    else:
        context["words"]="no words existing"
    return render(request, 'wedraw/worddetail.json', context, content_type='application/json')

@login_required
# Action for check the user's guessing result
def check_guessing_result(request):
    
    response_data = {}
    result = False
    message = []
    userprofile = get_object_or_404(UserProfile, user = request.user)
    room = userprofile.room
    status = userprofile.guess_status

    # get the selected word for this round
    controller = get_object_or_404(Controller, room = room)
    word = controller.selected_word
    
    form = GuessingForm(request.POST)
    # form validation
    if not form.is_valid():
        
        message.append("Invalid input")
        response_data['message'] = message
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    # user's guess
    guess = form.cleaned_data['guess']    
    
    # if status is False, means this is the user hasn't made a correct guess.
    if not status:
        if guess == word:
            result = True
            message.append("Correct! Awsome!")
            userprofile.guess_status = True
            userprofile.save()
        elif len(guess) != len(word):
            message.append("You are suppose to guess a "+str(len(word))+" letter word!")
        else:
            message.append("Sorry, try again.")
            
    # The user has already made a correct guess
    else:
        message.append("You have already made a correct guess.")

    response_data['result'] = result
    response_data['message'] = message

    return HttpResponse(json.dumps(response_data), content_type="application/json")

# Action for the signup route
def signup(request):
    if request.user.is_authenticated():
        return redirect('home')
    context={}
    errors=[]

    # Just display the signup form if this is a GET request
    if request.method== 'GET':
        context['form'] = SignUpForm()
        return render(request,'wedraw/signup.html',context)

    form = SignUpForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        errors.append(form.errors)
        context = {'form':form,'errors':errors}
        return render(request,'wedraw/signup.html', context)

# # # TODO:create Defalult Controller for every profile
    if Room.objects.count() == 0 :
        room = Room.objects.create(label = "000")
        # controller = Controller.objects.create(room=room)
        # controller.save()
        room.save()
    else:
        room = Room.objects.get(label = "000")
        # controller = Controller.objects.get(room=room)

# TODO:create User ,UserProfile, Controller
    # Create the new user from the valid form data
    new_user = User.objects.create_user(username = form.cleaned_data['username'], \
                                        password = form.cleaned_data['password1'],)
    new_user.save()
    profile = UserProfile.objects.create(user=new_user,room = room)
    profile.save()


     # Logs in the new user and redirects to his/her home page
    new_user = authenticate(username = request.POST['username'], \
                            password = request.POST['password1'])

    login(request,new_user)

    return redirect('/wedraw/')

# Action for join the game
@login_required
def join_game(request,label):

    room = get_object_or_404(Room, label = label)
    room.in_game = True
    room.save()
    user = request.user
    user_list = room.get_curr_user_list(room)
    
    profile = get_object_or_404(UserProfile, user = user)
    profile.room = room
    profile.save()
    user.save()

    try:
        controller = Controller.objects.get(room=room)
        
        player_list = UserProfile.objects.filter(room=room).order_by('join_room_time')
        player_number = len(player_list)
        player_list_json = serializers.serialize('json', player_list)
        
        controller.curr_round_number = 0
        controller.curr_turn_number = 0
        controller.player_number = player_number
        controller.player_list = player_list_json
        controller.save()

    except:
        player_list = UserProfile.objects.filter(room=room).order_by('join_room_time')
        player_number = len(player_list)

        player_list_json = serializers.serialize('json', player_list)
        controller = Controller.objects.create(curr_round_number = 0,
                                               max_round_number = 2,
                                               curr_turn_number = 0,
                                               player_number = player_number,
                                               player_list = player_list_json,
                                               room = room)
        controller.save()
    controller = Controller.objects.get(room=room)

    profile_list = UserProfile.objects.filter(room = room)
    # find out who is going to be the drawer
    # drawer = room.is_drawer(room)
    drawer = controller.get_curr_painter(controller).username
    # set in_game field to true
    room.in_game = True
    room.save()

    if room.current_player == 1:
         return HttpResponse("no")
    else:
        return HttpResponse("yes")
#backend
@login_required
def backend(request) :
    return render(request,'backend.html', {})

#check userinfo
@login_required
def userinfo(request,user_id="undifinded") :
    context = {}
    if user_id == "undifined":
        return HttpResponse("No such user")
    try:
        for p in UserProfile.objects.raw('select * from wedraw_userprofile where user_id = %s',[user_id]):
            context['score'] = p.score
            context['status'] = p.status
            context['guess_status'] = p.guess_status
            context['room_id'] = p.room_id
            context['user_id'] = p.user_id
            return HttpResponse(json.dumps(context), content_type="application/json")
        return HttpResponse("No such userid")
    except:
        return HttpResponse("error user id")
   
#check roominfo
@login_required
def roominfo(request,label="undifined") :
    context = {}
    if label == "undifined":
        return HttpResponse("No such room")
    try:
        for p in Room.objects.raw('select * from wedraw_room where label = %s',[label]):
            context['label'] = p.label
            context['host'] = p.host
            context['max_number'] = p.max_number
            context['current_playerNum'] = p.current_player
            context['in_game'] = p.in_game
            return HttpResponse(json.dumps(context), content_type="application/json")
        return HttpResponse("No such room")
    except:
        return HttpResponse("error room label")
