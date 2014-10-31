//packages
var bodyParser = require('body-parser'),
    express = require('express'),
    session = require('express-session'),
    go_api = require('./apis/apis'),
    http = require('http'),
    app = express(),
    server = http.createServer(app),
    io = require('socket.io')(server);

//express middleware setup
app.use(express.static(__dirname + '/public'));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.set('view engine', 'jade');
app.use(session({ secret: 'foodupzzz', cookie: { maxAge: 60000 }}));

//server globals
var players = [],
    stats = {
      correct: 0,
      incorrect: 0,
    },
    GO_queue = [],
    queue_max_size = 10,
    requeue_size = 5;

//init routine
//cache 10 game objects
for(var i = 0; i < queue_max_size; i++) {
  go_api.getNextGameObject(function(err, go) {
    GO_queue.push(go);
  });
}

//server game functions
var broadcastPlayers,
    popGameObject,
    runGameCycle,
    sendStats;

broadcastPlayers = function(type, msg) {
  console.log(msg);
  for(var i = 0; i < players.length; i++) {
    players[i].socket.emit(type, msg);
  }
}

popGameObject = function() {
  var go = GO_queue.pop();

  if(GO_queue.length < requeue_size) {
    go_api.getNextGameObject(function(err, go) {
      GO_queue.push(go);
    });
  }

  return go;
}

runGameCycle = function() {
  var go = popGameObject();
  broadcastPlayers("game_object", go); 

  setTimeout(function() {
    broadcastPlayers("stats", stats); 
    stats.correct = 0;
    stats.incorrect = 0;

  }, 10000);
};

//socket.io setup
io.on('connection', function(socket) {
  socket.on('joined', function(data) {
    console.log('a player joined');
    for(var i = 0; i < players.length; i++) {
      socket.emit("new_player", {name: players[i].name});
    }
  	console.log(data);
    players.push({
      socket: socket,
      name: data.name
    });

    broadcastPlayers("new_player", {name: data.name});
  });

  socket.on('remove_player', function(data) {
    console.log("removing:" + data.name);
    broadcastPlayers("remove_player", {name: data.name});
  });

  socket.on('answer', function(data) {
    if(data.result) {
      stats.correct = stats.correct + 1;
    } else if (!data.result) {
      stats.incorrect = stats.incorrect + 1;
    }
  });

});

//start server
server.listen(80);

//start game
setInterval(runGameCycle, 15000);

//express functions
app.get('/', function(req, res) {
  res.render('index.jade');
});

app.get('/testBroadcast', function(req, res) {
  broadcastPlayers("test", {msg: "hello players"});
});
