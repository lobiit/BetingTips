$('.modal').on('show.bs.modal', function () {
    if ($(document).height() > $(window).height()) {
        // no-scroll
        $('body').addClass("modal-open-noscroll");
    }
    else {
        $('body').removeClass("modal-open-noscroll");
    }
});

$('#pay-btn').click(function(){
    var price = $(this).closest('.modal-body').find('#price').text();
    var mobile = $(this).closest('.modal-body').find('#phone').val();
    var bet_type = $(this).closest('.modal-content').find('.modal-title').text();

    $(this).text("Processing..");
    $.ajax({
        type:"POST", //First change type to method here
        url:"controllers/pay.php",
        data:{
        price: price,
        mobile: mobile,
        bet_type: bet_type
        },
        success:function(response) {
            //alert(response);
            if(response == "200"){
                $('#pay-btn').hide();
                $('.no-phone').hide();
                $('.append-response').html("<div class='w3-border w3-border-green'><p class='w3-text-green w3-padding'>Your payment request has been received.\nPlease enter mpesa pin on your phone to complete payment.</p></div>");

            }else if(response == "Enter phone Number"){
                $('#pay-btn').text("Pay Now");
                $('.no-phone').html("<p class='w3-text-red w3-small'>Please Enter Phone Number </p>")
            }
            else{
                $('#pay-btn').hide();
                $('.append-response').html("<div class='w3-border w3-border-red'><p class='w3-text-red w3-padding'>Payment not received. Please try again later !</p></div>");
            }
    },
    error: function (request, error) {
    console.log(arguments);
    alert(" Can't do because: " + error);
}
  });
});

$('#tips-modal').on('hidden.bs.modal', function (e) {
    $('.no-phone').hide();
    $('.append-response').html(" ");
    $('#pay-btn').show().text("Pay Now");
});

$('#tips-modal').on('show.bs.modal', function (event) {
var button = $(event.relatedTarget) // Button that triggered the modal
var bet_data = button.data('whatever') // Extract info from data-* attributes
var res =  bet_data.split(",");
var bet_type = res[0];
var no_of_games = res[1];
var price = res[2];
// If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
// Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
var modal = $(this)
modal.find('.modal-title').text(bet_type)
modal.find('.modal-body .no_of_games').text(no_of_games)
modal.find('.modal-body .price').text(price)
})
