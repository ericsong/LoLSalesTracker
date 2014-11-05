LOLWISHLIST_APP = {}

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
	newItem.removeAttr('id');
	newItem.css('display', 'inline');
	return newItem;
}

var loadSkins = function(skins) {
	for(var i = 0; i < skins.length; i++) {
		var newItem = createSkinItem(skins[i]).hide().fadeIn(2000);
		$('.select-area').append(newItem);
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
