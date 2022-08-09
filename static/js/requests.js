
function delete_reservation(id){
    let confirmAction = confirm("Are You Sure To Delete This Reservation?");
    if (confirmAction) {
        $.ajax({
            url: "/delete-reservation/" + id + '/',
            headers: {
                'Conten-Type': 'application/json',
                'X-CSRFToken': csrf_token,
            },
            type: "DELETE",
            cache: false,
            processData: false,
            contentType: false,
            success: function (data) {
                $("#reservation-" + id).remove()
                console.log('success', data);
            },
            error: function (rs, e) {
                console.error(rs.responseText);
                console.error(rs.status);
                let message = JSON.parse(rs.responseText)['detail'];
                $("#messages").addClass("alert message text-center alert-danger");
                $("#messages").html(message);
            },
            complete: function () {
                console.log('request completed')
            }
        });
    }
}