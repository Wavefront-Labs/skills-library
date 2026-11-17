---
id: computing-software.database-administration.pgbouncer.prepared-statements-client-workarounds
name: prepared-statements-client-workarounds
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, prepared-statements, jdbc, php-pdo, faq]
level: practitioner
status: docs-checked
description: "FAQ guidance for prepared statements in session and transaction pooling, including JDBC prepareThreshold=0 and PHP/PDO emulation."
sources:
  - https://www.pgbouncer.org/faq.html
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make clients and PgBouncer agree on prepared statements.

Session pooling: the reset query must clean old prepared statements. Use `server_reset_query = DISCARD ALL;` or at least `DEALLOCATE ALL;`.

Transaction pooling: since version 1.21.0 PgBouncer can track prepared statements and prepare them on the fly on the linked server connection. Enable it by setting `max_prepared_statements` to a non-zero value.

If you cannot use that, disable prepared statements on the client side.

JDBC: add `prepareThreshold=0` to the connection string.

PHP/PDO: set `PDO::ATTR_EMULATE_PREPARES` to true, at connect time:

```php
$db = new PDO("dsn", "user", "pass", array(PDO::ATTR_EMULATE_PREPARES => true));
```

or later:

```php
$db->setAttribute(PDO::ATTR_EMULATE_PREPARES, true);
```

Compatibility note from the FAQ: depending on version, PHP/PDO may be incompatible with PgBouncer's prepared statement support (issue #991). PDO is only compatible when PHP 8.4+ and libpq 17 are used. For older setups, upgrade or disable client-side prepared statements.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. Removed: a cross-reference line.

Method: documentation only; no commands were run.
