jQuery(document).ready(function($) {

    // Fixa navbar ao ultrapassa-lo
    var navbar = $('#app-navbar'),
            distance = navbar.offset().top,
        $window = $(window);

    $window.scroll(function() {
        if ($window.scrollTop() >= distance) {
            navbar.removeClass('fixed-top').addClass('fixed-top');
              $("body").css("padding-top", "20px");
        } else {
            navbar.removeClass('fixed-top');
            $("body").css("padding-top", "0px");
        }
    });
  });