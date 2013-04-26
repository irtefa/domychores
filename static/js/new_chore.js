$(document).ready(function() {

    $('#post-chore').click(function(event) {
        event.preventDefault();
        if (isValid()) {
            $("#post-invalid").addClass("hidden");
            add_chore();
        }
        else {
            $("#post-invalid").removeClass("hidden");
        }
    });
});

function isValid() {
    var task = $('#task').val();
    var description = $('#description').val();

    if (task === "" || description === "") {
        return false;
    }
    else {
        return true;
    }
}

function add_chore() {
    var owner_id = $('#user-id').html();
    var task = $('#task').val();
    var description = $('#description').val();

    var post_data = {
        "task": task,
        "description": description,
        "owner_id": owner_id
    };

    $.ajax({
        url: '/api/chores/new',
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(post_data),
        success: function(data) {
            if (data.success) {
                window.location.replace("/");
            }
        }
    });
}