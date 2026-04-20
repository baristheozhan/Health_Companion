DROP DATABASE IF EXISTS health;
CREATE DATABASE health;
USE health;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    tckn VARCHAR(11) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,
    hospital VARCHAR(100),
    rating FLOAT DEFAULT 0
);

CREATE TABLE medication_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    med_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    institution_id INT DEFAULT 1,
    date VARCHAR(50) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (doctor_id, date)
);

CREATE TABLE ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    appointment_id INT DEFAULT 1,
    rated_by VARCHAR(20),
    score INT,
    doctor_communication INT,
    medication_discipline INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);