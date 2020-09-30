<?php
$servername = "localhost";
$username = "webuser";
$password = "webuser";
$db_name = "db_wvi";
$conn = new mysqli($servername, $username, $password, $db_name);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$sql = "SELECT Name FROM images ORDER BY id DESC LIMIT 7;";
$result = $conn->query($sql);

$response = '[';
while($row = $result->fetch_assoc()) {
    $response .= '{"Name":"'. $row["Name"] . '"},';
}
$response = rtrim($response, ",") . "]";
echo $response;

?>