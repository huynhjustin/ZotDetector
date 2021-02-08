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

CREATE TABLE Emotions (
	date        DATE,
    id  		INTEGER,
    angry       DECIMAL(4,2) NOT NULL,
    disgusted   DECIMAL(4,2) NOT NULL,
    fearful     DECIMAL(4,2) NOT NULL,
    happy       DECIMAL(4,2) NOT NULL,
    neutral     DECIMAL(4,2) NOT NULL,
    sad         DECIMAL(4,2) NOT NULL,
    surprised   DECIMAL(4,2) NOT NULL,
    PRIMARY KEY (id, date),
    FOREIGN KEY (id) REFERENCES Student (id) ON DELETE CASCADE
);