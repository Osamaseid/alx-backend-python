USE alx_prodev;

CREATE TABLE user_data (
    user_id CHAR(36) PRIMARY KEY,  -- Using CHAR(36) to store UUIDs
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age DECIMAL(3, 0) NOT NULL      -- Adjust precision and scale if necessary
);