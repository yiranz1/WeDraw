from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels.sessions import channel_session
from channels import Group
from channels import Channel
import ast
import json
from channels.auth import channel_session_user_from_http, channel_session_user
from .models import Room
# In consumers.py

@channel_session_user_from_http
def ws_add(message):

    info = message.content['path'].strip("/").split("/")
    if len(info) == 2:
        message.reply_channel.send({"accept": True})
        cmd = info[0]
        roomID = info[1]
        message.channel_session['room'] = roomID
        Group("%s-%s" % (cmd,roomID)).add(message.reply_channel)

        user = message.user.username
        if cmd == "room":
            Group("%s-%s" % (cmd,roomID)).send({"text": json.dumps({"user": user})})
    else:
        message.reply_channel.send({"accept": True})
        Group("home").add(message.reply_channel)


@channel_session
def ws_message(message):
    array = json.loads(message.content['text'])
    arrayjson = json.loads(array)
    cmd = arrayjson['command']
    if cmd == 'home':
        Group("home").send({
            "text": json.dumps({
                "text": arrayjson,
            })})
    elif cmd == 'begin' or cmd == 'clear' or cmd== 'word' or cmd=='draw' or cmd == 'leave':
        room = message.channel_session['room']
        Group("room-%s" % room).send({
            "text": json.dumps({
                "text": arrayjson,
            })})
    # command score, room, count go in here
    else:
        room = message.channel_session['room']
        Group("%s-%s" % (cmd, room)).send(
            {
                "text": json.dumps({
                    "text": arrayjson,
                }),
            }
        )

@channel_session
def ws_disconnect(message):
    
    if message.channel_session.get("room") is not None:
        room_id = message.channel_session.get('room')
        try:
            room = Room.objects.get(pk=room_id)
                
            # Removes user from the room's send group. If this doesn't get run,
            # we'll get removed once our first reply message expires.
            Group("room-%s" % room_id).discard(message.reply_channel)
        except Room.DoesNotExist:
            pass
    Group("home").discard(message.reply_channel)
