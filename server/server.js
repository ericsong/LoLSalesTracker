//packages
var bodyParser = require('body-parser'),
    express = require('express'),
    session = require('express-session'),
    http = require('http'),
    app = express(),
    server = http.createServer(app);

//express middleware setup
app.use(express.static(__dirname + '/public'));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.set('view engine', 'jade');

//init routine
//start game

//express functions
app.get('/', function(req, res) {
  res.render('index.jade');
});

app.get('/testBroadcast', function(req, res) {
  broadcastPlayers("test", {msg: "hello players"});
});
