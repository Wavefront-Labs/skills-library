---
id: computing-software.software-engineering.quarkus.quarkus-datasource-named-and-active
name: quarkus-datasource-named-and-active
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, datasource, jdbc, agroal, named-datasource, db-kind, cdi]
level: practitioner
status: docs-checked
description: "Configure default and named Quarkus datasources, inject them with @DataSource, pick db-kind, and activate or deactivate datasources at runtime."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/datasource.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus datasources: default, named and runtime-active

## Single JDBC datasource
Add the JDBC extension for your database (`quarkus-jdbc-postgresql`, `-mysql`, `-mariadb`, `-mssql`, `-oracle`, `-db2`, `-h2`), then:

```properties
quarkus.datasource.username=<your username>
quarkus.datasource.password=<your password>
quarkus.datasource.jdbc.url=jdbc:postgresql://localhost:5432/hibernate_orm_test
quarkus.datasource.jdbc.max-size=16
```

JDBC-specific properties use the `jdbc` prefix; reactive ones use `reactive`. If several driver extensions are on the classpath, set `quarkus.datasource.db-kind` (values: `db2`, `h2`, `mariadb`, `mssql`, `mysql`, `oracle`, `postgresql`/`pgsql`/`pg`) or the build may fail. Tip: prefix prod-only connection details with `%prod.` so dev mode uses Dev Services.

## Named datasources
Key syntax: `quarkus.datasource.[optional name.][property]`.

```properties
quarkus.datasource.db-kind=h2
quarkus.datasource.users.db-kind=h2
quarkus.datasource.users.jdbc.max-size=11
quarkus.datasource.inventory.db-kind=h2
```

A named datasource must set at least one build-time property (usually `db-kind`) so Quarkus detects it, unless an extension such as Hibernate ORM, Flyway or Liquibase requests it. Inject with the `io.quarkus.agroal.DataSource` qualifier:

```java
@Inject AgroalDataSource defaultDataSource;
@Inject @DataSource("users") AgroalDataSource usersDataSource;
```

`AgroalDataSource` is a `javax.sql.DataSource` subtype, so either type works.

## Activate or deactivate at runtime
A datasource is active when configured at build time and its URL is set at runtime. Deactivate it by leaving `jdbc.url`/`reactive.url` unset or setting `quarkus.datasource."name".active=false`. An inactive datasource does not connect, adds no health check, and static injection points (`@Inject DataSource ds`) fail startup; dynamic lookup throws. Extensions consuming it (e.g. Hibernate ORM) must be deactivated too.

```properties
quarkus.datasource."pg".db-kind=postgres
quarkus.datasource."pg".active=false
%pg.quarkus.datasource."pg".active=true
```

Run with `quarkus.profile=prod,pg` to select it. To touch only the active one, inject `InjectableInstance<DataSource>` with `@Any` and call `getActive()`, or write a `@Produces @ApplicationScoped DataSource` that checks `getHandle().getBean().isActive()` on the `@DataSource("pg")`/`@DataSource("oracle")` instances. Never inject an inactive `DataSource` directly.

## Also
- Disable one side when both JDBC and reactive extensions exist: `quarkus.datasource.jdbc=false` or `quarkus.datasource.reactive=false`.
- Health check: `quarkus.datasource."name".health-exclude=true` or `quarkus.datasource.health.enabled=false`.

## Checked

2026-11-07. Read in full: datasource.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
