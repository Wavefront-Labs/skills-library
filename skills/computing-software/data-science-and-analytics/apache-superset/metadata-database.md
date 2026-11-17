---
id: computing-software.data-science-and-analytics.apache-superset.metadata-database
name: metadata-database
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [metadata-database, postgresql, mysql, sqlalchemy, db-upgrade]
level: intro
status: docs-checked
description: "Choose and configure the Superset metadata database: supported PostgreSQL and MySQL versions, SQLALCHEMY_DATABASE_URI and why SQLite is not for production."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/configuring-superset.mdx
  - https://github.com/apache/superset/blob/master/docs/admin_docs/installation/architecture.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: point Superset at a durable metadata store.

The metadata database holds chart and dashboard definitions, user information and logs. By default Superset uses SQLite; the docs strongly discourage that for production (security, scalability, data integrity) and recommend a supported engine on a separate host or container.

Supported engines and drivers:
- PostgreSQL 10.X to 17.X: `pip install psycopg2`, URI `postgresql://<UserName>:<DBPassword>@<Database Host>/<Database Name>`
- MySQL 5.7 and 8.X: `pip install mysqlclient`, URI `mysql://<UserName>:<DBPassword>@<Database Host>/<Database Name>`

Set the connection string in `superset_config.py`:

```python
SQLALCHEMY_DATABASE_URI = "postgresql://<UserName>:<DBPassword>@<Database Host>/<Database Name>"
```

The configuration page says to change at least `SECRET_KEY` and `SQLALCHEMY_DATABASE_URI`.

From the architecture page: for production use a properly configured, managed, standalone database and back it up regularly. Every worker node and web server must share a common metadata database (see the Celery async queries skill), which SQLite cannot do. Migration after upgrades is `superset db upgrade` then `superset init` (see the upgrading skill).

## Checked

2026-11-08: read architecture.mdx in full; read the metadata-database section of configuring-superset.mdx (lines around 60-85 and 170-190), not the whole page. Removed claims not on those pages: the list of what the database stores beyond definitions, users and logs, and the "keep separate from analytic sources" rule.
Method: documentation only; no commands were run.
