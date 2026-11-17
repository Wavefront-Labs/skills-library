---
id: computing-software.software-engineering.haskell.forkio-and-mvar
name: forkio-and-mvar
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, forkio, mvar, threaddelay, killthread, green-threads, threaded-rts, forkfinally, chan, forkio-and-mvar, haskell-concurrency]
level: practitioner
status: docs-checked
description: "Create lightweight threads with forkIO, coordinate with MVar and Chan, compile with -threaded and +RTS -N, and handle thread exceptions."
sources: ["https://hackage.haskell.org/package/base", "https://hackage.haskell.org/package//stm", "https://hackage.haskell.org/package//async"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Threads and MVar

**Goal:** run concurrent IO tasks and synchronise them. Module: `Control.Concurrent`.

```haskell
import Control.Concurrent
import Control.Exception

main = do
  done <- newEmptyMVar
  tid <- forkIO $ (work >>= putMVar done) `catch` \e -> putMVar done (Left (e :: SomeException))
  r <- takeMVar done                         -- blocks until filled
  lock <- newMVar ()
  withMVar lock $ \_ -> putStrLn "exclusive"  -- mutex
  killThread tid
  threadDelay 1000000                        -- microseconds
  ch <- newChan; writeChan ch 1; readChan ch
  _ <- forkFinally work (\_ -> putMVar done ())
```

## Facts
- `forkIO` makes a lightweight, unbound thread scheduled by the RTS. `forkOS` creates a bound thread, needed for foreign libraries that use thread-local state.
- Multiple OS threads need the `-threaded` option when linking; the number of capabilities is set with `+RTS -N`. Without `-threaded` the runtime does not use multiple OS threads and foreign calls block all other Haskell threads.
- `MVar` is a one-slot box: `takeMVar` blocks on empty, `putMVar` on full. Blocked threads are served first-in-first-out in GHC (not guaranteed by the semantics).

## Gotchas
- GHC detects deadlocks using the garbage collector and sends the thread `BlockedIndefinitelyOnMVar` (or a related exception).
- A `forkIO` thread's handler discards `BlockedIndefinitelyOnMVar`, `BlockedIndefinitelyOnSTM` and `ThreadKilled`, and passes all other exceptions to the uncaught exception handler.
- `timeout` from `System.Timeout` takes microseconds and returns `Nothing` if no result arrives in time.

## Self-check
- [ ] Program waits for the threads it needs (for example on an `MVar`) before `main` ends.
- [ ] Linked with `-threaded` and run with `+RTS -N` when parallelism is wanted.

## Checked

2026-11-03. Confirmed against base Control.Concurrent, Control.Concurrent.MVar and System.Timeout pages: forkIO/forkOS semantics, -threaded and +RTS -N, MVar FIFO fairness, deadlock detection, forkIO exception handler, timeout units. Removed: -rtsopts, -with-rtsopts, thread-count, output-interleaving and threadDelay precision claims. Fixed the child-thread exception claim.
Method: documentation only; no commands were run.
