$(function() {
    $('.hp-trigger').click(function(event) {
	    event.preventDefault();
        $('.hidden-price').toggleClass('hidden');
        $('html,body').animate({scrollTop:$('#hidden-price').offset().top}, 500);
    })
});
