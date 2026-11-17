---
id: computing-software.software-engineering.java.hibernate-batch-inserts-and-id-generation
name: hibernate-batch-inserts-and-id-generation
category: computing-software
field: software-engineering
product: java
tags: [java, spring-data, hibernate-batching, jdbc-batch-size, generationtype-sequence, identity-batching, order-inserts, persistence-context-clear]
level: advanced
status: docs-checked
description: "Batch Hibernate inserts: jdbc.batch_size, order_inserts, flush/clear loops, StatelessSession, and why IDENTITY ids disable batching."
sources: ["https://docs.jboss.org/hibernate/orm/6.4/userguide/html_single/Hibernate_User_Guide.html#batch", "https://docs.spring.io/spring-boot/reference/data/sql.html#data.sql.jpa-and-spring-data"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hibernate batch inserts and ID generation

## Settings
```yaml
spring.jpa.properties.hibernate:
  jdbc.batch_size: 50
  order_inserts: true
  order_updates: true
```
Spring Boot passes native Hibernate properties through `spring.jpa.properties.*` (the prefix is stripped). Hibernate documentation for these settings:
- `hibernate.jdbc.batch_size`: maximum statements batched before asking the driver to execute; zero or negative disables batching. JDBC batching is not enabled by default, so each insert costs a round trip; the guide suggests an integer between 10 and 50. It can also be overridden per session with `session.setJdbcBatchSize(n)` (since 5.2).
- `hibernate.order_inserts`: orders inserts so more can be batched.
- `hibernate.order_updates`: orders updates by entity type and primary key, allowing more batching and, per the guide, fewer deadlocks in highly concurrent systems. Both ordering settings carry a performance cost, so benchmark before and after.
- `hibernate.jdbc.batch_versioned_data`: defaults to true since 5.0; set false only if your driver returns wrong row counts for batches, because versioned-entity batching relies on those counts for optimistic lock checks.

## ID strategy
Hibernate transparently disables JDBC insert batching for entities using an IDENTITY generator, because each insert must run to obtain the key. The guide says the importance depends on how many new instances of that type you create. Sequence-based generation with an explicit allocation size ("increment by") avoids this; the pooled and pooled-lo optimizers rely on the database sequence being defined with an increment greater than 1 (for example `create sequence m_sequence start with 1 increment by 20`), so the mapping's allocation size must match the sequence definition.

## Loop pattern for big imports
Persisting 100,000 entities in one session is an anti-pattern: they all stay in the session-level cache (risking out-of-memory), a long transaction can deplete the connection pool, and without batching each insert is a round trip. Flush and clear regularly:
```java
int batchSize = 25;
for (int i = 0; i < entityCount; i++) {
    if (i > 0 && i % batchSize == 0) {
        entityManager.flush();
        entityManager.clear();
    }
    entityManager.persist(new Person(String.format("Person %d", i)));
}
```
- Read-heavy updates: flush and clear periodically, and use `scroll(ScrollMode.FORWARD_ONLY)` with `CacheMode.IGNORE` for server-side cursors; close the `ScrollableResults` explicitly.
- `StatelessSession` is an alternative with no persistence context: operations run synchronously, returned entities are detached, and `insert()`, `update()` and `delete()` act directly on rows. It comes with limitations listed in the guide.

## Verify
Insert a known number of rows in a test and count the batch executions with a datasource proxy or the JDBC driver's statement logging; confirm it is far fewer than the number of rows.

## Checked
Read the Hibernate 6.4 User Guide batching chapter (section 13 in full), the identifier-generation notes on IDENTITY and optimizers, and the Spring Boot SQL data page section on `spring.jpa.properties`. Removed as unconfirmed: driver URL flags for MySQL and PostgreSQL, the claim that the default allocation size is 50, UUID batching, PostgreSQL bigserial notes, statistics logger names, pg_stat_statements, cascade and second-level cache gotchas, and the claim that dirty checking is O(n).
Method: docs-checked 2026-11-09 against the Hibernate 6.4 User Guide batching and identifier generator sections and the Spring Boot SQL data page.
