function  delete_request(url, element_id){
    const xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", url, true);
    xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhttp.setRequestHeader('X-CSRFToken', csrf_token);
    xhttp.onload = function (){
        if (xhttp.status === 200){
            let image = document.getElementById(element_id);
            image.remove();
        }
        else {
            let response = JSON.parse(xhttp.response);
            let message_div = document.getElementById('messages');
            message_div.className = "alert message text-center alert-danger"
            message_div.innerHTML = response['detail'];
            window.scrollTo(0,0);
        }
    }
    xhttp.send();

}

function delete_images(id){
     let url = "/delete-image/" + id + '/';
    let element_id = 'image-'+id;
    delete_request(url, element_id);
}

function delete_reservation(id){
    let confirmAction = confirm("Are You Sure To Delete This Reservation?");
    if (confirmAction) {
        let url =  "/delete-reservation/" + id + '/';
        let element_id = 'reservation-'+id;
        delete_request(url, element_id);
    }
}