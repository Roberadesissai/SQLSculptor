CREATE TABLE IF NOT EXISTS users_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50)
);

INSERT INTO users_info (username, password) VALUES ('admin', 'adminpassword');
INSERT INTO users_info (username, password) VALUES ('user1', 'user1password');

SELECT * FROM users_info WHERE username = 'USERNAME' AND password = 'PASSWORD';
SELECT * FROM users_info WHERE username = 'admin' AND password = 'adminpassword';

SELECT * FROM users_info WHERE username = 'admin' OR '1'='1' AND password = 'anything';


