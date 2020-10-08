<?php
$servername = "localhost";
$username = "webuser";
$password = "webuser";
$db_name = "db_wvi";
$conn = new mysqli($servername, $username, $password, $db_name);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$response = "[";
$data_types = ["temperature", "pressure", "humidity", "lux", "noise", "gas/oxidising", "gas/reducing", "gas/nh3", "msg"];
foreach($data_types as $data_type) {
    $sql = "CALL get_most_recent_of_type('$data_type',0);";
    $result = $conn->query($sql);
    $row = $result->fetch_assoc();
    $response .= '{"packet_type":"' . $data_type . '","id":"' . $row["id"] . '","contents":"' . $row["contents"] . '"},';
    $conn->next_result();

    if($data_type == 'msg' && $row["contents"] == '0 seconds of calibration left') {
        $sql = "CALL insert_testing('msg','Mission started.');";
        $conn->query($sql);
    }   
}
$response = rtrim($response, ",") . "]";
echo $response;
?>