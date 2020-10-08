<?php

$detection = "";
if(isset(getallheaders()["A1-Detected"])) $detection = "A1,";
if(isset(getallheaders()["A2-Detected"])) $detection = $detection . "A2,";
if(isset(getallheaders()["B-Detected"])) $detection = $detection . getallheaders()["B-Detected"];

file_put_contents("uploads/test.txt", $detection);
$filename = microtime(false);

if(isset($_FILES['current_image_jpg'])) {
    move_uploaded_file($_FILES['current_image_jpg']['tmp_name'], "uploads/$filename.jpg");
}

$servername = "localhost";
$username = "webuser";
$password = "webuser";
$db_name = "db_wvi";

$conn = new mysqli($servername, $username, $password, $db_name);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "CALL insert_image('$filename','');";
$conn->query($sql);

if($detection != '') {
    $sql = "CALL insert_testing('msg','$detection');";
    $conn->query($sql);
}
$conn->close();
?>
