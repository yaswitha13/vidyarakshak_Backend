-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 01, 2026 at 10:37 AM
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
-- Table structure for table `admin_profiles`
--

CREATE TABLE `admin_profiles` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  `school` varchar(100) DEFAULT NULL,
  `school_code` varchar(50) NOT NULL,
  `state` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_profiles`
--

INSERT INTO `admin_profiles` (`id`, `name`, `email`, `password`, `phone`, `gender`, `role`, `school`, `school_code`, `state`, `created_at`) VALUES
(2, 'Admin', 'vidhyarakshaka@gmail.com', 'Admin@123', '9638527410', 'Male', 'Administrator', 'government high school', '102', 'andhra', '2026-03-20 06:54:04');

-- --------------------------------------------------------

--
-- Table structure for table `alerts`
--

CREATE TABLE `alerts` (
  `alert_id` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `student_name` varchar(100) DEFAULT NULL,
  `roll_number` varchar(20) DEFAULT NULL,
  `attendance` int(11) DEFAULT NULL,
  `class_name` varchar(20) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `teacher_name` varchar(100) DEFAULT NULL,
  `alert_type` varchar(50) NOT NULL,
  `alert_message` text NOT NULL,
  `priority` varchar(20) NOT NULL,
  `date_created` datetime DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alerts`
--

INSERT INTO `alerts` (`alert_id`, `student_id`, `student_name`, `roll_number`, `attendance`, `class_name`, `teacher_id`, `teacher_name`, `alert_type`, `alert_message`, `priority`, `date_created`, `status`) VALUES
(6, 8, 'ravi', '101', 100, '1st', 3, 'sai', 'Low Performance', 'not coming to school', 'Medium', '2026-03-23 04:40:34', 'Seen');

-- --------------------------------------------------------

--
-- Table structure for table `attendance_logs`
--

