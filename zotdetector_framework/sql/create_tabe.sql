DROP DATABASE IF EXISTS zotdetectordb;
CREATE DATABASE zotdetectordb;
USE zotdetectordb;

-- SQL DDLs for Entities and their supporting tables
CREATE TABLE Student (
	id  		INTEGER,
	email       VARCHAR(50) NOT NULL,
    name_first  VARCHAR(20) NOT NULL,
    name_last   VARCHAR(20) NOT NULL,
	PRIMARY KEY (id)
);

-- SQL DDLs for Relationships
CREATE TABLE TrackDay (
	date        DATE,
    id  		INTEGER,
    emotion     ENUM('sad', 'happy', 'stressed') NOT NULL,
    amount      DECIMAL(3,2) NOT NULL,
    PRIMARY KEY (id, date),
    FOREIGN KEY (id) REFERENCES Student (id) ON DELETE CASCADE
);