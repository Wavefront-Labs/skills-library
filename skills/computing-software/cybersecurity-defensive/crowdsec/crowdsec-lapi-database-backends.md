---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-lapi-database-backends
name: crowdsec-lapi-database-backends
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [database, sqlite, mysql, postgresql, db-config, flush, retention]
level: practitioner
status: docs-checked
description: "Choose and configure the Local API database (SQLite, MySQL, MariaDB, PostgreSQL) and set alert and metric retention with flush."
sources: ["https://docs.crowdsec.net/docs/local_api/database", "https://docs.crowdsec.net/docs/configuration/crowdsec_configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SQLite is the default and needs no setup. For heavy traffic use MySQL, MariaDB or PostgreSQL. The docs list MySQL 5.6.35, 5.7.26 and 8, MariaDB 10.2, 10.3 and latest, and PostgreSQL 13 to 17.

Switching an existing install to a new backend does not migrate data: re-register machines (for example `cscli machines add -a`) and bouncers against the new database.

## MySQL or MariaDB

```sql
CREATE DATABASE crowdsec;
CREATE USER 'crowdsec'@'%' IDENTIFIED BY '<password>';
GRANT ALL PRIVILEGES ON crowdsec.* TO 'crowdsec'@'%';
FLUSH PRIVILEGES;
```

## PostgreSQL

```sql
CREATE DATABASE crowdsec;
CREATE USER crowdsec WITH PASSWORD '<password>';
ALTER SCHEMA public owner to crowdsec;
GRANT ALL PRIVILEGES ON DATABASE crowdsec TO crowdsec;
```

On PostgreSQL 15 or later also run `GRANT CREATE on SCHEMA public TO crowdsec;` inside the crowdsec database. Then edit `db_config` in `/etc/crowdsec/config.yaml` and restart. The configuration page shows `${DB_PASSWORD}` environment-variable substitution so the password need not be stored in the file.

## Retention (flush)

```yaml
db_config:
  flush:
    max_items: 5000
    max_age: 7d
    metrics_max_age: 7d
    bouncers_autodelete:
      cert: 30d
      api_key: 30d
    agents_autodelete:
      cert: 30d
      login_password: 30d
```

`max_items` caps alerts in the database, `max_age` is alert retention. The autodelete values remove bouncers that have not pulled, or agents that have not pushed, for that duration. Agent deletion also requires that the agent has no active alerts. Supported units are s, m, h and d.

## Checked
2026-11-08. Confirmed against the Databases page (supported versions, SQL setup, PostgreSQL 15 grant, no data migration) and the sections of the CrowdSec configuration page on environment variables and `db_config.flush` (read in part, not the whole 40 KB page). Added the `GRANT ALL PRIVILEGES` line from the page. Removed: the claim that only certificate-authenticated agents need no active alerts (the page says it for both agent types).
Method: documentation only; no commands were run.
