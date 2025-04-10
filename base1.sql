-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: base1
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alertes`
--

DROP TABLE IF EXISTS `alertes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alertes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `utilisateur_id` int NOT NULL,
  `type_alert` varchar(50) DEFAULT NULL,
  `message` text,
  `date_alert` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `utilisateur_id` (`utilisateur_id`),
  CONSTRAINT `alertes_ibfk_1` FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateurs` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alertes`
--

LOCK TABLES `alertes` WRITE;
/*!40000 ALTER TABLE `alertes` DISABLE KEYS */;
/*!40000 ALTER TABLE `alertes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `banquiers`
--

DROP TABLE IF EXISTS `banquiers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `banquiers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  `date_inscription` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `banquiers`
--

LOCK TABLES `banquiers` WRITE;
/*!40000 ALTER TABLE `banquiers` DISABLE KEYS */;
/*!40000 ALTER TABLE `banquiers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `description` text,
  `date_creation` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nom` (`nom`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comptes`
--

DROP TABLE IF EXISTS `comptes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comptes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `utilisateur_id` int NOT NULL,
  `numero_compte` varchar(20) NOT NULL,
  `solde` decimal(10,2) DEFAULT '0.00',
  `date_creation` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_compte` (`numero_compte`),
  KEY `utilisateur_id` (`utilisateur_id`),
  CONSTRAINT `comptes_ibfk_1` FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateurs` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comptes`
--

LOCK TABLES `comptes` WRITE;
/*!40000 ALTER TABLE `comptes` DISABLE KEYS */;
INSERT INTO `comptes` VALUES (1,1,'7634003F021',1000.00,'2025-03-17 16:43:48'),(2,2,'7630203J012',1500.50,'2025-03-17 16:43:48'),(3,3,'7630002T093',800.75,'2025-03-17 16:43:48'),(4,4,'6301040D024',1200.00,'2025-03-17 16:43:48'),(5,5,'6304032R055',600.25,'2025-03-17 16:43:48'),(6,9,'FR920250320093612',0.00,'2025-03-20 08:36:12'),(7,11,'FR1120250320095150',4800.00,'2025-03-20 08:51:50');
/*!40000 ALTER TABLE `comptes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `portefeuille`
--

DROP TABLE IF EXISTS `portefeuille`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `portefeuille` (
  `id` int NOT NULL AUTO_INCREMENT,
  `banquier_id` int NOT NULL,
  `compte_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `banquier_id` (`banquier_id`),
  KEY `compte_id` (`compte_id`),
  CONSTRAINT `portefeuille_ibfk_1` FOREIGN KEY (`banquier_id`) REFERENCES `banquiers` (`id`) ON DELETE CASCADE,
  CONSTRAINT `portefeuille_ibfk_2` FOREIGN KEY (`compte_id`) REFERENCES `comptes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `portefeuille`
--

LOCK TABLES `portefeuille` WRITE;
/*!40000 ALTER TABLE `portefeuille` DISABLE KEYS */;
/*!40000 ALTER TABLE `portefeuille` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `compte_id` int NOT NULL,
  `reference_transaction` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `montant` decimal(10,2) NOT NULL,
  `date_transaction` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `type_transaction` enum('retrait','d├®p├┤t','transfert') NOT NULL,
  `categorie` varchar(50) DEFAULT NULL,
  `categorie_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reference_transaction` (`reference_transaction`),
  KEY `compte_id` (`compte_id`),
  KEY `categorie_id` (`categorie_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`compte_id`) REFERENCES `comptes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`categorie_id`) REFERENCES `categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,1,'DEP20230301','D├®p├┤t salaire',2000.00,'2025-02-28 23:00:00','d├®p├┤t','salaire',NULL),(2,2,'DEP20230302','D├®p├┤t ├®pargne',300.00,'2025-03-01 23:00:00','d├®p├┤t','├®pargne',NULL),(3,3,'DEP20230303','D├®p├┤t cadeau',150.00,'2025-03-02 23:00:00','d├®p├┤t','cadeau',NULL),(4,4,'DEP20230304','D├®p├┤t remboursement',500.00,'2025-03-03 23:00:00','d├®p├┤t','remboursement',NULL),(5,5,'DEP20230305','D├®p├┤t divers',100.00,'2025-03-04 23:00:00','d├®p├┤t','divers',NULL),(6,1,'RET20230309','Retrait loisirs',-100.00,'2025-03-08 23:00:00','retrait','loisirs',NULL),(7,2,'PAY20230310','Paiement restaurant',-50.00,'2025-03-09 23:00:00','retrait','repas',NULL),(17,7,'DEP20250320231516','paye de mars 2025',4500.00,'2025-03-20 22:15:16','d├®p├┤t','paye',NULL),(18,7,'DEP20250320232745','prime de 1er tr',400.00,'2025-03-20 22:27:45','d├®p├┤t','prime',NULL),(26,7,'RET20250320233033','retrais',100.00,'2025-03-20 22:30:33','retrait',NULL,NULL);
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transferts`
--

DROP TABLE IF EXISTS `transferts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transferts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `compte_source_id` int NOT NULL,
  `compte_dest_id` int NOT NULL,
  `montant` decimal(10,2) NOT NULL,
  `date_transfert` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `compte_source_id` (`compte_source_id`),
  KEY `compte_dest_id` (`compte_dest_id`),
  CONSTRAINT `transferts_ibfk_1` FOREIGN KEY (`compte_source_id`) REFERENCES `comptes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `transferts_ibfk_2` FOREIGN KEY (`compte_dest_id`) REFERENCES `comptes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transferts`
--

LOCK TABLES `transferts` WRITE;
/*!40000 ALTER TABLE `transferts` DISABLE KEYS */;
INSERT INTO `transferts` VALUES (1,1,2,300.00,'2025-03-05 23:00:00'),(2,3,4,200.00,'2025-03-06 23:00:00'),(3,5,1,50.00,'2025-03-07 23:00:00');
/*!40000 ALTER TABLE `transferts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utilisateurs`
--

DROP TABLE IF EXISTS `utilisateurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utilisateurs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  `date_inscription` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utilisateurs`
--

LOCK TABLES `utilisateurs` WRITE;
/*!40000 ALTER TABLE `utilisateurs` DISABLE KEYS */;
INSERT INTO `utilisateurs` VALUES (1,'Fariday','Falira','falirz@examlpe.com','6f266d11a9454454c9bb80816e980e9ade587c38b2fca25db515432bfe94427b','2025-03-17 16:20:35'),(2,'zozo','momo','momo@example.com','9f4eb3aeab8da788847093b8cdba0f16fcaf362b1fd2e9b396ed654520e6d05b','2025-03-17 16:25:04'),(3,'Jean','Dupont','jean.dupont@example.com','hashedpassword1','2025-03-17 16:38:54'),(4,'Marie','Curie','marie.curie@example.com','hashedpassword2','2025-03-17 16:38:54'),(5,'Ali','Baba','ali.baba@example.com','hashedpassword3','2025-03-17 16:38:54'),(6,'Sophia','Loren','sophia.loren@example.com','hashedpassword4','2025-03-17 16:38:54'),(7,'Marco','Polo','marco.polo@example.com','hashedpassword5','2025-03-17 16:38:54'),(9,'zozo','momo','zozo@example.com','a76ca86640b67ffd3be4ea90969a69ec62586a15754a34197f843718c398bc20','2025-03-20 08:36:12'),(11,'zozo','momo','fofo@example.com','a76ca86640b67ffd3be4ea90969a69ec62586a15754a34197f843718c398bc20','2025-03-20 08:51:50');
/*!40000 ALTER TABLE `utilisateurs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-21  0:16:47
