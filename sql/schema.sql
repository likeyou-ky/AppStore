/*******************

  Create the schema

********************/

CREATE TABLE IF NOT EXISTS users (
display_photo VARCHAR(200) NOT NULL,
display_name VARCHAR(64) NOT NULL,
your_email VARCHAR(64) PRIMARY KEY CHECK(your_email LIKE '%_@_%._%' ),
age INT NOT NULL,
phone_number INT NOT NULL,
gender VARCHAR(64) NOT NULL CHECK(gender = 'Male' OR gender = 'Female' OR gender = 'Prefer not to say'),
vaccination_status VARCHAR(64) NOT NULL CHECK(vaccination_status = 'Fully Vaccinated' or vaccination_status = 'Not Vaccinated'),
password VARCHAR(10) NOT NULL,
rating VARCHAR(10),
count_rate VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS buddies (
your_email VARCHAR(64) PRIMARY KEY CHECK(your_email LIKE '%_@_%._%' ),
education VARCHAR(256),
interest VARCHAR(256),
height DECIMAL(5,2),
rate_per_hour DECIMAL NOT NULL,
);

CREATE TABLE If NOT EXISTS meeting_log (
meeting_id INT PRIMARY KEY UNIQUE,
buddy INT(8) REFERENCES buddy(phone_number) DEFERRABLE,
client INT(8) REFERENCES client(phone_number) DEFERRABLE,
rating_on_buddy INT(1) CHECK(rating BETWEEN 1 AND 5),
rating_on_client INT(1) CHECK(rating BETWEEN 1 AND 5),	
);

SELECT * from users
delete from users
drop table users

UPDATE users
SET rating = '0', count_rate = '0'
WHERE your_email = 'abc@gmail.com';