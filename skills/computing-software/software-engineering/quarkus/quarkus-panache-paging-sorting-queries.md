---
id: computing-software.software-engineering.quarkus.quarkus-panache-paging-sorting-queries
name: quarkus-panache-paging-sorting-queries
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, panache, hibernate-orm, paging, sorting, named-queries, hql]
level: practitioner
status: docs-checked
description: "Page, range, sort and parameterise Panache queries in Quarkus: PanacheQuery, Page, Sort, simplified HQL forms, named queries and index/name parameters."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/hibernate-orm-panache.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Panache paging, sorting and query forms

## Paging
`list` and `stream` suit small tables only. For larger sets use `find`, which returns a `PanacheQuery`:

```java
PanacheQuery<Person> living = Person.find("status", Status.Alive);
living.page(Page.ofSize(25));
List<Person> first  = living.list();
List<Person> second = living.nextPage().list();
List<Person> page7  = living.page(Page.of(7, 25)).list();
int pages = living.pageCount();
long total = living.count();
```

Ranges: `living.range(0, 24)` (inclusive end), then `range(25, 49)` for the next one. You cannot mix ranges and pages: with a range, methods needing a current page throw `UnsupportedOperationException`; switch back with `page(Page)` or `page(int, int)`.

## Sorting
Simplified string: `Person.list("order by name,birth")`. Or pass a `Sort`:

```java
Person.list(Sort.by("name").and("birth"));
Person.list("status", Sort.by("name").and("birth"), Status.Alive);
Person.list(Sort.by("birth", Sort.NullPrecedence.NULLS_FIRST));
```

Panache escapes column names in `Sort` to prevent HQL injection. For HQL functions such as `lower()` call `Sort.by("lower(name)").disableEscaping()`.

## Simplified query forms
If a select query does not start with `from`, `select` or `with`: `order by ...` expands to `from Entity order by ...`; a single attribute with one parameter expands to `where attr = ?`; `where <q>` and `<q>` expand to `from Entity where <q>`. Update queries may omit `update` (`set? <attr>`), and delete queries may omit `delete` (`from Entity ...`, single attribute, or `<query>`). Plain HQL still works, e.g. `Order.find("select distinct o from Order o left join fetch o.lineItems")`.

## Parameters
By 1-based index: `Person.find("name = ?1 and status = ?2", "stef", Status.Alive)`. By name with a `Map`: `Person.find("name = :name and status = :status", Map.of("name","stef","status",Status.Alive))`. All query operations accept `Object...` or `Map<String,Object>`.

## Named queries
Prefix the name with `#`: `find("#Person.getByName", name)`; also valid for `count`, `update` and `delete`. Define them with `@NamedQueries`/`@NamedQuery` on the entity (or a superclass). Named queries can only be defined inside Jakarta Persistence entity classes or their super classes.

## Checked

2026-11-07. Matched against the text (with includes) of: hibernate-orm-panache.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
