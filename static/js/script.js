

document.getElementById('save-template-button').onclick = function() {
    // if(document.getElementById('save-template-button').style.display=='block') {
    //     document.getElementById('save-template-button').style.display = 'none';
    // }
    // else {
        document.getElementById('save-template-row').style.display = 'block';
        document.getElementById('select-template-row').style.display = 'none';
    // }
}

document.getElementById('view-template-button').onclick = function() {
    document.getElementById('select-template-row').style.display = 'block';
    document.getElementById('save-template-row').style.display = 'none';
}