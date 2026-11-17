---
id: computing-software.devops-ci-cd.forgejo.database-mysql-mariadb-setup
name: database-mysql-mariadb-setup
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [mysql-setup, mariadb-setup, utf8mb4-bin, charset-collation]
level: practitioner
status: docs-checked
description: "Create a MySQL or MariaDB user and case-sensitive database for Forgejo with the minimal grants."
sources:
  - https://forgejo.org/docs/latest/admin/installation/database-preparation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Log in as root (`mysql -u root -p`) and create a dedicated user. For a database on the same machine use `CREATE USER 'forgejo'@'localhost' IDENTIFIED BY '<strong-password>';`. For a remote database, use the address Forgejo connects from instead, such as `'forgejo'@'192.0.2.10'`.

Forgejo expects a case-sensitive collation. Create the database with:

`CREATE DATABASE forgejo CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_bin';`

utf8mb4_bin is a common choice for MariaDB and MySQL. At startup Forgejo tries to find a better collation (utf8mb4_0900_as_cs or uca1400_as_cs) and alters the database if possible. To force another collation, set `[database].CHARSET_COLLATION` in app.ini.

Then grant exactly these privileges:

`GRANT ALTER, CREATE, DELETE, DROP, INDEX, INSERT, REFERENCES, SELECT, UPDATE ON forgejo.* TO 'forgejo'@'localhost'; FLUSH PRIVILEGES;`

Use the remote address in the grant for non-local setups, then leave the client with `exit`. The docs ask for a secure generated password rather than the example one, and say an existing database installation can be reused.

## Checked

2026-11-04. Confirmed against the Forgejo Database Preparation page (MySQL/MariaDB section): root login, both CREATE USER forms, the utf8mb4_bin database statement, the collation upgrade at startup, CHARSET_COLLATION, the grant list and FLUSH PRIVILEGES. Nothing removed.

Method: documentation only; no commands were run.
