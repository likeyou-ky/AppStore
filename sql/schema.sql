/*******************

  Create the schema

********************/

CREATE TABLE IF NOT EXISTS users (
display_photo VARCHAR(200) NOT NULL CHECK(display_photo LIKE '%.jpg' OR display_photo LIKE '%.png' OR display_photo LIKE '%.jpeg'),
display_name VARCHAR(64) NOT NULL,
your_email VARCHAR(64) PRIMARY KEY CHECK(your_email LIKE '%_@_%._%' ),
age INT NOT NULL CHECK(age>=18),
phone_number INT NOT NULL CHECK (phone_number BETWEEN 80000000 AND 99999999),
gender VARCHAR(64) NOT NULL CHECK(gender = 'Male' OR gender = 'Female' OR gender = 'Prefer not to say'),
vaccination_status VARCHAR(64) NOT NULL CHECK(vaccination_status = 'Fully Vaccinated' or vaccination_status = 'Not Vaccinated'),
password VARCHAR(64) NOT NULL CHECK (LENGTH(password)>=6 AND LENGTH(password)<=64),
rating DECIMAL(3,2),
count_rate INT DEFAULT 0 CHECK(count_rate>=0)
);

CREATE TABLE IF NOT EXISTS interests (
interest VARCHAR(256) PRIMARY KEY UNIQUE
);

CREATE TABLE IF NOT EXISTS buddies (
your_email VARCHAR(64) PRIMARY KEY CHECK(your_email LIKE '%_@_%._%' ),
education VARCHAR(256),
height DECIMAL CHECK(height BETWEEN 90 and 250),
rate_per_hour DECIMAL NOT NULL,
interest_1 VARCHAR(256) REFERENCES interests(interest) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE,
interest_2 VARCHAR(256) REFERENCES interests(interest) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE,
interest_3 VARCHAR(256) REFERENCES interests(interest) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE,
interest_4 VARCHAR(256) REFERENCES interests(interest) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE,
interest_5 VARCHAR(256) REFERENCES interests(interest) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE,
FOREIGN KEY (your_email) REFERENCES users(your_email) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE
);

CREATE TABLE IF NOT EXISTS meeting_logs (
meeting_id INT PRIMARY KEY UNIQUE,
buddy VARCHAR(64) REFERENCES users(your_email) ON UPDATE CASCADE ON DELETE NO ACTION NOT DEFERRABLE,
client VARCHAR(64) REFERENCES users(your_email) ON UPDATE CASCADE ON DELETE NO ACTION NOT DEFERRABLE,
rating_on_buddy INT CHECK(rating_on_buddy BETWEEN 1 AND 5),
rating_on_client INT CHECK(rating_on_client BETWEEN 1 AND 5)	
);