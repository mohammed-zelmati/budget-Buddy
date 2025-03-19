CREATE TABLE `follows` (
  `following_user_id` integer,
  `followed_user_id` integer,
  `created_at` timestamp
);

CREATE TABLE `users` (
  `id` integer PRIMARY KEY,
  `username` varchar(255),
  `role` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `posts` (
  `id` integer PRIMARY KEY,
  `title` varchar(255),
  `body` text COMMENT 'Content of the post',
  `user_id` integer NOT NULL,
  `status` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `utilisateurs` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `nom` VARCHAR(50) NOT NULL,
  `prenom` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) UNIQUE NOT NULL,
  `mot_de_passe` VARCHAR(255) NOT NULL,
  `date_inscription` TIMESTAMP DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `comptes` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `utilisateur_id` INT NOT NULL,
  `numero_compte` VARCHAR(20) UNIQUE NOT NULL,
  `solde` DECIMAL(10,2) DEFAULT 0,
  `date_creation` TIMESTAMP DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `transactions` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `compte_id` INT NOT NULL,
  `reference_transaction` VARCHAR(50) UNIQUE NOT NULL,
  `description` TEXT NOT NULL,
  `montant` DECIMAL(10,2) NOT NULL,
  `date_transaction` TIMESTAMP DEFAULT (CURRENT_TIMESTAMP),
  `type_transaction` ENUM ('retrait', 'dépôt', 'transfert') NOT NULL,
  `categorie` VARCHAR(50)
);

CREATE TABLE `banquiers` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `nom` VARCHAR(50) NOT NULL,
  `prenom` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) UNIQUE NOT NULL,
  `mot_de_passe` VARCHAR(255) NOT NULL,
  `date_inscription` TIMESTAMP DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `transferts` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `compte_source_id` INT NOT NULL,
  `compte_dest_id` INT NOT NULL,
  `montant` DECIMAL(10,2) NOT NULL,
  `date_transfert` TIMESTAMP DEFAULT (CURRENT_TIMESTAMP)
);

ALTER TABLE `posts` ADD CONSTRAINT `user_posts` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `follows` ADD FOREIGN KEY (`following_user_id`) REFERENCES `users` (`id`);

ALTER TABLE `follows` ADD FOREIGN KEY (`followed_user_id`) REFERENCES `users` (`id`);

ALTER TABLE `comptes` ADD FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateurs` (`id`) ON DELETE CASCADE;

ALTER TABLE `transactions` ADD FOREIGN KEY (`compte_id`) REFERENCES `comptes` (`id`) ON DELETE CASCADE;

ALTER TABLE `transferts` ADD FOREIGN KEY (`compte_source_id`) REFERENCES `comptes` (`id`) ON DELETE CASCADE;

ALTER TABLE `transferts` ADD FOREIGN KEY (`compte_dest_id`) REFERENCES `comptes` (`id`) ON DELETE CASCADE;
