-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Sep 10, 2025 at 08:06 AM
-- Server version: 8.3.0
-- PHP Version: 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `insurance _db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
CREATE TABLE IF NOT EXISTS `admin` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `admin_users`
--

DROP TABLE IF EXISTS `admin_users`;
CREATE TABLE IF NOT EXISTS `admin_users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `role` enum('admin') DEFAULT 'admin',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_admin_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `admin_users`
--

INSERT INTO `admin_users` (`id`, `username`, `email`, `password`, `created_at`, `role`) VALUES
(1, 'sumithra', 'navodipahalawela@gmail.com', '$2b$12$4fx4Q4kzAl8eebv6KZUXd.dRWojiEVy9TBZ6TXzxmAFw5SCmdlyyu', '2025-08-31 08:43:22', 'admin'),
(2, 'navodipahalawela@gmail.com', '123@na', '$2b$12$.nnD.4NSBC.QgQxyrbdl.OtbeY5Dxj39OwnnQRjur0o4lMm5alfXm', '2025-09-04 06:27:16', 'admin'),
(3, 'sume', 'sume@gmail.com', '$2b$12$UfPwj5g9sW0qRvketOuSPOD7I0Q9dC2r37IAfSUf7jrCu0dtWg7ba', '2025-09-04 16:52:39', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `insurance_claims`
--

DROP TABLE IF EXISTS `insurance_claims`;
CREATE TABLE IF NOT EXISTS `insurance_claims` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nic` varchar(12) NOT NULL,
  `insurance_plan` varchar(100) NOT NULL,
  `incident_date` date NOT NULL,
  `claim_amount` decimal(15,2) NOT NULL,
  `description` text NOT NULL,
  `claim_status` varchar(50) DEFAULT 'Submitted',
  `payout_status` varchar(50) DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `insurance_claims`
--

INSERT INTO `insurance_claims` (`id`, `nic`, `insurance_plan`, `incident_date`, `claim_amount`, `description`, `claim_status`, `payout_status`, `reason`, `created_at`) VALUES
(1, '200086302419', 'Minimuthu Dayada', '2025-09-01', 50000.00, 'gggg', 'Approved', 'Paid', NULL, '2025-09-06 06:18:55'),
(2, '200086302419', 'Minimuthu Dayada', '2025-09-01', 50000.00, 'gggg', 'Approved', 'Paid', NULL, '2025-09-06 06:19:21'),
(3, '123456789v', 'Minimuthu Dayada', '2025-09-01', 50000.00, 'gggg', 'Approved', 'Paid', NULL, '2025-09-06 06:22:09'),
(4, '200086302419', 'Minimuthu Dayada', '2025-09-03', 5000.00, 'emergwncy', 'Approved', 'Paid', NULL, '2025-09-06 14:51:17'),
(5, '200086302419', 'Minimuthu Dayada', '2025-09-05', 5000.00, 'Emergency', 'Approved', 'Paid', NULL, '2025-09-07 01:32:12'),
(6, '200086302419', 'Minimuthu Dayada', '2003-07-03', 50000.00, 'hghgh', 'Approved', 'Paid', NULL, '2025-09-09 14:42:09'),
(7, '200086302419', 'Minimuthu Dayada', '2025-09-04', 5000.00, 'gggggg', 'Approved', 'Paid', NULL, '2025-09-09 20:39:00'),
(8, '200086302419', 'Minimuthu Dayada', '2025-09-04', 5000.00, 'jjjjjj', 'Approved', 'Paid', NULL, '2025-09-09 21:01:15'),
(9, '200086302419', 'Minimuthu Dayada', '2025-09-04', 5000.00, 'jjjjjj', 'Approved', 'Paid', NULL, '2025-09-09 21:02:51'),
(10, '200086302419', 'Minimuthu Dayada', '2025-09-04', 5000.00, 'jjjjjj', 'Approved', 'Paid', NULL, '2025-09-09 21:04:00'),
(11, '200086302419', 'Minimuthu Dayada', '2025-09-04', 5000.00, 'jjjjjj', 'Approved', 'Paid', NULL, '2025-09-09 21:04:51'),
(12, '200086302419', 'Minimuthu Dayada', '2025-09-04', 5000.00, 'jjjjjj', 'Approved', 'Paid', NULL, '2025-09-09 21:05:45'),
(13, '200086302419', 'Minimuthu Dayada', '2025-09-04', 5000.00, 'bbbbbbbb', 'Approved', 'Paid', NULL, '2025-09-09 21:20:00'),
(14, '200086302419', 'Minimuthu Dayada', '2025-09-05', 5000.00, 'bbbbbb', 'Approved', 'Paid', NULL, '2025-09-09 21:21:57'),
(15, '200086302419', 'Minimuthu Dayada', '2025-09-04', 50000.00, 'dddddd', 'Approved', 'Paid', NULL, '2025-09-09 21:33:42'),
(16, '200086302419', 'Minimuthu Dayada', '2025-09-04', 5000.00, 'ggggggggg', 'Approved', 'Paid', NULL, '2025-09-09 21:39:15'),
(17, '200086302419', 'Minimuthu Dayada', '2025-09-05', 5000.00, 'cfcfc', 'Approved', 'Paid', NULL, '2025-09-10 05:15:46'),
(18, '200086302419', 'Minimuthu Dayada', '2007-04-26', 15.00, 'Ut perferendis porro', 'Approved', 'Paid', NULL, '2025-09-10 06:00:23'),
(19, '200086302419', 'Minimuthu Dayada', '2025-09-09', 60000.00, 'asdasd', 'Approved', 'Paid', NULL, '2025-09-10 07:41:22');

-- --------------------------------------------------------

--
-- Table structure for table `insurance_plans`
--

DROP TABLE IF EXISTS `insurance_plans`;
CREATE TABLE IF NOT EXISTS `insurance_plans` (
  `PlanID` int NOT NULL,
  `PlanName` varchar(255) NOT NULL,
  `Description` text,
  `CoverageAmount` decimal(15,2) DEFAULT NULL,
  `Premium` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`PlanID`),
  UNIQUE KEY `PlanName` (`PlanName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `insurance_plans`
--

INSERT INTO `insurance_plans` (`PlanID`, `PlanName`, `Description`, `CoverageAmount`, `Premium`) VALUES
(1, 'Divithilna Protection Plan', 'Comprehensive life insurance protecting your family against unforeseen events.', 5000000.00, 'Monthly payment options available'),
(2, 'Early Cash', 'Provides early cash benefit for critical illnesses.', 2500000.00, 'Flexible premiums, monthly or annual'),
(3, 'Freedom LifeStyle Plus Plan', 'Life insurance plan with investment options for lifestyle needs.', 4000000.00, 'Quarterly, Half-Annual, Annual'),
(4, 'Janadhiri', 'Affordable plan for general public with basic coverage.', 1500000.00, 'Monthly or Annual'),
(5, 'Speed Investment Plan', 'Focuses on investment growth along with insurance coverage.', 3500000.00, 'Quarterly or Annual'),
(6, 'FREEDOM', 'Flexible plan allowing you to adjust coverage as life changes.', 6000000.00, 'Monthly or Annual'),
(7, 'Minimuthu Parithyaga', 'Small premium, essential coverage for families.', 1000000.00, 'Monthly'),
(8, 'SLIC Wealth Plus', 'Wealth growth plan combining investment and protection.', 5000000.00, 'Quarterly, Half-Annual, Annual'),
(9, 'SLIC Divisavi Protection Plan', 'Protection plan for serious illnesses and life events.', 4000000.00, 'Monthly or Annual'),
(10, 'Minimuthu Dayada', 'Affordable plan with limited coverage for daily needs.', 800000.00, 'Monthly'),
(11, 'School Fee Protector', 'Ensures your child’s school fees are covered in any event.', 0.00, 'Annual payment'),
(12, 'Swarna Dhaja', 'Premium plan offering high coverage with investment benefits.', 7000000.00, 'Quarterly or Annual');

-- --------------------------------------------------------

--
-- Table structure for table `insurance_register`
--

DROP TABLE IF EXISTS `insurance_register`;
CREATE TABLE IF NOT EXISTS `insurance_register` (
  `id` int NOT NULL AUTO_INCREMENT,
  `branch_name` varchar(255) NOT NULL,
  `full_name` varchar(150) NOT NULL,
  `citizenship` varchar(50) NOT NULL,
  `nic` varchar(20) NOT NULL,
  `birthday` date NOT NULL,
  `age` int NOT NULL,
  `monthly_income` decimal(15,2) NOT NULL,
  `email` varchar(150) NOT NULL,
  `children` int DEFAULT '0',
  `insurance_plan` varchar(150) NOT NULL,
  `benefit` varchar(100) NOT NULL,
  `relationship` varchar(50) NOT NULL,
  `payment_method` varchar(50) NOT NULL,
  `bank_name` varchar(100) DEFAULT NULL,
  `account_holder` varchar(100) DEFAULT NULL,
  `account_number` varchar(50) DEFAULT NULL,
  `signature` varchar(255) NOT NULL,
  `witness` varchar(150) NOT NULL,
  `register_date` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nic` (`nic`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `insurance_register`
--

INSERT INTO `insurance_register` (`id`, `branch_name`, `full_name`, `citizenship`, `nic`, `birthday`, `age`, `monthly_income`, `email`, `children`, `insurance_plan`, `benefit`, `relationship`, `payment_method`, `bank_name`, `account_holder`, `account_number`, `signature`, `witness`, `register_date`) VALUES
(1, 'Balangoda', 'John Doe', 'Sri Lankan', '200086302419', '2000-12-28', 24, 25000.00, 'navodipahalawela@gmail.com', 0, 'Minimuthu Dayada', 'Accident Cover', 'Self', 'Bank Transfer', 'nsb', 'asd', '123456', 'D:\\insurance_recommender_fullstack\\backend\\Uploads\\signatures\\1.png', 'asd', '2025-09-05'),
(2, 'Balangoda', 'John Doe', 'Sri Lankan', '123456789v', '2007-09-01', 18, 50000.00, 'navodipahalawela@gmail.com', 0, 'Minimuthu Dayada', 'Accident Cover', 'Self', 'Bank Transfer', 'nsb', 'asd', '123456', 'uploads\\2.png', 'John Doe', '2025-09-05'),
(5, 'asdasd', 'asdasd', 'Other', '122312341234', '2007-09-01', 18, 124325.00, '123@asd.s', 2, 'SLIC Divisavi Protection Plan', 'Life Cover', 'Self', 'Cheque', '123123', '123123123', '123123123123', 'D:\\navodi\\Insuarance_recommendation_\\backend\\uploads\\imgbin_0f6558f88fb457e68f92c042df252892.png', '123123', '2025-09-03');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('user') DEFAULT 'user',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_users_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `role`, `created_at`) VALUES
(1, 'udhan', 'udhanmadubhath03@gmail.com', '$2b$12$2aSU5mQFrB0ZY4IwXgGHK.HmGRzx1lc7E3qnWeLjg1j8u0VPHIyti', 'user', '2025-09-04 09:07:28'),
(2, 'sumith', 'sumith@gmail.com', '$2b$12$2xVGjysecbQD7vgbCFocGudF9cg/sVTv29QJNQlQxWDElQx0dVV6e', 'user', '2025-09-04 09:14:07'),
(4, 'sumith', 'sumith12@gmail.com', '$2b$12$.pAo4tikdEgd89s3knkLZe3/mSR5BRcy4pcBXuC78RSg63QLTVdu6', 'user', '2025-09-04 09:15:21'),
(5, 'ns', 'ns@123gmail.com', '$2b$12$XsiGgxp1HYtjXcTdzdfMfem7KxAvIKeZ6AAYIVBOVUIT5TVwTEK0S', 'user', '2025-09-04 09:50:34'),
(6, 'nimal@gmail.com', 'nimal@gmail.com', '$2b$12$IiH1OSgr0/LY1IuNSrKoYO1KbtnoJaE1novVT1lANum2Ds1l1xTDK', 'user', '2025-09-04 16:56:39'),
(7, 'udhan', 'udhan@gmail.com', '$2b$12$F4H1llgceHEN/W5aSatMNul2bh/MONCpWufn5shV7pK0PR/wP7uua', 'user', '2025-09-04 19:04:11'),
(8, 'zxc', 'zxc@gmail.com', '$2b$12$aadETJENS2zMBwjaBAwUEeW4ZQJDt98EzZSRxQh9qapmRhcUE.apW', 'user', '2025-09-04 22:53:20'),
(9, 'zxcv', 'zxcv@gmail.com', '$2b$12$osc3air8pefyx0Ve8jTF4uCfHagqh.OO9fXIhpgiAX5g/z69Nvgji', 'user', '2025-09-04 22:54:40'),
(10, 'navodipahalawela@gmail.com', 'navodipahalawela@gmail.com', '$2b$12$7391sNiV6LZFA5P4bb9P6e9RNCGHcpBvlqudbAoQNYQjNojXr9AA6', 'user', '2025-09-05 22:35:44'),
(12, 'wigolema', 'tabego@mailinator.com', '$2b$12$e4cPUVyykzzYurMDdWO/1.AGhH.VCi4SuyEFwJ5JVPXtNF4UwNSgS', 'user', '2025-09-07 01:36:57'),
(13, 'Martin Conway', 'jirirumuk@mailinator.com', '$2b$12$EMnj3v8KqhkykzhvaPaaceeP8tMeQye./qb8sl2FQt9qNWvXPu5GG', 'user', '2025-09-07 01:44:31'),
(14, 'himanmanduja', 'hghimanmanduja@gmail.com', '$2b$12$WNcOIMTWTSqfw16v5l9xHefNFQGPFNcIWzT6HcdI7i7udsPHlAOx2', 'user', '2025-09-10 07:47:10');

-- --------------------------------------------------------

--
-- Table structure for table `user_inputs`
--

DROP TABLE IF EXISTS `user_inputs`;
CREATE TABLE IF NOT EXISTS `user_inputs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `CustomerID` bigint NOT NULL,
  `Age` int NOT NULL DEFAULT '0',
  `Gender` tinyint NOT NULL DEFAULT '0',
  `MaritalStatus` tinyint NOT NULL DEFAULT '0',
  `Occupation` varchar(255) NOT NULL,
  `PreferredPaymentMode` varchar(255) NOT NULL,
  `MonthlyIncomeLKR` double NOT NULL DEFAULT '0',
  `Smoker` tinyint NOT NULL DEFAULT '0',
  `Weight` double NOT NULL DEFAULT '0',
  `Height` double NOT NULL DEFAULT '0',
  `BMI` double NOT NULL DEFAULT '0',
  `NumChildren` int NOT NULL DEFAULT '0',
  `Benefits` json DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_customer` (`CustomerID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user_inputs`
--

INSERT INTO `user_inputs` (`id`, `CustomerID`, `Age`, `Gender`, `MaritalStatus`, `Occupation`, `PreferredPaymentMode`, `MonthlyIncomeLKR`, `Smoker`, `Weight`, `Height`, `BMI`, `NumChildren`, `Benefits`, `created_at`) VALUES
(1, 1756626450038, 36, 1, 0, 'Government', 'Monthly', 65000, 0, 56, 157, 22.7, 0, '[\"Disability Cover\", \"Accidental Death Cover\"]', '2025-08-31 07:47:30'),
(2, 1756963923639, 25, 1, 0, 'Government', 'Monthly', 25000, 0, 50, 155, 20.8, 0, '[\"Hospital Bill Cover\"]', '2025-09-04 05:32:03'),
(3, 1757167725054, 25, 1, 0, '1', '1', 0, 1, 155, 170, 53.6, 0, '\"Hospital Bill Cover, Life Cover\"', '2025-09-06 14:08:45'),
(4, 1757168076917, 25, 0, 0, '2', '1', 0, 1, 55, 155, 22.9, 2, '\"Critical Illness Cover\"', '2025-09-06 14:14:36'),
(5, 1757168159737, 55, 0, 0, '1', '1', 0, 1, 55, 155, 22.9, 1, '\"Life Cover\"', '2025-09-06 14:15:59'),
(6, 1757170113019, 25, 0, 1, '1', '0', 0, 1, 55, 155, 22.9, 0, '\"Accident Cover, Critical Illness Cover\"', '2025-09-06 14:48:33'),
(7, 1757170134741, 12, 0, 1, '1', '0', 0, 1, 55, 155, 22.9, 0, '\"Accident Cover, Critical Illness Cover\"', '2025-09-06 14:48:54'),
(8, 1757176563823, 56, 1, 1, '5', '0', 0, 0, 61, 152, 26.4, 3, '\"Hospital Bill Cover, Life Cover, Disability Cover\"', '2025-09-06 16:36:03'),
(9, 1757176570973, 56, 1, 1, '5', '0', 0, 0, 61, 152, 26.4, 3, '\"Hospital Bill Cover, Life Cover, Disability Cover, Accident Cover, Critical Illness Cover, Maternity Cover\"', '2025-09-06 16:36:11'),
(10, 1757205183517, 56, 1, 1, '5', '0', 0, 0, 61, 152, 26.4, 3, '\"Hospital Bill Cover, Life Cover, Disability Cover, Accident Cover, Critical Illness Cover, Maternity Cover\"', '2025-09-07 00:33:03'),
(11, 1757205431635, 59, 0, 0, '6', '2', 0, 0, 46, 18, 1419.8, 43, '\"Hospital Bill Cover, Life Cover, Disability Cover, Accident Cover, Critical Illness Cover, Maternity Cover\"', '2025-09-07 00:37:11'),
(12, 1757205947381, -15, 0, 0, '6', '2', 0, 0, 46, 18, 1419.8, 0, '\"Hospital Bill Cover, Life Cover, Disability Cover, Accident Cover, Critical Illness Cover, Maternity Cover\"', '2025-09-07 00:45:47'),
(13, 1757207288841, 92, 2, 1, '0', '0', 0, 1, 37, 72, 71.4, 58, '\"Hospital Bill Cover, Life Cover\"', '2025-09-07 01:08:08'),
(14, 1757208079549, 47, 1, 1, '6', '2', 0, 0, 25, 96, 27.1, 71, '\"Hospital Bill Cover\"', '2025-09-07 01:21:19'),
(15, 1757428809641, 97, 0, 0, '3', '3', 0, 1, 76, 21, 1723.4, 59, '\"Disability Cover, Accident Cover, Maternity Cover\"', '2025-09-09 14:40:09'),
(16, 1757440698031, 25, 0, 1, '2', '1', 0, 0, 6, 30, 66.7, 72, '\"Life Cover, Maternity Cover\"', '2025-09-09 17:58:18'),
(17, 1757453525017, 9, 2, 0, '5', '0', 0, 0, 31, 100, 31, 13, '\"Hospital Bill Cover, Life Cover, Disability Cover\"', '2025-09-09 21:32:05'),
(18, 1757453928061, 78, 2, 1, '0', '2', 0, 1, 91, 33, 835.6, 36, '\"Life Cover, Disability Cover, Accident Cover, Critical Illness Cover, Maternity Cover\"', '2025-09-09 21:38:48'),
(19, 1757481268935, 71, 0, 1, '3', '0', 0, 1, 37, 37, 270.3, 40, '\"Hospital Bill Cover, Critical Illness Cover\"', '2025-09-10 05:14:29'),
(20, 1757483997465, 63, 2, 1, '5', '0', 0, 1, 13, 41, 77.3, 29, '\"Hospital Bill Cover, Disability Cover, Critical Illness Cover\"', '2025-09-10 05:59:57');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
