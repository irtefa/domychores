/**
* Setup click listener for signup form.
*
*/
$(document).ready(function() {

    $('#signup-btn').click(function(event) {
        event.preventDefault();
        if (isValidSignup()) {
            $("#signup-invalid").addClass("hidden");
            signup();
        }
        else {
            $("#signup-invalid").removeClass("hidden");
        }
    });
});

/**
* Send the form data to signup a new user.
*
* Note: Assumes form is valid.
*
*/
function signup() {
    var first_name = $('#signup-fname').val();
    var last_name = $('#signup-lname').val();
    var email = $('#signup-email').val();
    var password = $('#signup-password').val();
    var address = $('#signup-address').val();

    var post_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "address": address
    };

    $.ajax({
        url: '/api/signup',
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(post_data),
        success: function(data) {
            if (data.success) {
                window.location.replace("/");
            }
            else {
                $('#signup-error').removeClass('hidden');
            }
        }
    });
}

/**
* Check if signup is valid.
*
* Returns:
*   boolean - true if valid; false otherwise
*/
function isValidSignup() {
    var first_name = $('#signup-fname').val();
    var last_name = $('#signup-lname').val();
    var email = $('#signup-email').val();
    var password = $('#signup-password').val();
    var address = $('#signup-address').val();

    if (first_name === "" || last_name === "" || email === "" || password === "" || address === "") {
        return false;
    }
    else {
        return true;
    }
}