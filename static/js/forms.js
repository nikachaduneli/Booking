let make_reservation_button = document.getElementById('make_reservation');
let reservation_div = document.getElementById('reservation_form');
make_reservation_button.onclick = function (){
    reservation_div.innerHTML = `
                    <form method="POST" onsubmit="submit_button.disabled=true; return true;" class="form" action="${'/place/'+object_id+'/'}" >
                        ${csrf_token_input}
                        ${reservation_form}
                         <button type="submit" class="btn btn-outline-dark"  value="Submit" name="submit_button">Add</button>
                    </form>`;
}
let add_review_button = document.getElementById('add_review')
let review_form_div = document.getElementById('review_form_div');
add_review_button.onclick = function (){
    review_form_div.innerHTML = `
            <form method="POST" onsubmit="submit_button.disabled=true; return true;" class="form" action="${'/place/'+object_id+'/'}" >
                ${csrf_token_input}
                ${review_form}
                <button type="submit" class="btn btn-outline-dark"  value="Submit" name="submit_button">Add</button>
            </form>`;
    window.scrollTo(0,document.body.scrollHeight);
}