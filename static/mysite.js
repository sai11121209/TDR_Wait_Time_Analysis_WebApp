$(function(){
	var scrollPos;

	scrollPos = $(window).scrollTop();

	$('.headerTitle').hide();

	$('.headerTitle').each(function(i) {
		$(this).fadeIn(1500);
	});

	$('.headerNav ul li').hide();

	$('.headerNav ul li').each(function(i) {
		$(this).fadeIn(1500);
	});

	$('.headerUser ul li').hide();

	$('.headerUser ul li').each(function(i) {
		$(this).fadeIn(1500);
	});

	$(window).on('load', function() {
		var url = $(location).attr('href');
		if(url.indexOf("#") != -1){
			var anchor = url.split("#");
			var target = $('#' + anchor[anchor.length - 1]);
			if(target.length){
				var pos = Math.floor(target.offset().top) - 100;
				$("html, body").animate({scrollTop:pos}, 1);
			}
		}
	});

	$('a[href^=#]').click(function() {
		var speed = 400;
		var href= $(this).attr("href");
		var target = $(href == "#" || href == "" ? 'html' : href);
		var position = target.offset().top-100;
		$('body,html').animate({scrollTop:position}, speed, 'swing');
		return false;
	});

	$('#openModal1').click(function(){
		$('#modalArea1').fadeIn();
		scrollPos = $(window).scrollTop();
		$('body').addClass('fixed').css({ top: -scrollPos });
	});

	$('#closeModal1, #modalBg1').click(function(){
		$('body').removeClass('fixed').css({ top: $(window).scrollTop(scrollPos) });
		$('#modalArea1').fadeOut();
		return false;
	});

	$('#openModal2').click(function(){
		$('#modalArea2').fadeIn();
		scrollPos = $(window).scrollTop();
		$('body').addClass('fixed').css({ top: -scrollPos });
	});

	$('#closeModal2, #modalBg2').click(function(){
		$('body').removeClass('fixed').css({ top: $(window).scrollTop(scrollPos) });
		$('#modalArea2').fadeOut();
		return false;
	});

	$('#openModal3').click(function(){
		$('#modalArea3').fadeIn();
		scrollPos = $(window).scrollTop();
		$('body').addClass('fixed').css({ top: -scrollPos });
	});

	$('#closeModal3, #modalBg3').click(function(){
		$('body').removeClass('fixed').css({ top: $(window).scrollTop(scrollPos) });
		$('#modalArea3').fadeOut();
		return false;
	});
});
