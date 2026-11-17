---
id: computing-software.software-engineering.haskell.effect-systems-and-free-monads
name: effect-systems-and-free-monads
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, effectful, polysemy, free-monad, mtl-style, handle-pattern, tagless-final, fused-effects, bluefin, effect-systems-and-free-monads]
level: sme
status: draft
description: "Structure effects with the handle pattern, tagless final (mtl style), free monads and effect libraries (effectful, polysemy), with tradeoffs."
sources: ["https://hackage.haskell.org/package//conduit", "https://hackage.haskell.org/package//effectful"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Effect organisation

**Goal:** choose an architecture for side effects that is testable and fast enough.

## Options, simplest first
1. **Handle pattern / records of functions.** Pass a record of IO operations in an `Env`:
```haskell
data DB = DB { getUser :: UserId -> IO (Maybe User), putUser :: User -> IO () }
-- real impl in IO; tests use an in-memory impl
```
2. **ReaderT Env IO** around the record (see the transformers skill): minimal magic, great performance.
3. **mtl-style / tagless final:** `class Monad m => MonadDB m where ...` with instances for the real stack and test monads; functions are polymorphic in `m`.
4. **Effect libraries:** `effectful` (ReaderT-IO based, fast, dynamic dispatch), `polysemy` and `fused-effects` (free-monad/fusion based; polysemy relies on plugins and has had performance caveats), `bluefin` (handle-passing style), `eff` (experimental, unmaintained status unconfirmed). Compare benchmarks and maintenance before adopting.
5. **Free monads** (`free` package): represent programs as data and interpret later; flexible, slow without care, rarely necessary.

## Guidance
- Start with 1 or 2. Move to a library only when you need many composable effects with local handlers.
- Keep business logic pure; make the effectful shell thin.
- Exceptions: decide whether errors are `Either`, effects (`Error e`), or IO exceptions, and be consistent.
- For concurrency and resource safety, effect libraries need `UnliftIO`-like support (`withRunInIO`), otherwise forking loses the environment.

## Gotchas
- Deep monad stacks with many layers cost performance without optimisation (`-O2` and specialisation).
- Orphan-heavy mtl instances confuse type inference; keep instance declarations near the newtype.
- Libraries differ greatly in compile-time and runtime overhead; benchmark your own workload.

## Self-check
- [ ] Tests run the business logic with a fake implementation and no real IO.
- [ ] Effect choice documented in the repo README.
