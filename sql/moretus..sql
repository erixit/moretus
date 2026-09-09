CREATE DATABASE  IF NOT EXISTS `moretus` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `moretus`;
-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 192.168.0.153    Database: invest
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dividend`
--

DROP TABLE IF EXISTS `spelers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `spelers` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `voornaam` varchar(20) DEFAULT '',
  `achternaam` varchar(30) DEFAULT '',
  `fide_elo` int DEFAULT '0',
  `sterktelijst_elo` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41876 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dividend`
--

LOCK TABLES `spelers` WRITE;
/*!40000 ALTER TABLE `dividend` DISABLE KEYS */;
INSERT INTO `spelers` VALUES (1,'Gerry','De Rop',2080,2080);
INSERT INTO `spelers` VALUES (1,'Alain','Talon',2030,2030);
INSERT INTO `spelers` VALUES (1,'Tim','Rüssche',2002,2002);
INSERT INTO `spelers` VALUES (1,'Tomas Dias','Machado',1986,1986);
INSERT INTO `spelers` VALUES (1,'Erik','Vande Velde',1919,1919);
INSERT INTO `spelers` VALUES (1,'Bart','Slachmuylders',1912,1912);
INSERT INTO `spelers` VALUES (1,'Sam','Van Hoofstat',1912,1912);
INSERT INTO `spelers` VALUES (1,'Gert','Van Bunderen',1888,1888);
INSERT INTO `spelers` VALUES (1,'Benny', 'Kleykens',1871,1871);
/*!40000 ALTER TABLE `dividend` ENABLE KEYS */;
UNLOCK TABLES;