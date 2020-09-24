<?php
$servername = "localhost";
$username = "webuser";
$password = "webuser";
$db_name = "db_wvi";
$conn = new mysqli($servername, $username, $password, $db_name);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$incoming_json = json_decode(file_get_contents("php://input"));
foreach($incoming_json as $key => $value) {
    if($key == "gas") {
        foreach($value as $gas_key => $gas_value) {
            $data = $gas_value->data;
            $name = "gas/" . $gas_key;
            $sql = "CALL insert_testing('$name','$data');";
            $conn->query($sql);
        }
    } else {
        $data = $conn->real_escape_string($value->data);
        $sql = "CALL insert_testing('$key','$data');";
        $conn->query($sql);
    }
}
$conn->close();
?>