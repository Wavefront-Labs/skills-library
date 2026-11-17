---
id: computing-software.software-engineering.haskell.async-and-structured-concurrency
name: async-and-structured-concurrency
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, async, concurrently, race, mapconcurrently, withasync, wait, cancel, timeout, structured-concurrency, async-and-structured-concurrency]
level: practitioner
status: docs-checked
description: "Run tasks concurrently with async: async/wait, concurrently, race, mapConcurrently, withAsync, cancellation, timeouts and exception propagation."
sources: ["https://hackage.haskell.org/package/base", "https://hackage.haskell.org/package//stm", "https://hackage.haskell.org/package//async"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# async

**Goal:** manage concurrent tasks with correct cancellation. Package: `async`.

```haskell
import Control.Concurrent.Async
import System.Timeout (timeout)

main = do
  (a, b) <- concurrently fetchA fetchB          -- both run, both results; exception cancels the other
  r <- race slow fast                            -- Either: first to finish wins, loser cancelled
  rs <- mapConcurrently fetch urls               -- parallel traverse
  mapConcurrently_ process items
  withAsync longJob $ \h -> do                   -- h cancelled when the block exits
    other
    wait h                                       -- rethrows the child's exception
  x <- async job; waitCatch x; cancel x; poll x
  t <- timeout 2000000 (wait x)                  -- Maybe result
  replicateConcurrently_ 4 worker
  forConcurrently xs f                            -- flipped mapConcurrently
```
Bound the number of concurrent actions yourself, for example with a bounded `TBQueue` from `stm`.

## Rules
- Prefer `withAsync` and `concurrently` over bare `async` + manual `cancel`: they clean up on exceptions.
- `wait` rethrows the child's exception in the waiting thread.
- `mapConcurrently` performs all the IO actions concurrently; if any throws, the others are cancelled.
- `link` re-throws a child's exception in the current thread, wrapped in `ExceptionInLinkedThread`.

## Gotchas
- Compile with `-threaded` and run with `-N` for real parallelism; concurrency works without.
- Async exceptions (`cancel`) can land anywhere; use `bracket`/`mask` for cleanup.
- Shared state still needs `MVar`/`STM`.

## Self-check
- [ ] No leaked threads after exceptions (check with a test that cancels a running group).
- [ ] Parallel width bounded for network calls.

## Checked

2026-11-03. Confirmed against the async Control.Concurrent.Async page: concurrently, race, mapConcurrently, withAsync, poll, link semantics. Removed: pooledMapConcurrently and thread-per-element claims.
Method: documentation only; no commands were run.
