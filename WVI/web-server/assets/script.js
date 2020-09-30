let chartSettings = {
    title: {text: 'Sensor Data Header'},
    chart: {
        //type: 'line',
        type: 'scatter',
        animation: {
            duration: 50
        }
    },
    //yAxis: {title: {text: 'Results'}},
    //height: '200px',
    xAxis: {
        title: {text: "Time Elapsed (sec)"},
        //softMin: 0,
        softMax: 20,
        tickInterval: 2
    },
    plotOptions: {
        series: {marker: {enabled: false}},
        scatter: {lineWidth: 2}
    },
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
settingsTemperature.title.text = "Temperature Sensor Readings";
settingsTemperature.yAxis = {title: {text: "Temperature (°C)"}, softMin: 15, softMax: 30, tickInterval: 5};
settingsHumidity.title.text = "Humidity Sensor Readings";
settingsHumidity.yAxis = {title: {text: "Relative Humidity (%)"}, softMin: 0, softMax: 100, tickInterval: 20};
settingsLux.title.text = "Light Sensor Readings";
settingsLux.yAxis = {title: {text: "Illuminance (lux)"}, softMin: 0, softMax: 500, tickInterval: 100};
settingsPressure.title.text = "Pressure Sensor Readings";
settingsPressure.yAxis = {title: {text: "Pressure (hPa)"}, softMin: 1000, softMax: 1025, tickInterval: 5};
settingsNoise.title.text = "Noise Sensor Readings";
settingsNoise.yAxis = {title: {text: "Noise (dBSPL)"}, softMin: 0, softMax: 120, tickInterval: 30};
settingsGasOxidising.title.text = "Oxidising Gas Sensor Readings";
settingsGasOxidising.yAxis = {title: {text: "Change from baseline (%)"}, softMin: -50, softMax: 50, tickInterval: 25};
settingsGasReducing.title.text = "Reducing Gas Sensor Readings";
settingsGasReducing.yAxis = {title: {text: "Change from baseline (%)"}, softMin: -50, softMax: 50, tickInterval: 25};
settingsGasNH3.title.text = "NH3 Gas Sensor Readings";
settingsGasNH3.yAxis = {title: {text: "Change from baseline (%)"}, softMin: -50, softMax: 50, tickInterval: 25};

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
        .then(response => response.json())
        .then(result => {
            document.querySelector("#bigImage .cameraImage").setAttribute('src',"uploads/" + result[0].Name + ".jpg")
            let historyImgList = document.querySelectorAll("#imageHistory .cameraImage")
            for(let i=0;i<6;i++){
                historyImgList[i].setAttribute('src',"uploads/" + result[i+1].Name + ".jpg")
            }
        });
}, 500);
//window.clearInterval(imageRefresher);

var lastIDs = {
    temperature: 0,
    pressure: 0,
    humidity: 0,
    lux: 0,
    noise: 0,
    'gas/oxidising': 0,
    'gas/reducing': 0,
    'gas/nh3': 0,
    msg: 0
}

var counter = 0;
let sensorRefresher = window.setInterval(function() {
    fetch('/fetch_data')
        .then(response => response.json())
        .then(result => {
            result.forEach(data => {
                if(data.packet_type === 'temperature' && data.id > lastIDs['temperature']) {
                    lastIDs['temperature'] = data.id;
                    if(Highcharts.charts[0].series[0].data.length < 20)
                        Highcharts.charts[0].series[0].addPoint([counter,Number(data.contents)]);
                    else
                        Highcharts.charts[0].series[0].addPoint([counter,Number(data.contents)],true,true);
                }
                if(data.packet_type === 'humidity' && data.id > lastIDs['humidity']) {
                    lastIDs['humidity'] = data.id;
                    if(Highcharts.charts[1].series[0].data.length < 20)
                        Highcharts.charts[1].series[0].addPoint([counter,Number(data.contents)]);
                    else
                        Highcharts.charts[1].series[0].addPoint([counter,Number(data.contents)],true,true);
                }
                if(data.packet_type === 'lux' && data.id > lastIDs['lux']) {
                    lastIDs['lux'] = data.id;
                    if(Highcharts.charts[2].series[0].data.length < 20)
                        Highcharts.charts[2].series[0].addPoint([counter,Number(data.contents)]);
                    else
                        Highcharts.charts[2].series[0].addPoint([counter,Number(data.contents)],true,true);
                }
                if(data.packet_type === 'pressure' && data.id > lastIDs['pressure']) {
                    lastIDs['pressure'] = data.id;
                    if(Highcharts.charts[3].series[0].data.length < 20)
                        Highcharts.charts[3].series[0].addPoint([counter,Number(data.contents)]);
                    else
                        Highcharts.charts[3].series[0].addPoint([counter,Number(data.contents)],true,true);
                }
                if(data.packet_type === 'noise' && data.id > lastIDs['noise']) {
                    lastIDs['noise'] = data.id;
                    if(Highcharts.charts[4].series[0].data.length < 40)
                        Highcharts.charts[4].series[0].addPoint([counter,Number(data.contents)]);
                    else
                        Highcharts.charts[4].series[0].addPoint([counter,Number(data.contents)],true,true);
                }
                if(data.packet_type === 'gas/oxidising' && data.id > lastIDs['gas/oxidising']) {
                    lastIDs['gas/oxidising'] = data.id;
                    if(Highcharts.charts[5].series[0].data.length < 20)
                        Highcharts.charts[5].series[0].addPoint([counter,Number(data.contents)]);
                    else
                        Highcharts.charts[5].series[0].addPoint([counter,Number(data.contents)],true,true);
                }
                if(data.packet_type === 'gas/reducing' && data.id > lastIDs['gas/reducing']) {
                    lastIDs['gas/reducing'] = data.id;
                    if(Highcharts.charts[6].series[0].data.length < 20)
                        Highcharts.charts[6].series[0].addPoint([counter,Number(data.contents)]);
                    else
                        Highcharts.charts[6].series[0].addPoint([counter,Number(data.contents)],true,true);
                }
                if(data.packet_type === 'gas/nh3' && data.id > lastIDs['gas/nh3']) {
                    lastIDs['gas/nh3'] = data.id;
                    if(Highcharts.charts[7].series[0].data.length < 20)
                        Highcharts.charts[7].series[0].addPoint([counter,Number(data.contents)]);
                    else
                        Highcharts.charts[7].series[0].addPoint([counter,Number(data.contents)],true,true);
                }
                if(data.packet_type === 'msg' && data.id > lastIDs['msg']) {
                    if(data.contents === '0 seconds of calibration left') {
                        
                        location.reload();
                    }

                    lastIDs['msg'] = data.id;
                    document.querySelector("#statusBar").innerText = data.contents;
                }
            });
        })

    /*document.querySelectorAll(".highcharts-xaxis-labels > text").forEach((Xlabel) => {
        //console.log(Xlabel);
        Xlabel.innerHTML = Xlabel.innerHTML / 2;
    })*/
    counter += 0.5;
}, 500);
//window.clearInterval(sensorRefresher);