CREATE TABLE `attendance_logs` (
  `id` int(11) NOT NULL,
  `student_roll_no` varchar(20) NOT NULL,
  `school_code` varchar(20) DEFAULT NULL,
  `status` varchar(10) NOT NULL,
  `reason` varchar(200) DEFAULT NULL,
  `entry_date` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `class_name` varchar(20) DEFAULT NULL,
  `session_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendance_logs`
--

INSERT INTO `attendance_logs` (`id`, `student_roll_no`, `school_code`, `status`, `reason`, `entry_date`, `created_at`, `class_name`, `session_id`) VALUES
(90, '101', '102', 'ABSENT', '', '28/03/2026', '2026-03-28 07:15:44', '1st', 2);

-- --------------------------------------------------------

--
-- Table structure for table `counseling_records`
--

CREATE TABLE `counseling_records` (
  `id` int(11) NOT NULL,
  `student_roll_no` varchar(20) NOT NULL,
  `student_name` varchar(100) DEFAULT NULL,
  `class_name` varchar(20) DEFAULT NULL,
  `counselor_name` varchar(100) DEFAULT NULL,
  `session_date` varchar(20) DEFAULT NULL,
  `counseling_type` varchar(100) DEFAULT NULL,
  `dropout_reason` varchar(100) DEFAULT NULL,
  `student_mood` varchar(100) DEFAULT NULL,
  `progress_status` varchar(100) DEFAULT NULL,
  `behavior_observation` varchar(100) DEFAULT NULL,
  `parent_involvement` varchar(100) DEFAULT NULL,
  `school_code` varchar(20) DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `action_plan` text DEFAULT NULL,
  `followup_date` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `counseling_records`
--

INSERT INTO `counseling_records` (`id`, `student_roll_no`, `student_name`, `class_name`, `counselor_name`, `session_date`, `counseling_type`, `dropout_reason`, `student_mood`, `progress_status`, `behavior_observation`, `parent_involvement`, `school_code`, `notes`, `action_plan`, `followup_date`, `created_at`) VALUES
(5, '101', 'ravi', '1st', 'sai', '2026-3-25', 'Behavioral Intervention', 'Select Dropout Reason', 'Neutral/Observant', 'Stable', 'Excellent Participation', 'Cooperative', '102', 'iydyosuozits', 'ydkgapusutsiz', '2026-3-24', '2026-03-24 05:29:14');

-- --------------------------------------------------------

--
-- Table structure for table `otps`
--

CREATE TABLE `otps` (
  `id` int(11) NOT NULL,
  `email` varchar(120) NOT NULL,
  `role` varchar(20) NOT NULL,
  `otp_code` varchar(6) NOT NULL,
  `expires_at` datetime NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `otps`
--

INSERT INTO `otps` (`id`, `email`, `role`, `otp_code`, `expires_at`, `created_at`) VALUES
(2, 'paruchurisai9@gmail.com', 'Teacher', '450158', '2026-03-22 12:25:30', '2026-03-22 12:15:30'),
(12, 'venkatarushitha039@gmail.com', 'Teacher', '749674', '2026-03-30 12:35:05', '2026-03-30 12:25:05'),
(17, 'paruchuriyaswitha13@gmail.com', 'Teacher', '691448', '2026-03-31 04:32:31', '2026-03-31 04:22:31');

-- --------------------------------------------------------

--
-- Table structure for table `risk_history`
--

CREATE TABLE `risk_history` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `risk_level` varchar(20) NOT NULL,
  `date_recorded` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `risk_history`
--

INSERT INTO `risk_history` (`id`, `student_id`, `risk_level`, `date_recorded`) VALUES
(108, 8, 'MEDIUM', '2026-03-26 10:36:59');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `class_name` varchar(20) NOT NULL,
  `roll_no` varchar(20) NOT NULL,
  `school_code` varchar(20) NOT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `dob` varchar(20) DEFAULT NULL,
  `total_classes` int(11) DEFAULT NULL,
  `present_days` int(11) DEFAULT NULL,
  `absent_days` int(11) DEFAULT NULL,
  `attendance_percentage` float DEFAULT NULL,
  `attendance` double DEFAULT 100,
  `risk_level` varchar(10) DEFAULT NULL,
  `family_income` varchar(100) DEFAULT NULL,
  `parents_occ` varchar(100) DEFAULT NULL,
  `distance` varchar(50) DEFAULT NULL,
  `num_siblings` int(11) DEFAULT NULL,
  `parent_involv` varchar(100) DEFAULT NULL,
  `parent_name` varchar(100) DEFAULT NULL,
  `mobile_number` varchar(20) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `base_total_classes` int(11) DEFAULT 0,
  `base_present_days` int(11) DEFAULT 0,
  `base_absent_days` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `name`, `class_name`, `roll_no`, `school_code`, `gender`, `dob`, `total_classes`, `present_days`, `absent_days`, `attendance_percentage`, `attendance`, `risk_level`, `family_income`, `parents_occ`, `distance`, `num_siblings`, `parent_involv`, `parent_name`, `mobile_number`, `address`, `created_at`, `base_total_classes`, `base_present_days`, `base_absent_days`) VALUES
(8, 'ravi', '1st', '101', '102', 'Male', '22/3/2026', 7, 3, 4, 42.86, 42.86, 'HIGH', '7000', 'farming', '6', 1, 'good', 'Bhadrachalam', '963852741', 'andhra pradesh', '2026-03-22 10:49:59', 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `teachers`
--

CREATE TABLE `teachers` (
  `id` int(11) NOT NULL,
  `teacher_id` varchar(50) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(120) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `subject` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `class_assigned` varchar(20) DEFAULT NULL,
  `school_code` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `status` varchar(20) DEFAULT 'PENDING'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `teachers`
--

INSERT INTO `teachers` (`id`, `teacher_id`, `name`, `email`, `password`, `subject`, `phone`, `gender`, `class_assigned`, `school_code`, `created_at`, `status`) VALUES
(6, 'tch001', 'sai', 'paruchurisai9@gmail.com', 'Teacher@123', 'science', '9638527410', 'Male', '1', '102', '2026-03-24 09:01:39', 'APPROVED');

-- --------------------------------------------------------

--
-- Table structure for table `teacher_edit_profile`
--

CREATE TABLE `teacher_edit_profile` (
  `id` int(11) NOT NULL,
  `teacher_email` varchar(120) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `teacher_edit_profile`
--

INSERT INTO `teacher_edit_profile` (`id`, `teacher_email`, `phone_number`, `gender`, `created_at`) VALUES
(2, 'paruchurisai9@gmail.com', '963852741', 'Male', '2026-03-22 11:06:58');

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
(16, 'sai', 'paruchurisai9@gmail.com', 'Teacher@123', 'Teacher', '102', '1', NULL, '2026-03-24 09:02:29', '2026-03-31 13:07:26', 'Active');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_profiles`
--
ALTER TABLE `admin_profiles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `alerts`
--
ALTER TABLE `alerts`
  ADD PRIMARY KEY (`alert_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `attendance_logs`
--
ALTER TABLE `attendance_logs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_attendance` (`student_roll_no`,`entry_date`,`session_id`);

--
-- Indexes for table `counseling_records`
--
ALTER TABLE `counseling_records`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `otps`
--
ALTER TABLE `otps`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `risk_history`
--
ALTER TABLE `risk_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `teachers`
--
ALTER TABLE `teachers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `teacher_edit_profile`
--
ALTER TABLE `teacher_edit_profile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `teacher_email` (`teacher_email`);

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
-- AUTO_INCREMENT for table `admin_profiles`
--
ALTER TABLE `admin_profiles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `alerts`
--
ALTER TABLE `alerts`
  MODIFY `alert_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `attendance_logs`
--
ALTER TABLE `attendance_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=151;

--
-- AUTO_INCREMENT for table `counseling_records`
--
ALTER TABLE `counseling_records`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `otps`
--
ALTER TABLE `otps`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `risk_history`
--
ALTER TABLE `risk_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=180;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=193;

--
-- AUTO_INCREMENT for table `teachers`
--
ALTER TABLE `teachers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `teacher_edit_profile`
--
ALTER TABLE `teacher_edit_profile`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `alerts`
--
ALTER TABLE `alerts`
  ADD CONSTRAINT `alerts_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
