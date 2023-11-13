use store;

create table users(
	id smallint unsigned not null auto_increment,
	username varchar(20) not null,
	password char(102) not null,
	fullname varchar(50),
    usertype tinyint not null,
	primary key(id)
) engine=InnoDB auto_increment=2 default charset=utf8mb4 collate=utf8mb4_unicode_ci;

DELIMITER //
CREATE PROCEDURE sp_AddUser(IN pUserName VARCHAR(20), IN pPassword VARCHAR(102), IN pFullName
	VARCHAR(50), in pUserType tinyint)
	BEGIN
 		DECLARE hashedPassword VARCHAR(255);
 		SET hashedPassword = SHA2(pPassword, 256); -- Utiliza SHA-256 para hashear la contraseña.
 		INSERT INTO users (username, password, fullname, usertype )
		VALUES (pUserName, hashedPassword, pFullName, pUserType);
	END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_verifyIdentity(IN pUsername VARCHAR(20), IN pPlainTextPassword VARCHAR(20))
	BEGIN
 		DECLARE storedPassword VARCHAR(255);

		SELECT password INTO storedPassword FROM users
		WHERE username = pUsername COLLATE utf8mb4_unicode_ci;

	IF storedPassword IS NOT NULL AND storedPassword = SHA2(pPlainTextPassword, 256) THEN
		SELECT id, username, storedPassword, fullname, usertype FROM users
		WHERE username = pUserName COLLATE utf8mb4_unicode_ci;
	ELSE
		SELECT NULL;
	END IF;
	END //
DELIMITER ;
