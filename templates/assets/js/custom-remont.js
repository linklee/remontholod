$(function() {
    $('.hp-trigger').click(function(e) {
        $('.hidden-price').toggleClass('hidden');
     	e.stopPropagation()
    })
});
