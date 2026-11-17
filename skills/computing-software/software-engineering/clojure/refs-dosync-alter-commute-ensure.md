---
id: computing-software.software-engineering.clojure.refs-dosync-alter-commute-ensure
name: refs-dosync-alter-commute-ensure
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, refs, stm, dosync, alter, commute, ref-set, ensure, transactions, coordinated-state, refs-stm-dosync]
level: advanced
status: docs-checked
description: "Coordinate multiple pieces of state in transactions with ref, dosync, alter, commute and ensure; understand retries, write skew and why side effects belong outside."
sources: ["https://clojure.org/reference/refs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Refs and software transactional memory

**Goal:** update several values atomically and consistently.

```clojure
(def a (ref 100)) (def b (ref 0))
(dosync
  (alter a - 10)
  (alter b + 10))                    ; both change or neither does
(dosync (commute counter inc))       ; commutative ops: less contention, may re-run at commit
(dosync (ref-set a 0))
(dosync (ensure a) ...)              ; protect a read from concurrent writes (write skew)
```
- All ref changes must occur inside `dosync`; outside a transaction they throw an IllegalStateException.
- Transactions may retry: do not perform I/O or use non-idempotent effects inside (see `io!` for guarding impure code).
- `alter` for order-dependent updates, `commute` for commutative ones such as increments.
- Reads see a consistent snapshot of the transaction start (MVCC); `ensure` guards read-only dependencies.
- Refs are rarely needed; prefer one atom containing a map unless you really need cross-reference consistency.

## Failure modes
- Many conflicting writers cause repeated retries.
- Long transactions starve; keep them short.

## Self-check
Transfer between two accounts from many futures and verify total balance is conserved.

## Checked
2026-11-02. Confirmed: clojure.org/reference/refs: dosync, alter, commute, ref-set, ensure, consistent snapshot (MVCC, snapshot isolation), transactions may retry, avoid I/O and side effects, io!. Removed: the agent-send hold claim and exact exception texts.
Method: documentation only; no commands were run.
