ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'admin';

DROP TABLE IF EXISTS `account`;

CREATE TABLE `account` (
  `name` varchar(60) DEFAULT NULL,
  `userid` varchar(60) NOT NULL,
  `password` varchar(60) DEFAULT NULL,
  `balance` int(11) DEFAULT NULL,
  `email` varchar(60) DEFAULT NULL,
  `contactno` int(11) DEFAULT NULL,
  PRIMARY KEY (`userid`)
);

LOCK TABLES `account` WRITE;

INSERT INTO `account` VALUES
 ('Yakuza','aa','aa',54725,'yakuzarockz@japan.com',9843059),
 ('Bogambo Vila','bagambo','bogambo',24350,'bogambo@paki.com',4643614),
 ('Heth Ledger','heth1','heth1',20000,'heth@gotham.com',6434614);

UNLOCK TABLES;