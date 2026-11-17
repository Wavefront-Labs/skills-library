---
id: computing-software.software-engineering.quarkus.quarkus-panache-active-record
name: quarkus-panache-active-record
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, panache, hibernate-orm, active-record, jpa, entity]
level: intro
status: docs-checked
description: "Define a Quarkus Hibernate ORM with Panache entity using the active record pattern: PanacheEntity, public fields, static finders and the common persist/find/delete calls."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/hibernate-orm-panache.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus Panache active record entities

## Setup
Add the `io.quarkus:quarkus-hibernate-orm-panache` extension plus a JDBC driver extension (for example `quarkus-jdbc-postgresql`). Configure the datasource in `application.properties`, e.g. `quarkus.datasource.db-kind`, and (for production experiments) `%prod.quarkus.hibernate-orm.schema-management.strategy=create`.

## Define the entity
Annotate with `@Entity`, extend `io.quarkus.hibernate.orm.panache.PanacheEntity` (gives an auto-generated `id`), and declare columns as public fields:

```java
@Entity
public class Person extends PanacheEntity {
    public String name;
    public LocalDate birth;
    public Status status;

    public static Person findByName(String name){
        return find("name", name).firstResult();
    }
    public static List<Person> findAlive(){
        return list("status", Status.Alive);
    }
}
```

- Jakarta Persistence column annotations go on the public fields; use `@Transient` for a field that must not be persisted.
- You may write your own getters/setters: Panache rewrites field access (`person.name`) into calls to them, so encapsulation still works at runtime.
- Put custom queries as static methods in the entity so they sit with the object they operate on.

## Common operations
Instance: `person.persist()`, `person.isPersistent()`, `person.delete()`. Once persisted, changes are saved automatically at transaction commit; no explicit save.

Static: `Person.listAll()`, `findById(id)`, `findByIds(List)`, `findByIdOptional(id)`, `list("status", Status.Alive)`, `count()`, `count("status", Status.Alive)`, `delete("status", Status.Alive)`, `deleteAll()`, `deleteById(id)`, `update("name = 'Mortal' where status = ?1", Status.Alive)`.

Every `list` method has a `stream` equivalent (`Person.streamAll()`). Stream methods require a transaction and should be closed (try-with-resources) so the underlying `ResultSet` is released; otherwise Agroal warns and closes it for you.

## Gotchas
- Wrap methods that modify the database in `@Transactional` (ideally at REST endpoint boundaries).
- `list()` takes HQL fragments, not full queries; the rest is filled in for you.
- Entities in external jars need an empty `META-INF/beans.xml` in that jar so Quarkus can enhance them.
- To use your own ID strategy, extend `PanacheEntityBase` and declare the `@Id` field yourself.

## Checked

2026-11-07. Matched against the text (with includes) of: hibernate-orm-panache.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
