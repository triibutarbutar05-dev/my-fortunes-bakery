-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 10, 2026 at 11:41 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_myfortunes`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `qty` int(11) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`id`, `user_id`, `product_id`, `qty`) VALUES
(4, 3, 5, 2);

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `nama_kategori` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `nama_kategori`) VALUES
(1, 'Cake'),
(2, 'Pocky'),
(3, 'Bolu'),
(4, 'Bread'),
(5, 'Dessert Box');

-- --------------------------------------------------------

--
-- Table structure for table `custom_cakes`
--

CREATE TABLE `custom_cakes` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `ukuran` varchar(50) DEFAULT NULL,
  `rasa` varchar(100) DEFAULT NULL,
  `tema` varchar(100) DEFAULT NULL,
  `tanggal_ambil` date DEFAULT NULL,
  `catatan` text DEFAULT NULL,
  `gambar_referensi` varchar(255) DEFAULT NULL,
  `status` enum('pending','diproses','selesai') DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `custom_cakes`
--

INSERT INTO `custom_cakes` (`id`, `user_id`, `ukuran`, `rasa`, `tema`, `tanggal_ambil`, `catatan`, `gambar_referensi`, `status`) VALUES
(1, NULL, 'Medium', 'chocolate', 'Birthday', '2026-06-01', 'mau warna biru', '', 'pending'),
(2, 3, 'Medium', 'chocolate', 'Birthday', '2026-06-08', 'tulisannya \"happy birthday sayang\" ya kak', '', 'selesai'),
(3, 3, 'Small', 'vanilla', 'wedding', '2026-06-09', 'mau ada strobery diatasnya ya', '', 'diproses');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `tanggal_order` datetime DEFAULT current_timestamp(),
  `total_harga` decimal(10,2) DEFAULT NULL,
  `status` enum('menunggu_verifikasi','diproses','selesai','dibatalkan') DEFAULT 'menunggu_verifikasi',
  `nama_penerima` varchar(100) DEFAULT NULL,
  `no_hp` varchar(20) DEFAULT NULL,
  `alamat` text DEFAULT NULL,
  `catatan` text DEFAULT NULL,
  `bukti_pembayaran` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `tanggal_order`, `total_harga`, `status`, `nama_penerima`, `no_hp`, `alamat`, `catatan`, `bukti_pembayaran`) VALUES
(1, NULL, '2026-05-31 14:43:01', 150000.00, 'diproses', NULL, NULL, NULL, NULL, NULL),
(2, 3, '2026-06-06 21:05:30', 150000.00, 'menunggu_verifikasi', NULL, NULL, NULL, NULL, NULL),
(3, 3, '2026-06-06 21:08:35', 150000.00, 'diproses', NULL, NULL, NULL, NULL, NULL),
(4, 3, '2026-06-07 13:53:08', 300000.00, 'diproses', NULL, NULL, NULL, NULL, NULL),
(5, 3, '2026-06-07 14:12:54', 150000.00, 'selesai', 'blubub', '000000000000', 'jl. rela', 'dmnsbfuyew', 'WhatsApp_Image_2026-06-05_at_5.14.50_PM.jpeg'),
(6, 3, '2026-06-08 10:23:36', 175000.00, 'selesai', 'blubub', '083240973847', 'jl. taduan', 'hai', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `qty` int(11) DEFAULT NULL,
  `subtotal` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `qty`, `subtotal`) VALUES
(3, 3, 6, 1, 150000.00),
(4, 4, 9, 2, NULL),
(5, 5, 8, 1, NULL),
(6, 6, 5, 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `nama_produk` varchar(150) NOT NULL,
  `harga` decimal(10,2) NOT NULL,
  `stok` int(11) DEFAULT 0,
  `deskripsi` text DEFAULT NULL,
  `gambar` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `category_id`, `nama_produk`, `harga`, `stok`, `deskripsi`, `gambar`) VALUES
(5, 1, 'Vintage White', 175000.00, 7, 'Fresh Cream Cake dengan ukuran 16 cm. Sudah termasuk lilin dan pisau cake. \r\n    ', 'WhatsApp_Image_2026-05-31_at_12.43.31.jpg.jpeg'),
(6, 1, 'Cake Love', 150000.00, 7, 'Fresh Cream Cake dengan ukuran 16 cm. Sudah termasuk lilin dan pisau cake\r\n    ', 'WhatsApp_Image_2026-05-31_at_12.53.30.jpg.jpeg'),
(7, 1, 'Heart Cake', 168750.00, 5, 'Fresh Cream Cake dengan ukuran 16 cm. Sudah termasuk lilin dan pisau cake', 'WhatsApp_Image_2026-05-31_at_12.53.50.jpg.jpeg'),
(8, 1, 'Hazel', 150000.00, 5, 'Fresh Cream Cake dengan ukuran 16 cm. Sudah termasuk lilin dan pisau cake', 'WhatsApp_Image_2026-05-31_at_12.55.00.jpg.jpeg'),
(9, 1, 'Cookies and Cream', 150000.00, 5, 'Fresh Cream Cake dengan ukuran 16 cm. Sudah termasuk lilin dan pisau cake', 'WhatsApp_Image_2026-05-31_at_12.55.01.jpg.jpeg'),
(10, 1, 'Carla', 135000.00, 5, 'Fresh Cream Cake dengan ukuran 16 cm. Sudah termasuk lilin dan pisau cake', 'WhatsApp_Image_2026-05-31_at_12.56.59_1.jpg.jpeg'),
(11, 1, 'Korean Pink', 135000.00, 5, 'Fresh Cream Cake dengan ukuran 16 cm. Sudah termasuk lilin dan pisau cake', 'WhatsApp_Image_2026-05-31_at_12.45.43.jpg.jpeg'),
(12, 1, 'Korean Blue', 135000.00, 5, 'Fresh Cream Cake dengan ukuran 16 cm. Sudah termasuk lilin dan pisau cake', 'WhatsApp_Image_2026-05-31_at_12.44.38.jpg.jpeg'),
(14, 1, 'Korean Brown', 135000.00, 3, 'Fresh Cream Cake dengan ukuran 16 cm. Sudah termasuk lilin dan pisau cake', 'WhatsApp_Image_2026-05-31_at_12.58.41.jpg.jpeg'),
(15, 1, 'Korean Gray', 135000.00, 3, 'Fresh Cream Cake dengan ukuran 16 cm. Sudah termasuk lilin dan pisau cake', 'WhatsApp_Image_2026-05-31_at_12.57.00.jpg.jpeg'),
(16, 1, 'Butterfly cake', 150000.00, 3, 'Fresh Cream Cake dengan ukuran 16 cm. Sudah termasuk lilin dan pisau cake', 'WhatsApp_Image_2026-05-31_at_13.00.35.jpg.jpeg'),
(17, 4, 'Paha ayam', 10000.00, 9, 'paha ayam legit', 'WhatsApp_Image_2026-06-08_at_12.48.02_AM_1.jpeg'),
(21, 4, 'Coffee Bun', 9999.00, 4, 'coffee bun premium', 'WhatsApp_Image_2026-06-08_at_1.05.59_AM.jpeg'),
(22, 2, 'Pocky Pink', 69999.00, 4, 'Fresh Cream Cake dengan ukuran 10 cm. Sudah termasuk lilin', 'WhatsApp_Image_2026-05-31_at_12.45.43.jpg_1.jpeg'),
(23, 2, 'Pocky Ribbon White', 69999.00, 2, 'Fresh Cream Cake dengan ukuran 10 cm. Sudah termasuk lilin', 'WhatsApp_Image_2026-05-31_at_12.43.31.jpg_1.jpeg'),
(24, 5, 'Dessert Chocolate', 44999.00, 4, 'Creamy Dessert', 'WhatsApp_Image_2026-06-10_at_2.12.09_PM.jpeg'),
(25, 3, 'Bolu Gulung Oreo', 97998.00, 8, 'Bolu legit', 'WhatsApp_Image_2026-06-10_at_2.12.20_PM.jpeg'),
(26, 3, 'Bolu Chocolate Keju', 57399.00, 5, 'Bolu box 2 rasa', 'WhatsApp_Image_2026-06-10_at_2.12.32_PM.jpeg');

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `komentar` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`id`, `user_id`, `product_id`, `rating`, `komentar`, `created_at`) VALUES
(3, 3, 5, 5, 'enak banget', '2026-06-07 19:47:38');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `nama`, `email`, `password`, `role`, `created_at`) VALUES
(2, 'lalas', 'lalas@gmail.com', 'scrypt:32768:8:1$bwXIXzbf88ZxcPj7$1178f76ebed0eb4a2dfdd41196a80c55cca7e21d4f15b29459a3172563ee456cd0e00c8b41f3d2ba2d05351e24a7e29ead5ce66248eae312a44a77042d728e36', 'admin', '2026-05-30 13:39:53'),
(3, 'blubub', 'blubub@gmail.com', 'scrypt:32768:8:1$hToEISqMHpaFdpXE$210ff99a1a2c01a8aa43c0b75348a3e70d05855bbe011a92d4e66ce0b101debb2a821382ae5986f4b7f3f112f7bb3e79ba201c2cecd50bc3ea56c7ecb21744be', 'user', '2026-06-06 12:25:50');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `custom_cakes`
--
ALTER TABLE `custom_cakes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

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
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `custom_cakes`
--
ALTER TABLE `custom_cakes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `custom_cakes`
--
ALTER TABLE `custom_cakes`
  ADD CONSTRAINT `custom_cakes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
