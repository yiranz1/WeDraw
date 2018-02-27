var webSocketBridge = new channels.WebSocketBridge();

var room = $("p.room");
roomId = room.attr("data-room-id");

var ws_path = "/room/"+roomId;

webSocketBridge.connect(ws_path);
webSocketBridge.listen(function(data) {
    // Decode the JSON
    if(data.user == undefined) {
        var begin = data.text;
        if (begin.command == "begin") {
            if ($("#begingame").length == 0) {
                window.location.href = "guesser"
            } else if ($("#begingame").length == 1) {
                window.location.href = "drawer";
            }
        }
        else if (begin.command == 'leave') {
            var host = data.text;
            max_time = host.max_time;
    
            var list = $("#start_game");
            var player_list = $("#player");
            var label = $("p.room").attr("room-label");
            var cur_user = $("#start_game").attr("user");

            var old_host = document.getElementById('begingame');
            $.get("/wedraw/get-changes-host/"+ max_time +"/" + label)
                    .done(function(data) {
                        
                        list.data('max-time', data['max-time']);
                        
                        // if the old host left the room and current user is the host, then give him the start button
                        if (old_host == undefined && data.host == cur_user) {
                            var start = $("<input class='btn btn-block btn-default' type='submit' value='Let us begin!' id ='begingame' room-label=" + label +">");
                            
                            list.append(start);
                            $('#begingame').click(function () {
                                    // var new_request = {};
                                    var rl = $('#begingame').attr("room-label");

                                    $.get("/wedraw/join-game/" + rl,{})
                                        .done(function (data) {
                                    if (data == "yes") {
                                    var roomInfoSend = new Object();
                                    roomInfoSend.command = "begin";
                                    webSocketBridge.send(JSON.stringify(roomInfoSend));
                                    }
                                });

                            });

                        }
                        
                    });
                $.get("/wedraw/whetherInCurrentRoom/" + label)
                    .done(function(data) {
                        if (data == "true") {
                            location.reload(true);
                        }
                    });

                }
    } 
    else {

        var user = document.getElementById(data.user);
        if (user != null) {           
            user.innerHTML = data.user;
        }       
        else {         
            var message = $("<p class = collection-item id =" + data.user + ">" + data.user + "</p>");
            
            $("#player").append(message);                   
        }
    }
    });



$(document).ready(function () {
    // when user clicks on begin button, start the game
    $('#begingame').click(function () {
        // var new_request = {};
        var rl = $('#begingame').attr("room-label");
        // new_request['label'] = rl;

        $.get("/wedraw/join-game/" + rl,{})
            .done(function (data) {
                if (data == "yes") {
                    var roomInfoSend = new Object();
                    roomInfoSend.command = "begin";
                    webSocketBridge.send(JSON.stringify(roomInfoSend));
                }
            })

    });

    // when a user click on leave-room, check the change in that game room
    // and send it to other users in the room
    $('#leave-room').click(function () {
        
        var list = $("#start_game");
        var max_time = list.data("max-time");
        
        var leave = new Object();
        leave.command = "leave";     
        leave.max_time = max_time;
               
        webSocketBridge.send(JSON.stringify(leave));
        
    });

    // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });

});