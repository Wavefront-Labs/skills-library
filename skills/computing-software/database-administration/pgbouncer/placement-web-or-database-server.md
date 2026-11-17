---
id: computing-software.database-administration.pgbouncer.placement-web-or-database-server
name: placement-web-or-database-server
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, deployment, architecture, latency, faq]
level: intro
status: docs-checked
description: "FAQ guidance on installing PgBouncer on the web server, the database server or both."
sources:
  - https://www.pgbouncer.org/faq.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide where to run PgBouncer.

The FAQ answer is "it depends":

- On the web (application) server: good when short-lived connections are used, because connection setup latency is minimised (TCP needs a couple of packet roundtrips before a connection is usable).
- On the database server: good when many different hosts, for example web servers, connect to it, because their connections can be optimised together.
- On both: possible, but each PgBouncer hop adds a small amount of latency to each query.

The FAQ says to test which model performs best for your needs, and to consider how the choice affects application failover when a web server versus the database server goes away.

How to connect: PgBouncer acts as a Postgres server, so you simply point the client at the PgBouncer port (default 6432).

```
psql -h pgbouncer-host -p 6432 -U someuser appdb
```

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. Removed: a padded closing section and cross-references.

Method: documentation only; no commands were run.
