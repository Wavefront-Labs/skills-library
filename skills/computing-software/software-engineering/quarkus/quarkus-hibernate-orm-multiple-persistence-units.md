---
id: computing-software.software-engineering.quarkus.quarkus-hibernate-orm-multiple-persistence-units
name: quarkus-hibernate-orm-multiple-persistence-units
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, hibernate-orm, persistence-unit, datasource, cdi, multi-database]
level: practitioner
status: docs-checked
description: "Configure multiple Hibernate ORM persistence units in Quarkus: named datasources, packages vs @PersistenceUnit, precedence, CDI injection and runtime activation."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/hibernate-orm.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple persistence units in Quarkus Hibernate ORM

## Declare units
Properties directly under `quarkus.hibernate-orm.` configure the default unit. Named units use a quoted map key, and `datasource` is mandatory for them (use `<default>` to point at the default datasource):

```properties
quarkus.hibernate-orm."users".datasource=users
quarkus.hibernate-orm."users".packages=org.acme.model.user
quarkus.hibernate-orm."inventory".datasource=inventory
quarkus.hibernate-orm."inventory".packages=org.acme.model.inventory
```

Several units may share one datasource. Datasources are defined as `quarkus.datasource."users".jdbc.url` etc.

## Attach entities (three ways)
1. `packages` config property (subpackages included; a comma-separated list is allowed).
2. Package-level `@io.quarkus.hibernate.orm.PersistenceUnit("users")` in `package-info.java`.
3. Class-level `@PersistenceUnit`; repeat it to attach one class to several units.

Use the Quarkus annotation, not the Jakarta Persistence one. If `packages` is set for at least one unit, all `@PersistenceUnit` annotations are ignored. Package and class annotations can combine; the class one wins. With nothing set, entities go to the default unit if no package annotations exist anywhere. Dependent classes (mapped superclasses, embeddables) must be attached consistently.

Panache entities can be attached to only one persistence unit.

## Injection
```java
@Inject @PersistenceUnit("users") Session session;
@Inject @PersistenceUnit("users") EntityManager em;
@Inject @PersistenceUnit("users") SessionFactory sf;
```
Without the qualifier you get the default unit. The injected `Session` needs a transaction (read-only use in a request scope is allowed unless `quarkus.hibernate-orm.request-scoped.enabled=false`).

## Activate/deactivate at runtime
Set `quarkus.hibernate-orm."pg".active=false` (and the datasource's `active=false`), then enable one at runtime. An inactive unit's static injection points fail startup, so inject `InjectableInstance<Session>` with `@Any` and call `getActive()`, or write a producer that checks `getHandle().getBean().isActive()`. Custom profiles (`%pg.`, `%oracle.`) can flip the flags via `quarkus.profile=prod,pg`.

## Gotchas
- Do not mix `persistence.xml` with `quarkus.hibernate-orm.*` properties; Quarkus raises an exception.
- With multiple units, the default `schema.sql`/`data.sql` are picked up by each unit. If units map different entities, preferably do not include SQL files with the default names, or set `quarkus.hibernate-orm."<name>".data-management.init-script` and `quarkus.hibernate-orm."<name>".schema-management.init-script` per unit (to `no-file` where none applies).

## Checked

2026-11-07. Read in full: hibernate-orm.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: the stale `import.sql` default; the page now documents `schema.sql`/`data.sql` with per-unit `init-script` properties and `no-file`.

Method: documentation only; no commands were run.
