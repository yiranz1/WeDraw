var context;
var startX;
var startY;
var start = false;
var rect;
var word;
var count = 0;

var timer;
var drawer = false;

// get the canvas element using the DOM for guesser
var canvas;
var room = $("p.room");
var roomId = room.attr("data-room-id");

var ws_path = "/room/"+roomId;

canvas = $('#displaying-area').get(0);

context = canvas.getContext("2d");
//draw canvas
//global variable for the DEFAULT brush effect
//these can be changes by clicking the button
var curTool = "Pencil";
var curRadius = 15;
//remember to change the color for BOTH fillstyle and strockstyle
var curColor = "rgb(0,0,0)";//bule

// build webSocketBridge
// for drawer, when change role need to be close!
const webSocketBridge = new channels.WebSocketBridge();
webSocketBridge.connect(ws_path);
const webScore = new channels.WebSocketBridge();

function draw() {
 
  if(!canvas) {
    alert("Can't find the canvas element");
    return;
  }

  if(!(canvas.getContext)) {
    alert("Sorry, can't find context");
    return;
  }

  // get the graph context
  context = canvas.getContext("2d");

  // get canvas area
  rect = canvas.getBoundingClientRect();

}

webScore.connect('/score/'+roomId);
    webScore.listen(function(data) {
      var D = data.text;
      var guesser = document.getElementById(D.user);

      var user = ("Score is : "+D.score);
      guesser.innerHTML = user;
  });

  webSocketBridge.listen(function(action, stream) {
    if (!drawer) {
      var dataGet = action.text;
    if (dataGet == undefined) {
      return;
    }
    else if (dataGet.command == "draw") {
      curTool = dataGet.drawstyle;
      curRadius = dataGet.curRadius;
      curColor = dataGet.curColor;
      var x = dataGet.x;
      var y = dataGet.y;
      if (curTool == "Pencil") {
        context.lineWidth = curRadius;
        context.fillStyle = curColor;
        context.strokeStyle = curColor;
      }
    
      if (curTool == "Eraser"){
        context.strokeStyle = "rgb(255,255,255)";//white
        context.fillStyle = "rgb(255,255,255)";
        context.lineWidth = 20;//this is the default radius for eraser
      }
      if (curTool == "Spray") {
        context.lineWidth = curRadius;
        context.fillStyle = curColor;
        context.strokeStyle = curColor;
        for (var i = 50; i--; ) {
              var radius = curRadius;
              var offsetX = getRandomInt(-radius, radius);
              var offsetY = getRandomInt(-radius, radius);
              context.fillRect(x + offsetX, y + offsetY, 1, 1);
          }
      }

      context.beginPath();
      context.moveTo(dataGet.x, dataGet.y);
      context.lineTo(dataGet.startX, dataGet.startY);
      context.closePath();
      context.stroke();
      if (curTool == "Spray") {
        context.lineWidth = curRadius;
        context.fillStyle = curColor;
        context.strokeStyle = curColor;
        for (var i = 50; i--; ) {
              var radius = curRadius;
              var offsetX = getRandomInt(-radius, radius);
              var offsetY = getRandomInt(-radius, radius);
              context.fillRect(x + offsetX, y + offsetY, 1, 1);
          }
      }
      else {
        context.stroke();
      }
    }
    if (dataGet.command == "clear") {
      context.clearRect(0, 0, context.canvas.width, context.canvas.height);
    } 
    if (dataGet.command == "word") {
      word = dataGet.word;
      var hint1 = dataGet.hint1;
      var hint2 = dataGet.hint2;
      var hint3 = dataGet.hint3; 
      document.getElementById("guesser-hint1").innerHTML = hint1;
      document.getElementById("guesser-hint2").innerHTML = hint2;
      document.getElementById("guesser-hint3").innerHTML = hint3;
      var str = "";
      for (var i = 0; i < word.length; i++) {
        str = str + " _";
      }
      document.getElementById("guesser-hint").innerHTML = str;
      $('#guesser-hint1').css("display","none");
      $('#guesser-hint2').css("display","none");
      $('#guesser-hint3').css("display","none");   
    }

  }
  
  });


//helper function for Tools
function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

$('#guesser-submit-btn').click(function (event) {
  event.preventDefault();
  if (word == null) {
    alert("no word for you to guess ");
    return;
  }

  var result = document.getElementById("guess-result");

  if (result == null) {
    alert("can't find place to display guessing result");
    return;
  }
  var postField = $("#guesser-submit-input");
  $.post("/wedraw/check-result/",{"guess":postField.val()})
        .done(function(data) { 
          
          if (data.result == true) {
            $.post("/wedraw/add-score")
              .done(function(data) { 
                var score = new Object();
                score.command = "score";  
          
                score.score = data['score'];
                score.user = data['username'];
                webScore.send(JSON.stringify(score));
              });
          } 
          result.innerHTML = data.message;
        });
});



