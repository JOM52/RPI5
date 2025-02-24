-- Batch pour la création de la base de donnee logger
-- 23.04.2020 Joseph Metrailler
-- --------------------------------------------------------------
-- si elle existe, supprimer la db existante et creer la nouvelle
DROP DATABASE IF EXISTS logger;
CREATE DATABASE logger;
USE logger;
-- --------------------------------------------------------------
-- table tlog pour les donnees
CREATE TABLE tlog
(
  t0 double NOT NULL,
  t1 double NOT NULL,
  t2 double NOT NULL,
  t3 double NOT NULL,
  t4 double NOT NULL,
  t5 double NOT NULL,
  t6 double NOT NULL,
  t7 double NOT NULL,
  t8 double NOT NULL,
  t9 double NOT NULL,
  t10 double NOT NULL,
  t11 double NOT NULL,
  t12 double NOT NULL,
  t13 double NOT NULL,
  t14 double NOT NULL,
  t15 double NOT NULL,
  t16 double NOT NULL,
  t17 double NOT NULL,
  t18 double NOT NULL,
  t19 double NOT NULL,
  t20 double NOT NULL,
  s10 tinyint,
  s11 tinyint,
  s20 tinyint,
  s21 tinyint,
  s30 tinyint,
  s31 tinyint,
  id int NOT NULL AUTO_INCREMENT,
  time_stamp timestamp NOT NULL,
  PRIMARY KEY (id),
  INDEX i_date (time_stamp),
  INDEX i_id (id),
  UNIQUE(id)
);
-- --------------------------------------------------------------
-- table tsensor pour les capteurs
CREATE TABLE tsensor
(
  id int NOT NULL AUTO_INCREMENT,
  sensor_no tinyint NOT NULL,
  sensor_type varchar(10) NOT NULL,
  sensor_chanel int NOT NULL,
  sensor_field varchar(5) NOT NULL,
  sensor_id varchar(15),
  sensor_txt varchar(30) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE(sensor_field),
  INDEX i_id (id)
);
-- --------------------------------------------------------------
-- remplir la table tsensor
INSERT INTO tsensor (sensor_no, sensor_type, sensor_chanel, sensor_field, sensor_id, sensor_txt) 
VALUES 
('0', 'ds18b20', '0', 't0', '28-000008a326e5', 'from pac'), 
('1', 'ds18b20', '0', 't1', '28-000008a10cf1', 'to pac'), 
('2', 'ds18b20', '0', 't2', '28-000008a27bb9', 'from accu'), 
('3', 'ds18b20', '0', 't3', '28-000008a32b37', 'on bypass'), 
('4', 'ds18b20', '0', 't4', '28-000008a109bf', 'to home'), 
('5', 'ds18b20', '0', 't5', '28-000008a12739', 'from home rez'), 
('6', 'ds18b20', '0', 't6', '28-000008a28337', 'from home 1er'), 
('7', 'ds18b20', '0', 't7', '28-000008a12a50', 'from home'), 
('8', 'ds18b20', '0', 't8', '28-000008a11bc7', 'from home after bypass'), 
('9', 'ds18b20', '0', 't9', '28-000008a11dcc', 'to boiler'), 
('10', 'ds18b20', '0', 't10', '28-000008a328cc', 'boiler'), 
('11', 'ds18b20', '0', 't11', '28-000008a233a1', 'from boiler'), 
('12', 'ds18b20', '0', 't12', '28-000008a3195f', 'salon'), 
('13', 'ds18b20', '0', 't13', '28-000008a1091e', 'bureau'), 
('14', 'ds18b20', '0', 't14', '28-000008a123a3', 'exterieur'), 
('15', 'ds18b20', '0', 't15', '', 't15'), 
('16', 'ds18b20', '0', 't16', '', 't16'), 
('17', 'ds18b20', '0', 't17', '', 't17'), 
('18', 'ds18b20', '0', 't18', '', 't18'), 
('19', 'ds18b20', '0', 't19', '', 't19'), 
('20', 'ds18b20', '0', 't20', '', 't20'), 
('21', 'ds2413', '0', 's10', '3a-000000462cd6', 'pump boiler on-off'), 
('22', 'ds2413', '1', 's11', '3a-000000462cd6', 'pump home on-off'), 
('23', 'ds2413', '0', 's20', '3a-000000465478', 'pac on-off'), 
('24', 'ds2413', '1', 's21', '3a-000000465478', 's21 on-off'), 
('25', 'ds2413', '0', 's30', '', 's30 on-off'), 
('26', 'ds2413', '1', 's31', '', 's31 on-off')
