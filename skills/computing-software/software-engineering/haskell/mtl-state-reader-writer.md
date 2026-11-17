---
id: computing-software.software-engineering.haskell.mtl-state-reader-writer
name: mtl-state-reader-writer
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, mtl, state-monad, reader-monad, writer-monad, monadstate, monadreader, get, put, modify-prime, runstate, mtl-state-reader-writer, haskell-transformers]
level: practitioner
status: docs-checked
description: "Use Control.Monad.State, Reader and Writer from mtl: get/put/modify', ask/asks/local, tell, and the run functions, preferring strict variants."
sources: ["https://hackage.haskell.org/package//transformers", "https://hackage.haskell.org/package//mtl"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State, Reader and Writer (mtl)

**Goal:** thread state, environment and logs without passing arguments by hand. Packages: `mtl`, `transformers`.

```haskell
import Control.Monad.State.Strict
import Control.Monad.Reader
import Control.Monad.Writer.Strict

counter :: State Int Int
counter = do { modify' (+1); n <- get; put (n * 2); gets (+ 100) }
runState counter 0            -- (result, finalState);  evalState / execState

data Env = Env { verbose :: Bool }
logIt :: String -> Reader Env String
logIt s = do { v <- asks verbose; pure (if v then "LOG " ++ s else s) }
runReader (logIt "x") (Env True)
local (\e -> e { verbose = False }) action

collect :: Writer [String] Int
collect = do { tell ["start"]; pure 42 }
runWriter collect             -- (42, ["start"])
```

## Class-based style
Constraints such as `MonadState Int m` and `MonadReader Env m` keep code polymorphic in the monad.

## Gotchas
- Prefer `Control.Monad.State.Strict` and `modify'`.
- `State s` is `StateT s Identity`; the transformer version is the general one.

## Self-check
- [ ] Long loops use the Strict module and `modify'`.
- [ ] Functions use mtl constraints rather than a concrete stack where reuse matters.

## Checked

2026-11-03. Confirmed against the mtl Control.Monad.State.Strict, Reader, Writer.Strict and State.Class pages: function names, Strict modules. Removed: thunk-leak, quadratic Writer, fundep and memory claims.
Method: documentation only; no commands were run.
