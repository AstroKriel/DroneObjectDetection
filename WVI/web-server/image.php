<?php


$detection = "";
if(isset(getallheaders()["A1-Detected"])) $detection = "A1,";
if(isset(getallheaders()["A2-Detected"])) $detection = $detection . "A2,";
if(isset(getallheaders()["B-Detected"])) $detection = $detection . getallheaders()["B-Detected"];

//file_put_contents("uploads/test.txt", var_export(getallheaders(), true));
file_put_contents("uploads/test.txt", $detection);

$filename = microtime(false);

//get detection url vars



/*
if(isset($_GET)) {
    $status = "testing.";
    //$var1 = $_GET["var1"];
    //$var2 = $_GET["var2"];
}
*/
if(isset($_FILES['current_image_jpg'])) {
    //write file name to db
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

//$outut = var_export($_FILES, true);

$sql = "CALL insert_image('$filename','');";
//$sql = "CALL insert_image('$filename','$outut');";
$conn->query($sql);

if($detection != '') {
    $sql = "CALL insert_testing('msg','$detection');";
    $conn->query($sql);
}

/*
$sql = "SELECT Name,Status FROM images ORDER BY Status LIMIT 1;";
$result = $conn->query($sql);

$row = $result->fetch_assoc();

echo "<img src='uploads/{$row['Name']}.jpg'>";
if(isset($row['Status'])) echo "<br><p>{$row['Status']}</p>";
*/
$conn->close();


?>