// When user resize the browser window, relocate the draw area
$(window).resize(function() {
  draw();
});

// draw
  // get the start position of the mouse, when mouse is down, start drawing
  $( "#drawing-area" ).mousedown(function(event) {
      // judgeUserStatus();
      if (drawer) {

        event.preventDefault();;
        // get the x and y coordinate in drawing-area
        // need to substract rect.left and rect.top in order to get the right coordinate
        startX = event.clientX - rect.left;
        startY = event.clientY - rect.top;
        start = true;
      }
  });

  // When the mouse is moving, draw as the mouse goes
  $( "#drawing-area" ).mousemove(function(event) {
    if(!start) {
        return;
      }
    // judgeUserStatus();
    if (drawer == false) {
      event.preventDefault();


      // get the x and y coordinate in drawing-area
      var x = event.clientX - rect.left;
      var y = event.clientY - rect.top;
     
      // draw something

      if (curTool == "Pencil") {
        context.lineWidth = curRadius;
        context.fillStyle = curColor;
        context.strokeStyle = curColor;
      }

      // TODO:implement tools
      if (curTool == "Eraser"){
        //TODO:reset radius,color,tool etc
        context.strokeStyle = "rgb(255,255,255)";//white
        context.fillStyle = "rgb(255,255,255)";
        curColor = "rgb(255,255,255)";
        context.lineWidth = 20;//this is the default radius for eraser
      }

      var contentSend = new Object();
      contentSend.x = x;
      contentSend.y = y;
      contentSend.startX = startX;
      contentSend.startY = startY;
      contentSend.drawstyle = curTool;
      contentSend.curColor = curColor;
      contentSend.curRadius = curRadius;
      contentSend.command = "draw";
      // contendSend.drawstyle = 1;
      webSocketBridge.send(JSON.stringify(contentSend));
      context.strokeStyle = curColor;
      context.beginPath();
      context.moveTo(x, y);
      context.lineTo(startX, startY);
      context.closePath();
      context.stroke();
      startX = x;
      startY = y;

      // dataURL = canvas.toDataURL();
      // localStorage.setItem( 'objectToPass', dataURL );
    }
});


  // when mouse is up, stop drawing
  $( "#drawing-area" ).mouseup(function(event) {
    // judgeUserStatus();
    if (drawer) {
      event.preventDefault();
      start = false;
    }
    // dataURL = canvas.toDataURL();
  });

  // when user moves his mouse out of the bound of canvas, stop drawing
  $( "#drawing-area" ).mouseout(function(event) {
    // judgeUserStatus();
    if (drawer) {
      event.preventDefault();
      start = false;
  }
  });
// draw area end 

// time counter
function counter(seconds) {
  // get the counter element in the html template
  var counter = $('#counter');

  // set a timer to run for every 1000ms, that's 1 second
  timer = setInterval(function(){
    seconds--;

    // display the remaining time
    counter[0].innerHTML = seconds;
    // if time counts down to 0, stop timing
    if(seconds == 0)
        clearInterval(timer);

    },1000);

}

function painter_mod() {

    rect = canvas.getBoundingClientRect();
}

// #=====================================================================================
// #
// #  Code chunk 3 ：
// #
// #===================================================================================


$(document).ready(function () {
  painter_mod();

  // counter(60);
  const webSocketBridgeCounter = new channels.WebSocketBridge();
  webSocketBridgeCounter.connect('/counter/'+roomId);
  webSocketBridgeCounter.listen(function(action, stream) {

      action = action['text'];

      if (action.command == "counter"){

        var counter = $('#counter');
        counter[0].innerHTML = action.seconds;
        if(action.seconds<20) {
          $('#guesser-hint1').css("display","block");
        }
        if(action.seconds<15) {
          $('#guesser-hint2').css("display","block");
        }
        if(action.seconds<10) {
           $('#guesser-hint3').css("display","block");
        }
        if(action.seconds == 0){
            
            $.post("/wedraw/get-curr-painter",{})
              .done(function (data) {
                
                if(data == "True"){
                  window.location.href = "drawer";
                }
                else if (data == "False") {
                  window.location.href = "guesser";
                }
                else {
                  
                  var message = "";
                  
                  for (var i = 0; i < data.user.length; i++) {
                    user = data.user[i];
                    score = data.score[i];
                    message += user +" Score is : " + score + "\n";
                  }
                  message += "Winner of the game is "+data.winner;
                  alert(message);
                  
                  var rl = room.attr("room-label");
                  var new_path = "/wedraw/join-room/" + rl;
                  window.location.href = new_path;
                  
                }
            });

        }
      }
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
