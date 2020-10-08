<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="assets/styles.css">
    <script src="https://code.highcharts.com/highcharts.js"></script>
</head>
<body>
    <div id="container">
        <div id="leftHalf">

            <div id="chartTemperature" class="chart"></div>
            <div id="chartHumidity" class="chart"></div>
            <div id="chartLux" class="chart"></div>
            <div id="chartPressure" class="chart"></div>
            <div id="chartNoise" class="chart"></div>
            <div id="chartGasOxidising" class="chart"></div>
            <div id="chartGasReducing" class="chart"></div>
            <div id="chartGasNH3" class="chart"></div>
        </div>
        <div id="rightHalf">
            <div id="imageSection">
                <div id="bigImage">
                    <img class='cameraImage' src='uploads/default.jpg'>
                    <br>
                </div>
                <div id="imageHistory">
                    <img class='cameraImage' src='uploads/default.jpg'>
                    <img class='cameraImage' src='uploads/default.jpg'>
                    <img class='cameraImage' src='uploads/default.jpg'>
                    <img class='cameraImage' src='uploads/default.jpg'>
                    <img class='cameraImage' src='uploads/default.jpg'>
                    <img class='cameraImage' src='uploads/default.jpg'>
                </div>
            </div>
            <p id='statusBar'></p>
            <p id='previousStatus'></p>
        </div>
    </div>
    </div>
    <script src="assets/script.js"></script>
</body>
</html>