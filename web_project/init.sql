-- יצירת דאטאבייס עבור היוזרים
CREATE DATABASE IF NOT EXISTS users_web;
USE users_web;
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL
);

-- יצירת דאטאבייס עבור הכניסות לאתר
CREATE DATABASE IF NOT EXISTS site_entries;
USE site_entries;
CREATE TABLE IF NOT EXISTS site_entries (
  id INT AUTO_INCREMENT PRIMARY KEY,
  entry_time DATETIME NOT NULL
);
