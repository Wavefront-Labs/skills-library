---
id: computing-software.software-engineering.haskell.stm-transactions
name: stm-transactions
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, stm, tvar, retry, orelse, atomically, tmvar, tqueue, tbqueue, transactional-memory, stm-transactions]
level: advanced
status: docs-checked
description: "Compose atomic operations with STM: TVar, atomically, retry, orElse, TMVar, TQueue/TBQueue, and exceptions inside transactions."
sources: ["https://hackage.haskell.org/package/base", "https://hackage.haskell.org/package//stm", "https://hackage.haskell.org/package//async"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STM

**Goal:** share state between threads without locks or deadlock-prone ordering. Package: `stm`.

```haskell
import Control.Concurrent.STM

transfer :: TVar Int -> TVar Int -> Int -> STM ()
transfer from to n = do
  b <- readTVar from
  when (b < n) retry                    -- block until a read TVar changes
  modifyTVar' from (subtract n)
  modifyTVar' to (+ n)

main = do
  a <- newTVarIO 100; b <- newTVarIO 0
  atomically (transfer a b 30)
  r <- atomically (readTVar a)
  q <- newTQueueIO; atomically (writeTQueue q "msg"); atomically (readTQueue q)
  atomically $ (Left <$> takeTMVar x) `orElse` (Right <$> takeTMVar y)   -- first that does not retry
  registerDelay 1000000                  -- TVar Bool set after a delay (for timeouts)
```

## Rules
- Compose `STM` actions and run them with `atomically`, which performs a series of STM actions atomically.
- `retry` abandons the transaction because it saw TVar values it cannot continue with; the implementation may block the thread until a TVar it read is updated. `orElse a b` runs `b` if `a` retries.
- `check b = if b then pure () else retry`.
- Types: `TVar`, `TMVar`, `TChan`, `TQueue`, `TBQueue` (bounded: `writeTBQueue` retries while the queue is full), `TArray`.
- `throwSTM` throws and `catchSTM` handles an exception inside a transaction; changes made by the failed action are rolled back.

## Gotchas
- `modifyTVar'` is the strict version of `modifyTVar`; prefer it for counters.

## Self-check
- [ ] Invariants hold under concurrent stress (run many threads in a test).
- [ ] No IO in STM; no thunk accumulation in TVars.

## Checked

2026-11-03. Confirmed against the stm Control.Monad.STM, TVar, TMVar, TQueue, TBQueue pages: retry, orElse, check, throwSTM/catchSTM rollback, registerDelay, modifyTVar', bounded queue. Removed: starvation, unsafeIOToSTM and bundling claims; rewrote retry blocking wording to match the docs.
Method: documentation only; no commands were run.
