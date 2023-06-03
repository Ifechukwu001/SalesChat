-- Setup database for Development

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS sc_db_dev;

-- Create User if it doesn't exists
CREATE USER IF NOT EXISTS 'sc_user_dev'@'localhost' IDENTIFIED BY 'sc_pass_dev';

-- Grants all priviledges on the database to the user
GRANT ALL PRIVILEGES ON sc_db_dev.* TO 'sc_user_dev'@'localhost';
FLUSH PRIVILEGES;
