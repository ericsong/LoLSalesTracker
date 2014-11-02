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

//express functions

//return list of champion names
app.get('/getChampions', function(req, res) {
	res.json();
});

//get list of skins for champ
app.get('/getChampSkins', function(req, res) {
	res.json();	
});

//save a wishlist
app.post('/saveWishlist', function(req, res) {

});
