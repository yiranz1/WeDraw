function decodeEntities(encodedString) {
    var textArea = document.createElement('textarea');
    textArea.innerHTML = encodedString;
    return textArea.value;
}

$(document).ready(function () {
  // Set up to-do list with initial DB items and DOM data
  $("#requestBackend").off().click(function(event) {
     //$('#postbottom').on('submit', function(event) {
    // console.log("post!")
    event.preventDefault(); // Prevent form from being submitted
    var myFormPost = $("#backend-form").serializeArray();
    var userInfoList = $("#UserInfoList")
    var content = {};
    $.each(myFormPost, function (index, itemfield ) {
        content[itemfield.name] = itemfield.value;
    });
    $.get("/wedraw/userinfo/" + content.user)
    .done(function(data) {
        console.log(data)
        userInfoList.empty()
        var jsonStr = JSON.stringify(data);
        userInfoList.append("<li>"+jsonStr+"</li>");

    });
  //});
});

$("#requestBackendRoom").off().click(function(event) {
    //$('#postbottom').on('submit', function(event) {
   // console.log("post!")
   event.preventDefault(); // Prevent form from being submitted
   var myFormPost = $("#backend-roomform").serializeArray();
   var roomInfoList = $("#RoomInfoList")
   var content = {};
   $.each(myFormPost, function (index, itemfield ) {
       content[itemfield.name] = itemfield.value;
   });
   console.log(content.room)
   $.get("/wedraw/roominfo/" + content.room)
   .done(function(data) {
       console.log(data)
       roomInfoList.empty()
       var jsonStr = JSON.stringify(data);
       roomInfoList.append("<li>"+jsonStr+"</li>");

   });
 //});
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
