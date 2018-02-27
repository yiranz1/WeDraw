from django.conf.urls import include, url
#from django.contrib.auth import views as auth_views
from wedraw import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Route for our application's home page
    url(r'^$', views.home, name = 'home'),

    url(r'^backend/$', views.backend, name = 'backend'),
    url(r'^userinfo/(?P<user_id>\d+)$', views.userinfo, name = 'userinfo'),
    url(r'^userinfo/?$', views.userinfo, name = 'userinfo'),
    url(r'^roominfo/(?P<label>[\w-]{,50})/$', views.roominfo, name = 'roominfo'),
    url(r'^roominfo/?/$', views.roominfo, name = 'roominfo'),
    url(r'^whetherInCurrentRoom/(?P<label>[\w-]{,50})/$', views.checkInRoom, name = 'incurrentRoom'),
    url(r'^join-game/(?P<label>[\w-]{,50})/$', views.join_game, name = 'join-game'),

    # User log in
    url(r'^login$',auth_views.login, {'template_name':'wedraw/login.html','redirect_authenticated_user': True},name = 'login'),    
    # Route to log out a user and send them back to the log in page.
    url(r'^logout$',auth_views.logout_then_login,name='logout'),
    # User sign up
    url(r'^signup',views.signup, name='signup'),

    # render to draw/guess
    url(r'^join-room/(?P<label>[\w-]{,50})/drawer$', views.drawer_page, name = 'drawer'),
    url(r'^join-room/(?P<label>[\w-]{,50})/guesser$', views.guesser_page, name = 'guesser'),
    url(r'^getWordInfo', views.getwordsInfo, name = 'getwordsInfo'),
    
    url(r'^new-a-turn', views.new_turn, name = 'new-a-turn'),
    url(r'^get-curr-painter',views.get_curr_painter,name='get-curr-painter'),
    url(r'^add-score',views.add_score,name='add-score'),
    # check guessing result
    url(r'^check-result/$', views.check_guessing_result, name = 'check_result'),
    
    url(r'^new/$', views.new_room, name='new_room'),

    # join game room, leave game room, get changes  
    url(r'^leave-room/(?P<label>[\w-]{,50})/$',views.leave_room,name='leave-room'),
    url(r'^join-room/(?P<label>[\w-]{,50})/$', views.join_room, name='join_room'),
    url(r'^get-changes/(?P<time>.+)$', views.get_changes),
    url(r'^get-changes/?$', views.get_changes),
    url(r'^get-results/?$', views.game_result),

    # changes in profile page
    url(r'^get-changes-host/(?P<time>.+)/(?P<label>[\w-]{,50})$', views.get_changes_host),
    url(r'^get-changes-host/(?P<label>[\w-]{,50})/?$', views.get_changes_host),

]