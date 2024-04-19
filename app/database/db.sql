-- Create the database if it does not exist
--CREATE DATABASE employee_records_db;

-- Switch to the newly created or existing database
--\c employee_records_db;


        -- Create the users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    reset_pwd_token VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    role VARCHAR(50) DEFAULT 'user'
        );

 

-- Insert dummy data into the users table
INSERT INTO users (username, email, hashed_password,  is_active, is_superuser, role)
VALUES
    ('user1', 'user1@example.com','$5$rounds=535000$password$af/Ygj2w7B1w9jXKDzXluSvqLRqzzCB8G7qosTH7MfC', TRUE, FALSE, 'user');
INSERT INTO users (username, email, hashed_password, is_active, is_superuser, role)
VALUES('admin1', 'admin1@example.com','$5$rounds=535000$password$fE6vn816vUe/rtcyL5RG4G7SNmTv5hvCsD80FkloYm8', TRUE, TRUE, 'admin');
