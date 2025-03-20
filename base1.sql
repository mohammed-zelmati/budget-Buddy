-- BASE DE DONNEES "base1"
CREATE TABLE utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comptes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    numero_compte VARCHAR(20) NOT NULL UNIQUE,
    solde DECIMAL(10, 2) DEFAULT 0.00,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);


CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    compte_id INT NOT NULL,
    reference_transaction VARCHAR(50) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    montant DECIMAL(10, 2) NOT NULL,
    date_transaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    type_transaction ENUM('retrait', 'dépôt', 'transfert') NOT NULL,
    categorie VARCHAR(50),
    FOREIGN KEY (compte_id) REFERENCES comptes(id) ON DELETE CASCADE
);

CREATE TABLE banquiers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transferts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    compte_source_id INT NOT NULL,
    compte_dest_id INT NOT NULL,
    montant DECIMAL(10, 2) NOT NULL,
    date_transfert TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (compte_source_id) REFERENCES comptes(id) ON DELETE CASCADE,
    FOREIGN KEY (compte_dest_id) REFERENCES comptes(id) ON DELETE CASCADE
);

CREATE TABLE portefeuille (
    id INT AUTO_INCREMENT PRIMARY KEY,
    banquier_id INT NOT NULL,
    compte_id INT NOT NULL,
    FOREIGN KEY (banquier_id) REFERENCES banquiers(id) ON DELETE CASCADE,
    FOREIGN KEY (compte_id) REFERENCES comptes(id) ON DELETE CASCADE
);

CREATE TABLE alertes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    type_alert VARCHAR(50),
    message TEXT,
    date_alert TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);

