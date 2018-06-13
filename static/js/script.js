

document.getElementById('save-template-button').onclick = function() {
    document.getElementById('save-template-row').style.display = 'block';
    document.getElementById('select-template-row').style.display = 'none';
    stuff();
    
}

document.getElementById('view-template-button').onclick = function() {
    document.getElementById('select-template-row').style.display = 'block';
    document.getElementById('save-template-row').style.display = 'none';
}

function clearBorders(chartDivs) {
    for(div in chartDivs) {
        div.style.border = '0px';
    }
}


