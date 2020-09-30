<?php

//echo "incoming parameters: " . $POST . "<br><br>";



$servername = "localhost";
$username = "webuser";
$password = "webuser";
$db_name = "db_wvi";

$conn = new mysqli($servername, $username, $password, $db_name);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

echo "Connected successfully.<br>";

//$sql = "CALL insert_testing('sent by','PHP endpoint');";
//$conn->query($sql);

$sql = "SELECT * FROM testing;";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        echo    "id: "              . $row["id"].
                " - Timestamp: "    . $row["date_rec"].
                " - Packet Type: "  . $row["packet_type"].
                " - Contents: "     . $row["contents"]. "<br>";
    }
} else {
    echo "0 results.";
}

$conn->close();

$incoming_json = json_decode(file_get_contents("php://input"));

//echo "<br>hello<br>";
/*
$temperature = $incoming_json["temperature"];
$pressure = $incoming_json["pressure"];
$humidity = $incoming_json["humidity"];
$lux = $incoming_json["lux"];
*/
echo "<br>";
echo $incoming_json->temperature->data . $incoming_json->temperature->unit;
echo "<br><br><br>";
//echo "Temperature: $temperature";
var_dump($incoming_json->temperature);

//var_dump($incoming_json);

//echo "<br>" . 

?>