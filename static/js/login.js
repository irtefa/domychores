/**
* Setup click listener for login form.
*
*/
$(document).ready(function() {

    $('#login-btn').click(function(event) {
        event.preventDefault();
        if (isValidLogin()) {
            $("#login-invalid").addClass("hidden");
            login();
        }
        else {
            $("#login-invalid").removeClass("hidden");
        }
    });
});

/**
* Send the form data to login a user.
*
* Note: Assumes form is valid.
*
*/
function login() {
    var email = $('#login-email').val();
    var password = $('#login-password').val();

    var post_data = {
        "email": email,
        "password": password
    };

    $.ajax({
        url: '/api/login',
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(post_data),
        success: function(data) {
            if (data.success) {
                window.location.replace("/");
            }
            else {
                $('#login-error').removeClass('hidden');
            }
        }
    });
}

/**
* Check if login is valid.
*
* Returns:
*   boolean - true if valid; false otherwise
*/
function isValidLogin() {
    var email = $('#login-email').val();
    var password = $('#login-password').val();

    if (email === "" || password === "") {
        return false;
    }
    else {
        return true;
    }
}