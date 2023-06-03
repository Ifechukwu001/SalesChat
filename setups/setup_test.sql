-- Setup database for Development

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS sc_db_test;

-- Create User if it doesn't exists
CREATE USER IF NOT EXISTS 'sc_user_test'@'localhost' IDENTIFIED BY 'sc_pass_test';

-- Grants all priviledges on the database to the user
GRANT ALL PRIVILEGES ON sc_db_test.* TO 'sc_user_test'@'localhost';
FLUSH PRIVILEGES;
