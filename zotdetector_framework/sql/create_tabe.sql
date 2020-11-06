DROP DATABASE IF EXISTS zotdetectordb;
CREATE DATABASE zotdetectordb;
USE zotdetectordb;

-- SQL DDLs for Entities and their supporting tables
CREATE TABLE Student (
	student_id  INTEGER,
	email       VARCHAR(50) NOT NULL,
    name_first  VARCHAR(20) NOT NULL,
    name_last   VARCHAR(20) NOT NULL,
	PRIMARY KEY (student_id)
);

CREATE TABLE Day (
    date DATE,
    PRIMARY KEY (date)
);

-- SQL DDLs for Relationships
CREATE TABLE TrackDay (
	date        DATE,
    student_id  INTEGER,
    emotion     ENUM('sad', 'happy', 'stressed') NOT NULL,
    amount      DECIMAL NOT NULL,
    PRIMARY KEY (student_id, date),
    FOREIGN KEY (student_id) REFERENCES Student (student_id) ON DELETE CASCADE,
    FOREIGN KEY (date) REFERENCES Day (date) ON DELETE CASCADE
);