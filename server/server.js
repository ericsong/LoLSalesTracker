//packages
var bodyParser = require('body-parser'),
    express = require('express'),
    session = require('express-session'),
    http = require('http'),
    sendgrid = require('sendgrid')(process.env.SENDGRID_API_USER, process.env.SENDGRID_API_KEY),
    uuid = require('node-uuid'),
    app = express(),
    server = http.createServer(app),
    mongoose = require('mongoose');

//express middleware setup
app.use(express.static(__dirname + '/public'));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.set('view engine', 'jade');

// database setup
mongoose.connect('mongodb://localhost/lolwishlist');
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
	splash_url: String,
	id: Number	
    }),
    Item = mongoose.model('items', ItemSchema);

var UserSchema = mongoose.Schema({
  email: { type: String, unique: true },
	wishlist: Array,
	verified: Boolean,
  uuid: String,
	}),
	User = mongoose.model('users', UserSchema);

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
    }
});

var nameToId = {};
Item.find({}, function(err, items) {
	for(var i = 0; i < items.length; i++) {
		nameToId[items[i].name] = items[i].id;
	}
	console.log(nameToId);
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
                display_name: data[i]['display_name'],
				splash_url: data[i]['splash_url'],
                id: data[i]['id']
            });
        }

        console.log(skins);

	    res.json(skins);	
    });
});

//save a wishlist
app.post('/saveWishlist', function(req, res) {
	var email = req.body.email,
	    wishlist = req.body['wishlist[]'],
      token_uuid = uuid.v4();

	for(var i = 0; i < wishlist.length; i++) {
    	var key = wishlist[i].replace(/\s/g, '').trim().toLowerCase();
		wishlist[i] = nameToId[key];
	}

	var new_user = new User({
		email: email,
		wishlist: wishlist,
		verified: false,
    uuid: token_uuid
	});

	new_user.save(function(err) {
		if(err) {
      console.log(err);
      
			return res.json({
				'msg': 'failed', 
				'err': err
			});
		}

    sendgrid.send({
        to:       email,
        from:     'lolwishlist@gmail.com',
        subject:  'Hi confirm pls',
        text:     'yoyoyo go here http//localhost:8000/verify/' + token_uuid
    }, function(err, json) {
        if (err) { 
          return console.error(err); 
        }
		  
        return res.json({'msg': 'success'});
    });
	});
});

//verify a user
app.get('/verify/:token', function(req, res) {
  var token = req.params.token;

  User.findOne({uuid: token}, function(err, data) {
    if(err) {
      console.log("ERROR: verification");
      console.log(err);
      cb(err);
    }

    if(!data) {
      return res.render("verify.jade", {msg: "User not found!"});
    }


    if(!data.verified){
      data.verified = true;

      data.save(function(err) {
        if(err) {
          console.log("ERROR: verification update");
          console.log(err);
          cb(err);
        }

        return res.render("verify.jade", {msg: "Email verified!"});
      });
    } else {
      return res.render("verify.jade", {msg: "Email already verified."});
    }
  });
});
