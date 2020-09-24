<?php
$servername = "localhost";
$username = "webuser";
$password = "webuser";
$db_name = "db_wvi";
$conn = new mysqli($servername, $username, $password, $db_name);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
//$sql = "SELECT packet_type,contents FROM testing WHERE packet_type = 'temperature' ORDER BY id DESC LIMIT 10;";
$sql = "CALL get_sensors();";
$result = $conn->query($sql);
$response = "[";
while($row = $result->fetch_assoc()) {
    $response .= '{"' . $row["packet_type"] . '":"' . $row["contents"] . '"},';
}
$response = rtrim($response, ",") . "]";
echo $response;

?>