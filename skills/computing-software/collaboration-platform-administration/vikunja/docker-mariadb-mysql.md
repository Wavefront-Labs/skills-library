---
id: computing-software.collaboration-platform-administration.vikunja.docker-mariadb-mysql
name: docker-mariadb-mysql
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, mariadb-container, mysql-backend, utf8mb4, database-type-mysql]
level: practitioner
status: docs-checked
description: "Swap the Vikunja compose example from PostgreSQL to MariaDB or MySQL, with the utf8mb4 server flags, env vars and healthcheck the docs use."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/full-docker-example.mdx
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/install.mdx
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/docker-start-to-finish.mdx
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In the compose examples, replace the `db` service with a MariaDB one and set `VIKUNJA_DATABASE_TYPE` to `mysql` on the vikunja service.

The `db` block uses `image: mariadb:10`, the command `--character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci`, environment `MYSQL_ROOT_PASSWORD`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`, a volume `./db:/var/lib/mysql`, and a healthcheck of `mysqladmin ping -h localhost -u $$MYSQL_USER --password=$$MYSQL_PASSWORD`.

Version floors: MySQL 8.0 (5.7 is unsupported because Vikunja needs recursive CTEs and window functions) and MariaDB 10.2. CI tests MySQL 8 and MariaDB 12.

If you use MySQL or MariaDB or non-latin characters, make sure the database is UTF-8 compatible; the postgres examples need no extra work.

Option `database.tls` (false, true, skip-verify, preferred) enables TLS for MySQL connections. A "commands out of sync" migration error on MySQL means wiping the db files and starting over.

## Checked

2026-11-04. Confirmed against the Vikunja Full docker example, Installing page (supported database versions and CI versions), Docker Walkthrough (commands out of sync) and config-raw.json (database.tls options). Nothing removed.

Method: documentation only; no commands were run.
