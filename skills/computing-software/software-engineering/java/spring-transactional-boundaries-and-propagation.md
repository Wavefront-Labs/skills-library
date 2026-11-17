---
id: computing-software.software-engineering.java.spring-transactional-boundaries-and-propagation
name: spring-transactional-boundaries-and-propagation
category: computing-software
field: software-engineering
product: java
tags: [java, spring-boot, transactional, spring-transactions, propagation, isolation, self-invocation]
level: practitioner
status: docs-checked
description: "Place @Transactional correctly: proxy self-invocation, propagation and isolation, rollback rules for checked exceptions, read-only transactions and outbox after-commit work."
sources:
  - https://github.com/spring-projects/spring-framework/blob/main/framework-docs/modules/ROOT/pages/data-access/transaction/declarative/annotations.adoc
  - https://github.com/spring-projects/spring-framework/blob/main/framework-docs/modules/ROOT/pages/data-access/transaction/declarative/rolling-back.adoc
  - https://github.com/spring-projects/spring-framework/blob/main/framework-docs/modules/ROOT/pages/data-access/transaction/declarative/tx-propagation.adoc
  - https://github.com/spring-projects/spring-framework/blob/main/framework-docs/modules/ROOT/pages/data-access/transaction/event.adoc
  - https://github.com/spring-projects/spring-framework/blob/main/framework-docs/modules/ROOT/pages/data-access/transaction/declarative/first-example.adoc
  - https://github.com/spring-projects/spring-framework/blob/main/spring-tx/src/main/java/org/springframework/transaction/annotation/Propagation.java
  - https://github.com/spring-projects/spring-framework/blob/main/spring-tx/src/main/java/org/springframework/transaction/annotation/Transactional.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spring @Transactional boundaries and propagation

**Goal:** each business operation commits or rolls back as a unit, and the annotation actually applies.

## 1. Where it goes
- On **public service methods** that represent a use case, not on repositories (already transactional) or controllers.
- Keep transactions short: no remote HTTP calls, sleeps or user input inside; they hold DB connections and locks.

## 2. Proxy pitfalls
```java
@Service
class OrderService {
    public void placeAll(List<Cmd> cmds) { cmds.forEach(this::place); }   // self-call: NO transaction
    @Transactional public void place(Cmd c) { ... }
}
```
Spring applies `@Transactional` via a proxy; calls within the same object bypass it. Move the method to another bean, or annotate the outer method. `@Transactional` is typically used on public methods; since Spring 6.0 protected and package-visible methods can also be transactional with class-based proxies, and private methods are never proxied. It has no effect on objects not managed by Spring.

## 3. Rollback rules
Default: roll back on `RuntimeException` and `Error`, **commit** on checked exceptions.
```java
@Transactional(rollbackFor = Exception.class)
```
Catching an exception inside a transactional method and swallowing it commits whatever ran. An inner `REQUIRED` method that throws marks the shared transaction rollback-only; the outer commit then fails with `UnexpectedRollbackException`.

## 4. Propagation
| Propagation | Behaviour | Use |
|---|---|---|
| REQUIRED (default) | join or create | almost everything |
| REQUIRES_NEW | suspend outer, new transaction (new connection) | audit log that must persist even if outer rolls back |
| NESTED | savepoint inside outer (JDBC only) | partial retry within a batch |
| MANDATORY | must already exist | guard internal methods |
| NOT_SUPPORTED / NEVER | run without | long reads, reporting |
`REQUIRES_NEW` always uses an independent physical transaction: the inner one commits or rolls back on its own and releases its locks immediately, while the outer transaction stays open.

## 5. Isolation and read-only
`@Transactional(isolation = Isolation.REPEATABLE_READ)`; `Isolation.DEFAULT` uses the default of the underlying datastore. `readOnly = true` is a hint to the transaction subsystem (a manager that cannot interpret it ignores it) and only applies to `REQUIRED` and `REQUIRES_NEW`.

## 6. Work after commit
Publishing messages or sending emails inside the transaction risks sending for a rolled-back change:
```java
@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
void on(OrderPlaced e) { broker.send(e); }
```
The default phase is `AFTER_COMMIT` (others: `BEFORE_COMMIT`, `AFTER_ROLLBACK`, `AFTER_COMPLETION`); without an active transaction the listener is not invoked unless `fallbackExecution = true`. For guaranteed delivery write an outbox row in the same transaction and relay it.

## Gotchas
- `@Transactional` on test methods rolls back after each test, hiding commit-time failures (constraint deferral, after-commit listeners). Have some tests without it.
- Reactive transactional methods use reactive return types and a reactive transaction manager; thread-bound transactions do not cross threads (`@Async`, `CompletableFuture`).
- Optimistic locking failures surface at flush/commit, outside your try/catch in the method; retry at the caller.

## Verify
- Raise logging for `org.springframework.transaction.interceptor` and confirm the `TransactionInterceptor` "Getting transaction for ..." line appears for `OrderService.place`; an integration test asserts rollback when a checked exception is thrown with `rollbackFor`.

## Checked

Date: 2026-10-25. Documentation release: Spring Framework 7.0.10 (GitHub main documentation and source; release of 2026-10-22).

Confirmed: default rollback on `RuntimeException` and `Error` only, with `rollbackFor` rules for checked exceptions; self-invocation does not trigger a transaction in proxy mode; method visibility rules since 6.0; inner rollback-only marker leads to `UnexpectedRollbackException`; `REQUIRES_NEW` semantics; `NESTED` is supported out of the box only for JDBC; `Isolation.DEFAULT`; `readOnly` is a hint; `@TransactionalEventListener` phases, default `AFTER_COMMIT` and `fallbackExecution`; the `TransactionInterceptor` "Getting transaction for" log line; `@Transactional @Async` behaviour note.

Removed as unconfirmed: the Postgres READ COMMITTED claim, the routing-datasource and Hibernate dirty-checking claims for `readOnly`, the connection-pool exhaustion claim and the explicit TRACE level for the log line.

Method: documentation only; no commands were run.
