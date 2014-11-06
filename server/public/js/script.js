$(document).foundation();

LOLWISHLIST_APP = {}
LOLWISHLIST_APP.wishlist = [];

var clearSkins = function() {
	var current_items = $('.select-area li.item-li');
	for(var i = 0; i < current_items.length; i++) {
		$(current_items[i]).fadeOut(1000, function() { $(this).remove(); });
	}
}

var createSkinItem = function(skin) {
	var newItem = $('#skin_template').clone();
	$($(newItem).find('img')[0]).attr('src', skin.splash_url);;
	$($(newItem).find('.title-container')[0]).text(skin.display_name);
	newItem.click(addItemClick);
	newItem.removeAttr('id');
	newItem.css('display', 'inline');
	return newItem;
}

var loadSkins = function(skins) {
	for(var i = 0; i < skins.length; i++) {
		var newItem = createSkinItem(skins[i]).hide().fadeIn(1000);
		$('.select-area').append(newItem);
	}
}

var addItemClick = function() {
	var title = $($(this).find('.title-container')[0]).text();
	addToWishlist(title);

	//remove from list
	$(this).fadeOut(500, function() { $(this).remove(); });
}

var removeItemClick = function() {
	var title = $($(this).parent().find('div')[0]).text();
	removeFromWishlist(title);
}

//add to wishlist var and draw item
var addToWishlist = function(title) {
	LOLWISHLIST_APP.wishlist.push(title);
	var newItem = $('#wishlist_template').clone();
	$($(newItem).find('div')[0]).text(title);
	$($(newItem).find('input')[0]).click(removeItemClick);
	newItem.removeAttr('id');
	newItem.css('display', 'list-item');
	newItem.hide().fadeIn(500);
	$($('.wishlist-list ul')[0]).append(newItem);
}

var removeFromWishlist = function(title) {
	var index = LOLWISHLIST_APP.wishlist.indexOf(title);

	//remove from wishlist array
	if(index > -1) {
		LOLWISHLIST_APP.wishlist.splice(index, 1);
	}

	//remove from wishlist html
	items = $('.wishlist-list ul li');
	for(var i = 0; i < items.length; i++) {
		if($($(items[i]).find('div')[0]).text() === title) {
			$(items[i]).fadeOut(500);
			break;
		}
	}
}

$.get('/getChampions', function(data) {
	LOLWISHLIST_APP.champ_names = [];
	for(var i = 0; i < data.length; i++) {
		LOLWISHLIST_APP.champ_names.push(data[i].display_name);
		$('<option/>', { value : data[i].display_name }).appendTo('#champions')
	}
});

$('#load-skins-button').click(function() {
	var champ_name = $('#champ-input').val();
	champ_name = champ_name.replace(/\s/g, '').trim().toLowerCase();

	//clear existing skins
	clearSkins();	
	
	$.get('/getChampSkins', {champ: champ_name}, function(data) {
		loadSkins(data);
		console.log(data);
	});
});

//Load default champ
clearSkins();
$.get('/getChampSkins', {champ: 'annie'}, function(data) {
		loadSkins(data);
		console.log(data);
});
