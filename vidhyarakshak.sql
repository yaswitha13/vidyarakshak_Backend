-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 01, 2026 at 09:58 AM
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
(2, 'Admin', 'vidhyarakshaka@gmail.com', 'Admin@123', '9638527410', 'Male', 'Administrator', 'government high school', '102', 'andhra', '2026-03-20 06:54:04'),
(4, 'Admin', 'gvennela1105@gmail.com', 'Vennela@123', '9638527410', 'Male', 'Administrator', 'government high school', '107', 'andhra', '2026-03-30 12:30:51');

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
(6, 8, 'ravi', '101', 100, '1st', 3, 'sai', 'Low Performance', 'not coming to school', 'Medium', '2026-03-23 04:40:34', 'Seen'),
(8, 8, 'ravi', '101', 60, '1st', 6, 'sai', 'Counseling Reminder', 'Reminder: Counseling session scheduled on 2026-3-26 for ravi.', 'High', '2026-03-26 08:00:00', 'Seen'),
(9, 143, 'Sravani', '105', 40, '1', 6, 'sai', 'Attendance Warning', 'not coming to school', 'Low', '2026-03-26 08:28:47', 'Not Seen'),
(10, 144, 'Teja', '201', 25, '2', 5, 'Yaswitha', 'Counseling Reminder', 'Reminder: Counseling session scheduled on 2026-3-29 for Teja.', 'High', '2026-03-28 08:00:00', 'Not Seen'),
(11, 144, 'Teja', '201', 25, '2', 5, 'Yaswitha', 'Counseling Reminder', 'Reminder: Counseling session scheduled on 2026-3-29 for Teja.', 'High', '2026-03-29 08:00:00', 'Not Seen'),
(12, 143, 'Sravani', '105', 50, '1', 6, 'sai', 'Low Performance', 'not coming to school', 'Low', '2026-03-28 07:16:14', 'Not Seen'),
(13, 190, NULL, '601', 100, '6th', 8, 'venn', 'Attendance Warning', 'not coming to scholl', 'Medium', '2026-03-30 08:55:51', 'Not Seen'),
(14, 191, NULL, '701', 40, '7th', 5, 'Yaswitha', 'Attendance Warning', ',jbvc', 'High', '2026-03-30 09:36:07', 'Seen'),
(15, 191, NULL, '701', 40, '7th', 5, 'Yaswitha', 'Behavioral Concern', 'hgbnc', 'Medium', '2026-03-30 09:37:30', 'Not Seen');

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
(67, '102', '102', 'PRESENT', '', '29/03/2026', '2026-03-28 05:17:02', '1st', 1),
(68, '103', '102', 'PRESENT', '', '29/03/2026', '2026-03-28 05:17:02', '1st', 1),
(69, '201', '102', 'ABSENT', '', '28/03/2026', '2026-03-28 06:46:43', '2', 1),
(70, '202', '102', 'ABSENT', '', '28/03/2026', '2026-03-28 06:46:43', '2', 1),
(71, '203', '102', 'ABSENT', '', '28/03/2026', '2026-03-28 06:46:43', '2', 1),
(72, '204', '102', 'PRESENT', '', '28/03/2026', '2026-03-28 06:46:43', '2', 1),
(73, '201', '102', 'ABSENT', '', '28/03/2026', '2026-03-28 07:09:09', '2', 2),
(74, '202', '102', 'ABSENT', '', '28/03/2026', '2026-03-28 07:09:09', '2', 2),
(75, '203', '102', 'PRESENT', '', '28/03/2026', '2026-03-28 07:09:09', '2', 2),
(76, '204', '102', 'PRESENT', '', '28/03/2026', '2026-03-28 07:09:09', '2', 2),
(77, '201', '102', 'ABSENT', '', '28/03/2026', '2026-03-28 07:09:18', '2', 3),
(78, '202', '102', 'ABSENT', '', '28/03/2026', '2026-03-28 07:09:18', '2', 3),
(79, '203', '102', 'ABSENT', '', '28/03/2026', '2026-03-28 07:09:18', '2', 3),
(80, '204', '102', 'ABSENT', '', '28/03/2026', '2026-03-28 07:09:18', '2', 3),
(81, '201', '102', 'PRESENT', '', '28/03/2026', '2026-03-28 07:09:36', '2', 4),
(82, '202', '102', 'PRESENT', '', '28/03/2026', '2026-03-28 07:09:37', '2', 4),
(83, '203', '102', 'PRESENT', '', '28/03/2026', '2026-03-28 07:09:37', '2', 4),
(84, '204', '102', 'PRESENT', '', '28/03/2026', '2026-03-28 07:09:37', '2', 4),
(85, '101', '102', 'ABSENT', '', '28/03/2026', '2026-03-28 07:15:32', '1st', 1),
(86, '105', '102', 'ABSENT', '', '28/03/2026', '2026-03-28 07:15:32', '1', 1),
(87, '106', '102', 'PRESENT', '', '28/03/2026', '2026-03-28 07:15:32', '1st', 1),
(88, '102', '102', 'ABSENT', '', '28/03/2026', '2026-03-28 07:15:32', '1st', 1),
(89, '103', '102', 'PRESENT', '', '28/03/2026', '2026-03-28 07:15:32', '1st', 1),
(90, '101', '102', 'ABSENT', '', '28/03/2026', '2026-03-28 07:15:44', '1st', 2),
(91, '105', '102', 'PRESENT', '', '28/03/2026', '2026-03-28 07:15:44', '1', 2),
(92, '106', '102', 'PRESENT', '', '28/03/2026', '2026-03-28 07:15:44', '1st', 2),
(93, '102', '102', 'ABSENT', '', '28/03/2026', '2026-03-28 07:15:44', '1st', 2),
(94, '103', '102', 'PRESENT', '', '28/03/2026', '2026-03-28 07:15:44', '1st', 2),
(95, '101', '102', 'PRESENT', '', '28/03/2026', '2026-03-28 07:17:08', '1st', 3),
(96, '105', '102', 'PRESENT', '', '28/03/2026', '2026-03-28 07:17:08', '1', 3),
(97, '106', '102', 'PRESENT', '', '28/03/2026', '2026-03-28 07:17:08', '1st', 3),
(98, '102', '102', 'ABSENT', '', '28/03/2026', '2026-03-28 07:17:08', '1st', 3),
(99, '103', '102', 'PRESENT', '', '28/03/2026', '2026-03-28 07:17:08', '1st', 3),
(100, '201', '102', 'PRESENT', '', '30/03/2026', '2026-03-30 03:42:57', '2', 1),
(101, '202', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 03:42:57', '2', 1),
(102, '203', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 03:42:57', '2', 1),
(103, '204', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 03:42:57', '2', 1),
(104, '205', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 03:42:57', '2', 1),
(105, '201', '102', 'PRESENT', '', '30/03/2026', '2026-03-30 03:42:58', '2', 2),
(106, '202', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 03:42:58', '2', 2),
(107, '203', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 03:42:58', '2', 2),
(108, '204', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 03:42:58', '2', 2),
(109, '205', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 03:42:58', '2', 2),
(110, '101', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 04:20:07', '1st', 1),
(111, '105', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 04:20:07', '1', 1),
(112, '106', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 04:20:07', '1st', 1),
(113, '102', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 04:20:07', '1st', 1),
(114, '103', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 04:20:07', '1st', 1),
(115, '701', '107', 'PRESENT', '', '30/03/2026', '2026-03-30 09:25:45', '7th', 1),
(116, '701', '107', 'PRESENT', '', '30/03/2026', '2026-03-30 09:25:48', '7th', 2),
(117, '701', '107', 'ABSENT', '', '30/03/2026', '2026-03-30 09:25:52', '7th', 3),
(118, '701', '107', 'ABSENT', '', '30/03/2026', '2026-03-30 09:25:55', '7th', 4),
(119, '701', '107', 'ABSENT', '', '30/03/2026', '2026-03-30 09:26:24', '7th', 5),
(120, '701', '107', 'ABSENT', '', '30/03/2026', '2026-03-30 09:42:36', '7th', 6),
(121, '701', '107', 'PRESENT', '', '30/03/2026', '2026-03-30 09:43:18', '7th', 7),
(123, '701', '107', 'PRESENT', '', '30/03/2026', '2026-03-30 09:43:18', '7th', 8),
(124, '701', '107', 'PRESENT', '', '30/03/2026', '2026-03-30 09:43:18', '7th', 9),
(128, '701', '107', 'ABSENT', '', '30/03/2026', '2026-03-30 09:43:37', '7th', 10),
(129, '101', '102', 'PRESENT', '', '30/03/2026', '2026-03-30 12:08:19', '1st', 2),
(130, '105', '102', 'PRESENT', '', '30/03/2026', '2026-03-30 12:08:19', '1', 2),
(131, '106', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 12:08:19', '1st', 2),
(132, '103', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 12:08:19', '1st', 2),
(133, '201', '102', 'PRESENT', '', '30/03/2026', '2026-03-30 15:40:08', '2', 3),
(134, '202', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 15:40:08', '2', 3),
(135, '203', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 15:40:08', '2', 3),
(136, '204', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 15:40:08', '2', 3),
(137, '205', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 15:40:08', '2', 3),
(138, '201', '102', 'PRESENT', '', '30/03/2026', '2026-03-30 17:27:48', '2', 4),
(139, '202', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 17:27:48', '2', 4),
(140, '203', '102', 'ABSENT', '', '30/03/2026', '2026-03-30 17:27:48', '2', 4),
(141, '204', '102', 'PRESENT', '', '30/03/2026', '2026-03-30 17:27:48', '2', 4),
(142, '205', '102', 'PRESENT', '', '30/03/2026', '2026-03-30 17:27:48', '2', 4),
(143, '101', '102', 'PRESENT', '', '30/03/2026', '2026-03-30 17:54:41', '1st', 3),
(144, '105', '102', 'PRESENT', '', '30/03/2026', '2026-03-30 17:54:42', '1', 3),
(145, '106', '102', 'PRESENT', '', '30/03/2026', '2026-03-30 17:54:42', '1st', 3),
(146, '103', '102', 'PRESENT', '', '30/03/2026', '2026-03-30 17:54:42', '1st', 3),
(147, '101', '102', 'ABSENT', '', '31/03/2026', '2026-03-31 04:57:13', '1st', 1),
(148, '105', '102', 'PRESENT', '', '31/03/2026', '2026-03-31 04:57:13', '1', 1),
(149, '106', '102', 'ABSENT', '', '31/03/2026', '2026-03-31 04:57:13', '1st', 1),
(150, '103', '102', 'PRESENT', '', '31/03/2026', '2026-03-31 04:57:13', '1st', 1);

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
(3, '102', 'Teja', '1', 'sai', '2026-3-22', 'Academic Support', 'Financial Constraints', 'Happy/Engaged', 'Improvising', 'Excellent Participation', 'Very Active', '102', 'good need to encourage ', 'encouraging ', '2026-3-22', '2026-03-22 17:50:35'),
(4, '101', 'ravi', '1st', 'sai', '2026-3-23', 'Academic Support', 'Academic Struggle', 'Happy/Engaged', 'Improvising', 'Excellent Participation', 'Very Active', '102', 'good', 'need to improve ', '2026-3-23', '2026-03-23 08:17:39'),
(5, '101', 'ravi', '1st', 'sai', '2026-3-25', 'Behavioral Intervention', 'Select Dropout Reason', 'Neutral/Observant', 'Stable', 'Excellent Participation', 'Cooperative', '102', 'iydyosuozits', 'ydkgapusutsiz', '2026-3-24', '2026-03-24 05:29:14'),
(6, '106', 'Vennela', '1st', 'sai', '2026-3-24', 'Career Guidance', 'Financial Constraints', 'Happy/Engaged', 'Select Progress', 'Improved Behavior', 'Select Parent Involvement', '102', 'hi', '', '2026-3-24', '2026-03-24 09:14:28'),
(7, '101', 'ravi', '1st', 'sai', '2026-3-26', 'Academic Support', 'Financial Constraints', 'Happy/Engaged', 'Stable', 'Excellent Participation', 'Very Active', '102', 'vzhzj', 'bahaj', '2026-3-26', '2026-03-26 07:06:01'),
(8, '201', 'Teja', '2', 'Yaswitha', '2026-3-28', 'Academic Support', 'Financial Constraints', 'Disengaged/Withdrawn', 'Improvising', 'Needs Improvement (Disruptive)', 'Very Active', '102', 'not coming to school ', 'need to encourage ', '2026-3-29', '2026-03-28 07:10:54'),
(9, '601', NULL, '6', 'venn', '2026-03-30', NULL, NULL, NULL, NULL, NULL, NULL, '107', 'Type: Academic\nDropout Risk: None\nBehavior: Attentive\nMood: Positive\nNotes: need to improve\nAction Plan: encourge\nFollow-Up: 2026-04-01\nProgress: Improving\nParent Involvement: Somewhat Involved', NULL, NULL, '2026-03-30 08:55:07'),
(10, '601', NULL, '6', 'venn', '2026-03-30', NULL, NULL, NULL, NULL, NULL, NULL, '107', 'Type: Academic\nDropout Risk: None\nBehavior: Attentive\nMood: Positive\nNotes: need to improve\nAction Plan: encourge\nFollow-Up: 2026-04-01\nProgress: Improving\nParent Involvement: Somewhat Involved', NULL, NULL, '2026-03-30 08:55:08'),
(11, '701', NULL, '7', 'Yaswitha', '2026-03-30', NULL, NULL, NULL, NULL, NULL, NULL, '107', 'Type: Academic\nDropout Risk: Academic\nBehavior: Attentive\nMood: Positive\nNotes: mbsdnm\nAction Plan: snbds\nFollow-Up: 2026-03-30\nProgress: Improving\nParent Involvement: Highly Involved', NULL, NULL, '2026-03-30 09:34:42'),
(12, '701', NULL, '7', 'Yaswitha', '2026-03-30', NULL, NULL, NULL, NULL, NULL, NULL, '107', 'Type: Academic\nDropout Risk: Academic\nBehavior: Attentive\nMood: Positive\nNotes: mbsdnm\nAction Plan: snbds\nFollow-Up: 2026-03-30\nProgress: Improving\nParent Involvement: Highly Involved', NULL, NULL, '2026-03-30 09:34:44');

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
(36, 144, 'HIGH', '2026-03-26 07:13:59'),
(37, 145, 'HIGH', '2026-03-26 07:13:59'),
(38, 146, 'HIGH', '2026-03-26 07:13:59'),
(39, 147, 'HIGH', '2026-03-26 07:13:59'),
(40, 144, 'LOW', '2026-03-26 07:14:06'),
(41, 145, 'LOW', '2026-03-26 07:14:06'),
(42, 146, 'LOW', '2026-03-26 07:14:06'),
(43, 147, 'LOW', '2026-03-26 07:14:06'),
(44, 144, 'HIGH', '2026-03-26 07:15:05'),
(45, 145, 'HIGH', '2026-03-26 07:15:05'),
(46, 146, 'HIGH', '2026-03-26 07:15:05'),
(47, 147, 'HIGH', '2026-03-26 07:15:05'),
(48, 144, 'LOW', '2026-03-26 07:15:13'),
(49, 145, 'LOW', '2026-03-26 07:15:13'),
(50, 146, 'LOW', '2026-03-26 07:15:13'),
(51, 147, 'LOW', '2026-03-26 07:15:13'),
(52, 144, 'HIGH', '2026-03-26 08:02:05'),
(53, 145, 'HIGH', '2026-03-26 08:02:05'),
(54, 146, 'HIGH', '2026-03-26 08:02:05'),
(55, 147, 'HIGH', '2026-03-26 08:02:05'),
(56, 144, 'LOW', '2026-03-26 08:02:12'),
(57, 145, 'LOW', '2026-03-26 08:02:12'),
(58, 146, 'LOW', '2026-03-26 08:02:12'),
(59, 147, 'LOW', '2026-03-26 08:02:12'),
(60, 144, 'HIGH', '2026-03-26 08:03:53'),
(61, 145, 'HIGH', '2026-03-26 08:03:53'),
(62, 146, 'HIGH', '2026-03-26 08:03:53'),
(63, 147, 'HIGH', '2026-03-26 08:03:53'),
(64, 144, 'LOW', '2026-03-26 08:03:58'),
(65, 145, 'LOW', '2026-03-26 08:03:58'),
(66, 146, 'LOW', '2026-03-26 08:03:58'),
(67, 147, 'LOW', '2026-03-26 08:03:58'),
(68, 8, 'LOW', '2026-03-26 08:39:06'),
(69, 143, 'MEDIUM', '2026-03-26 08:39:06'),
(70, 180, 'LOW', '2026-03-26 08:39:06'),
(71, 8, 'MEDIUM', '2026-03-26 08:39:14'),
(72, 143, 'HIGH', '2026-03-26 08:39:14'),
(73, 180, 'MEDIUM', '2026-03-26 08:39:14'),
(74, 8, 'LOW', '2026-03-26 08:39:26'),
(75, 143, 'MEDIUM', '2026-03-26 08:39:26'),
(76, 180, 'LOW', '2026-03-26 08:39:26'),
(77, 8, 'MEDIUM', '2026-03-26 08:40:05'),
(78, 143, 'HIGH', '2026-03-26 08:40:05'),
(79, 180, 'MEDIUM', '2026-03-26 08:40:05'),
(80, 8, 'LOW', '2026-03-26 08:40:12'),
(81, 143, 'MEDIUM', '2026-03-26 08:40:12'),
(82, 180, 'LOW', '2026-03-26 08:40:12'),
(83, 8, 'MEDIUM', '2026-03-26 08:45:50'),
(84, 143, 'HIGH', '2026-03-26 08:45:50'),
(85, 180, 'MEDIUM', '2026-03-26 08:45:50'),
(86, 8, 'LOW', '2026-03-26 08:45:56'),
(87, 143, 'MEDIUM', '2026-03-26 08:45:56'),
(88, 180, 'LOW', '2026-03-26 08:45:56'),
(89, 8, 'MEDIUM', '2026-03-26 09:10:18'),
(90, 143, 'HIGH', '2026-03-26 09:10:18'),
(91, 180, 'MEDIUM', '2026-03-26 09:10:18'),
(92, 8, 'HIGH', '2026-03-26 09:26:10'),
(93, 8, 'MEDIUM', '2026-03-26 10:22:21'),
(94, 8, 'HIGH', '2026-03-26 10:22:32'),
(95, 143, 'MEDIUM', '2026-03-26 10:22:47'),
(96, 8, 'MEDIUM', '2026-03-26 10:22:58'),
(97, 180, 'LOW', '2026-03-26 10:22:58'),
(98, 8, 'HIGH', '2026-03-26 10:24:02'),
(99, 143, 'HIGH', '2026-03-26 10:24:02'),
(100, 180, 'MEDIUM', '2026-03-26 10:24:02'),
(101, 8, 'MEDIUM', '2026-03-26 10:30:24'),
(102, 8, 'LOW', '2026-03-26 10:36:09'),
(103, 143, 'MEDIUM', '2026-03-26 10:36:09'),
(104, 180, 'LOW', '2026-03-26 10:36:09'),
(105, 143, 'HIGH', '2026-03-26 10:36:29'),
(106, 143, 'MEDIUM', '2026-03-26 10:36:37'),
(107, 180, 'MEDIUM', '2026-03-26 10:36:37'),
(108, 8, 'MEDIUM', '2026-03-26 10:36:59'),
(109, 143, 'HIGH', '2026-03-26 11:06:50'),
(110, 143, 'MEDIUM', '2026-03-27 03:43:15'),
(111, 180, 'LOW', '2026-03-27 03:43:15'),
(112, 8, 'HIGH', '2026-03-27 03:48:43'),
(113, 143, 'HIGH', '2026-03-27 03:48:43'),
(114, 180, 'MEDIUM', '2026-03-27 03:48:43'),
(115, 187, 'HIGH', '2026-03-27 03:48:52'),
(116, 8, 'MEDIUM', '2026-03-27 04:06:59'),
(117, 143, 'MEDIUM', '2026-03-27 04:06:59'),
(118, 180, 'LOW', '2026-03-27 04:06:59'),
(119, 187, 'LOW', '2026-03-27 04:06:59'),
(120, 8, 'HIGH', '2026-03-27 04:39:13'),
(121, 143, 'HIGH', '2026-03-27 04:39:13'),
(122, 180, 'MEDIUM', '2026-03-27 04:39:13'),
(123, 187, 'HIGH', '2026-03-27 04:39:13'),
(124, 188, 'HIGH', '2026-03-27 04:39:13'),
(125, 144, 'HIGH', '2026-03-28 04:06:00'),
(126, 145, 'HIGH', '2026-03-28 04:06:00'),
(127, 146, 'HIGH', '2026-03-28 04:06:00'),
(128, 147, 'HIGH', '2026-03-28 04:06:00'),
(129, 144, 'LOW', '2026-03-28 04:06:21'),
(130, 146, 'LOW', '2026-03-28 04:06:21'),
(131, 144, 'HIGH', '2026-03-28 04:06:58'),
(132, 146, 'HIGH', '2026-03-28 04:06:58'),
(133, 144, 'LOW', '2026-03-28 04:15:31'),
(134, 145, 'LOW', '2026-03-28 04:15:31'),
(135, 146, 'LOW', '2026-03-28 04:15:31'),
(136, 147, 'LOW', '2026-03-28 04:15:31'),
(137, 144, 'HIGH', '2026-03-28 04:20:15'),
(138, 145, 'HIGH', '2026-03-28 04:20:15'),
(139, 146, 'HIGH', '2026-03-28 04:20:21'),
(140, 147, 'HIGH', '2026-03-28 04:20:21'),
(141, 144, 'LOW', '2026-03-28 04:22:37'),
(142, 145, 'LOW', '2026-03-28 04:22:37'),
(143, 146, 'LOW', '2026-03-28 04:22:37'),
(144, 147, 'LOW', '2026-03-28 04:22:37'),
(145, 144, 'HIGH', '2026-03-28 04:22:47'),
(146, 145, 'HIGH', '2026-03-28 04:22:47'),
(147, 144, 'LOW', '2026-03-28 04:41:18'),
(148, 145, 'LOW', '2026-03-28 04:41:18'),
(149, 144, 'HIGH', '2026-03-28 04:41:28'),
(150, 145, 'HIGH', '2026-03-28 04:41:28'),
(151, 8, 'LOW', '2026-03-28 05:17:02'),
(152, 143, 'LOW', '2026-03-28 05:17:02'),
(153, 180, 'LOW', '2026-03-28 05:17:02'),
(154, 187, 'LOW', '2026-03-28 05:17:02'),
(155, 188, 'LOW', '2026-03-28 05:17:02'),
(156, 144, 'LOW', '2026-03-28 06:46:43'),
(157, 145, 'LOW', '2026-03-28 06:46:43'),
(158, 144, 'HIGH', '2026-03-28 06:46:52'),
(159, 145, 'HIGH', '2026-03-28 06:46:52'),
(160, 144, 'LOW', '2026-03-28 06:47:05'),
(161, 145, 'LOW', '2026-03-28 06:47:05'),
(162, 146, 'HIGH', '2026-03-28 06:47:05'),
(163, 144, 'HIGH', '2026-03-28 06:48:17'),
(164, 145, 'HIGH', '2026-03-28 06:48:17'),
(165, 147, 'MEDIUM', '2026-03-28 07:09:18'),
(166, 8, 'HIGH', '2026-03-28 07:15:32'),
(167, 143, 'HIGH', '2026-03-28 07:15:32'),
(168, 187, 'HIGH', '2026-03-28 07:15:32'),
(169, 143, 'MEDIUM', '2026-03-28 07:17:08'),
(170, 189, 'HIGH', '2026-03-30 03:42:57'),
(171, 147, 'HIGH', '2026-03-30 03:42:58'),
(172, 143, 'HIGH', '2026-03-30 04:20:07'),
(173, 180, 'MEDIUM', '2026-03-30 04:20:07'),
(174, 191, 'MEDIUM', '2026-03-30 09:25:52'),
(175, 191, 'HIGH', '2026-03-30 09:25:55'),
(176, 143, 'MEDIUM', '2026-03-30 12:08:19'),
(177, 188, 'MEDIUM', '2026-03-30 12:08:19'),
(178, 144, 'MEDIUM', '2026-03-30 17:27:48'),
(179, 180, 'HIGH', '2026-03-31 04:57:13');

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
(8, 'ravi', '1st', '101', '102', 'Male', '22/3/2026', 7, 3, 4, 42.86, 42.86, 'HIGH', '7000', 'farming', '6', 1, 'good', 'Bhadrachalam', '963852741', 'andhra pradesh', '2026-03-22 10:49:59', 0, 0, 0),
(143, 'Sravani', '1', '105', '102', 'Female', '14-04-2020', 7, 5, 2, 71.43, 71.43, 'MEDIUM', '1-2 Lakhs', 'Teacher', '15 km', 2, 'Medium', 'Sravani\'s Parent', '9886874480', 'H.No 49, Main Bazaar Road', '2026-03-22 16:43:19', 0, 0, 0),
(144, 'Teja', '2', '201', '102', 'Female', '04-07-2019', 8, 5, 3, 62.5, 62.5, 'MEDIUM', '2-5 Lakhs', 'Shop Owner', '15 km', 2, 'None', 'Teja\'s Parent', '9897005318', 'H.No 17, Station Road', '2026-03-22 16:43:19', 0, 0, 0),
(145, 'Sujatha', '2', '202', '102', 'Male', '28-04-2019', 8, 1, 7, 12.5, 12.5, 'HIGH', '2-5 Lakhs', 'Teacher', '12 km', 3, 'None', 'Sujatha\'s Parent', '9816671592', 'H.No 86, Subhash Nagar', '2026-03-22 16:43:19', 0, 0, 0),
(146, 'Kavitha', '2', '203', '102', 'Female', '20-06-2019', 8, 2, 6, 25, 25, 'HIGH', '1-2 Lakhs', 'Clerk', '14 km', 2, 'Low', 'Kavitha\'s Parent', '9893014513', 'H.No 16, Station Road', '2026-03-22 16:43:19', 0, 0, 0),
(147, 'Praveen', '2', '204', '102', 'Female', '08-05-2019', 8, 4, 4, 50, 50, 'HIGH', '2-5 Lakhs', 'Driver', '13 km', 4, 'Low', 'Praveen\'s Parent', '9885254637', 'H.No 34, Station Road', '2026-03-22 16:43:19', 0, 0, 0),
(148, 'Praveen', '3', '301', '102', 'Female', '18-07-2018', 0, 0, 0, 100, 100, 'LOW', '1-2 Lakhs', 'Farmer', '5 km', 4, 'High', 'Praveen\'s Parent', '9894562320', 'H.No 79, Station Road', '2026-03-22 16:43:19', 0, 0, 0),
(149, 'Suresh', '3', '302', '102', 'Male', '24-08-2018', 0, 0, 0, 100, 100, 'LOW', 'Under 1 Lakh', 'Farmer', '14 km', 1, 'None', 'Suresh\'s Parent', '9848237205', 'H.No 71, Temple Street', '2026-03-22 16:43:19', 0, 0, 0),
(150, 'Harish', '3', '303', '102', 'Male', '11-05-2018', 0, 0, 0, 100, 100, 'LOW', '2-5 Lakhs', 'Daily Wager', '13 km', 1, 'High', 'Harish\'s Parent', '9885130645', 'H.No 47, Subhash Nagar', '2026-03-22 16:43:19', 0, 0, 0),
(151, 'Satish', '3', '304', '102', 'Male', '19-12-2018', 0, 0, 0, 100, 100, 'LOW', 'Above 5 Lakhs', 'Driver', '4 km', 2, 'Low', 'Satish\'s Parent', '9896431788', 'H.No 100, Subhash Nagar', '2026-03-22 16:43:19', 0, 0, 0),
(152, 'Suresh', '4', '401', '102', 'Male', '04-01-2017', 0, 0, 0, 100, 100, 'LOW', 'Under 1 Lakh', 'Driver', '6 km', 0, 'High', 'Suresh\'s Parent', '9881858576', 'H.No 82, Station Road', '2026-03-22 16:43:19', 0, 0, 0),
(153, 'Lakshmi', '4', '402', '102', 'Male', '07-11-2017', 0, 0, 0, 100, 100, 'LOW', '1-2 Lakhs', 'Daily Wager', '11 km', 2, 'Medium', 'Lakshmi\'s Parent', '9810002095', 'H.No 1, Station Road', '2026-03-22 16:43:19', 0, 0, 0),
(154, 'Mahesh', '4', '403', '102', 'Female', '21-07-2017', 0, 0, 0, 100, 100, 'LOW', '1-2 Lakhs', 'Farmer', '9 km', 2, 'None', 'Mahesh\'s Parent', '9880081105', 'H.No 51, Village Panchayat limit', '2026-03-22 16:43:19', 0, 0, 0),
(155, 'Akhila', '4', '404', '102', 'Female', '16-03-2017', 0, 0, 0, 100, 100, 'LOW', 'Above 5 Lakhs', 'Shop Owner', '2 km', 2, 'Low', 'Akhila\'s Parent', '9859609870', 'H.No 31, Village Panchayat limit', '2026-03-22 16:43:19', 0, 0, 0),
(156, 'Jyothi', '4', '405', '102', 'Male', '18-11-2017', 0, 0, 0, 100, 100, 'LOW', '1-2 Lakhs', 'Daily Wager', '7 km', 0, 'Medium', 'Jyothi\'s Parent', '9812698583', 'H.No 14, Village Panchayat limit', '2026-03-22 16:43:19', 0, 0, 0),
(157, 'Naveen', '5', '501', '102', 'Male', '10-12-2016', 0, 0, 0, 100, 100, 'LOW', '1-2 Lakhs', 'Daily Wager', '6 km', 1, 'Low', 'Naveen\'s Parent', '9834561681', 'H.No 1, Temple Street', '2026-03-22 16:43:19', 0, 0, 0),
(158, 'Jyothi', '5', '502', '102', 'Male', '06-11-2016', 0, 0, 0, 100, 100, 'LOW', '1-2 Lakhs', 'Clerk', '4 km', 1, 'None', 'Jyothi\'s Parent', '9854701219', 'H.No 58, Subhash Nagar', '2026-03-22 16:43:19', 0, 0, 0),
(159, 'Anitha', '5', '503', '102', 'Male', '11-05-2016', 0, 0, 0, 100, 100, 'LOW', '2-5 Lakhs', 'Teacher', '15 km', 0, 'None', 'Anitha\'s Parent', '9826826334', 'H.No 11, Main Bazaar Road', '2026-03-22 16:43:19', 0, 0, 0),
(160, 'Ganesh', '5', '504', '102', 'Female', '24-04-2016', 0, 0, 0, 100, 100, 'LOW', 'Under 1 Lakh', 'Farmer', '13 km', 0, 'Medium', 'Ganesh\'s Parent', '9828619459', 'H.No 40, Village Panchayat limit', '2026-03-22 16:43:19', 0, 0, 0),
(161, 'Teja', '6', '601', '102', 'Male', '06-01-2015', 0, 0, 0, 100, 100, 'LOW', '2-5 Lakhs', 'Farmer', '8 km', 2, 'Medium', 'Teja\'s Parent', '9853122426', 'H.No 30, Main Bazaar Road', '2026-03-22 16:43:19', 0, 0, 0),
(162, 'Swathi', '6', '602', '102', 'Male', '15-05-2015', 0, 0, 0, 100, 100, 'LOW', '2-5 Lakhs', 'Teacher', '9 km', 1, 'Medium', 'Swathi\'s Parent', '9883096967', 'H.No 88, Station Road', '2026-03-22 16:43:19', 0, 0, 0),
(163, 'Mahesh', '6', '603', '102', 'Female', '16-11-2015', 0, 0, 0, 100, 100, 'LOW', '1-2 Lakhs', 'Driver', '10 km', 4, 'None', 'Mahesh\'s Parent', '9858152840', 'H.No 64, Temple Street', '2026-03-22 16:43:19', 0, 0, 0),
(164, 'Rushithya', '6', '604', '102', 'Male', '17-01-2015', 0, 0, 0, 100, 100, 'LOW', 'Above 5 Lakhs', 'Teacher', '8 km', 4, 'Medium', 'Rushithya\'s Parent', '9856637084', 'H.No 14, Temple Street', '2026-03-22 16:43:19', 0, 0, 0),
(165, 'Bhavani', '7', '701', '102', 'Male', '06-10-2014', 0, 0, 0, 100, 100, 'LOW', 'Above 5 Lakhs', 'Daily Wager', '15 km', 0, 'Low', 'Bhavani\'s Parent', '9837483798', 'H.No 45, Village Panchayat limit', '2026-03-22 16:43:19', 0, 0, 0),
(166, 'Radha', '7', '702', '102', 'Female', '08-06-2014', 0, 0, 0, 100, 100, 'LOW', '1-2 Lakhs', 'Driver', '6 km', 2, 'Medium', 'Radha\'s Parent', '9826478815', 'H.No 78, Gandhi Nagar, Ward 4', '2026-03-22 16:43:19', 0, 0, 0),
(167, 'Anitha', '7', '703', '102', 'Male', '20-10-2014', 0, 0, 0, 100, 100, 'LOW', 'Under 1 Lakh', 'Clerk', '6 km', 1, 'High', 'Anitha\'s Parent', '9885937232', 'H.No 97, Main Bazaar Road', '2026-03-22 16:43:19', 0, 0, 0),
(168, 'Karthik', '7', '704', '102', 'Female', '10-02-2014', 0, 0, 0, 100, 100, 'LOW', '2-5 Lakhs', 'Clerk', '10 km', 0, 'None', 'Karthik\'s Parent', '9829061692', 'H.No 8, Station Road', '2026-03-22 16:43:19', 0, 0, 0),
(169, 'Venkatesh', '8', '801', '102', 'Female', '08-01-2013', 0, 0, 0, 100, 100, 'LOW', '2-5 Lakhs', 'Teacher', '14 km', 3, 'Low', 'Venkatesh\'s Parent', '9850452272', 'H.No 24, Temple Street', '2026-03-22 16:43:19', 0, 0, 0),
(170, 'Rushithya', '8', '802', '102', 'Female', '08-10-2013', 0, 0, 0, 100, 100, 'LOW', '2-5 Lakhs', 'Daily Wager', '3 km', 1, 'Low', 'Rushithya\'s Parent', '9828687118', 'H.No 64, Temple Street', '2026-03-22 16:43:19', 0, 0, 0),
(171, 'Rushithya', '8', '803', '102', 'Female', '23-04-2013', 0, 0, 0, 100, 100, 'LOW', 'Above 5 Lakhs', 'Driver', '10 km', 0, 'High', 'Rushithya\'s Parent', '9862839538', 'H.No 33, Temple Street', '2026-03-22 16:43:19', 0, 0, 0),
(172, 'Bhavani', '8', '804', '102', 'Male', '25-03-2013', 0, 0, 0, 100, 100, 'LOW', 'Above 5 Lakhs', 'Teacher', '8 km', 1, 'High', 'Bhavani\'s Parent', '9810518259', 'H.No 89, Temple Street', '2026-03-22 16:43:19', 0, 0, 0),
(173, 'Kiran', '9', '901', '102', 'Male', '02-07-2012', 0, 0, 0, 100, 100, 'LOW', 'Above 5 Lakhs', 'Farmer', '11 km', 1, 'None', 'Kiran\'s Parent', '9897657050', 'H.No 69, Main Bazaar Road', '2026-03-22 16:43:19', 0, 0, 0),
(174, 'Radha', '9', '902', '102', 'Female', '04-05-2012', 0, 0, 0, 100, 100, 'LOW', '2-5 Lakhs', 'Farmer', '7 km', 3, 'Medium', 'Radha\'s Parent', '9857453201', 'H.No 71, Temple Street', '2026-03-22 16:43:19', 0, 0, 0),
(175, 'Rajesh', '9', '903', '102', 'Female', '02-02-2012', 0, 0, 0, 100, 100, 'LOW', '2-5 Lakhs', 'Clerk', '10 km', 1, 'High', 'Rajesh\'s Parent', '9856284844', 'H.No 57, Temple Street', '2026-03-22 16:43:19', 0, 0, 0),
(176, 'Rajesh', '9', '904', '102', 'Male', '06-01-2012', 0, 0, 0, 100, 100, 'LOW', '1-2 Lakhs', 'Clerk', '15 km', 4, 'High', 'Rajesh\'s Parent', '9827217910', 'H.No 22, Station Road', '2026-03-22 16:43:19', 0, 0, 0),
(177, 'Suresh', '10', '1001', '102', 'Male', '21-02-2011', 0, 0, 0, 100, 100, 'LOW', 'Under 1 Lakh', 'Driver', '5 km', 2, 'Low', 'Suresh\'s Parent', '9852398712', 'H.No 74, Subhash Nagar', '2026-03-22 16:43:19', 0, 0, 0),
(178, 'Sujatha', '10', '1002', '102', 'Female', '08-10-2011', 0, 0, 0, 100, 100, 'LOW', '1-2 Lakhs', 'Daily Wager', '4 km', 3, 'High', 'Sujatha\'s Parent', '9813205515', 'H.No 70, Station Road', '2026-03-22 16:43:19', 0, 0, 0),
(179, 'Praveen', '10', '1003', '102', 'Female', '05-12-2011', 0, 0, 0, 100, 100, 'LOW', '1-2 Lakhs', 'Clerk', '15 km', 3, 'Medium', 'Praveen\'s Parent', '9893553951', 'H.No 37, Gandhi Nagar, Ward 4', '2026-03-22 16:43:19', 0, 0, 0),
(180, 'Vennela', '1st', '106', '102', 'Female', '26/11/2025', 7, 4, 3, 57.14, 57.14, 'HIGH', '1000000', NULL, '100', 0, NULL, 'ramu', '8978982191', NULL, '2026-03-23 06:50:07', 0, 0, 0),
(181, 'Rahul Kumar', '10th', '1075', '102', 'Male', NULL, 0, 0, 0, 100, 100, 'LOW', NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, '2026-03-23 07:05:06', 0, 0, 0),
(188, 'jaya', '1st', '103', '102', 'Male', '27/3/2026', 8, 6, 2, 75, 75, 'MEDIUM', '50,000', NULL, '1', 0, NULL, 'Yaswitha', '9638527412', 'andhra pradhan', '2026-03-27 04:39:02', 0, 0, 0),
(189, 'radha', '2', '205', '102', 'Female', '2026-03-30', 4, 1, 3, 25, 25, 'HIGH', '50000', 'farmer', NULL, 1, NULL, 'ramya', '9874563211', 'gdbdjad', '2026-03-30 03:42:34', 0, 0, 0),
(190, 'nani', '6th', '601', '107', 'Male', '17/12/2025', 0, 0, 0, 100, 100, 'LOW', '1000000', NULL, '10', 0, NULL, 'venno', '6565665556', 'tirupathi', '2026-03-30 07:52:25', 0, 0, 0),
(191, 'Dhanush', '7th', '701', '107', 'Male', '30/3/2026', 10, 5, 5, 50, 50, 'HIGH', 'd d x', NULL, '27377336636363737336646474747', 0, NULL, 'Dhanalakshmi', '8631256948', 'bzbzb', '2026-03-30 09:22:48', 0, 0, 0),
(192, 'qw', '1', '108', '102', 'Male', '2026-03-31', 0, 0, 0, 100, 100, 'LOW', '100000', '123', NULL, 1, NULL, 'ra', '258369147', 'mzmbyj', '2026-03-31 06:56:00', 0, 0, 0);

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
(4, 'tch1001', 'john', 'john@example.com', NULL, 'maths', '9876543210', NULL, '10th', '102', '2026-03-24 05:19:52', 'APPROVED'),
(5, 'tch002', 'Yaswitha', 'paruchuriyaswitha13@gmail.com', 'Yaswitha@123', 'science', '9638527413', 'Male', '2', '102', '2026-03-24 07:07:14', 'APPROVED'),
(6, 'tch001', 'sai', 'paruchurisai9@gmail.com', 'Teacher@123', 'science', '9638527410', 'Male', '1', '102', '2026-03-24 09:01:39', 'APPROVED'),
(7, 'tch003', 'ravi', 'paruchuribhadrachalam12@gmail.com', 'Teacher@123', 'science', '9638527412', NULL, '3', '102', '2026-03-26 04:03:51', 'APPROVED'),
(8, 'Tech-123', 'venn', 'mudesai09@gmail.com', 'Vennela@11', 'maths', '8978382191', NULL, '6', '107', '2026-03-30 07:50:07', 'APPROVED'),
(9, 'T001', 'Yaswitha', '1@1.1', 'Ab@12345', 'maths', '6392587410', NULL, '7', '107', '2026-03-30 09:15:26', 'APPROVED'),
(10, 'tch009', 'rushii', 'venkatarushitha039@gmail.com', 'Rushitha@123', 'maths', '9346687824', NULL, '9', '107', '2026-03-30 12:15:42', 'APPROVED'),
(11, 'tch002', 'yaswitha', 'yaswithayaswitha13@gmail.com', 'Teacher@123', 'science', '9632587412', NULL, '2', '107', '2026-03-30 18:36:51', 'APPROVED'),
(12, 'tch009', 'ramya', 'ramya13@gmail.com', 'Teacher@12', 'Telugu', '9638527412', NULL, '9', '102', '2026-03-31 06:39:20', 'APPROVED');

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
