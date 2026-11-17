---
id: computing-software.software-engineering.quarkus.quarkus-panache-query-projection
name: quarkus-panache-query-projection
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, panache, hibernate-orm, projection, dto, native]
level: advanced
status: docs-checked
description: "Project Panache queries into DTOs in Quarkus with project(Class): constructor rules, @ProjectedFieldName, @NestedProjectedClass, @ProjectedConstructor and native-image reflection."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/hibernate-orm-panache.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Panache query projection into DTOs

Call `project(Class)` on the `PanacheQuery` returned by `find()` to load only some fields. Hibernate generates a SELECT with the projection class's attributes (DTO projection / constructor expression).

```java
@RegisterForReflection
public class PersonName {
    public final String name;
    public PersonName(String name){ this.name = name; }
}
PanacheQuery<PersonName> q = Person.find("status", Status.Alive).project(PersonName.class);
```

## Rules
- The class needs a constructor taking all its attributes; it is used instead of the entity.
- `@RegisterForReflection` keeps the class in native compilation.
- The select clause is built from constructor parameter names, so the compiler must store parameter names: the Maven archetype enables it; otherwise add `<maven.compiler.parameters>true</maven.compiler.parameters>` to `pom.xml`.
- Records (Java 17+) are a good fit.

## Referenced entities and aggregates
`@ProjectedFieldName` (in `io.quarkus.hibernate.orm.panache.common`) gives the HQL path:

```java
public DogDto(String name, @ProjectedFieldName("owner.name") String ownerName) { ... }
```

It also accepts HQL expressions such as `@ProjectedFieldName("SUM(weight)")`, useful for GROUP BY, e.g. `Dog.find("FROM Dog d JOIN d.owner o GROUP BY o.name").project(DogWeightTotal.class)`.

## Nested classes
Annotate a nested class with `@NestedProjectedClass` to project an `@Embedded`, `@ManyToOne` or `@OneToOne`. It does not support `@OneToMany` or `@ManyToMany`.

## Explicit select clause
You can give HQL with a select clause, e.g. `Person.find("select d.race, AVG(d.weight) from Dog d group by d.race").project(RaceWeight.class)`; the class needs a constructor matching the selected values, and may then have several constructors. You cannot combine an HQL `select new` query with `.project(Class)`: it fails.

## Multiple constructors
Annotate the intended one with `@ProjectedConstructor`. Resolution order: (1) constructor with `@ProjectedConstructor`, (2) parameters annotated `@ProjectedFieldName`, (3) first non-parameterless constructor, (4) first constructor found. An unannotated multi-constructor DTO can behave unexpectedly.

## Checked

2026-11-07. Matched against the text (with includes) of: hibernate-orm-panache.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
