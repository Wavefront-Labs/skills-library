---
id: computing-software.software-engineering.haskell.transformer-stacks-and-except
name: transformer-stacks-and-except
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, monad-transformers, exceptt, statet, readert, lift, liftio, runexceptt, stack-order, readert-pattern, transformer-stacks-and-except]
level: advanced
status: draft
description: "Build ReaderT/StateT/ExceptT stacks over IO, order layers deliberately, use lift and liftIO, runExceptT, and the ReaderT-over-IO application pattern."
sources: ["https://hackage.haskell.org/package//transformers", "https://hackage.haskell.org/package//mtl"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Transformer stacks and ExceptT

**Goal:** combine effects in an application monad and know how layer order changes semantics.

```haskell
import Control.Monad.Except
import Control.Monad.Reader
import Control.Monad.State.Strict

data AppError = NotFound String | Invalid Int deriving Show
type App = ReaderT Config (ExceptT AppError IO)

run :: Config -> App a -> IO (Either AppError a)
run cfg app = runExceptT (runReaderT app cfg)

fetch :: String -> App Int
fetch k = do
  cfg <- ask
  liftIO (putStrLn ("fetching " ++ k))           -- IO at the bottom
  when (k == "") $ throwError (Invalid 0)
  pure 1
handler = fetch "x" `catchError` \e -> pure 0
```

## Ordering
- `StateT s (Either e)`: an error discards the state (state is lost on `Left`).
- `ExceptT e (State s)`: state changes survive an error.
- Choose by what must survive failure. Run functions peel the outermost layer first.

## Practices
- `liftIO` for IO; `lift` for one layer; mtl classes (`MonadIO`, `MonadError e`) avoid manual lifting.
- The "ReaderT pattern": `newtype App a = App (ReaderT Env IO a)` with `deriving newtype` instances; keep mutable
  state in `IORef`s/`TVar`s in `Env`. Simple, fast, and exception-friendly.
- Deep stacks are slow without optimisation; compile with `-O` and consider effect libraries (`effectful`,
  `polysemy`, `fused-effects`) when stacks get unwieldy (library comparison is unconfirmed here).

## Gotchas
- `ExceptT` does not catch exceptions thrown in IO (`error`, `throwIO`); use `Control.Exception` for those.
- `StateT` over `ExceptT` with `MonadBaseControl` forking loses state; see `lifted-async`/`unliftio`.
- `Control.Monad.Trans.Except` (transformers) has `throwE`/`catchE`; mtl has `throwError`/`catchError`.

## Self-check
- [ ] Documented decision for each layer order.
- [ ] Domain errors are in ExceptT, runtime failures remain exceptions.
