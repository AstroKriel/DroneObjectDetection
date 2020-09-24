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

<?php

// setup static page
//echo "hello there dashboard user<br><br>";

// ajax calls for new image url
//fetch(make new url that just returns newest url as response)
// setup javascript state to hold onto existing images to add them to history list


// ajax calls for new data
//fetch(make new url that just returns most recent data of each sensor)
// setup javascript state to hold onto existing data to keep charts populated and scrolling

// ajax calls for mission status
//fetch(make new url that just returns a mission status string)



//echo "incoming parameters: " . $POST . "<br><br>";

$servername = "localhost";
$username = "webuser";
$password = "webuser";
$db_name = "db_wvi";

$conn = new mysqli($servername, $username, $password, $db_name);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
/*
$sql = "SELECT * FROM testing;";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        echo "<p>" . $row["packet_type"] . ":" . $row["contents"] . "</p>";
        /*echo    "id: "              . $row["id"].
                " - Timestamp: "    . $row["date_rec"].
                " - Packet Type: "  . $row["packet_type"].
                " - Contents: "     . $row["contents"]. "<br>";
    }
} else {
    echo "0 results.";
}
*/
?>

</div>
<div id="rightHalf">
<div id="bigImage">
<?php

$sql = "SELECT Name,Status FROM images ORDER BY id DESC LIMIT 5;";
$result = $conn->query($sql);

$first = 0;
while($row = $result->fetch_assoc()) {
    if($first == 0) {
        echo "<img class='cameraImage' width='480' src='uploads/{$row['Name']}.jpg'><br>";
        echo "<p id='statusBar'></p>";
        /*
        $detection = $row['Status'];
        if(isset($detection)) {
            if(strpos($detection, 'A1') !== false) {
                echo "Found A1; ";
            }
            if(strpos($detection, 'A2') !== false) {
                echo "Found A2; ";
            }
            if(strpos($detection, '[') !== false) {
                $number = strpos($detection, '[') + 1;
                echo "Found Aruco #$number";
            }
        }
        */
        ?></div><div id="imageHistory"><?php
        $first = 1;
    } else {
        echo "<img class='cameraImage' width='160' src='uploads/{$row['Name']}.jpg'>";
    }
}

$conn->close();


?>

</div>
</div>
</div>
<script src="assets/script.js"></script>
</body>
</html>