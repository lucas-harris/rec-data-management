{% if name_taken_flag == None %}
    var name_taken = false;
{% else %}
    var name_taken = true;//{{name_taken_flag}}
{% endif %}

window.onload = function() {
    if(name_taken) {
        alert('Chart Set Name Taken');
    }
}


document.getElementById('save-template-button').onclick = function() {
    document.getElementById('save-template-row').style.display = 'block';
}

