---
id: computing-software.messaging-and-integration.debezium.mysql-connector-user-and-privileges
name: mysql-connector-user-and-privileges
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mysql, user, privileges, grants]
level: practitioner
status: docs-checked
description: "Create the MySQL account Debezium needs with SELECT, RELOAD, SHOW DATABASES, REPLICATION SLAVE and REPLICATION CLIENT."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mysql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The connector needs a MySQL user with permissions on every database it captures.

```sql
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT, RELOAD, SHOW DATABASES, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'user' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;
```

What each grant does, per the docs:

- `SELECT`: read table rows, used only during snapshots.
- `RELOAD`: run `FLUSH` to clear caches, flush tables or acquire locks; snapshots only.
- `SHOW DATABASES`: list database names; snapshots only.
- `REPLICATION SLAVE`: connect to and read the binlog.
- `REPLICATION CLIENT`: allows `SHOW MASTER STATUS`, `SHOW SLAVE STATUS` and `SHOW BINARY LOGS`. The connector always requires it.

On hosted services such as Amazon RDS or Aurora that do not allow a global read lock, the connector falls back to table-level locks, so also grant `LOCK TABLES`.

Gotcha: `SELECT`, `RELOAD` and `SHOW DATABASES` are used only when performing a snapshot, so a snapshot needs them in addition to the replication grants.

Use a host pattern that matches where Kafka Connect runs, not `localhost`, in real deployments.

Check: the account holds the five privileges above, plus `LOCK TABLES` on hosted services.

## Checked

2026-11-03. Page used: the Debezium mysql connector reference, https://debezium.io/documentation/reference/stable/connectors/mysql.html.
Confirmed against it: the CREATE USER and GRANT statements, the purpose of each privilege, the LOCK TABLES fallback on hosted services.
Removed or reworded: the global-privilege rationale, the schema-history claim, SHOW GRANTS.
Method: documentation only; no commands were run.
