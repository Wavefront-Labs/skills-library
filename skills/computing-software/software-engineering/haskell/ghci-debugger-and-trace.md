---
id: computing-software.software-engineering.haskell.ghci-debugger-and-trace
name: ghci-debugger-and-trace
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, ghci-debugger, breakpoint, debug-trace, traceshow, ghci-step, ghci-trace, history, force, ghci-debugger-and-trace]
level: practitioner
status: docs-checked
description: "Debug with GHCi breakpoints (:break, :step, :trace, :history, :print, :force), Debug.Trace (trace, traceShowId, traceM) and the call stack in failures."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/ghci.html", "https://hackage.haskell.org/package/base/docs/Debug-Trace.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GHCi debugger and Debug.Trace

**Goal:** inspect lazy evaluation and find where values go wrong.

## Debugger (interpreted modules only)
```
ghci> :load Main.hs
ghci> :break myFunction            -- or :break Main 42  (line)  / :break 42 7 (line col)
ghci> :main                         -- or evaluate an expression; stops at the breakpoint
Stopped in Main.myFunction, Main.hs:12:5-20
_result :: Int = _
x :: [Int] = _                      -- '_' means an unevaluated thunk
[Main.hs:12:5-20] ghci> :print x    -- show without forcing
[...] ghci> :force x                -- evaluate fully then print
[...] ghci> :step                   -- :steplocal  :stepmodule  :continue
[...] ghci> :trace expr             -- record history; then :hist and :back / :forward
ghci> :show breakpoints; :delete 0
ghci> :set -fbreak-on-exception     -- stop at exceptions (-fbreak-on-error: uncaught only)
```
Breakpoints require the module loaded as bytecode (not `-fobject-code`).

## Debug.Trace
```haskell
import Debug.Trace
f x = trace ("f called with " ++ show x) (x + 1)
g x = traceShowId (x * 2)                 -- prints and returns
h = do { traceM "step 1"; pure () }       -- in any Applicative
traceShow (a, b) result
```
Output goes to stderr, in evaluation order (not program order). `traceEvent`/`traceMarker` write to the eventlog for ThreadScope.

## Gotchas
- Trace calls can change strictness only when added in the wrong place; they themselves are impure: remove them before release (add a CI grep).
- `:print` of a function shows `<function>`; a thunk is `_`.
- Optimised builds inline and reorder: reproduce bugs with `-O0` first, then optimised.
- Stack traces: compile with `-prof -fprof-auto` and run with `+RTS -xc` to see cost-centre stack on exceptions; `HasCallStack` for explicit stacks.
- For real programs, `ghc-debug` (heap debugging) and external tools like `gdb` on the RTS exist (details unconfirmed).

## Self-check
- [ ] Reproduced the failure under `ghci` with a breakpoint on the suspected function.
- [ ] No leftover `trace` calls (`grep -rn "Debug.Trace" src`).

## Checked

2026-11-02. Confirmed against the GHC User's Guide ghci page, runtime_control (-xc); base Debug.Trace docs: debugger commands, break-on flags, trace functions, stderr output. Removed or fixed: none.
Method: documentation only; no commands were run.
