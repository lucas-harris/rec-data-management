

var chartType;
var chartTitle;
var buttonPressed;
var testChart;

window.onload = function() {
    buttonPressed = false;
    testChart = new Chart(document.getElementById("chart"), {});
    document.getElementById('title').value = "";
}

function resetChecks() {
    document.getElementById('stepped').checked = false;
    document.getElementById('lines').checked = false;
    document.getElementById('filled').checked = false;
    document.getElementById('horizontal').checked = false;
}

function showElements() {
    document.getElementById('titles').style.display = "flex";
    document.getElementById('test-chart').style.display = "flex";
    document.getElementById('test-chart-button').style.display = "flex";
    document.getElementById('create-chart-button').style.display = "flex";
}

document.getElementById('line-radio').onclick = function() {
    document.getElementById('line-check').style.display = "flex";
    document.getElementById('bar-check').style.display = "none";
    document.getElementById('pie-check').style.display = "none";
    document.getElementById('scatter-check').style.display = "none";
    document.getElementById('test-chart').style.display = "flex";
    resetChecks();
    document.getElementById('lines').checked = true;
    if(!buttonPressed) {
        showElements();
    }
    buttonPressed = true;
    chartType = "line";
}

document.getElementById('bar-radio').onclick = function() {
    document.getElementById('line-check').style.display = "none";
    document.getElementById('bar-check').style.display = "flex";
    document.getElementById('pie-check').style.display = "none";
    document.getElementById('scatter-check').style.display = "none";
    document.getElementById('test-chart').style.display = "flex";
    resetChecks();
    if(!buttonPressed) {
        showElements();
    }
    buttonPressed = true;
    chartType = "bar";
}

document.getElementById('horizontal').onclick = function() {
    if(document.getElementById('horizontal').checked) {
        chartType = "horizontalBar";
    }
    else {
        chartType = "bar";
    }
}

document.getElementById('pie-radio').onclick = function() {
    document.getElementById('line-check').style.display = "none";
    document.getElementById('bar-check').style.display = "none";
    document.getElementById('pie-check').style.display = "flex";
    document.getElementById('scatter-check').style.display = "none";
    document.getElementById('test-chart').style.display = "flex";
    resetChecks();
    if(!buttonPressed) {
        showElements();
    }
    buttonPressed = true;
    chartType = "pie";
}
document.getElementById('scatter-radio').onclick = function() {
    document.getElementById('line-check').style.display = "none";
    document.getElementById('bar-check').style.display = "none";
    document.getElementById('pie-check').style.display = "none";
    document.getElementById('scatter-check').style.display = "flex";
    document.getElementById('test-chart').style.display = "flex";
    resetChecks();
    if(!buttonPressed) {
        showElements();
    }
    buttonPressed = true;
    chartType = "scatter";
}

document.getElementById('test-chart-button').onclick = function() {
    testChart.destroy();
    document.getElementById('chart-top').innerHTML = document.getElementById('title').value;
    var ctx = document.getElementById("chart");
    testChart = new Chart(ctx, {
        type: chartType,
        data: {
            labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
            datasets: [{
                label: '# of People',
                data: chart_data[0],
                backgroundColor: [
                    'rgba(0, 0, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(0,99,132,1)'
                ],
                borderWidth: 1,
                steppedLine: document.getElementById('stepped').checked,
                fill: document.getElementById('filled').checked,
                showLine: document.getElementById('lines').checked,
            }
            ]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
}

