-- sql.ini

-- יצירת מסד הנתונים
CREATE DATABASE users;

-- שימוש במסד הנתונים
USE users;

-- יצירת הטבלה לניהול משתמשים
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);


