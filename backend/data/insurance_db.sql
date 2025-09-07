DROP DATABASE IF EXISTS insurance_db;


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

CREATE TABLE IF NOT EXISTS admin_users (
   id BIGINT AUTO_INCREMENT PRIMARY KEY,
   username VARCHAR(255) NOT NULL UNIQUE,
   email VARCHAR(255) NOT NULL UNIQUE,
   password VARCHAR(255) NOT NULL,  -- store hashed passwords
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE insurance_register (
    id INT AUTO_INCREMENT PRIMARY KEY,
    branch_name VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    citizenship VARCHAR(50) NOT NULL,
    nic VARCHAR(20) NOT NULL UNIQUE,
    birthday DATE NOT NULL,
    age INT NOT NULL,
    monthly_income DECIMAL(15,2) NOT NULL,
    email VARCHAR(150) NOT NULL,
    children INT DEFAULT 0,
    insurance_plan VARCHAR(150) NOT NULL,
    benefit VARCHAR(100) NOT NULL,
    relationship VARCHAR(50) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    bank_name VARCHAR(100),
    account_holder VARCHAR(100),
    account_number VARCHAR(50),
    signature VARCHAR(255) NOT NULL, -- store file path
    witness VARCHAR(150) NOT NULL,
    register_date DATE NOT NULL
);

CREATE TABLE insurance_plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    PlanName VARCHAR(255),
    CoverageAmount BIGINT
);

INSERT INTO insurance_plans (PlanName, CoverageAmount) VALUES
('Divithilna Protection Plan', 5000000),
('Early Cash', 2500000),
('Freedom LifeStyle Plus Plan', 4000000),
('Janadhiri', 1500000),
('Speed Investment Plan', 3500000),
('FREEDOM', 6000000),
('Minimuthu Parithyaga', 1000000),
('SLIC Wealth Plus', 5000000),
('SLIC Divisavi Protection Plan', 4000000),
('Minimuthu Dayada', 800000),
('School Fee Protector', NULL), -- no numeric coverage provided
('Swarna Dhaja', 7000000);

SELECT*from insurance_claims;

CREATE TABLE insurance_claims (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nic VARCHAR(12) NOT NULL,
    insurance_plan VARCHAR(100) NOT NULL,
    incident_date DATE NOT NULL,
    claim_amount DECIMAL(15,2) NOT NULL,
    description TEXT NOT NULL,
    claim_status VARCHAR(50) DEFAULT 'Submitted',
    payout_status VARCHAR(50) DEFAULT NULL,
    reason VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);







