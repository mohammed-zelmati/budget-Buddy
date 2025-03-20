CREATE DATABASE budget_buddy;
USE budget_buddy;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reference VARCHAR(100),
    description TEXT,
    montant DECIMAL(10, 2),
    date DATE,
    type ENUM('deposit', 'withdrawal', 'transfer'),
    user_id INT,
    category_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

INSERT INTO categories (name) VALUES ('Food'), ('Transport'), ('Entertainment'), ('Bills'), ('Other');