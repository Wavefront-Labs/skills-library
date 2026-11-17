---
id: computing-software.software-engineering.quarkus.quarkus-flyway-migrations
name: quarkus-flyway-migrations
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, flyway, migrations, schema, database, jdbc, datasource]
level: practitioner
status: docs-checked
description: "Run Flyway schema migrations in Quarkus: dependencies, migrate-at-start, named datasources, customizers, injecting Flyway, repair and Kubernetes init Jobs."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/flyway.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flyway migrations in Quarkus

## Setup
Add `io.quarkus:quarkus-flyway`, a JDBC driver extension (e.g. `quarkus-jdbc-postgresql`), and, unless you use an in-memory or file database such as H2 or SQLite, the matching Flyway module (e.g. `org.flywaydb:flyway-database-postgresql`, `flyway-mysql`, `flyway-sqlserver`, `flyway-database-oracle`, `flyway-database-db2`).

Put migrations in `src/main/resources/db/migration` using Flyway naming, e.g. `V1.0.0__Quarkus.sql`.

```properties
quarkus.datasource.db-kind=postgresql
quarkus.datasource.username=sarah
quarkus.datasource.password=connor
quarkus.datasource.jdbc.url=jdbc:postgresql://localhost:5432/mydatabase
quarkus.flyway.migrate-at-start=true
# optional: baseline-on-migrate, baseline-version, connect-retries, schemas,
# table, locations (comma list), sql-migration-prefix, repeatable-sql-migration-prefix
```

With `migrate-at-start=true` migration runs during application startup. Without it, inject `Flyway` and call `migrate()` yourself. In dev mode, modified migration scripts restart the app; set `%dev.quarkus.flyway.clean-at-start=true` so Flyway actually reruns the modified script.

## Repair
After a failed migration (e.g. on a database without transactional DDL), set `quarkus.flyway.repair-at-start=true` or call `Flyway#repair()`.

## Multiple datasources
Flyway keys mirror datasource names: `quarkus.flyway.[optional name.][property]`.

```properties
quarkus.flyway.schemas=DEFAULT_TEST_SCHEMA
quarkus.flyway.users.locations=db/users/location1,db/users/location2
quarkus.flyway.users.migrate-at-start=true
```

Without configuration, Flyway is set up for every datasource with defaults.

## Injection and customisation
```java
@Inject Flyway flyway;
@Inject @FlywayDataSource("inventory") Flyway flywayForInventory;
@Inject @Named("flyway_users") Flyway flywayForUsers;
```
For extra settings, add a bean implementing `io.quarkus.flyway.FlywayConfigurationCustomizer` (`customize(FluentConfiguration)`); annotate it `@FlywayDataSource("users")` to target a named datasource.

## Reactive datasources
Flyway uses JDBC. For a datasource also used reactively, configure it as both JDBC and reactive (e.g. `quarkus-jdbc-postgresql` and `quarkus-reactive-pg-client`).

## Kubernetes
Generated Kubernetes manifests include an init `Job` running Flyway once before the Pod starts. Disable with `quarkus.kubernetes.init-task-defaults.enabled=false` (or `quarkus.openshift...`). Change the wait image (default `groundnuty/k8s-wait-for:no-root-v1.7`) via `quarkus.kubernetes.init-task-defaults.wait-for-container.image`.

## Known issue: Oracle schemas in Dev Services
Managing multiple schemas runs as the `quarkus` user, which needs DBA rights. Add a script containing `ALTER SESSION SET CONTAINER=quarkus;` and `GRANT DBA TO quarkus;` and point `quarkus.datasource.devservices.init-privileged-script-path` at it.

## Checked

2026-11-07. Read in full: flyway.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
