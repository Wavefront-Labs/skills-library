---
id: computing-software.software-engineering.java.spring-data-jpa-repositories-and-n-plus-one
name: spring-data-jpa-repositories-and-n-plus-one
category: computing-software
field: software-engineering
product: java
tags: [java, spring-boot, spring-data-jpa, jpa, hibernate, n-plus-one, entity-graph, projections]
level: practitioner
status: docs-checked
description: "Use Spring Data JPA without performance traps: repository queries, fetch strategies, detecting and fixing N+1 with fetch joins and entity graphs, projections and paging."
sources:
  - https://docs.spring.io/spring-data/jpa/reference/jpa.html
  - https://docs.spring.io/spring-data/jpa/reference/jpa/query-methods.html
  - https://docs.spring.io/spring-data/jpa/reference/jpa/entity-persistence.html
  - https://docs.spring.io/spring-data/jpa/reference/jpa/transactions.html
  - https://docs.spring.io/spring-data/jpa/reference/repositories/projections.html
  - https://docs.spring.io/spring-boot/appendix/application-properties/index.html
  - https://docs.jboss.org/hibernate/orm/6.6/userguide/html_single/Hibernate_User_Guide.html#fetching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spring Data JPA repositories and N+1 queries

**Goal:** repositories that issue a predictable, small number of SQL statements per request.

## 1. Repositories
```java
public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByCustomerIdAndStatusOrderByCreatedAtDesc(long customerId, Status status);

    @Query("select o from Order o join fetch o.lines where o.id = :id")
    Optional<Order> findWithLines(@Param("id") long id);

    @EntityGraph(attributePaths = {"customer", "lines"})
    Page<Order> findByStatus(Status status, Pageable pageable);
}
```
Derived query names are fine for 1-2 conditions; beyond that use `@Query` or Specifications/Querydsl.

## 2. Fetching defaults
- JPA defines collection associations (`@OneToMany`, `@ManyToMany`) as LAZY: keep it.
- Set `fetch = FetchType.LAZY` explicitly on `@ManyToOne`/`@OneToOne`.
- Fetch per use case (fetch join, entity graph), not by changing mappings globally.

## 3. N+1: detect
Loading 50 orders then touching `order.getCustomer().getName()` in a loop = 1 + 50 queries. Turn on SQL logging in development and count statements per request; in tests assert the statement count for the endpoint.

## 4. N+1: fix
- `join fetch` / `@EntityGraph` for the specific query.
- `hibernate.default_batch_fetch_size` sets the default batch size for batch fetching; by default Hibernate batch-fetches only associations annotated `@BatchSize`.
- Fetching several collections in one query produces a Cartesian product at the database level; fetch the second collection in a separate query.
- Fetch joins combined with paging or limits make Hibernate apply the limit in memory. Avoid it: page the root IDs first, then fetch by IDs.

## 5. Projections for reads
```java
public interface OrderSummary { Long getId(); String getCustomerName(); BigDecimal getTotal(); }
List<OrderSummary> findByStatus(Status status);
record OrderRow(long id, String customer) {}
@Query("select new com.acme.OrderRow(o.id, o.customer.name) from Order o")
```
Class and record projections through `@Query` need a constructor expression with the fully qualified DTO name. Methods inherited from `CrudRepository` run read-only transactions by default; mark your own read-only service methods `@Transactional(readOnly = true)`.

## Gotchas
- `spring.jpa.open-in-view` defaults to `true` (it binds an `EntityManager` to the thread for the whole request), so lazy loads happen in the view layer and hide N+1. Set it to `false` and fetch explicitly.
- Return DTOs from endpoints, not entities, so serialisation does not trigger lazy loads.
- If an entity implements `Persistable`, Spring Data uses its `isNew()` to choose `persist()` or `merge()` to decide whether `save()` calls `persist()` or `merge()`.
- `findAll()` without paging on a large table loads everything into memory.

## Verify
- An integration test asserts the SQL count for the list endpoint stays constant as rows grow from 10 to 100.

## Checked
2026-11-01. Confirmed in the Spring Data JPA reference (query methods: `@EntityGraph` `attributePaths`;
entity persistence: `Persistable.isNew()`; transactions: read-only default for inherited read methods;
projections: interface, record and constructor-expression DTOs), the Spring Boot property appendix
(`spring.jpa.open-in-view` default true) and the Hibernate 6.6 guide (collections LAZY by JPA,
`default_batch_fetch_size`, Cartesian product from several collection fetch joins, limits applied in memory
with fetch joins). Removed unconfirmed claims: `@ManyToOne` EAGER default, `@Modifying` example, the
statistics and logging property names, the statement-count library names, `MultipleBagFetchException`, the
`HHH90003004` code, the N/50 IN-query formula and the dirty-checking claim.
Method: documentation only; no commands were run.
