DROP DATABASE IF EXISTS `tp`;
CREATE DATABASE `tp`;

-- -----------------------------------------------------
-- Table `tp`.`company`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tp`.`company` ;

CREATE TABLE IF NOT EXISTS `tp`.`company` (
  `company_id` INT NOT NULL AUTO_INCREMENT,
  `domain_name` VARCHAR(255) NOT NULL,
  `review_count` INT NOT NULL,
  `reviews_updated_at` INT NOT NULL,
  PRIMARY KEY (`company_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tp`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tp`.`user` ;

CREATE TABLE IF NOT EXISTS `tp`.`user` (
  `user_id` INT NOT NULL,
  `review_count` INT NOT NULL,
  `gender` ENUM('m', 'f', 'und') NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tp`.`review`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tp`.`review` ;

CREATE TABLE IF NOT EXISTS `tp`.`review` (
  `review_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `company_id` INT NOT NULL,
  `tp_review_id` INT NOT NULL,
  `title` VARCHAR(200) NULL,
  `content` TEXT NULL,
  `rating` INT NOT NULL,
  `created_at` INT NOT NULL,
  PRIMARY KEY (`review_id`),
  INDEX `fk_review_company_idx` (`company_id` ASC),
  INDEX `fk_review_user1_idx` (`user_id` ASC),
  UNIQUE INDEX `tp_review_id_UNIQUE` (`tp_review_id` ASC),
  CONSTRAINT `fk_review_company`
    FOREIGN KEY (`company_id`)
    REFERENCES `tp`.`company` (`company_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_review_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `tp`.`user` (`user_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tp`.`category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tp`.`category` ;

CREATE TABLE IF NOT EXISTS `tp`.`category` (
  `category_id` INT NOT NULL AUTO_INCREMENT,
  `tp_category_id` VARCHAR(255) NOT NULL,
  `url` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE INDEX `tp_category_id_UNIQUE` (`tp_category_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tp`.`company_category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tp`.`company_category` ;

CREATE TABLE IF NOT EXISTS `tp`.`company_category` (
  `company_category_id` INT NOT NULL AUTO_INCREMENT,
  `company_id` INT NOT NULL,
  `category_id` INT NOT NULL,
  PRIMARY KEY (`company_category_id`, `category_id`),
  INDEX `fk_category_company1_idx` (`company_id` ASC),
  INDEX `fk_company_category_category1_idx` (`category_id` ASC),
  CONSTRAINT `fk_category_company1`
    FOREIGN KEY (`company_id`)
    REFERENCES `tp`.`company` (`company_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_company_category_category1`
    FOREIGN KEY (`category_id`)
    REFERENCES `tp`.`category` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tp`.`category_position`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tp`.`category_position` ;

CREATE TABLE IF NOT EXISTS `tp`.`category_position` (
  `company_category_id` INT NOT NULL,
  `created_at` INT NOT NULL,
  `position` INT NOT NULL,
  `group` ENUM('general', 'rma', 'price', 'delivery') NOT NULL,
  PRIMARY KEY (`company_category_id`, `created_at`),
  CONSTRAINT `fk_category_position_category1`
    FOREIGN KEY (`company_category_id`)
    REFERENCES `tp`.`company_category` (`company_category_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tp`.`rating`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tp`.`rating` ;

CREATE TABLE IF NOT EXISTS `tp`.`rating` (
  `rating_id` INT NOT NULL AUTO_INCREMENT,
  `company_id` INT NOT NULL,
  `created_at` INT NOT NULL,
  `value` FLOAT NOT NULL,
  `group` ENUM('general', 'rma', 'price', 'delivery') NOT NULL,
  PRIMARY KEY (`rating_id`),
  CONSTRAINT `fk_rating_company1`
    FOREIGN KEY (`company_id`)
    REFERENCES `tp`.`company` (`company_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tp`.`job`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `tp`.`job` ;

CREATE TABLE IF NOT EXISTS `tp`.`job` (
  `job_id` INT NOT NULL AUTO_INCREMENT,
  `status` VARCHAR(45) NOT NULL,
  `start_time` INT NOT NULL,
  `target` INT NOT NULL,
  `type` ENUM('category', 'company', 'rating') NOT NULL,
  PRIMARY KEY (`job_id`))
ENGINE = InnoDB;
