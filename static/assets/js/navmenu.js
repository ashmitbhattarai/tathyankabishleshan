(function($) {
	$('nav#search_nav ul li a').click(function(){
		var el = $(this);
		var top = $('nav#search_nav ul li a');
		console.log(top);
		top.removeClass('selected');
		el.addClass('selected');
	});

	$('select#top_box option').click(function(){
		var bel = $(this);
		var gtop = $('select#top_box option');
		console.log(gtop);
		if (gtop.hasClass('selected')){
			gtop.removeClass('selected');
		}
		bel.addClass('selected');
	});
	
})(jQuery);