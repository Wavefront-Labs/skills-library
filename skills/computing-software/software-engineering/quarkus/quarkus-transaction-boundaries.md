---
id: computing-software.software-engineering.quarkus.quarkus-transaction-boundaries
name: quarkus-transaction-boundaries
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, transactions, jta, narayana, transactional, quarkustransaction, rollback]
level: practitioner
status: docs-checked
description: "Define Quarkus transaction boundaries with @Transactional, QuarkusTransaction or UserTransaction, including propagation modes, rollback rules and timeouts."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/transaction.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus transaction boundaries

The `quarkus-narayana-jta` extension provides the transaction manager (Jakarta Transactions). Hibernate ORM pulls it in automatically; add `io.quarkus:quarkus-narayana-jta` yourself when using transactions without it. Distributed transaction models (JTS, REST-AT, WS-Atomic Transaction) are not supported.

## Declarative: `@Transactional`
Use `jakarta.transaction.Transactional` on a method or class of any CDI bean (including REST endpoints).

- `REQUIRED` (default): start one if none, otherwise join.
- `REQUIRES_NEW`: suspend any existing transaction and start a new one for the method.
- `MANDATORY`: fail if none exists.
- `SUPPORTS`: join if present, otherwise run without.
- `NOT_SUPPORTED`: suspend any existing one and run without.
- `NEVER`: raise an exception if one exists.

A `RuntimeException` crossing the boundary rolls back; override with `rollbackOn` / `dontRollbackOn`. To mark rollback programmatically, inject `TransactionManager` and call `setRollbackOnly()`.

`@TransactionConfiguration(timeout = ...)` (seconds) is added alongside `@Transactional`; put it only on the top-level method that starts the transaction (a nested use throws), and method-level beats class-level.

If the method returns a `CompletionStage` or `Publisher` (or a type convertible to them), the transaction ends only when the returned reactive value terminates; exceptional termination marks rollback.

## Programmatic: `QuarkusTransaction`
```java
QuarkusTransaction.begin();
// work
QuarkusTransaction.commit();

QuarkusTransaction.requiringNew().timeout(10)
    .exceptionHandler(t -> t instanceof SomeException
        ? TransactionExceptionResult.COMMIT : TransactionExceptionResult.ROLLBACK)
    .call(() -> 0);
```
`begin()` ties the transaction to the CDI request scope: an active one is rolled back when the scope is destroyed, so it needs an active request scope. Semantics: `disallowingExisting()` (throws `QuarkusTransactionException` if one exists), `joiningExisting()`, `requiringNew()`, `suspendingExisting()` (runs outside any transaction; never consults an exception handler, and specifying one is an error).

## Lower-level: `UserTransaction`
The JTA API, less user-friendly than `QuarkusTransaction`. Inject it and call `begin()`/`commit()`/`rollback()` yourself. It cannot be used in a method whose transaction was started by `@Transactional`.

## Timeout
Default timeout is 60 seconds; change with `quarkus.transaction-manager.default-transaction-timeout` (a duration).

## Tip
For read-only work you can opt out with `@Transactional(NOT_SUPPORTED)` (or `NEVER`/`SUPPORTS`); several SELECTs in one transaction are consistent with each other.

## Checked

2026-11-07. Matched against the text (with includes) of: transaction.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: the label `Legacy` for `UserTransaction`; the page only calls it less user-friendly than `QuarkusTransaction`.

Method: documentation only; no commands were run.
