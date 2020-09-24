<?php
$servername = "localhost";
$username = "webuser";
$password = "webuser";
$db_name = "db_wvi";
$conn = new mysqli($servername, $username, $password, $db_name);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$sql = "SELECT Name FROM images ORDER BY id DESC LIMIT 1;";
$result = $conn->query($sql);
$row = $result->fetch_assoc();

echo $row["Name"];

?>