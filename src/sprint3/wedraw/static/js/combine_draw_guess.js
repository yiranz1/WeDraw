var context;
var startX;
var startY;
var start = false;
var rect;
var dataURL;
var word;

var timer;
var drawer = true;


// get the canvas element using the DOM for guesser
var canvas;
var room = $("p.room");
var roomId = room.attr("data-room-id");

const webSocketBridgeCounter = new channels.WebSocketBridge();
webSocketBridgeCounter.connect('/counter/'+roomId);
webSocketBridgeCounter.listen(function(action, stream) {
  //console.log("======paiter.js listern : wsbridge counter ===")
});

var ws_path = '/room/'+roomId;

canvas = $('#drawing-area').get(0);

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
webScore.connect('/score/'+roomId);

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
    if (action.draw) {
      curTool = action.drawstyle;
      curRadius = action.curRadius;
      curColor = action.curColor;
      if (curTool == "Pencil") {
        context.lineWidth = curRadius;
        context.fillStyle = curColor;
        context.strokeStyle = curColor;
      }
    
      if (curTool == "Eraser"){
        //TODO:reset radius,color,tool etc
        context.strokeStyle = "rgb(255,255,255)";//white
        context.fillStyle = "rgb(255,255,255)";
        context.lineWidth = 20;//this is the default radius for eraser
      }
     
      context.beginPath();
      context.moveTo(action.x, action.y);
      context.lineTo(action.startX, action.startY);
      context.closePath();
      context.stroke();
      if (curTool == "Spray") {

        context.lineWidth = curRadius;
        context.fillStyle = curColor;
        context.strokeStyle = curColor;
        alert(context.strokeStyle);
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
    if (action.guess){
      alert(stream.guess);
    }
  }
    
  });


//helper function for Tools
function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

//initlize word information, hints, ect.
function wordInfoset(){
  $.post("/wedraw/getWordInfo/")
  .done(function(data) {
    if (true) {
      var word = data['word'];
      var wordSend = new Object();
      wordSend.word = data['word'];
      wordSend.hint1 = data['hint1'];
      wordSend.hint2 = data['hint2'];
      wordSend.hint3 = data['hint3'];
      wordSend.command = "word";
      // contendSend.drawstyle = 1;
      webSocketBridge.send(JSON.stringify(wordSend));
      document.getElementById("painter-hint").innerHTML = "You Are Drawing : " + word;
    }
    painter_mod();
});
}

function wait(ms){
  var start = new Date().getTime();
  var end = start;
  while(end < start + ms) {
    end = new Date().getTime();
 }
}

// #=====================================================================================
// #
// #  Code chunk 2 : painter - DOM (copy from draw.js)
// #
// #=========================================================================================
// get the start position of the mouse, when mouse is down, start drawing

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
    if (drawer) {
      event.preventDefault();

      // get the x and y coordinate in drawing-area
      var x = event.clientX - rect.left;
      var y = event.clientY - rect.top;
     
      //   // draw something
      if (curTool == "Pencil") {
        context.lineWidth = curRadius;
        context.fillStyle = curColor;
        context.strokeStyle = curColor;
      }
      if (curTool == "Spray") {
        //TODO:reset
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

      // TODO:implement tools
      if (curTool == "Eraser"){
        //TODO:reset radius,color,tool etc
        context.strokeStyle = "rgb(255,255,255)";//white
        context.fillStyle = "rgb(255,255,255)";
        // curColor = "rgb(255,255,255)";
        context.lineWidth = curRadius;
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
      context.beginPath();
      context.moveTo(x, y);
      context.lineTo(startX, startY);
      context.closePath();
      context.stroke();
      startX = x;
      startY = y;

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

function counter(seconds) {
  var counter = $('#counter');

  timer = setInterval(function(){
    seconds--;

    counter[0].innerHTML = seconds;
    var contentSend = new Object();
    contentSend.seconds = seconds;
    contentSend.command = "counter";
    webSocketBridgeCounter.send(JSON.stringify(contentSend));

    if(seconds == 0) {
        clearInterval(timer);
        
        $.post("/wedraw/new-a-turn",{})
            .done(function (data) {
                if (data == "True"){
                  alert("Check code! Bug!");
                }
                else if(data == "False"){
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
        })
    }
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
  wait(1000);
  wordInfoset();

  counter(25);

  $('#clear-btn').click(function () {
      context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
      var contentSend = new Object();
      contentSend.command = "clear";
      webSocketBridge.send(JSON.stringify(contentSend));
  });

  $('#tool-form li[class="tool"]').click(function(){
      curTool = this.id;
  });

// Choose color
  $('#color-form li[class="color"]').click(function(){

    var color = this.id;
    if(color == "Red") {
      curColor = "rgb(255, 0, 0)";
    } else if (color == "Blue")
    curColor = "rgb(0, 153, 255)";
    else if (color == "Yellow") {
      curColor = "rgb(255, 255, 0)";
    }
    else if (color == "Black") {
      curColor = "rgb(0,0,0)";
    }
});

$('#size-form li[class="size"]').click(function(){
  var size = this.id;
  if(size == "Big") {
    curRadius = 25;
  } else if (size == "Medium")
  curRadius = 15;
  else if (size == "Small") {
    curRadius = 5;
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
