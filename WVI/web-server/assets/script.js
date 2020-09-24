let chartSettings = {
    title: {text: 'Sensor Data Header'},
    chart: {type: 'area'},
    //yAxis: {title: {text: 'Results'}},
    //height: '200px',
    plotOptions: {series: {marker: {enabled: false}}},
    series: [{
        name: 'Sensor1',
        showInLegend: false,
        data: []
    }],
};

let settingsTemperature     = JSON.parse(JSON.stringify(chartSettings));
let settingsHumidity        = JSON.parse(JSON.stringify(chartSettings));
let settingsLux             = JSON.parse(JSON.stringify(chartSettings));
let settingsPressure        = JSON.parse(JSON.stringify(chartSettings));
let settingsNoise           = JSON.parse(JSON.stringify(chartSettings));
let settingsGasOxidising    = JSON.parse(JSON.stringify(chartSettings));
let settingsGasReducing     = JSON.parse(JSON.stringify(chartSettings));
let settingsGasNH3          = JSON.parse(JSON.stringify(chartSettings));
settingsTemperature.title.text = "Temperature";
settingsHumidity.title.text = "Humidity";
settingsLux.title.text = "Lux";
settingsPressure.title.text = "Pressure";
settingsNoise.title.text = "Noise";
settingsGasOxidising.title.text = "Gas: Oxidising";
settingsGasReducing.title.text = "Gas: Reducing";
settingsGasNH3.title.text = "Gas: NH3";

Highcharts.chart('chartTemperature', settingsTemperature);
Highcharts.chart('chartHumidity', settingsHumidity);
Highcharts.chart('chartLux', settingsLux);
Highcharts.chart('chartPressure', settingsPressure);
Highcharts.chart('chartNoise', settingsNoise);
Highcharts.chart('chartGasOxidising', settingsGasOxidising);
Highcharts.chart('chartGasReducing', settingsGasReducing);
Highcharts.chart('chartGasNH3', settingsGasNH3);

let imageRefresher = window.setInterval(function() {
    fetch('/fetch_image')
        .then(response => response.text())
        .then(result => document.querySelector(".cameraImage").setAttribute('src',"uploads/" + result + ".jpg"));
}, 250);
//window.clearInterval(imageRefresher);
let sensorRefresher = window.setInterval(function() {
    fetch('/fetch_data')
        .then(response => response.json())
        .then(result => {
            //console.log(result);
            result.forEach(function(data) {
                if('temperature' in data) {
                    Highcharts.charts[0].series[0].addPoint(Number(data.temperature));
                }
                if('humidity' in data) {
                    Highcharts.charts[1].series[0].addPoint(Number(data.humidity));
                }
                if('lux' in data) {
                    Highcharts.charts[2].series[0].addPoint(Number(data.lux));
                }
                if('pressure' in data) {
                    Highcharts.charts[3].series[0].addPoint(Number(data.pressure));
                }
                if('noise' in data) {
                    Highcharts.charts[4].series[0].addPoint(Number(data.noise));
                }
                if('gas/oxidising' in data) {
                    Highcharts.charts[5].series[0].addPoint(Number(data['gas/oxidising']));
                }
                if('gas/reducing' in data) {
                    Highcharts.charts[6].series[0].addPoint(Number(data['gas/reducing']));
                }
                if('gas/nh3' in data) {
                    Highcharts.charts[7].series[0].addPoint(Number(data['gas/nh3']));
                }
                //TODO: add msg 
                if('msg' in data) {
                    document.querySelector("#statusBar").innerText = data.msg;
                }
            });
        })
}, 1000);