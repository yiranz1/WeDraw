Please complete all your project development in this directory and 
its subdirectories (which you may create as neeeded).

For sprint 1 we have a working drawing canvas and guessing system.
When users log in or sign up, they will be navigate to the home page, 
then they can click on Join Game button to join the game.

For sprint 1 our logic is that if the user is the first registered user to 
our application, then he is considered to be the painter, other users will
be guessers. To test paint function, if currently there is no user registered,
you can register a first user and then join the game. When you create a second user and 
join the game, you will be a guesser, currently you can't see the drawings since we haven't 
implement any real-time interations, but you can still guess the word. There are 3 hints, 
every five seconds one of the hint will show up although right now the hints are not very meaningful.
To make a guess, you can type your answer in the box and click on "Guess" and you will get a
guessing result.

If you are in guesser mode and want to test painter mode, simply click on Fource 
Quit in the page and click on 'Join Game' again, then you will be in the painter 
mode and can draw with different tools. Currently you can draw with different colors
and different brush sizes, you can also erase your drawings or clear the whole canvas.

For sprint 2 we implemented real-time game interactions using websocket, we created a room model 
for users to create a public game room, currently the room only allows two users to enter.
In the game room, only the host(creater) of the room can start the game, both users can choose to 
leave the room, if the host leaves the room, the other user becomes the host.
We can also switch the player's role (painter/guesser) when the time is up.