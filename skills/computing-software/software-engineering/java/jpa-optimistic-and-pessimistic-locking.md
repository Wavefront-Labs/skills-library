---
id: computing-software.software-engineering.java.jpa-optimistic-and-pessimistic-locking
name: jpa-optimistic-and-pessimistic-locking
category: computing-software
field: software-engineering
product: java
tags: [java, spring-data, jpa-locking, optimistic-locking, version-field, pessimistic-write, select-for-update, lock-timeout]
level: advanced
status: draft
description: "Prevent lost updates in JPA/Hibernate with @Version optimistic locking, retry on OptimisticLockException, and PESSIMISTIC_WRITE with lock timeouts and SKIP LOCKED queues."
sources: ["https://jakarta.ee/specifications/persistence/3.1/jakarta-persistence-spec-3.1#locking-and-concurrency", "https://docs.spring.io/spring-data/jpa/reference/jpa/locking.html", "https://docs.jboss.org/hibernate/orm/6.4/userguide/html_single/Hibernate_User_Guide.html#locking"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JPA locking

## Optimistic (default choice)
```java
@Entity class Account {
    @Id Long id;
    @Version long version;          // incremented on every update; UPDATE ... WHERE id=? AND version=?
    BigDecimal balance;
}
```
On conflict the second writer's update affects 0 rows and Hibernate throws `OptimisticLockException` (Spring translates to `ObjectOptimisticLockingFailureException`). Handle by **retrying the whole transaction** (reload, reapply) or returning HTTP 409 with the current state. Spring: `@Retryable(retryFor = ObjectOptimisticLockingFailureException.class, maxAttempts = 3)` on a method outside the `@Transactional` boundary.
Expose the version in your API (ETag/`If-Match`) so clients detect stale edits across requests. Use `LockModeType.OPTIMISTIC_FORCE_INCREMENT` to bump a parent's version when only children change.

## Pessimistic
```java
public interface AccountRepo extends JpaRepository<Account, Long> {
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @QueryHints(@QueryHint(name = "jakarta.persistence.lock.timeout", value = "3000"))
    @Query("select a from Account a where a.id = :id")
    Optional<Account> lockById(Long id);
}
```
Generates `SELECT ... FOR UPDATE`. Use for short critical sections with high contention (inventory decrement, sequence allocation) and within a transaction. `PESSIMISTIC_READ` maps to `FOR SHARE`/`FOR UPDATE` depending on the DB.

## Work queues
`FOR UPDATE SKIP LOCKED` lets many workers claim distinct rows: lock timeout hint `-2` (`LockOptions.SKIP_LOCKED`) with Hibernate, or a native query.

## Gotchas
- A lock is held until the transaction ends; do not call remote services while holding it. Keep lock order consistent to avoid deadlocks; detect `PessimisticLockException`/`LockTimeoutException`/deadlock victim and retry.
- `@Version` on a detached entity merge compares the supplied version: DTO-to-entity copies must carry it.
- Bulk `@Modifying` queries bypass `@Version` unless you update it yourself (`set version = version + 1`).
- Isolation `READ COMMITTED` plus `@Version` is usually enough; `SERIALIZABLE` needs retry logic anyway.
- Lock timeouts are DB-dependent (MySQL/PostgreSQL honor it differently; PostgreSQL uses `lock_timeout` session setting).

## Verify
Two-thread integration test: both load the same row, both update; assert one fails with the optimistic exception and the final value equals exactly one update.
