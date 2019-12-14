CREATE TABLE IF NOT EXISTS `accounts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `project_name` Nvarchar(255) NOT NULL,
  `email` Nvarchar(255) NOT NULL,
  `username` Nvarchar(255) NOT NULL,
  `password` Nvarchar(255) NOT NULL,
  `salt` Nvarchar(255) NOT NULL,
  `admin_level` INTEGER UNSIGNED NOT NULL DEFAULT 0,
  `created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
)
ENGINE = InnoDB;

insert into accounts (project_name, email, username, password, salt, admin_level) values ('SREmu', 'admin@swgsremu.com', 'shared', 'jfklQ*!nbZbbV@#I0$', '5be0a44dd4183b5842c2763d8a1585b1305aabb4', 0);
update accounts set id='0' where id='1';