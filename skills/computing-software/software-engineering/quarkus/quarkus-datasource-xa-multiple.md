---
id: computing-software.software-engineering.quarkus.quarkus-datasource-xa-multiple
name: quarkus-datasource-xa-multiple
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, datasource, xa, narayana, jta, recovery, transactions]
level: advanced
status: docs-checked
description: "Use several Quarkus JDBC datasources in one transaction by enabling XA, with recovery settings, the failure signature, and LRCO or REQUIRES_NEW fallbacks."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/datasource.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple datasources in one Quarkus transaction (XA)

## The problem
XA support is disabled by default, so a transaction can include at most one datasource. Touching a second non-XA datasource in the same transaction fails with an exception like:

```text
Caused by: java.sql.SQLException: Exception in association of connection to existing transaction
Caused by: java.sql.SQLException: Failed to enlist. Check if a connection from another datasource is already enlisted to the same transaction
```

## Enable XA
1. Make sure the JDBC driver supports XA. All built-in drivers do; custom drivers (`db-kind=other`) might not.
2. Make sure the database server is configured to enable XA.
3. Set it explicitly on each relevant datasource:

```properties
quarkus.datasource.jdbc.transactions=xa
quarkus.datasource.inventory.jdbc.transactions=xa
```

With XA, a rollback in one datasource rolls back every datasource enrolled in the transaction. XA on reactive datasources is not supported. Non-datasource resources in the transaction may not support XA or may need extra configuration.

## Recovery
When a datasource uses `transactions=xa` and `quarkus.transaction-manager.enable-recovery=true`, the datasource is automatically registered for recovery (the preferred, safe default). Opt out per datasource with `quarkus.datasource.jdbc.enable-recovery=false` or `quarkus.datasource."datasource-name".jdbc.enable-recovery=false`. Change this only in advanced cases when certain recovery is not needed: wrong settings can leave resources locked indefinitely and cause data loss or unavailability.

Integration with Narayana is automatic when the Narayana JTA extension is present; override with the `transactions` property (`quarkus.datasource.jdbc.transactions` for the default, `quarkus.datasource.<name>.jdbc.transactions` for named).

## If XA cannot be enabled everywhere
- Enabling XA for all datasources except exactly one is still supported through Last Resource Commit Optimization (LRCO).
- If a rollback in one datasource need not roll back the others, split the work into separate transactions: prefer `QuarkusTransaction.requiringNew()` or `@Transactional(REQUIRES_NEW)`; use `UserTransaction` for more complex cases.

## Driver XA classes (from the page's mapping table)
`org.postgresql.xa.PGXADataSource` (PostgreSQL), `com.mysql.cj.jdbc.MysqlXADataSource` (MySQL), `org.mariadb.jdbc.MariaDbDataSource` (MariaDB), `oracle.jdbc.xa.client.OracleXADataSource` (Oracle), `com.microsoft.sqlserver.jdbc.SQLServerXADataSource` (SQL Server), `com.ibm.db2.jcc.DB2XADataSource` (DB2), `org.h2.jdbcx.JdbcDataSource` (H2). Driver resolution from `db-kind` is automatic; you rarely set it.

Note for Oracle: closing a connection can commit uncommitted work, so Quarkus rolls back unfinished transactions on close; with XA the transaction manager handles the rollback.

## Checked

2026-11-07. Read in full: datasource.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
