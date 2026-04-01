-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 01, 2026 at 09:52 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vidhyarakshak`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(120) DEFAULT NULL,
  `password` varchar(200) NOT NULL,
  `role` varchar(20) NOT NULL,
  `school_code` varchar(20) DEFAULT NULL,
  `class_assigned` varchar(20) DEFAULT NULL,
  `roll_no` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `login_time` varchar(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `full_name`, `email`, `password`, `role`, `school_code`, `class_assigned`, `roll_no`, `created_at`, `login_time`, `status`) VALUES
(12, 'Admin', 'vidhyarakshaka@gmail.com', 'Admin@123', 'Admin', '102', NULL, NULL, '2026-03-20 06:54:04', '2026-03-31 10:08:02', 'Active'),
(13, 'Parent of 101', NULL, 'Parent@123', 'Parent', '102', NULL, '101', '2026-03-22 12:16:46', '2026-03-31 10:08:46', 'Active'),
(15, 'Yaswitha', 'paruchuriyaswitha13@gmail.com', 'Yaswitha@123', 'Teacher', '102', '2', NULL, '2026-03-24 07:07:46', '2026-03-30 18:07:23', 'Active'),
(16, 'sai', 'paruchurisai9@gmail.com', 'Teacher@123', 'Teacher', '102', '1', NULL, '2026-03-24 09:02:29', '2026-03-31 13:07:26', 'Active'),
(17, 'Parent of 102', NULL, 'Parent@123', 'Parent', '102', NULL, '102', '2026-03-30 05:00:36', '2026-03-30 05:00:58', 'Active'),
(18, 'Parent of 103', NULL, 'Parent@123', 'Parent', '102', NULL, '103', '2026-03-30 05:07:39', '2026-03-30 05:19:51', 'Active'),
(20, 'Admin', 'gvennela1105@gmail.com', 'Vennela@123', 'Admin', '107', NULL, NULL, '2026-03-30 12:45:56', '2026-03-31 05:02:48', 'Active'),
(21, 'venn', 'mudesai09@gmail.com', 'Vennela@11', 'Teacher', '107', '6', NULL, '2026-03-30 07:51:02', '2026-03-30 18:34:04', 'Active'),
(22, 'Parent of 601', NULL, 'Parent@123', 'Parent', '107', NULL, '601', '2026-03-30 07:53:46', '2026-03-31 05:27:11', 'Active'),
(24, 'Yaswitha', '1@1.1', 'Ab@12345', 'Teacher', '107', '7', NULL, '2026-03-30 09:19:04', '2026-03-30 09:42:22', 'Active'),
(25, 'Parent of 701', NULL, 'Ab@12345', 'Parent', '107', NULL, '701', '2026-03-30 09:31:11', '2026-03-30 09:47:32', 'Active'),
(26, 'Parent of 402', NULL, 'Userr@123', 'Parent', '102', NULL, '402', '2026-03-30 12:05:10', '2026-03-30 12:06:51', 'Active'),
(27, 'rushii', 'venkatarushitha039@gmail.com', 'Rushitha@123', 'Teacher', '107', '9', NULL, '2026-03-30 12:16:11', '2026-03-30 12:16:11', 'Active'),
(28, 'Parent of 201', NULL, 'Parent@123', 'Parent', '102', NULL, '201', '2026-03-31 03:59:16', NULL, 'Active');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
