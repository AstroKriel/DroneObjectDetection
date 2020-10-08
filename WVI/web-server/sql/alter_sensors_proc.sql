DELIMITER $$
DROP PROCEDURE IF EXISTS db_wvi.get_most_recent_of_type$$
CREATE DEFINER=root@localhost
PROCEDURE get_most_recent_of_type(IN sensor_type VARCHAR(30), IN old_id INT)
BEGIN
SELECT  id,contents
FROM    testing
WHERE   packet_type = sensor_type
    AND id > old_id
ORDER BY id DESC
LIMIT 1;
END$$
DELIMITER ;