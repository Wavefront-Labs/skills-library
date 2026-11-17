---
id: computing-software.software-engineering.haskell.bottom-error-undefined-callstacks
name: bottom-error-undefined-callstacks
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, error, undefined, hascallstack, bottom, partial-functions, assert, callstack, impossible, bottom-error-undefined-callstacks]
level: practitioner
status: draft
description: "Use error, undefined, assert and HasCallStack, understand bottom values, partial function warnings and how to get a call stack in failures."
sources: ["https://hackage.haskell.org/package/base"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# error, undefined and call stacks

**Goal:** treat bottoms as bugs, and make failures locatable.

```haskell
import GHC.Stack (HasCallStack)
import Control.Exception (assert)

safeIdx :: HasCallStack => [a] -> Int -> a
safeIdx xs i
  | i < 0 || i >= length xs = error ("index out of range: " ++ show i)
  | otherwise = xs !! i

todo :: Int
todo = undefined            -- type checks anywhere; crashes when forced
```
`error` output in a binary shows `CallStack (from HasCallStack)` listing each `HasCallStack` function up the chain.

## Rules
- Bottom (`_|_`) is a non-terminating or crashing value; every type contains it. `error`/`undefined`/infinite loops.
- `HasCallStack =>` is a constraint that threads the call site; add it to partial helpers to blame callers.
- `assert` is disabled by `-O` unless `-fno-ignore-asserts`; do not rely on it for validation.
- `-Wall` includes `-Wincomplete-patterns`, `-Wincomplete-uni-patterns` (GHC 9.2 and later), and recent GHC warns on `head`/`tail`
  (`-Wx-partial`, unconfirmed exact version).
- For a real stack trace in profiled builds: `+RTS -xc` (needs profiling) or `-fprof-auto`.

## Gotchas
- Type holes `_` are the better placeholder for unfinished code; `undefined` hides until runtime.
- Lazy bottoms do not fail until forced, so the stack shows the forcing place, not the creation.
- `Debug.Trace.traceShow` for quick checks; remove before release.
- `ghc -O` can legally change which of two bottoms you observe (imprecise exceptions).

## Self-check
- [ ] No `undefined` in committed code (`grep -rn undefined src`).
- [ ] Partial helpers carry `HasCallStack` or return Maybe.
