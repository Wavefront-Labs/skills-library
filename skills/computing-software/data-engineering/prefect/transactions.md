---
id: computing-software.data-engineering.prefect.transactions
name: transactions
category: computing-software
field: data-engineering
product: prefect
tags: [transactions, rollback, commit-mode, isolation-level, idempotency]
level: advanced
status: docs-checked
description: "Group Prefect tasks atomically with transaction, using key for idempotency, commit_mode, isolation_level, lock managers and on_commit and on_rollback hooks."
sources:
  - https://docs.prefect.io/v3/advanced/transactions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make multi-task work atomic and idempotent.

`transaction` from `prefect.transactions` is a context manager: `with transaction(): ...`. Every task run is governed by a transaction. Lifecycle: BEGIN, STAGE, ROLLBACK (error after staging), COMMIT.

`key` sets the record location; a committed record at the key means the work is already complete. `txn.is_committed()` is true only when the persisted record exists.

`commit_mode`:
- `LAZY`: defer to the parent; commit on successful exit if none (default without a parent).
- `EAGER`: commit on successful exit even with an active parent; a later outer failure cannot roll it back.
- `OFF`: no automatic commit; a parent or `txn.commit()` commits; without a parent it rolls back on exit.
- Omitted: inherits the parent's mode.

`isolation_level`: `READ_COMMITTED` (default; concurrent same-key transactions can overwrite each other) or `SERIALIZABLE` (locks the key; needs `store=ResultStore(lock_manager=...)`). Lock managers: `MemoryLockManager` (`prefect.locking.memory`, threads in one process), a filesystem lock manager in `prefect.locking.filesystem` (processes on one machine), `RedisLockManager` from `prefect-redis` (distributed).

Hooks, both receiving the transaction:
- `@task.on_rollback`: runs when the enclosing transaction fails after the task staged, even if another task failed; use it to clean external side effects, which Prefect does not undo.
- `@task.on_commit`: runs when the transaction commits.

Rollback propagates upward from child to parent; committed work cannot be rolled back. `txn.set("k", v)` and `txn.get("k")` pass data to `on_rollback`.

## Checked

2026-11-08. Lifecycle stages, key and is_committed behaviour, the three commit modes and inheritance, isolation levels, the lock manager table (the page's filesystem example uses FileSystemLockManager), the on_rollback and on_commit hooks, no rollback after commit, and txn.set and txn.get confirmed against the transactional workflows page.

Method: documentation only; no commands were run.
