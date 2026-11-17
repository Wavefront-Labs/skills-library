---
id: computing-software.devops-ci-cd.rundeck.mysql-database-backend
name: mysql-database-backend
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, mysql, mariadb-driver, autoreconnect, database-backend]
level: practitioner
status: docs-checked
description: "Set up MySQL or MariaDB as the Rundeck database: create database and user, configure the datasource URL, choose a JDBC driver, and handle Azure invisible primary keys."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/configuration/database/mysql.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Version guidance from the page: MySQL 8.0 (8.0.35 or newer) is recommended; 8.4 is supported as of Rundeck 6.0.0; 5.7 lacks `utf8mb4` as default so some parts of Rundeck fail; 5.6 is end of life.

Prepare MySQL: run `mysql_secure_installation`, and set a suitable `innodb_buffer_pool_size` (80% of memory is the common wisdom on dedicated servers).

Create database and user (use the host Rundeck connects from):

```sql
create database rundeck;
create user 'rundeckuser'@'localhost' identified by 'rundeckpassword';
grant ALL on rundeck.* to 'rundeckuser'@'localhost';
```

Edit `rundeck-config.properties` (`/etc/rundeck/` for RPM/DEB, `$RDECK_BASE/server/config/` for the launcher):

```properties
dataSource.driverClassName = org.mariadb.jdbc.Driver
dataSource.url = jdbc:mysql://myserver/rundeck?autoReconnect=true&useSSL=false
dataSource.username = rundeckuser
dataSource.password = rundeckpassword
```

`autoReconnect=true` fixes dropped idle connections ("Can not read response from server. Expected to read 4 bytes, read 0 bytes").

Gotchas:
- A startup database access error usually means the client hostname MySQL sees differs from the one granted.
- Oracle's MySQL driver goes in `$RDECK_BASE/server/lib` (launcher) or `/var/lib/rundeck/lib` (create it) for RPM/DEB.
- Azure Database for MySQL Flexible Server: set `sql_generate_invisible_primary_key` to OFF in Server parameters.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Using MySQL as a database backend: version guidance (8.0.35+, 8.4 from Rundeck 6.0.0, 5.7 utf8mb4, 5.6 EOL), mysql_secure_installation, innodb_buffer_pool_size 80% advice, SQL statements, rundeck-config.properties locations and datasource lines, autoReconnect error text, Oracle driver locations, and Azure sql_generate_invisible_primary_key OFF. Nothing removed.

Method: documentation only; no commands were run.
