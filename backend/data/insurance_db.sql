CREATE DATABASE IF NOT EXISTS insurance_db;
USE insurance_db;

CREATE TABLE IF NOT EXISTS user_inputs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    CustomerID BIGINT NOT NULL,
    Age INT NOT NULL DEFAULT 0,
    Gender TINYINT NOT NULL DEFAULT 0,
    MaritalStatus TINYINT NOT NULL DEFAULT 0,
    Occupation VARCHAR(255) NOT NULL,
    PreferredPaymentMode VARCHAR(255) NOT NULL,
    MonthlyIncomeLKR DOUBLE NOT NULL DEFAULT 0,
    Smoker TINYINT NOT NULL DEFAULT 0,
    Weight DOUBLE NOT NULL DEFAULT 0,
    Height DOUBLE NOT NULL DEFAULT 0,
    BMI DOUBLE NOT NULL DEFAULT 0,
    NumChildren INT NOT NULL DEFAULT 0,
    Benefits JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_customer (CustomerID)  -- optional: ensures no duplicate CustomerID
);
