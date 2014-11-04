//packages
var bodyParser = require('body-parser'),
    express = require('express'),
    session = require('express-session'),
    http = require('http'),
    app = express(),
    server = http.createServer(app),
    mongoose = require('mongoose');

//express middleware setup
app.use(express.static(__dirname + '/public'));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.set('view engine', 'jade');

// database setup
mongoose.connect('mongodb://localhost/skinsfarm');
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function cb() {
	console.log("mongoose connected");
});

// item schema
var ItemSchema = mongoose.Schema({
	type: String,
	name: String,
	display_name: String,
	id: Number	
    }),
    Item = mongoose.model('items', ItemSchema);

//
// init
//

//cache champ list
var champions = [];
Item.find({type: "champ"}, function(err, champs) {
	for(var i = 0; i < champs.length; i++) {
        champions.push({
            name: champs[i]['name'],
			display_name: champs[i]['display_name'],
            id: champs[i]['id']
        });
		console.log(champs[i]);
		console.log(champs[i]['key']);
    }
});

//start server
server.listen(8000);

//
//express functions
//

//landing page
app.get('/', function(req, res) {
    res.render('home.jade');
});

//return list of champion names
app.get('/getChampions', function(req, res) {
	res.json(champions);
});

//get list of skins for champ
app.get('/getChampSkins', function(req, res) {
    var champ = req.query.champ;
    champ = champ.replace(/\s/g, '').trim().toLowerCase();

    Item.find({'champ': champ}, function(err, data) {
        var skins = [];

        for(var i = 0; i < data.length; i++) {
            skins.push({
                type: data[i]['type'],
                champ: data[i]['champ'],
                name: data[i]['name'],
                id: data[i]['id']
            });
        }

	    res.json(skins);	
    });
});

//save a wishlist
app.post('/saveWishlist', function(req, res) {

});
