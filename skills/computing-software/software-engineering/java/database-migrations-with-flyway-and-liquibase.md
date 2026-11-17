---
id: computing-software.software-engineering.java.database-migrations-with-flyway-and-liquibase
name: database-migrations-with-flyway-and-liquibase
category: computing-software
field: software-engineering
product: java
tags: [java, flyway, liquibase, schema-migrations, spring-boot]
level: practitioner
status: docs-checked
description: "Version database schemas in JVM apps with Flyway or Liquibase: how migrate works, Spring Boot auto-configuration, test-only migrations, and not mixing with schema.sql."
sources:
  - https://documentation.red-gate.com/fd/migrations-271585107.html
  - https://docs.spring.io/spring-boot/how-to/data-initialization.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database migrations with Flyway and Liquibase

**Goal:** every environment's schema is built from the same ordered migration history.

## Flyway concepts
- Migrations are SQL scripts (also Java or script migrations) tracked in version control; the same scripts run in the same order in each environment.
- Types: versioned (regular and undo), repeatable, and baseline.
- `migrate` scans the filesystem or classpath, compares with what is applied (recorded in a schema history table) and applies the gap; it is idempotent. Flyway recommends running it on application startup.
- In one run, pending versioned migrations are applied in order first, then changed repeatable migrations, ordered by description.
- By default each migration script runs in a single transaction; a failed migration is marked failed and rolled back if possible. Per-script behaviour is set with a `.conf` file of the same name beside the script.

## Spring Boot
- Flyway: add the Flyway module to the classpath (the `spring-boot-starter-flyway` starter covers in-memory and file-based databases; other databases also need a database-specific module such as `org.flywaydb:flyway-database-postgresql`). Boot calls `Flyway.migrate()`; provide a `FlywayMigrationStrategy` bean for more control.
- Liquibase: add `spring-boot-starter-liquibase`. The master changelog is read from `db/changelog/db.changelog-master.yaml` by default (`spring.liquibase.change-log` changes it); YAML, JSON, XML and SQL formats are supported.
- Test-only data: Flyway migrations in `src/test/resources/db/migration` (for example `V9999__test-data.sql`) run after production migrations only when testing; for Liquibase use contexts. Profile-specific `spring.flyway.locations` can restrict migrations to a profile.
- With the Liquibase starter, migrations run by default at startup and before tests (`spring.liquibase.enabled` customizes this); you cannot use two different ways to initialize the database, such as Liquibase for startup and JPA for tests.
- Do not combine the basic `schema.sql` and `data.sql` scripts with Flyway or Liquibase.

## Verify
- [ ] Only one tool creates the schema in every environment, including tests.
- [ ] Migrations run at startup or as a deliberate deployment step.

## Checked
2026-11-01. Confirmed against the Flyway "Migrations" page and the Spring Boot data-initialization how-to. Removed as unconfirmed by those pages: file naming and checksum-mismatch behaviour, repair and baseline-on-migrate, ddl-auto advice, expand/contract and PostgreSQL lock advice, Liquibase changeset details, cleanDisabled default.
Method: documentation only; no commands were run.
