---
id: computing-software.software-engineering.concurrency.software-transactional-memory
name: software-transactional-memory
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, software-transactional-memory, stm, clojure-refs, haskell-stm, optimistic-concurrency]
level: advanced
status: draft
description: "Use software transactional memory (Clojure refs, Haskell STM, ScalaSTM): composable atomic transactions, retry semantics, side-effect rules and limits."
sources: ["https://clojure.org/reference/refs", "https://hackage.haskell.org/package/stm/docs/Control-Concurrent-STM.html", "https://nbronson.github.io/scala-stm/", "https://www.microsoft.com/en-us/research/publication/composable-memory-transactions/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Software transactional memory

STM applies database-style transactions to in-memory data: a block of reads/writes to
transactional variables commits atomically and in isolation, or retries if another transaction
conflicted. No locks in user code, no lock-ordering deadlocks, and **transactions compose**.

## Haskell (the reference design: Harris, Marlow, Peyton Jones, Herlihy)
```haskell
transfer :: TVar Int -> TVar Int -> Int -> STM ()
transfer from to n = do
  bal <- readTVar from
  when (bal < n) retry              -- block until 'from' changes, then rerun
  modifyTVar' from (subtract n)
  modifyTVar' to (+ n)

main = atomically (transfer a b 10 `orElse` transfer c b 10)
```
- `retry` blocks the transaction until a TVar it read changes: composable condition waiting.
- `orElse` composes alternatives. The `STM` type prevents I/O inside transactions at compile time.

## Clojure
```clojure
(def a (ref 100)) (def b (ref 0))
(dosync (alter a - 10) (alter b + 10))     ; MVCC snapshot isolation, retries on conflict
```
`commute` for commutative updates (fewer retries), `ensure` to prevent write skew on reads,
`io!` marks code that must not run in a transaction. Atoms (CAS on one value) and agents cover
simpler cases; refs are for coordinated multi-value updates.

## Rules
- **No side effects inside transactions** (they may run many times): no I/O, logging, sending
  messages. Defer effects until after commit (Clojure agents dispatched in a transaction are held
  until commit).
- Keep transactions short; long transactions touching hot TVars livelock or starve.
- Only transactional variables are protected; mutable objects stored inside them aren't.

## Where it fits
Coordinated updates to a few shared in-memory structures with complex conditions (games, schedulers,
caches with invariants). Elsewhere: actors/CSP for isolation, locks for simple critical sections.
Hardware TM (Intel TSX) was disabled on most CPUs; mainstream languages (Java, C#, Go) never shipped
STM in the standard library, though libraries exist (ScalaSTM, Multiverse, ZIO STM, `stm` crates).
