<?php
/*
var_dump($_POST);
echo "<br><br>";
var_dump($_FILES);
*/
if(isset($_FILES['image'])) {
    move_uploaded_file($_FILES['image']['tmp_name'], 'uploads/test.gif');
}

echo "<img src='uploads/test.gif'>";

?>