var webSocketBridge = new channels.WebSocketBridge();

// var room = $("p.room");
// roomId = room.attr("data-room-id");

var ws_path = "/home/";

webSocketBridge.connect(ws_path);
webSocketBridge.listen(function(data) {
    // Decode the JSON
    
    var rooms = data.text;
    max_time = rooms.max_time;
    var list = $("#roomlist");

    $.get("/wedraw/get-changes/"+ max_time)
            .done(function(data) {
                list.data('max-time', data['max-time']);
                for (var i = 0; i < data.rooms.length; i++) {
                    var room = data.rooms[i];
                    var new_room = $(room.html);

                    list.prepend(new_room);              
                }
            });

});

function roomList() {
    $.get("/wedraw/get-changes")
      .done(function(data) {
          
          var list = $("#roomlist");
          list.data('max-time', data['max-time']);
          var max_time = list.data("max-time");
          list.html('');
          
          for (var i = 0; i < data.rooms.length; i++) {
              room = data.rooms[i];
              
              var new_room = $(room.html);
              list.prepend(new_room);
          }
          
      });
      
}


$(document).ready(function () {
    roomList();
    // Periodically refresh to-do list
    //window.setInterval(getUpdates, 5000);
    $('#new_room').click(function () {

        var list = $("#roomlist");
        var max_time = list.data("max-time");
        
        var home = new Object();
        home.command = "home";         
        home.list = list;
        home.max_time = max_time;
               
        webSocketBridge.send(JSON.stringify(home));
        
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