LOLWISHLIST_APP = {}

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
	$.get('/getChampSkins', {champ: champ_name}, function(data) {
		console.log(data);
	});
});
