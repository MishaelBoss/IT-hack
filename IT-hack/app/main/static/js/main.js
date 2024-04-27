// https://gist.github.com/AnisahTiaraPratiwi/65bb4a8c05d67554431539b2e2c5ee0c my post

let members_count = 1; // + input

let add_button = document.getElementById('add_input'); // button add input
let add_input = document.getElementById('add_input');

let my_form = document.getElementById('form'); // forms

//coroutines
add_button.onclick = function(){
    members_count += 1;

    document.getElementById('button').remove();
    let div = document.createElement('div');
    div.setAttribute('class', 'form-item');

    // input
    let input = document.createElement('input');
    input.type = "text";
    input.placeholder = "Логин пользователя"+members_count.toString(); // new input
    input.name = "user"+members_count.toString();

    div.appendChild(input);
    my_form.appendChild(div);

    //button
    let button = document.createElement('button');
    button.type = 'submit';
    button.innerHTML = 'Забронировать';
    button.id='button';
    my_form.appendChild(button)
}